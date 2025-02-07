from re import S
from fastapi.params import Query
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv
import os, sys, json, time

# Загружаем переменные из .env
load_dotenv()

# Доступ к ключу

def get_table_data_as_json(account, list_name):
    try:
        print(f"Starting to collect data for {account['username']}")

        # Set up Google Sheets API credentials
        scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive.file",
            "https://www.googleapis.com/auth/drive"
        ]
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            'static/reelstranscription-a94a4b07252e.json', scope)
        client = gspread.authorize(credentials)

        # Open the Google Sheet
        google_sheet_url = f'https://docs.google.com/spreadsheets/d/{account["table_id"]}/edit?usp=sharing'
        sheet = client.open_by_url(google_sheet_url).worksheet(list_name)

        # Define the expected headers
        expected_headers = [
            "username", "trigger", "viewsFilter", "reels_count"
        ]

        # Get all records with expected headers
        records = sheet.get_all_records(expected_headers=expected_headers)

        # Convert records to JSON format, filtering out rows with "off" triggers
        users_data = []
        for record in records:
            #print(record)
            if record.get("trigger") == "on":
                try:
                    user_data = {
                        "username": record.get("username"),
                        "viewsFilter":
                        int(record.get("viewsFilter", 0)),
                        "reels_count": int(record.get("reels_count", 0))
                    }
                    users_data.append(user_data)
                except ValueError:
                    print(f"Skipping row with invalid data: {record}")
        return users_data
    except Exception as e:
        print(f"Ошибка в процессе get_table_data_as_json: {e}")
        return []



# Example usage
#table_id = "1C9bpCjytr-J1kruMLzt0X-omxQW0s0MJHyOvDILjtYs"
#list_name = "Data"
#json_results = get_table_data_as_json(table_id, list_name)
#print(json.dumps(json_results, indent=1))



###########################
# 1. Вспомогательная функция
###########################

def col_index_to_excel_name(idx_zero_based: int) -> str:
    """
    Преобразует индекс 0-based (0,1,2...) в название столбца (A,B,C...).
    0 -> A
    1 -> B
    25 -> Z
    26 -> AA
    27 -> AB
    ...
    """
    result = []
    i = idx_zero_based
    while True:
        i, r = divmod(i, 26)
        result.append(chr(r + ord('A')))
        if i == 0:
            break
        i -= 1
    return "".join(reversed(result))


def generate_original_script(item):
    """
    Формирует текст для колонки 'original_script'.
    """
    # Проверка на отсутствие текста
    if (
        item.get("original_script", {}).get("hook", "") == '-' and 
        item.get("original_script", {}).get("content", "") == '-' and 
        item.get("original_script", {}).get("cta", "") == '-'
    ):
        return (f'''НЕТ ТЕКСТА

#CAPTION
{item.get("caption", "")}''')
    
    # Формируем финальный текст
    return (
        f"""#HOOK
{item.get("original_script", {}).get("hook", "")}

#CONTENT
{item.get("original_script", {}).get("content", "")}

#CTA
{item.get("original_script", {}).get("cta", "")}

#CAPTION
{item.get("caption", "")}"""
    )


def generate_rewrited_script(item):
    """
    Формирует текст для колонки 'original_script'.
    """
    # Собираем префикс (song и humor, если они есть)
    prefix = ""
    if item.get("song"):
        prefix += '''>>>ВОЗМОЖНО ПЕСНЯ<<<
'''

    # Проверка на отсутствие текста
    if (
        item.get("rewrited_script", {}).get("hook", "") == '-' and 
        item.get("rewrited_script", {}).get("content", "") == '-' and 
        item.get("rewrited_script", {}).get("cta", "") == '-'
    ):
        return (f'''НЕТ ТЕКСТА
        
#CAPTION
{item.get("rewrited_script", {}).get("caption", "")}''')
    
    # Формируем финальный текст
    return (
        f"""{prefix}#HOOK
{item.get("rewrited_script", {}).get("hook", "")}

#CONTENT
{item.get("rewrited_script", {}).get("content", "")}

#CTA
{item.get("rewrited_script", {}).get("cta", "")}

#CAPTION
{item.get("rewrited_script", {}).get("caption", "")}"""
    )

