import time
from tqdm import tqdm
import logging
from datetime import datetime, timedelta

from faster_whisper import WhisperModel
import os, sys
import json
import subprocess

import requests
''' #for api server
#from fastapi import FastAPI
#from fastapi.staticfiles import StaticFiles
#from fastapi.responses import HTMLResponse
#
'''
from pydantic import BaseModel, Field

import utils.apify as apify
import utils.prompts as gpt
import utils.ggl as ggl
import utils.shares as sh
from dotenv import load_dotenv
from openai import OpenAI
from concurrent.futures import ThreadPoolExecutor, as_completed


print('SERVER STARTED')

# Загружаем переменные из .env
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

# Настройка логирования
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ReelLinksData(BaseModel):
    urls: list[str]


class ReelLinks(BaseModel):
    username: str
    links: str


# Функция для получения хоста (начала) URL
def extract_host_from_url(url):
    from urllib.parse import urlparse
    parsed_url = urlparse(url)
    return parsed_url.netloc  # Возвращаем только хост (например, instagram.fcgh7-1.fna.fbcdn.net)


def attempt_download(video_url, save_path):
    """
    Общая функция для скачивания одного файла по ссылке `video_url`.
    Возвращает True, если скачано успешно, иначе False.
    """
    try:
        response = requests.get(video_url, stream=True, timeout=10)
        if response.status_code == 200:
            with open(save_path, 'wb') as video_file:
                for chunk in response.iter_content(chunk_size=256*1024):
                    if chunk:
                        video_file.write(chunk)
            # print(f"Видео файл сохранен: {save_path}")
            return True
        else:
            print(f"Ошибка загрузки {video_url}: {response.status_code}")
            return False
    except Exception as e:
        print(f"Ошибка при загрузке {video_url}: {e}")
        return False

def download_single_video(item, save_directory, scraping_type, host_list=None):
    """
    Универсальная функция скачивания ОДНОГО видео для Instagram или TikTok.

    Параметры:
      - item: dict с полями 'shortCode', 'videoUrl'
      - save_directory: путь к папке для сохранения
      - scraping_type: 'instagram' / 'tiktok'
      - host_list: список fallback-хостов (только для instagram)
    
    Возвращает (shortCode, reel_info) или (shortCode, None)
    """
    print()
    shortCode = item.get('shortCode')
    original_url = item.get('videoUrl')
    if not (shortCode and original_url):
        return (shortCode, None)

    video_file_name = f'{shortCode}.mp4'
    file_path = os.path.join(save_directory, video_file_name)

    if scraping_type == "instagram":
        # 1) Пробуем скачать по оригинальной ссылке
        success = attempt_download(original_url, file_path)

        # 2) Если неудача — пробуем fallback-хосты
        if not success and host_list:
            original_host = extract_host_from_url(original_url)
            url_parts = original_url.split(original_host, maxsplit=1)
            url_path = url_parts[1] if len(url_parts) > 1 else ""

            for host in host_list:
                if host != original_host:
                    modified_url = f"https://{host}{url_path}"
                    success = attempt_download(modified_url, file_path)
                    if success:
                        break
    else:
        # Для TikTok — просто одна попытка скачать
        success = attempt_download(original_url, file_path)

    if success:
        reel_info = {
            "video_path": file_path,
            "audio_path": None,
            "transcription": None
        }
        return (shortCode, reel_info)
    else:
        print(f"Не удалось скачать видео для шорткода: {shortCode}")
        return (shortCode, None)

