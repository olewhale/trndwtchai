import time
from tqdm import tqdm
import logging
from datetime import datetime, timedelta

from faster_whisper import WhisperModel
import os, sys
import json
import subprocess

import requests
from pydantic import BaseModel, Field

import utils.apify as apify
import utils.prompts as gpt
import utils.ggl as ggl
import utils.shares as sh
import utils.tg as tg
from dotenv import load_dotenv
from openai import OpenAI
from concurrent.futures import ThreadPoolExecutor, as_completed


#print(f"\033[91m STRANGE \033[0m")
print('SERVER STARTED')

# Загружаем переменные из .env
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

# Настройка логирования
class NoOpenAILogFilter(logging.Filter):
    def filter(self, record):
        return "https://api.openai.com/v1/chat/completions" not in record.getMessage()

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
logger.addFilter(NoOpenAILogFilter())

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
    try:
        shortCode = item.get('shortCode')
        original_url = item.get('videoUrl')
        #print(f"\033[91m {shortCode} \033[0m")

        duration = item.get('videoDuration') if item.get('videoDuration') != "NoVideo" else 0

        if not (shortCode and original_url):
            return (shortCode, None)


        video_file_name = f'{shortCode}.mp4'
        file_path = os.path.join(save_directory, video_file_name)

        success = False  # ✅ Initialize the variable to prevent errors

        if scraping_type == "instagram":

            # 1) Пробуем скачать по оригинальной ссылке
            success = attempt_download(original_url, file_path)

            # 2) Если неудача — пробуем fallback-хосты
            if not success and host_list:
                print('TRYING DOWNLOAD AGAIN -----')
                original_host = extract_host_from_url(original_url)
                url_parts = original_url.split(original_host, maxsplit=1)
                url_path = url_parts[1] if len(url_parts) > 1 else ""

                for host in host_list:
                    if host != original_host:
                        modified_url = f"https://{host}{url_path}"
                        success = attempt_download(modified_url, file_path)
                        if success:
                            break
        elif scraping_type == "tiktok":
            # Для TikTok — просто одна попытка скачать
            success = attempt_download(original_url, file_path)
        else:
            print('CANT DOWNLOAD VIDEO FILE')

        if success:
            reel_info = {
                "video_path": file_path,
                "audio_path": None,
                "transcription": None,
                "duration": duration
            }
            return (shortCode, reel_info)
        else:
            print(f"Не удалось скачать видео для шорткода: {shortCode}")
            return (shortCode, None)
    except Exception as e:
        print(f"Ошибка при загрузке {item.get('shortCode')}: {e}")
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
    print("---------- HERE WE GO ----------")
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
        # for x in reel_data:
        #     print("\033[91m" + str(x) + "\033[0m")
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