###########################
# 2. Конфигурация столбцов
###########################
# Здесь объявляем, какие столбцы и в каком порядке должны быть
# для (scheme, scraping_type). 
# Каждый элемент — это словарь:
#   "name"       - любое уникальное имя столбца
#   "value_func" - функция (item, row_number, i2excel, name2idx), 
#                  которая возвращает финальное значение ячейки.
#
# Параметры внутри value_func:
#  - item       : один объект из json_results
#  - row_number : текущее значение new_number (номер строки «логический»)
#  - i2excel(i) : функция, которая вернёт буквенный код столбца по индексу
#  - name2idx   : словарь { "имя_столбца" -> индекс }, чтобы можно было
#                 сослаться на другие колонки



COLUMNS_CONFIG = {
    (0, "instagram"): [
        {
            "name": "num",
            "value_func": lambda item, row_n, i2excel, name2idx: row_n
        },
        {
            "name": "userlink",
            "value_func": lambda item, row_n, i2excel, name2idx: f'=HYPERLINK("{item.get("account_url", "")}", "{item.get("username", "")}")'
        },
        {
            "name": "url",
            "value_func": lambda item, row_n, i2excel, name2idx: item.get("url", "")
        },
        {
            "name": "timestamp",
            "value_func": lambda item, row_n, i2excel, name2idx: item.get("timestamp", "")
        },
        {
            "name": "topic",
            "value_func": lambda item, row_n, i2excel, name2idx: item.get("topic", "")
        },
        {
            "name": "theme",
            "value_func": lambda item, row_n, i2excel, name2idx: item.get("theme", "")
        },
        {
            "name": "hook",
            "value_func": lambda item, row_n, i2excel, name2idx: item["original_script"].get("hook", "")
        },
        {
            "name": "caption",
            "value_func": lambda item, row_n, i2excel, name2idx: item.get("caption", "")
        },
        {
            "name": "len_caption",
            "value_func": lambda item, row_n, i2excel, name2idx:
                f'=len(INDIRECT("{col_index_to_excel_name(name2idx["caption"])}"&ROW()))'
        },
        {
            "name": "followers",
            "value_func": lambda item, row_n, i2excel, name2idx: ""
        },
        {
            "name": "views",
            "value_func": lambda item, row_n, i2excel, name2idx: item.get("videoPlayCount", "")
        },
        {
            "name": "er_followers-views",
            "value_func": lambda item, row_n, i2excel, name2idx: ""
        },
        {
            "name": "likes",
            "value_func": lambda item, row_n, i2excel, name2idx: item.get("likesCount", "")
        },
        {
            "name": "comments",
            "value_func": lambda item, row_n, i2excel, name2idx: item.get("commentsCount", "")
        },
        {
            "name": "er_commlike",
            "value_func": lambda item, row_n, i2excel, name2idx: (
                f'=TO_PERCENT({item.get("er_commlike", "-")})'
                if item.get("er_commlike") != "-"
                else "-"
            )
        },
        {
            "name": "virus_detector",
            "value_func": lambda item, row_n, i2excel, name2idx: (
                f'=IF(COUNT(FILTER({col_index_to_excel_name(name2idx["views"])}:{col_index_to_excel_name(name2idx["views"])}, {col_index_to_excel_name(name2idx["userlink"])}:{col_index_to_excel_name(name2idx["userlink"])} = INDIRECT("{col_index_to_excel_name(name2idx["userlink"])}"&ROW()))) = 1, 0, (INDIRECT("{col_index_to_excel_name(name2idx["views"])}"&ROW()) - MEDIAN(FILTER({col_index_to_excel_name(name2idx["views"])}:{col_index_to_excel_name(name2idx["views"])}, {col_index_to_excel_name(name2idx["userlink"])}:{col_index_to_excel_name(name2idx["userlink"])} = INDIRECT("{col_index_to_excel_name(name2idx["userlink"])}"&ROW())))) / (2 * STDEV(FILTER({col_index_to_excel_name(name2idx["views"])}:{col_index_to_excel_name(name2idx["views"])}, {col_index_to_excel_name(name2idx["userlink"])}:{col_index_to_excel_name(name2idx["userlink"])} = INDIRECT("{col_index_to_excel_name(name2idx["userlink"])}"&ROW())))))'
            )
        },
        {
            "name": "shares",
            "value_func": lambda item, row_n, i2excel, name2idx: item.get("shareCount", "")
        },
        {
            "name": "ER_shares_views",
            "value_func": lambda item, row_n, i2excel, name2idx: (
                '=IF(OR(INDIRECT("Q"&ROW())="", INDIRECT("K"&ROW())="", INDIRECT("Q"&ROW())="-", NOT(ISNUMBER(INDIRECT("Q"&ROW())))), '
                '"NoN", INDIRECT("Q"&ROW())/INDIRECT("K"&ROW()))'
            )
        },
        {
            "name": "duration",
            "value_func": lambda item, row_n, i2excel, name2idx: item.get("videoDuration", "")
        },
        {
            "name": "original_script",
            "value_func": lambda item, row_n, i2excel, name2idx: generate_original_script(item)
        },
        {
            "name": "rewrited_script",
            "value_func": lambda item, row_n, i2excel, name2idx: generate_rewrited_script(item)
        },
        {
            "name": "musicInfo",
            "value_func": lambda item, row_n, i2excel, name2idx: item.get("musicInfo", "")
        }
    ],

    (0, "tiktok"): [
        # Аналогично, но нужный порядок и функции для TikTok
        {
            "name": "num",
            "value_func": lambda item, row_n, i2excel, name2idx: row_n
        },
        {
            "name": "userlink",
            "value_func": lambda item, row_n, i2excel, name2idx: f'=HYPERLINK("{item.get("account_url", "")}", "{item.get("username", "")}")'
        },
        {
            "name": "url",
            "value_func": lambda item, row_n, i2excel, name2idx: item.get("url", "")
        },
        {
            "name": "timestamp",
            "value_func": lambda item, row_n, i2excel, name2idx: item.get("timestamp", "")
        },
        {
            "name": "topic",
            "value_func": lambda item, row_n, i2excel, name2idx: item.get("topic", "")
        },
        {
            "name": "theme",
            "value_func": lambda item, row_n, i2excel, name2idx: item.get("theme", "")
        },
        {
            "name": "empty",
            "value_func": lambda item, row_n, i2excel, name2idx: ""
        },
        {
            "name": "caption",
            "value_func": lambda item, row_n, i2excel, name2idx: item.get("caption", "")
        },
        {
            "name": "len_caption",
            "value_func": lambda item, row_n, i2excel, name2idx:
                f'=len(INDIRECT("{col_index_to_excel_name(name2idx["caption"])}"&ROW()))'
        },
        {
            "name": "followers",
            "value_func": lambda item, row_n, i2excel, name2idx: item.get("followersCount", "")
        },
        {
            "name": "views",
            "value_func": lambda item, row_n, i2excel, name2idx: item.get("videoPlayCount", "")
        },
        {
            "name": "er_followers",
            "value_func": lambda item, row_n, i2excel, name2idx: item.get("er_followers", "")
        },
        {
            "name": "likes",
            "value_func": lambda item, row_n, i2excel, name2idx: item.get("likesCount", "")
        },
        {
            "name": "comments",
            "value_func": lambda item, row_n, i2excel, name2idx: item.get("commentsCount", "")
        },
        {
            "name": "shares",
            "value_func": lambda item, row_n, i2excel, name2idx: item.get("shareCount", "")
        },
        {
            "name": "saves",
            "value_func": lambda item, row_n, i2excel, name2idx: item.get("collectCount", "")
        },
        {
            "name": "er_all",
            "value_func": lambda item, row_n, i2excel, name2idx: (f'=TO_PERCENT({item.get("er_all", "-")})')
        },
        {
            "name": "er_shares",
            "value_func": lambda item, row_n, i2excel, name2idx: ( f'=TO_PERCENT({item.get("er_shares", "-")})')
        },
        {
            "name": "virus_detector",
            "value_func": lambda item, row_n, i2excel, name2idx: (
                f'=IF(COUNT(FILTER({col_index_to_excel_name(name2idx["views"])}:{col_index_to_excel_name(name2idx["views"])}, {col_index_to_excel_name(name2idx["userlink"])}:{col_index_to_excel_name(name2idx["userlink"])} = INDIRECT("{col_index_to_excel_name(name2idx["userlink"])}"&ROW()))) = 1, 0, (INDIRECT("{col_index_to_excel_name(name2idx["views"])}"&ROW()) - MEDIAN(FILTER({col_index_to_excel_name(name2idx["views"])}:{col_index_to_excel_name(name2idx["views"])}, {col_index_to_excel_name(name2idx["userlink"])}:{col_index_to_excel_name(name2idx["userlink"])} = INDIRECT("{col_index_to_excel_name(name2idx["userlink"])}"&ROW())))) / (2 * STDEV(FILTER({col_index_to_excel_name(name2idx["views"])}:{col_index_to_excel_name(name2idx["views"])}, {col_index_to_excel_name(name2idx["userlink"])}:{col_index_to_excel_name(name2idx["userlink"])} = INDIRECT("{col_index_to_excel_name(name2idx["userlink"])}"&ROW())))))'
            )
        },
        {
            "name": "duration",
            "value_func": lambda item, row_n, i2excel, name2idx: item.get("videoDuration", "")
        },
        {
            "name": "original_script",
            "value_func": lambda item, row_n, i2excel, name2idx: generate_original_script(item)
        },
        {
            "name": "rewrited_script",
            "value_func": lambda item, row_n, i2excel, name2idx: generate_rewrited_script(item)
        },
        {
            "name": "musicInfo",
            "value_func": lambda item, row_n, i2excel, name2idx: item.get("musicInfo", "")
        }
    ],

    (2, "instagram"): [
        # Пример для scheme=2
        # Здесь можно аналогично прописать нужные столбцы
        # ...
    ],
}