def download_videos(data, scraping_type):
    """
    Универсальная функция для скачивания видео (Reels/TikTok), 
    в зависимости от scraping_type.

    Аргументы:
     - data: список элементов (dict), каждый должен содержать 'shortCode' и 'videoUrl'
     - scraping_type: "instagram" или "tiktok"

    Возвращает dict: { shortCode: { "video_path": ..., "audio_path": ..., "transcription": ... }, ... }
    """
    # 1. Создаём папку с датой
    now = datetime.now()
    date_time_folder = now.strftime("%Y%m%d")

    # Для наглядности: разные папки для IG vs TikTok
    # Можно сделать единый корень "videos" / date_time_folder, но 
    # обычно хочется разделять, чтобы не смешивать файлы.
    if scraping_type == "instagram":
        base_folder = "reels"
    elif scraping_type == "tiktok":
        base_folder = "tiktok"
    else:
        base_folder = "other"

    save_directory = os.path.join(base_folder, date_time_folder)
    os.makedirs(save_directory, exist_ok=True)

    # 2. Собираем host_list (только для Instagram)
    host_list = []
    if scraping_type == "instagram":
        for item in data:
            host = extract_host_from_url(item.get('videoUrl'))
            if host not in host_list and host is not None:
                host_list.append(host)

    # 3. Параллельное скачивание
    reel_data = {}
    max_workers = 10  # подбирайте число потоков

    futures = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for item in data:
            future = executor.submit(download_single_video, 
                                     item=item, 
                                     save_directory=save_directory, 
                                     scraping_type=scraping_type,
                                     host_list=host_list)
            futures.append(future)

        # tqdm + as_completed для красивой полоски прогресса
        for fut in tqdm(as_completed(futures), total=len(futures), 
                        desc=f"Скачивание {scraping_type} видео", unit="видео"):
            shortCode, info = fut.result()  # (shortCode, {video_path, ...} или None)
            if shortCode and info:
                reel_data[shortCode] = info

    return reel_data


def convert_video_to_audio(video_path):
    """Конвертация видео в аудиофайл (WAV) с использованием FFmpeg и извлечение длительности."""
    audio_path = video_path.replace(".mp4", ".wav")
    try:
        # Конвертация видео в аудио с помощью FFmpeg
        command = [
            "ffmpeg", "-i", video_path, "-ac", "1", "-ar", "16000", "-y",
            audio_path
        ]
        # Перенаправляем стандартный вывод и вывод ошибок в /dev/null (или в subprocess.PIPE для подавления)
        with open(os.devnull, 'w') as devnull:
            subprocess.run(command, check=True, stdout=devnull, stderr=devnull)
        print(f"Конвертация выполнена: {audio_path}")

        # Проверяем, что файл создан
        if os.path.exists(audio_path):
            print(f"Аудиофайл успешно создан: {audio_path}")
        else:
            print(f"Ошибка: Аудиофайл {audio_path} не найден!")
            return None  # Если файл не найден

        return audio_path
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при конвертации {video_path}: {e}")
        return None


def transcribe_audio(audio_path, model):
    try:
        transcribe_option = "local"
        if transcribe_option == "openai":
            with open(audio_path, "rb") as audio_file:  # Используем with для автоматического закрытия файла
                transcription = client.audio.transcriptions.create(
                    model="whisper-1", 
                    file=audio_file
                )
            print(f"TRANSCRIPT: {transcription.text}")
            transcription = transcription.text
        #transcribe(word_timestamps=True)

        #link to repo https://github.com/SYSTRAN/faster-whisper
        elif transcribe_option == "local":
            segments, info = model.transcribe(audio_path, language=None)
            # соединение фрагментов
            transcription = "".join(segment.text for segment in segments)

        return transcription
        
    except Exception as e:
        print(f"Ошибка при транскрибации {audio_path}: {e}")
        return None


def process_reel(shortCode, transcript_data, output_filename, model):
    video_path = transcript_data[shortCode]["video_path"]
    audio_path = convert_video_to_audio(video_path)
    if audio_path:
        transcript_data[shortCode]["audio_path"] = audio_path
        transcription = transcribe_audio(audio_path, model)
        if transcription:
            transcript_data[shortCode]["transcription"] = transcription
        else:
            transcript_data[shortCode][
                "transcription"] = "Ошибка транскрибации"
    else:
        transcript_data[shortCode]["transcription"] = "Ошибка конвертации"

    save_partial_transcription(transcript_data, output_filename)

    # Удаление файлов после обработки
    time.sleep(1)  # Добавляем задержку перед удалением
    if os.path.exists(video_path):
        os.remove(video_path)
    if os.path.exists(audio_path):
        os.remove(audio_path)

    return transcript_data[shortCode]


