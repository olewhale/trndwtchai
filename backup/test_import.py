import os
import json
import time
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

# Ваши модули:
# import ggl
# import sh
# import gpt
# import apify  # содержит: instagram_posts_scrapper, instagram_scrapper_filter_sorter, extracted_reels_data_maker, и т.д.
# from faster_whisper import WhisperModel

# Допустим, у вас есть эти функции где-то в коде:
# from your_code import download_videos, process_reel, insert_transcription

# =============================
# БЛОК ПОДЗАДАЧ (01 - 06)
# =============================

def task_01_scraping(account, days, scheme, range_days, scraping_type, date_time_str, debug=0):
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

    # Подготовим переменные для итогов
    reelsData = []
    extracted_data = []

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
        else:
            # DEBUG-режим (если есть свои заглушечные данные):
            with open("db/manual/test_asyncio.json", "r", encoding="utf-8") as file:
                dataset_items = json.load(file)

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
            dataset_items = apify.tiktok_posts_scrapper(users_data, start_of_day, range_days=range_days)

            with open(save_path_apify_database, "w", encoding="utf-8") as f:
                json.dump(dataset_items, f, ensure_ascii=False, indent=4)
        else:
            # DEBUG-режим
            with open("db/manual/test_asyncio.json", "r", encoding="utf-8") as file:
                dataset_items = json.load(file)

        if not dataset_items:
            print('No tiktok data found')
            return [], []

        reelsData, sorted_data, sortedReelsCount = apify.tiktok_scrapper_filter_sorter(
            dataset_items, users_data, start_of_day, end_of_day
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

    return reelsData, extracted_data


def task_02_transcription(extracted_data, account, date_time_str, scraping_type):
    """
    02 - TRANSCRIPTION
    (Как в вашем предыдущем коде.)
    """
    # Шаг 1: скачиваем видео
    transcript_data = download_videos(extracted_data, scraping_type)

    # Шаг 2: путь для сохранения транскриптов
    output_filename = f"{account['username']}_transcriptions_{date_time_str}.json"
    save_path_transcript = os.path.join('db', str(account['id']), output_filename)

    # Пустой файл
    with open(save_path_transcript, "w", encoding="utf-8") as file:
        json.dump("", file, ensure_ascii=False, indent=4)

    # Инициализация модели
    model = WhisperModel("small", device="cuda", compute_type="float16")

    # Цикл транскрибации
    for shortCode in tqdm(transcript_data, desc="Процесс транскрибации", unit="рилс"):
        try:
            transcript_data[shortCode] = process_reel(shortCode,
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
    results = insert_transcription(extracted_data, transcript_data)
    return results


def task_03_openai_original(results):
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

    for index, item in tqdm(enumerate(results, start=1),
                            total=len_results,
                            desc="Process spez_rewriter:",
                            unit="reel"):
        transcription = item.get('transcription')
        if transcription != "Ошибка транскрибации":
            original_script = item.get('original_script', {})
            hook = original_script.get('hook', '')
            content = original_script.get('content', '')
            cta = original_script.get('cta', '')

            spez_rewriter_answer = gpt.spez_rewriter_script(
                {'hook': hook, 'content': content, 'cta': cta},
                item.get('caption')
            )
            item['rewrited_script'] = {
                "hook":    spez_rewriter_answer.get('hook', '-'),
                "content": spez_rewriter_answer.get('content', '-'),
                "cta":     spez_rewriter_answer.get('cta', '-'),
                "caption": spez_rewriter_answer.get('caption', '')
            }
        else:
            # Нет транскрипции
            spez_rewriter_answer = gpt.spez_rewriter_script({}, item.get('caption'))
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


def task_05_get_shares(extracted_data, scraping_type, account, date_time_str):
    """
    05 - GET SHARES
    """
    if scraping_type == "instagram":
        result_filename = f"{account['username']}_result_{date_time_str}.json"
        save_path_result = os.path.join('db', str(account['id']), result_filename)
        try:
            shareCountResults = sh.execute_shares_scraping(extracted_data, result_filename, save_path_result)
        except Exception as e:
            print(f"Ошибка в процессе получения репостов: {e}")
    return shareCountResults


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
        print("*")
        print(f"Общее время обработки: {total_process_time_print:.2f} секунд")
        print("*")
        print("*")
        print("*")

        return "Process completed successfully!"
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
    results_02 = task_02_transcription(extracted_data, account, date_time_str, scraping_type)
    results_03 = task_03_openai_original(results_02)
    results_04 = task_04_openai_rewrite(results_03, account, date_time_str)
    return results_04


def chain_get_shares(extracted_data, scraping_type, account, date_time_str):
    """
    Задача B:
      05 - GET SHARES
    """
    results_05 = task_05_get_shares(extracted_data, scraping_type, account, date_time_str)
    return results_05


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
    extracted_data = task_01_scraping(
        account,
        days,
        scheme,
        range_days,
        scraping_type,
        date_time_str,
        debug=0
    )
    if not extracted_data:
        # Если вдруг ничего не получили
        print("No extracted_data found, stop.")
        return

    # ПАРАЛЛЕЛЬНО: A) (02->03->04), B) (05)
    results_A = None
    results_B = None

    def parallel_chain_A():
        return chain_transcript_and_openai(extracted_data, account, date_time_str, scraping_type)

    def parallel_chain_B():

        return chain_get_shares(extracted_data, scraping_type, account, date_time_str)


    with ThreadPoolExecutor(max_workers=2) as executor:
        future_A = executor.submit(parallel_chain_A)
        future_B = executor.submit(parallel_chain_B)

        for f in as_completed([future_A, future_B]):
            if f is future_A:
                results_A = f.result()
            else:
                results_B = f.result()

    # Если нам надо "объединять" данные из A и B — тут можно дописать merge.
    # Для простоты возьмём за основу results_A:
    results_final = results_A

    # 06 - WRITE DATA TO GOOGLE SHEET
    task_06_write_data_to_gs(results_final, account, scheme, scraping_type, start_time)

    return "Process completed successfully!"