############################
# 3. Генерация данных строки
############################



def generate_row_data(item, row_number, scheme, scraping_type):
    """
    Возвращает список значений ячеек для конкретного 'item' и 'row_number',
    в том порядке, в котором они описаны в COLUMNS_CONFIG[(scheme, scraping_type)].
    """
    columns = COLUMNS_CONFIG.get((scheme, scraping_type), [])
    # name2idx: { "название_столбца" -> индекс_в_этом_списке }
    name2idx = {}
    for i, col_def in enumerate(columns):
        name2idx[col_def["name"]] = i

    row_values = []
    for i, col_def in enumerate(columns):
        val = col_def["value_func"](item, row_number, col_index_to_excel_name, name2idx)
        row_values.append(val)
    return row_values


############################
# 4. Основная функция
############################

def append_data_to_google_sheet(json_results, table_id, list_name, scheme=0, scraping_type=None):
    try:
        print('Starting collect data for google sheet')
        # --- Авторизация ---
        scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive.file",
            "https://www.googleapis.com/auth/drive"
        ]
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            'static/reelstranscription-a94a4b07252e.json', scope)
        client = gspread.authorize(credentials)

        # --- Открываем таблицу ---
        google_sheet_url = f'https://docs.google.com/spreadsheets/d/{table_id}/edit?usp=sharing'
        sheet = client.open_by_url(google_sheet_url).worksheet(list_name)

        # --- Считываем текущее значение нумерации в A3 (3-я строка, 1-й столбец) ---
        cell_value = sheet.cell(3, 1).value
        if cell_value is None or not cell_value.isdigit():
            new_number = 1
        else:
            new_number = int(cell_value) + 1

        # --- Подготавливаем строки для вставки ---
        rows_to_insert = []
        for i, item in enumerate(json_results):
            row_to_insert = generate_row_data(item, new_number, scheme, scraping_type)
            rows_to_insert.append(row_to_insert)
            new_number += 1
            print(f'Запись {i + 1} добавлена в список для отправки')

        # --- Вставляем сразу все данные (реверсом, если нужно) ---
        rows_to_insert.reverse()
        sheet.insert_rows(rows_to_insert, row=3, value_input_option='USER_ENTERED')
        print(f"Все данные успешно добавлены в таблицу")

    except Exception as e:
        print(f"Ошибка в процессе обработки в ggl: {e}")

    print("Done!")