def save_partial_transcription(reel_data, save_path_transcript):
    try:
        output = {
            "processing_time_seconds":
            0,  # Время добавим позже
            "transcriptions": [{
                "shortCode":
                shortCode,
                "video_path":
                reel_data[shortCode]["video_path"],
                "audio_path":
                reel_data[shortCode]["audio_path"],
                "transcription":
                reel_data[shortCode]["transcription"]
            } for shortCode in reel_data]
        }

        with open(f'{save_path_transcript}', "w",
                  encoding="utf-8") as json_file:
            json.dump(output, json_file, ensure_ascii=False, indent=4)
        print(f"Транскрипция сохранена")
    except Exception as e:
        print(f"Ошибка при сохранении JSON: {e}")


def insert_transcription(extracted_data, output_data):
    # Создаем словарь для быстрого поиска по shortCode
    transcription_dict = {
        t['shortCode']: t['transcription']
        for t in output_data['transcriptions']
    }

    # Обновляем extracted_data
    for item in extracted_data:
        shortCode = item.get('shortCode')
        if shortCode in transcription_dict:
            item['transcription'] = transcription_dict[shortCode]

    return extracted_data



def process_data(account, days=3, links=[], scheme=0, range_days=None, scraping_type = "instagram"):
    start_time = time.time()
    print('process data started')

    debug = 0

    # Генерируем имя файла только один раз
    now = datetime.now()
    date_time_str = now.strftime("%Y%m%d_%H%M%S")
    save_path = os.path.join('db', str(account['id']))
    os.makedirs(save_path, exist_ok=True)


    '''
    *
    01 - SCRAPING
    *
    '''

    output_apify_filename = f"{account['username']}_apify_{date_time_str}.json"
    output_database_filename = f"{account['username']}_database_{date_time_str}.json"
    save_path_apify = os.path.join('db', str(account['id']),
                                   output_apify_filename)
    save_path_apify_database = os.path.join('db', str(account['id']),
                                   output_database_filename)
    output_shares_filename = f"{account['username']}_shares_{date_time_str}.json"

    if debug == 1:
        #<DEBUG>
        with open("db/0/olegmazunin_apify_20250110_161037.json", "r", encoding="utf-8") as file:
            test_data = json.load(file)
        #</DEBUG>


    if scheme == 0:

        # Рассчитываем целевые дни
        target_day = datetime.now() - timedelta(days=days)
        start_of_day = target_day.date()  # Получаем только дату
        end_of_day = (target_day + timedelta(days=1)).date()  # Получаем только дату
        
        # Если указан диапазон дней
        if range_days:
            start_range, end_range = map(int, range_days.split('-'))
            start_of_day = (datetime.now() - timedelta(days=end_range)).date()  # Получаем только дату
            end_of_day = (datetime.now() - timedelta(days=start_range)).date()  # Получаем только дату



        if scraping_type == "instagram":
            users_data = ggl.get_table_data_as_json(account, 'DATA')
            if debug == 0:
                if not users_data and print('No users') is None: return
                dataset_items = apify.instagram_posts_scrapper(users_data, start_of_day, range_days=range_days)
                
                with open(save_path_apify_database, "w", encoding="utf-8") as file:
                        json.dump(dataset_items, file, ensure_ascii=False, indent=4)
                        
            else:
                #<DEBUG>
                dataset_items = test_data
                #</DEBUG>
            
            if not dataset_items and print('No reels data found') is None: return

            reelsData, sorted_data, sortedReelsCount = apify.instagram_scrapper_filter_sorter(
                dataset_items, users_data, start_of_day, end_of_day)
            if sortedReelsCount == 0 and print('No new reels') is None: return

            extracted_data = apify.extracted_reels_data_maker(sorted_data)


        elif scraping_type == "tiktok":
            users_data = ggl.get_table_data_as_json(account, 'DATA_TIKTOK')
            if debug == 0:
                if not users_data and print('No users') is None: return
                dataset_items = apify.tiktok_posts_scrapper(users_data, start_of_day, range_days=range_days)
                
                with open(save_path_apify_database, "w", encoding="utf-8") as file:
                        json.dump(dataset_items, file, ensure_ascii=False, indent=4)
            
            else:
                #<DEBUG>
                dataset_items = test_data
                #</DEBUG>
            
            if not dataset_items and print('No tiktok data found') is None: return

            reelsData, sorted_data, sortedReelsCount = apify.tiktok_scrapper_filter_sorter(
                dataset_items, users_data, start_of_day, end_of_day)
            if sortedReelsCount == 0 and print('No new tiktok') is None: return

            extracted_data = apify.extracted_tiktok_data_maker(sorted_data) 
        

    elif scheme == 1:
        print(scheme)
        '''
        account['username'] = account.get('username') + "_saves"
        # apify request
        reelsData = apify.reels_scrapper(links)
        if not reelsData and print('No reels data found') is None: return

        sorted_data = reelsData
        extracted_data = apify.extracted_reels_data_maker(sorted_data)
        transcript_data = download_videos(extracted_data, scraping_type)
        '''
    elif scheme == 2:
        print(scheme)
        '''
        account['username'] = account.get('username') + "_saves"
        # apify request
        reelsData = apify.tiktok_scrapper(links)
        if not reelsData and print('No reels data found') is None: return

        sorted_data = reelsData
        extracted_data = apify.extracted_tiktok_data_maker(sorted_data) #TIKTOK
        transcript_data = download_videos(extracted_data, scraping_type)
        '''

    if debug == 1:
        #print(json.dumps(extracted_data, ensure_ascii=False, indent=4))
        print("DEBUG   Done")
    

    apify_end_time = time.time()
    total_apify_time_print = apify_end_time - start_time
    print("*")
    print("*")
    print(f"Общее время обработки: {total_apify_time_print:.2f} секунд")
    print("*")
    print("*")


    #Сохраняем отфильтрованные рилсы в json файл
    with open(save_path_apify, "w", encoding="utf-8") as file:
        json.dump(reelsData, file, ensure_ascii=False, indent=4)


    '''
    *
    02 - TRANSCRIPTION
    *
    '''

    transcript_data = download_videos(extracted_data, scraping_type)

    output_filename = f"{account['username']}_transcriptions_{date_time_str}.json"
    save_path_transcript = os.path.join('db', str(account['id']),
                                        output_filename)
    
    #Сохраняем пустой файл
    with open(save_path_transcript, "w", encoding="utf-8") as file:
        json.dump("", file, ensure_ascii=False, indent=4)


    # Инициализируем модель один раз
    #model_size types - 'tiny', 'base', 'small', 'medium', 'large'
    #если openai whisper
    #model = "small"
    #елси faster-whisper
    model = WhisperModel("small", device="cuda", compute_type="float16")

    for shortCode in tqdm(transcript_data, desc="Процесс транскрибации", unit="рилс"):
        try:
            transcript_data[shortCode] = process_reel(shortCode,
                                                      transcript_data,
                                                      save_path_transcript, model)
        except Exception as e:
            print(f"Ошибка при обработке {shortCode}: {e}")

    with open(save_path_transcript, "r", encoding="utf-8") as file:
        output_data = json.load(file)

    output_data["processing_time_seconds"] = "0"

    # Удаляем поля video_path и audio_path из каждого элемента списка transcriptions
    for transcription in output_data["transcriptions"]:
        transcription.pop("video_path", None)
        transcription.pop("audio_path", None)

    with open(save_path_transcript, "w", encoding="utf-8") as file:
        json.dump(output_data, file, ensure_ascii=False, indent=4)
    print(json.dumps(output_data, ensure_ascii=False, indent=4))
    # Выводим только первые 10 транскрипций
    print(json.dumps(output_data["transcriptions"][:5], ensure_ascii=False, indent=4))
    #sys.exit()

    results = insert_transcription(extracted_data, output_data)
    len_results = len(results)
    # Save JSON file with the specified naming convention
    result_filename = f"{account['username']}_result_{date_time_str}.json"
    save_path_result = os.path.join('db', str(account['id']), result_filename)





    '''
    *
    03 - OPENAI_ORIGINAL
    *
    '''

    for index, item in tqdm(enumerate(results, start=1), total=len(results), desc="Process spez_original:", unit="reel"):
        spez_common_answer = {}
        spez_original_answer = {}
        transcription = item.get('transcription')

        spez_common_answer = gpt.spez_common_script(transcription,
                                                    item.get('caption'))
        item['topic'] = spez_common_answer.get('topic', '')
        item['theme'] = spez_common_answer.get('theme', '')

        print(
            f"--------- spez_original run for {index}/{len_results} ---------")
        #checking if the transcription is not empty
        if transcription != "Ошибка транскрибации":
            spez_original_answer = gpt.spez_original_script(transcription)

            # Выводим первые 100 символов из JSON-данных
            json_output_spez_original = json.dumps(spez_original_answer, ensure_ascii=False, indent=4)
            print(json_output_spez_original[:100])  # Выводим только первые 100 символов
            try:
                #gpt_answer_dict = json.loads(str(gpt_answer))
                item['original_script'] = {}
                item['original_script']['hook'] = spez_original_answer.get(
                    'hook', '')
                item['original_script']['content'] = spez_original_answer.get(
                    'content', '')
                item['original_script']['cta'] = spez_original_answer.get(
                    'cta', '')
                item['song'] = spez_original_answer.get('song', None)
                item['humor'] = spez_original_answer.get('humor', None)
            except json.JSONDecodeError:
                print(
                    "Error: String returned from spez_reelsmaker is not valid JSON"
                )
                # Optionally handle the error, e.g., set defaults or skip
                continue
        else:
            try:
                item['original_script'] = {}
                item['original_script']['hook'] = '-'
                item['original_script']['content'] = '-'
                item['original_script']['cta'] = '-'
                item['song'] = 0
                item['humor'] = 0
            except json.JSONDecodeError:
                print(
                    "Error: String returned from spez_reelsmaker is not valid JSON"
                )
                # Optionally handle the error, e.g., set defaults or skip
                continue
            print(f"No transcription found for item {item.get('shortCode')}")

    '''
    *
    04 - OPENAI_REWRITE
    *
    '''

    #make a file
    os.makedirs(os.path.dirname(save_path_result), exist_ok=True)
    with open(save_path_result, "w", encoding="utf-8") as result_file:
        json.dump(results, result_file, ensure_ascii=False, indent=4)

    #Сюда надо добавить данные с второго агента
    for index, item in tqdm(enumerate(results, start=1), total=len(results), desc="Process spez_rewriter:", unit="reel"):
        spez_rewriter_answer = {}
        transcription = item.get('transcription')

        print(
            f"--------- spez_rewriter run for {index}/{len_results} ---------")
        #checking if the transcription is not empty
        if transcription != "Ошибка транскрибации":
            # Получаем уже сохранённые данные скрипта
            original_script = item.get('original_script', {})
            hook = original_script.get('hook', '')
            content = original_script.get('content', '')
            cta = original_script.get('cta', '')

            spez_rewriter_answer = gpt.spez_rewriter_script(
                {
                    'hook': hook,
                    'content': content,
                    'cta': cta
                }, item.get('caption'))
            # Выводим первые 100 символов из JSON-данных
            json_output_spez_rewriter = json.dumps(spez_rewriter_answer, ensure_ascii=False, indent=4)
            print(json_output_spez_rewriter[:100])  # Выводим только первые 100 символов
            print("------------------")
            try:
                item['rewrited_script'] = {}
                item['rewrited_script']['hook'] = spez_rewriter_answer.get(
                    'hook', "-")
                item['rewrited_script']['content'] = spez_rewriter_answer.get(
                    'content', "-")
                item['rewrited_script']['cta'] = spez_rewriter_answer.get(
                    'cta', "-")
                item['rewrited_script']['caption'] = spez_rewriter_answer.get(
                    'caption', '')
            except json.JSONDecodeError:
                print(
                    "Error: String returned from spez_reelsmaker is not valid JSON"
                )
                # Optionally handle the error, e.g., set defaults or skip
                continue
        else:
            spez_rewriter_answer = gpt.spez_rewriter_script(
                {}, item.get('caption'))

            try:
                item['rewrited_script'] = {}
                item['rewrited_script']['hook'] = "-"
                item['rewrited_script']['content'] = "-"
                item['rewrited_script']['cta'] = "-"
                item['rewrited_script']['caption'] = spez_rewriter_answer.get(
                    'caption', '')
            except json.JSONDecodeError:
                print(
                    "Error: String returned from spez_reelsmaker is not valid JSON"
                )
                # Optionally handle the error, e.g., set defaults or skip
                continue
            print(f"No transcription found for item {item.get('shortCode')}")
    total_processing_time = 0

    os.makedirs(os.path.dirname(save_path_result), exist_ok=True)
    with open(save_path_result, "w", encoding="utf-8") as result_file:
        json.dump(results, result_file, ensure_ascii=False, indent=4)
    ###

    #print(results)
    #json_results = json.dumps(results, indent=4) # эта строка преобразует список в json строку

    '''
    *
    05 - GET SHARES
    *
    '''


    if scraping_type == "instagram":
        #SHARES SECTION START HERE
        #result_filename, save_path_result нужны для предосторожности. Если много рилсов, у которых нужно сохранить репосты, то мы периодически сохраняем количество репостов у рилсов в финальный файл, чтобы, если возникнет ошибка, у нас сохранились данные
        try:
            results = sh.execute_shares_scraping(results, result_filename, save_path_result)
        except Exception as e:
            print(f"Ошибка в процессе получения репостов: {e}")

    '''
    *
    06 - WRITE DATA TO GOOGLE SHEET
    *
    '''

    try:
        if scheme == 0:
            if scraping_type == "instagram":
                ggl.append_data_to_google_sheet(results, account["table_id"],
                                            'INSTAGRAM', scraping_type=scraping_type)
            elif scraping_type == "tiktok":
                ggl.append_data_to_google_sheet(results, account["table_id"],
                                            'TIKTOK', scraping_type=scraping_type)
            else:
                print("ERROR Wrong scraping type variable")

        elif scheme == 1:
            ggl.append_data_to_google_sheet(results, account["table_id"],
                                            'INSTAGRAM_SAVED')
        elif scheme == 2:
            ggl.append_data_to_google_sheet(results,
                                            account["table_id"],
                                            'TIKTOK_SAVED',
                                            scheme=2)

        print(f"\nDONE\n\n")

        end_time = time.time()
        total_process_time_print = end_time - start_time
        print("*")
        print("*")
        print("*")
        print(f"Общее время обработки: {total_process_time_print:.2f} секунд")
        print("*")
        print("*")
        print("*")

        return "Process completed successfully!"
    except Exception as e:
        print(f"Ошибка в процессе обработки в ggl: {e}")