def process_reel(shortCode, duration, transcript_data, output_filename, model):
    video_path = transcript_data[shortCode]["video_path"]
    audio_path = convert_video_to_audio(video_path)

    if audio_path:
        transcript_data[shortCode]["audio_path"] = audio_path

        # Определяем транскрипцию в зависимости от длительности
        transcription = transcribe_audio(audio_path, model) if duration <= 300 else None

        # if duration <= 250:
        #     print("\033[91m" + str("МЕНЬШЕ 250") + "\033[0m")
        # else:
        #     print("\033[91m" + str("БОЛЬШЕ 250") + "\033[0m")

        # Устанавливаем транскрипцию или сообщение об ошибке
        transcript_data[shortCode]["transcription"] = transcription if transcription else "Ошибка транскрибации"
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
            "transcriptions": [{
                "shortCode":shortCode,
                "video_path":reel_data[shortCode]["video_path"],
                "audio_path":reel_data[shortCode]["audio_path"],
                "transcription":reel_data[shortCode]["transcription"]
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

    for item in extracted_data:
        shortCode = item.get('shortCode')
        if shortCode in transcription_dict:
            item['transcription'] = transcription_dict[shortCode]

    return extracted_data



# =============================
# БЛОК ПОДЗАДАЧ (01 - 06)
# =============================

def task_01_scraping(account, days, scheme, range_days, scraping_type, date_time_str):
    """
    01 - SCRAPING

    Выполняет логику:
      - Получает пользователей через ggl.get_table_data_as_json(...)
      - Считает даты (start_of_day, end_of_day) с учётом days и range_days
      - Вызывает нужный скрапер (instagram_posts_scrapper / tiktok_posts_scrapper)
      - Фильтрует результаты (instagram_scrapper_filter_sorter / tiktok_scrapper_filter_sorter)
      - Создаёт reelsData (сырые рилсы) и extracted_data (приведённые к удобной структуре)
      - Сохраняет часть результатов (reelsData) в JSON-файл (save_path_apify)
      - Возвращает reelsData, extracted_data
    """
    
    debug = 0

    if debug == 1:
        # DEBUG-режим (если есть свои заглушечные данные):
        with open("db/0/olegmazunin_database_20250213_232659.json", "r", encoding="utf-8") as file:
            dataset_debug = json.load(file)

    # Генерируем пути для сохранения
    output_apify_filename = f"{account['username']}_apify_{date_time_str}.json"
    output_database_filename = f"{account['username']}_database_{date_time_str}.json"

    save_folder = os.path.join('db', str(account['id']))
    os.makedirs(save_folder, exist_ok=True)  # на случай, если папки нет
    save_path_apify = os.path.join(save_folder, output_apify_filename)
    save_path_apify_database = os.path.join(save_folder, output_database_filename)

    # Расчёт дат:
    target_day = datetime.now() - timedelta(days=days)
    start_of_day = target_day.date()  # например, позавчера, дата без времени
    end_of_day = (target_day + timedelta(days=1)).date()

    if range_days:
        # range_days типа '2-1' => start_range=2, end_range=1
        start_range, end_range = map(int, range_days.split('-'))
        start_of_day = (datetime.now() - timedelta(days=end_range)).date()
        end_of_day = (datetime.now() - timedelta(days=start_range)).date()


    print(f"target_day - {target_day}")
    print(f"start_of_day - {start_of_day}")
    print(f"end_of_day - {end_of_day}")
    print(f"range_days - {range_days}")

    # Подготовим переменные для итогов
    reelsData = []
    extracted_data = []

    #sys.exit()

    # В зависимости от scraping_type:
    if scraping_type == "instagram":
        # Считываем данные из гугл-таблицы (поле 'DATA')
        users_data = ggl.get_table_data_as_json(account, 'DATA')
        if debug == 0:
            # Вызываем скрапер Apify
            if not users_data:
                print('No users')
                return [], []
            dataset_items = apify.instagram_posts_scrapper(users_data, start_of_day, range_days=range_days)

            # Сохраняем сырые данные в save_path_apify_database
            with open(save_path_apify_database, "w", encoding="utf-8") as f:
                json.dump(dataset_items, f, ensure_ascii=False, indent=4)
        elif debug == 1:
            # DEBUG-режим (если есть свои заглушечные данные):
            dataset_items = dataset_debug

        if not dataset_items:
            print('No reels data found')
            return [], []

        # Фильтруем рилсы по датам, сортируем
        reelsData, sorted_data, sortedReelsCount = apify.instagram_scrapper_filter_sorter(
            dataset_items, users_data, start_of_day, end_of_day
        )
        if sortedReelsCount == 0:
            print('No new reels')
            return [], []

        # Создаём extracted_data
        extracted_data = apify.extracted_reels_data_maker(sorted_data)

    elif scraping_type == "tiktok":
        # Считываем из гугл-таблицы (поле 'DATA_TIKTOK')
        users_data = ggl.get_table_data_as_json(account, 'DATA_TIKTOK')
        if debug == 0:
            if not users_data:
                print('No users')
                return [], []
            dataset_items = apify.tiktok_posts_scrapper(users_data, account['search_type'], start_of_day, range_days=range_days)

            with open(save_path_apify_database, "w", encoding="utf-8") as f:
                json.dump(dataset_items, f, ensure_ascii=False, indent=4)
        elif debug == 1:
            # DEBUG-режим (если есть свои заглушечные данные):
            dataset_items = dataset_debug

        if not dataset_items:
            print('No tiktok data found')
            return [], []

        reelsData, sorted_data, sortedReelsCount = apify.tiktok_scrapper_filter_sorter(
            dataset_items, users_data, account['search_type'], start_of_day, end_of_day
        )
        if sortedReelsCount == 0:
            print('No new tiktok')
            return [], []

        extracted_data = apify.extracted_tiktok_data_maker(sorted_data)

    elif scheme in [1, 2]:
        # Если у вас есть альтернативные схемы (добавление "_saves" и т.д.):
        print(f"Scheme {scheme} not fully implemented here, you can add logic.")
        # reelsData = ...
        # extracted_data = ...
        pass
    else:
        print("ERROR: Unknown scraping_type or scheme")

    # Сохраняем reelsData в JSON (как в вашем скрипте)
    with open(save_path_apify, "w", encoding="utf-8") as file:
        json.dump(reelsData, file, ensure_ascii=False, indent=4)
    
    # Сохраняем reelsData в JSON (как в вашем скрипте)
    with open(str(save_path_apify + "_extractedData"), "w", encoding="utf-8") as file:
        json.dump(extracted_data, file, ensure_ascii=False, indent=4)

    # Сохраняем reelsData в JSON (как в вашем скрипте)
    base_name = os.path.splitext(save_path_apify)[0]  # Убираем .json
    with open(f"{base_name}_extractedData.json", "w", encoding="utf-8") as file:
        json.dump(extracted_data, file, ensure_ascii=False, indent=4)

    return reelsData, extracted_data


def task_02_transcription(extracted_data, account, date_time_str, scraping_type):
    """
    02 - TRANSCRIPTION
    (Как в вашем предыдущем коде.)
    """
    # Шаг 1: скачиваем видео
    transcript_data = download_videos(extracted_data, scraping_type)
    #sys.exit()
    # Шаг 2: путь для сохранения транскриптов
    output_filename = f"{account['username']}_transcriptions_{date_time_str}.json"
    save_path_transcript = os.path.join('db', str(account['id']), output_filename)

    # Пустой файл
    with open(save_path_transcript, "w", encoding="utf-8") as file:
        json.dump("", file, ensure_ascii=False, indent=4)
        #json.dump({"transcriptions": []}, file, ensure_ascii=False, indent=4)

    # Инициализация модели
    model = WhisperModel("small", device="cuda", compute_type="float16")

    # Цикл транскрибации
    for shortCode in tqdm(transcript_data, desc="Процесс транскрибации", unit="рилс"):
        
        video_info = transcript_data[shortCode]  # Получаем словарь по ключу shortCode
        duration = video_info.get('duration')

        try:
            transcript_data[shortCode] = process_reel(shortCode,
                                                      duration,
                                                      transcript_data,
                                                      save_path_transcript,
                                                      model)
        except Exception as e:
            print(f"Ошибка при обработке {shortCode}: {e}")

    # Читаем файл, если нужно удалить пути video/audio
    with open(save_path_transcript, "r", encoding="utf-8") as file:
        output_data = json.load(file)

    # Удаляем поля video_path/audio_path
    if isinstance(output_data, dict) and "transcriptions" in output_data:
        for t_item in output_data["transcriptions"]:
            t_item.pop("video_path", None)
            t_item.pop("audio_path", None)
        # Сохраняем обратно
        with open(save_path_transcript, "w", encoding="utf-8") as file:
            json.dump(output_data, file, ensure_ascii=False, indent=4)

    # Объединяем всё
    results = insert_transcription(extracted_data, output_data)
    return results


def task_03_openai_original(results, account):
    """
    03 - OPENAI_ORIGINAL
    """
    len_results = len(results)

    for index, item in tqdm(enumerate(results, start=1),
                            total=len_results,
                            desc="Process spez_original:",
                            unit="reel"):
        transcription = item.get('transcription')
        # 1) Общая логика
        
        spez_common_answer = gpt.spez_common_script(transcription, item.get('caption'))
        item['topic'] = spez_common_answer.get('topic', '')
        item['theme'] = spez_common_answer.get('theme', '')

        # 2) spez_original_script
        if transcription != "Ошибка транскрибации":
            spez_original_answer = gpt.spez_original_script(transcription)
            item['original_script'] = {
                "hook":    spez_original_answer.get('hook', ''),
                "content": spez_original_answer.get('content', ''),
                "cta":     spez_original_answer.get('cta', '')
            }
            item['song'] = spez_original_answer.get('song', 0)
            item['humor'] = spez_original_answer.get('humor', 0)
        else:
            item['original_script'] = {
                "hook": "-",
                "content": "-",
                "cta": "-"
            }
            item['song'] = 0
            item['humor'] = 0

    return results


def task_04_openai_rewrite(results, account, date_time_str):
    """
    04 - OPENAI_REWRITE
    """
    len_results = len(results)
    result_filename = f"{account['username']}_result_{date_time_str}.json"
    save_path_result = os.path.join('db', str(account['id']), result_filename)
    os.makedirs(os.path.dirname(save_path_result), exist_ok=True)
    
    language = account.get('language')

    for index, item in tqdm(enumerate(results, start=1),
                            total=len_results,
                            desc="Process spez_rewriter:",
                            unit="reel"):
        transcription = item.get('transcription')

        no_transcript = (item.get("original_script", {}).get("hook", "") == '-' and 
                          item.get("original_script", {}).get("content", "") == '-' and 
                          item.get("original_script", {}).get("cta", "") == '-')

        if transcription != "Ошибка транскрибации" and not no_transcript:
            original_script = item.get('original_script', {})
            hook = original_script.get('hook', '')
            content = original_script.get('content', '')
            cta = original_script.get('cta', '')

            spez_rewriter_answer = gpt.spez_rewriter_script(
                {'hook': hook, 'content': content, 'cta': cta},
                item.get('caption'), language
            )
            item['rewrited_script'] = {
                "hook":    spez_rewriter_answer.get('hook', '-'),
                "content": spez_rewriter_answer.get('content', '-'),
                "cta":     spez_rewriter_answer.get('cta', '-'),
                "caption": spez_rewriter_answer.get('caption', '')
            }
        else:
            # Нет транскрипции
            spez_rewriter_answer = gpt.spez_rewriter_script({}, item.get('caption'), language)
            item['rewrited_script'] = {
                "hook": "-",
                "content": "-",
                "cta": "-",
                "caption": spez_rewriter_answer.get('caption', '')
            }

    # Сохраняем результат
    with open(save_path_result, "w", encoding="utf-8") as result_file:
        json.dump(results, result_file, ensure_ascii=False, indent=4)

    return results


def task_05_get_shares(reels_data, scraping_type, account, date_time_str):
    """
    05 - GET SHARES
    """
    sharesCountResults = {}
    if scraping_type == "instagram":
        shares_filename = f"{account['username']}_shares_{date_time_str}.json"
        save_path_shares = os.path.join('db', str(account['id']), shares_filename)
        try:
            sharesCountResults = sh.execute_shares_scraping(reels_data, shares_filename, save_path_shares)
        except Exception as e:
            print(f"Ошибка в процессе получения репостов: {e}")
    return sharesCountResults


def task_06_write_data_to_gs(results, account, scheme, scraping_type, start_time):
    """
    06 - WRITE DATA TO GOOGLE SHEET
    """
    try:
        if scheme == 0:
            if scraping_type == "instagram":
                ggl.append_data_to_google_sheet(results, account["table_id"], 'INSTAGRAM', scraping_type=scraping_type)
            elif scraping_type == "tiktok":
                ggl.append_data_to_google_sheet(results, account["table_id"], 'TIKTOK', scraping_type=scraping_type)
            else:
                print("ERROR Wrong scraping type variable")
        elif scheme == 1:
            ggl.append_data_to_google_sheet(results, account["table_id"], 'INSTAGRAM_SAVED')
        elif scheme == 2:
            ggl.append_data_to_google_sheet(results, account["table_id"], 'TIKTOK_SAVED', scheme=2)
        print(f"\nDONE\n\n")
        end_time = time.time()
        total_process_time_print = end_time - start_time
        print("*")
        print("*")
        print(f"Общее время обработки: {total_process_time_print:.2f} секунд")
        print("*")
        print("*")
        return "Process completed successfully!"
    except Exception as e:
        print(f"Ошибка в процессе обработки в ggl: {e}")
        return None
    
def task_07_send_notification(results, account, scheme, scraping_type, start_time):
    """
    07 - SEND NOTIFICATION TO TELEGRAM
    """
    try:
        tg.send_table_update(results, account)

        return "Notification has been sent!"
    except Exception as e:
        print(f"Ошибка в процессе обработки в ggl: {e}")
        return None


# =============================
# ОБЁРТКИ ДЛЯ ПОСЛЕДОВАТЕЛЬНОСТИ
# =============================

def chain_transcript_and_openai(extracted_data, account, date_time_str, scraping_type):
    """
    Задача A:
      02 -> 03 -> 04
    """
    print("---STARTED chain_A---")
    results_02 = task_02_transcription(extracted_data, account, date_time_str, scraping_type)
    results_03 = task_03_openai_original(results_02, account)
    results_04 = task_04_openai_rewrite(results_03, account, date_time_str)
    return results_04


def chain_get_shares(extracted_data, scraping_type, account, date_time_str):
    """
    Задача B:
      05 - GET SHARES
    """
    print("---STARTED chain_B---")
    sharesCountResults = task_05_get_shares(extracted_data, scraping_type, account, date_time_str)
    return sharesCountResults


# =============================
# ГЛАВНАЯ ФУНКЦИЯ process_data
# =============================

def process_data(account, days=3, links=[], scheme=0, range_days=None, scraping_type="instagram"):
    start_time = time.time()
    print("process data started")

    now = datetime.now()
    date_time_str = now.strftime("%Y%m%d_%H%M%S")

    # Создаём базовую папку db/<account_id>
    save_path = os.path.join('db', str(account['id']))
    os.makedirs(save_path, exist_ok=True)

    # 01 - SCRAPING (синхронно)
    reelsData, extracted_data = task_01_scraping(
        account,
        days,
        scheme,
        range_days,
        scraping_type,
        date_time_str
    )
    if not extracted_data:
        # Если вдруг ничего не получили
        print("No extracted_data found, stop.")
        return

    # ПАРАЛЛЕЛЬНО: A) (02->03->04), B) (05)
    chain_main_results = None
    shares_results = None

    def parallel_chain_A():
        return chain_transcript_and_openai(extracted_data, account, date_time_str, scraping_type)

    def parallel_chain_B():
        return chain_get_shares(extracted_data, scraping_type, account, date_time_str)

    with ThreadPoolExecutor(max_workers=2) as executor:
        future_A = executor.submit(parallel_chain_A)
        # Задача B (05 - GET SHARES) — только если instagram
        if scraping_type == "instagram":
            future_B = executor.submit(parallel_chain_B)   
        else:
            future_B = None 

        # Ждём окончания A
        chain_main_results = future_A.result()

        # Если есть future_B (instagram), ждём и его
        if future_B:
            shares_results = future_B.result()


    # Если нам надо "объединять" данные из A и B
    results_final = chain_main_results
    if scraping_type == "instagram":
        for item in results_final:
            shortCode = item.get('shortCode')
            if shortCode in shares_results:

                if shares_results[shortCode] > 0 and item.get('videoPlayCount') > 0:
                    er_shares = float( round( shares_results[shortCode] / item.get('videoPlayCount'), 10))
                else:
                    er_shares = 0
                    
                item['shareCount'] = shares_results[shortCode]
                item['er_shares'] = er_shares

    # 06 - WRITE DATA TO GOOGLE SHEET
    task_06_write_data_to_gs(results_final, account, scheme, scraping_type, start_time)
    task_07_send_notification(results_final, account, scheme, scraping_type, start_time)

    return "Process completed successfully!"





def app_run(option="all", account_id=0, range_days="3-3", scraping_type="instagram"):
    logger.info("------APP IS RUNNING------")
    with open("db/main/db.json", "r", encoding="utf-8") as file:
        table_list = json.load(file)

    switcher = option  # This should be set appropriately as per your context
    if switcher == "one":
        process_data(table_list["accounts"][account_id], range_days=range_days, scheme=0, scraping_type=scraping_type)
        #process_data_onlyspez(table_list["accounts"][account_id], days=day_for_one, scheme=0)

    elif switcher == "pro":
        # For all accounts
        for account in table_list["accounts"]:
            if account["subscription"] == "pro":
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