############################
# SCRAPE NUMBER OF REELS IN TABLES
############################


def get_video_processed_number(account):
    try:
        print(f"----Starting to collect data for {account['username']}")

        # Set up Google Sheets API credentials
        scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive.file",
            "https://www.googleapis.com/auth/drive"
        ]
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            'static/reelstranscription-a94a4b07252e.json', scope)
        client = gspread.authorize(credentials)

        # Open the Google Sheet
        google_sheet_url = f'https://docs.google.com/spreadsheets/d/{account["table_id"]}/edit?usp=sharing'
        # Open the Google Sheets for both INSTAGRAM and TIKTOK
        instagram_sheet = client.open_by_url(google_sheet_url).worksheet('INSTAGRAM')
        tiktok_sheet = client.open_by_url(google_sheet_url).worksheet('TIKTOK')

        # Read the value from cell A3 for both sheets
        instagram_a3_value = instagram_sheet.cell(3, 1).value
        tiktok_a3_value = tiktok_sheet.cell(3, 1).value

        print(f"INSTAGRAM A3 Value: {instagram_a3_value}")
        print(f"TIKTOK A3 Value: {tiktok_a3_value}")
        return instagram_a3_value, tiktok_a3_value
    except Exception as e:
        print(f"Ошибка в процессе get_table_data_as_json: {e}")
        return None