#if you need only spez with openai
def process_data_onlyspez(account, days=2, links=[], scheme=0):

    save_path_result = 'db/19/potok_germany_result_20241230_124000.json'


    start_time = time.time()
    print('process data started')

    if scheme == 0:
        users_data = ggl.get_table_data_as_json(account, 'DATA')
        if not users_data and print('No users') is None: return

    with open(save_path_result, "r", encoding="utf-8") as file:
        results = json.load(file)
    results = list(results)

    for i, item in tqdm(enumerate(results, start=1), total=len(results), desc="Process spez_original:", unit="reel"):
        spez_common_answer = {}
        spez_original_answer = {}
        transcription = item.get('transcription')

        spez_common_answer = gpt.spez_common_script(transcription,
                                                    item.get('caption'))
        item['topic'] = spez_common_answer.get('topic', '')
        item['theme'] = spez_common_answer.get('theme', '')

        if transcription != "Ошибка транскрибации":
            spez_original_answer = gpt.spez_original_script(transcription)

            # Выводим первые 100 символов из JSON-данных
            json_output_spez_original = json.dumps(spez_original_answer, ensure_ascii=False, indent=4)
            print(json_output_spez_original[:100])  # Выводим только первые 100 символов
            try:
                #gpt_answer_dict = json.loads(str(gpt_answer))
                item['original_script'] = {}
                item['original_script']['hook'] = spez_original_answer.get(
                    'hook', '')
                item['original_script']['content'] = spez_original_answer.get(
                    'content', '')
                item['original_script']['cta'] = spez_original_answer.get(
                    'cta', '')
                item['song'] = spez_original_answer.get('song', None)
                item['humor'] = spez_original_answer.get('humor', None)
            except json.JSONDecodeError:
                print(
                    "Error: String returned from spez_reelsmaker is not valid JSON"
                )
                # Optionally handle the error, e.g., set defaults or skip
                continue
        else:
            try:
                item['original_script'] = {}
                item['original_script']['hook'] = '-'
                item['original_script']['content'] = '-'
                item['original_script']['cta'] = '-'
                item['song'] = 0
                item['humor'] = 0
            except json.JSONDecodeError:
                print(
                    "Error: String returned from spez_reelsmaker is not valid JSON"
                )
                # Optionally handle the error, e.g., set defaults or skip
                continue
            print(f"No transcription found for item {item.get('shortCode')}")



    #make a file
    os.makedirs(os.path.dirname(save_path_result), exist_ok=True)
    with open(save_path_result, "w", encoding="utf-8") as result_file:
        json.dump(results, result_file, ensure_ascii=False, indent=4)

    #Сюда надо добавить данные с второго агента
    for i, item in tqdm(enumerate(results, start=1), total=len(results), desc="Process spez_rewriter:", unit="reel"):
        spez_rewriter_answer = {}
        transcription = item.get('transcription')

        if transcription != "Ошибка транскрибации":
            # Получаем уже сохранённые данные скрипта
            original_script = item.get('original_script', {})
            hook = original_script.get('hook', '')
            content = original_script.get('content', '')
            cta = original_script.get('cta', '')

            spez_rewriter_answer = gpt.spez_rewriter_script(
                {
                    'hook': hook,
                    'content': content,
                    'cta': cta
                }, item.get('caption'))
            # Выводим первые 100 символов из JSON-данных
            json_output_spez_rewriter = json.dumps(spez_rewriter_answer, ensure_ascii=False, indent=4)
            print(json_output_spez_rewriter[:100])  # Выводим только первые 100 символов
            print("------------------")
            try:
                item['rewrited_script'] = {}
                item['rewrited_script']['hook'] = spez_rewriter_answer.get(
                    'hook', "-")
                item['rewrited_script']['content'] = spez_rewriter_answer.get(
                    'content', "-")
                item['rewrited_script']['cta'] = spez_rewriter_answer.get(
                    'cta', "-")
                item['rewrited_script']['caption'] = spez_rewriter_answer.get(
                    'caption', '')
            except json.JSONDecodeError:
                print(
                    "Error: String returned from spez_reelsmaker is not valid JSON"
                )
                # Optionally handle the error, e.g., set defaults or skip
                continue
        else:
            spez_rewriter_answer = gpt.spez_rewriter_script(
                {}, item.get('caption'))

            try:
                item['rewrited_script'] = {}
                item['rewrited_script']['hook'] = "-"
                item['rewrited_script']['content'] = "-"
                item['rewrited_script']['cta'] = "-"
                item['rewrited_script']['caption'] = spez_rewriter_answer.get(
                    'caption', '')
            except json.JSONDecodeError:
                print(
                    "Error: String returned from spez_reelsmaker is not valid JSON"
                )
                # Optionally handle the error, e.g., set defaults or skip
                continue
            print(f"No transcription found for item {item.get('shortCode')}")
    total_processing_time = 0

    os.makedirs(os.path.dirname(save_path_result), exist_ok=True)
    with open(save_path_result, "w", encoding="utf-8") as result_file:
        json.dump(results, result_file, ensure_ascii=False, indent=4)
    ###

    #print(results)
    #json_results = json.dumps(results, indent=4) # эта строка преобразует список в json строку

    try:
        if scheme == 0:
            ggl.append_data_to_google_sheet(results, account["table_id"],
                                            'INSTAGRAM')
        elif scheme == 1:
            ggl.append_data_to_google_sheet(results, account["table_id"],
                                            'INSTAGRAM_SAVED')
        elif scheme == 2:
            ggl.append_data_to_google_sheet(results,
                                            account["table_id"],
                                            'TIKTOK_SAVED',
                                            scheme=2)

        print(f"\nDONE\n\n")

        end_time = time.time()
        total_process_time_print = end_time - start_time
        print("*")
        print("*")
        print("*")
        print(f"Общее время обработки: {total_process_time_print:.2f} секунд")
        print("*")
        print("*")
        print("*")

        return "Process completed successfully!"
    except Exception as e:
        print(f"Ошибка в процессе обработки в ggl: {e}")