def sum_a3_values():

    with open("db/main/db.json", "r", encoding="utf-8") as file:
        table_list = json.load(file)
    
    total_instagram_a3 = 0
    total_tiktok_a3 = 0

    for account in table_list["accounts"]:
        try:
            instagram_a3_value, tiktok_a3_value = get_video_processed_number(account)
            
            # Проверяем, что значения не None и преобразуем их в целые числа
            if instagram_a3_value is not None:
                total_instagram_a3 += int(instagram_a3_value)
            if tiktok_a3_value is not None:
                total_tiktok_a3 += int(tiktok_a3_value)
            time.sleep(2)
            print(f'-----account {account["username"]} scrapped')
        except Exception as e:
            print(f"Ошибка в процессе for account in table_list: {e}")
            return None

    print(f"Total INSTAGRAM A3 Value: {total_instagram_a3}")
    print(f"Total TIKTOK A3 Value: {total_tiktok_a3}")
    sum = total_instagram_a3+total_tiktok_a3
    print(f"Total SUM: {sum}")
    return sum


#sum_a3_values()



############################
# DEBUG
############################
'''
with open("db/22/damir_result_20250104_151517.json", "r", encoding="utf-8") as file:
    results = json.load(file)
append_data_to_google_sheet(results, "1uXEWHBW2aNChgtR9mB4JOV-fpTZS83i_oMT_Ar-vtJo", 'TIKTOK', scraping_type="tiktok")
'''