def app_run(option="all", account_id=0, range_days="3-3", scraping_type="instagram"):
    logger.info("------APP IS RUNNING------")
    with open("db/main/db.json", "r", encoding="utf-8") as file:
        table_list = json.load(file)

    switcher = option  # This should be set appropriately as per your context
    if switcher == "one":
        process_data(table_list["accounts"][account_id], range_days=range_days, scheme=0, scraping_type=scraping_type)
        #process_data_onlyspez(table_list["accounts"][account_id], days=day_for_one, scheme=0)

    elif switcher == "all":
        # For all accounts
        for account in table_list["accounts"]:
            if account["subscription"] != "stop" and account["subscription"] != "free":
                process_data(account, range_days=range_days, scheme=0)
    elif switcher == "":
        #process_data(account, days=1, scheme=0)
        pass
    logger.info("------APP IS STOPPED------")
    #executor.submit(process_data, request, table_list[2], 10)
    return None









links_list = ReelLinks(username="olegmazunin",
                       links='''
https://www.instagram.com/reel/DCurCVtsLvq,
https://vt.tiktok.com/ZSjT4XnMH
''')

def update_reels(request: ReelLinks):
    #def update_reels(request):
    print(f"Received URLs: {request}")
    request_links = str(request.links)
    # Normalize the separators to make link extraction easier
    data = request_links.replace(',', '\n').replace('\\n', '\n')

    # Split into list and strip whitespace
    links = [link.strip() for link in data.split('\n') if link.strip()]

    # Separate Instagram and TikTok links
    instagram_links = [
        link.replace('reel', 'p') for link in links if 'instagram.com' in link
    ]
    tiktok_links = [link for link in links if 'tiktok' in link]

    # Prepare the response dictionary
    request_dict = {
        "username": request.username,
        "instagram_links": instagram_links,
        "tiktok_links": tiktok_links
    }

    print(json.dumps(request_dict, indent=4, ensure_ascii=False))

    # Путь к файлу
    file_path = "db/main/db.json"
    directory = os.path.dirname(file_path)

    # Проверяем, существует ли директория
    if not os.path.exists(directory):
        os.makedirs(directory)  # Создаем директорию, если она не существует

    # Открываем файл после проверки/создания директории
    with open(file_path, "r", encoding="utf-8") as file:
        table_list = json.load(file)

    # Получение username из запроса
    username = request_dict.get('username')

    # Поиск соответствующего table_id для данного username в списке аккаунтов
    account = next(
        (acc
         for acc in table_list['accounts'] if acc['username_tg'] == username),
        None)

    # Проверка на наличие соответствующего аккаунта и вывод результатов
    if account:
        print(
            f"Found table_id for {username}: {account.get('id')} : {account.get('table_id')}"
        )  # Использование переменной account вместо несуществующей table_id

        # Проверка и запуск соответствующих функций process_data
        if request_dict.get('instagram_links'):
            process_data(account,
                         links=request_dict.get('instagram_links'),
                         scheme=1)
        # Проверка и запуск соответствующих функций process_data
        if request_dict.get('tiktok_links'):
            process_data(account,
                         links=request_dict.get('tiktok_links'),
                         scheme=2)
    else:
        print(f"No matching table_id found for {username}")

    return {"status": "updated", "data": request}

#update_reels(links_list)