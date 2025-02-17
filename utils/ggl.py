import gspread
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build
from dotenv import load_dotenv
import json, time

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
        all_headers = ["username", "hashtag", "trigger", "viewsFilter", "likesFilter", "reels_count"]
        expected_headers = [header for header in all_headers if header in sheet.row_values(1)]  # Проверяем наличие заголовков

        # Get all records with expected headers
        records = sheet.get_all_records(expected_headers=expected_headers)

        # Convert records to JSON format, filtering out rows with "off" triggers
        users_data = []

        for record in records:
            #print(record)
            if record.get("trigger") == "on":
                try:
                    if account['search_type'] == 'username':
                        user_data = {
                            "username": record.get("username"),
                            "viewsFilter":
                            int(record.get("viewsFilter", 0)),
                            "reels_count": int(record.get("reels_count", 0))
                        }
                    elif account['search_type'] == 'hashtag':
                        user_data = {
                            "hashtag": record.get("hashtag"),
                            "likesFilter":
                            int(record.get("likesFilter", 0)),
                            "reels_count": int(record.get("reels_count", 0))
                        }
                    users_data.append(user_data)
                except ValueError:
                    print(f"Skipping row with invalid data: {record}")
        return users_data
    except Exception as e:
        print(f"Ошибка в процессе get_table_data_as_json: {e}")
        return []

def check_duplicates(apify_data, account, scraping_type, list_name):
    try:
        print(f"Starting to check for duplicates for {account['username']}")

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

        # Get all values from the third column (C) starting from the second row
        existing_urls = sheet.col_values(3)[1:]  # Пропускаем заголовок

        # print(len(existing_urls))
        # print()
        # for url in existing_urls:
        #     print(url)
        apify_data_noDuplicates = []
        # Extract URLs from apify_data for comparison
        if scraping_type == 'instagram':
            apify_urls = {x.get('url', "") for x in apify_data}
            # Find duplicates
            duplicates = set(existing_urls) & apify_urls
            print(f'Count elements before check_duplicates: {len(apify_data)}')
            # Remove duplicates from apify_data
            apify_data_noDuplicates = [item for item in apify_data if item.get('url', "") not in duplicates]
            print(f'Count elements after check_duplicates: {len(apify_data_noDuplicates)}')
        elif scraping_type == 'tiktok':
            apify_urls = {x.get('postPage', "") for x in apify_data}
            # Find duplicates
            duplicates = set(existing_urls) & apify_urls
            print(f'Count elements before check_duplicates: {len(apify_data)}')
            # Remove duplicates from apify_data
            apify_data_noDuplicates = [item for item in apify_data if item.get('postPage', "") not in duplicates]
            print(f'Count elements after check_duplicates: {len(apify_data_noDuplicates)}')
            print("----------------")
            print("DUPLICATES")
            print(duplicates)
            print("----------------")


        return apify_data_noDuplicates
    except Exception as e:
        print(f"Ошибка в процессе check_duplicates: {e}")
        return apify_data  # Возвращаем оригинальные данные в случае ошибки


# account_test = {
#         "id": 28,
#         "username": "saloapp",
#         "username_tg": "saloapp_test",
#         "table_id": "1EuPZzHvbq4I9PkkSNKGPO8Rsyg6HbISOujpk8ievzzI",
#         "topics" : "",
#         "subscription" : "1week",
#         "update_date" : "friday",
#         "language" : "english",
#         "search_type" : "hashtag"
#     }

# apify_data_test = [
#     {"postPage": "https://www.tiktok.com/@dee.yope/video/7466135328869338401"},
#     {"postPage": "https://www.tiktok.com/@dee.yope/video/7466135328869338402"},
#     {"postPage": "https://www.tiktok.com/@dee.yope/video/7466135328869338403"},
#     {"postPage": "https://www.tiktok.com/@dee.yope/video/7466135328869338404"},
#     {"postPage": "https://www.tiktok.com/@dee.yope/video/7466135328869338405"},
#     {"postPage": "https://www.tiktok.com/@dee.yope/video/7466135328869338406"}
# ]

# apify_data_test = [
#     {"url": "https://www.tiktok.com/@dee.yope/video/7466135328869338401"},
#     {"url": "https://www.tiktok.com/@dee.yope/video/7466135328869338402"},
#     {"url": "https://www.tiktok.com/@dee.yope/video/7466135328869338403"},
#     {"url": "https://www.tiktok.com/@dee.yope/video/7466135328869338404"},
#     {"url": "https://www.tiktok.com/@dee.yope/video/7466135328869338405"},
#     {"url": "https://www.tiktok.com/@dee.yope/video/7466135328869338406"}
# ]

# check_duplicates(apify_data_test, account_test, "tiktok", "TIKTOK")



# Example usage
#table_id = "1C9bpCjytr-J1kruMLzt0X-omxQW0s0MJHyOvDILjtYs"
#list_name = "Data"
#json_results = get_table_data_as_json(table_id, list_name)
#print(json.dumps(json_results, indent=1))



###########################
# 1. Вспомогательная функция
###########################

def col_name(idx_zero_based: int) -> str:
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
                f'=len(INDIRECT("{col_name(name2idx["caption"])}"&ROW()))'
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
            "name": "er_followers-views",
            "value_func": lambda item, row_n, i2excel, name2idx: ( f'=TO_PERCENT({item.get("er_followers", "-")})')
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
                f'=TO_PERCENT({item.get("er_commlike", "")})'
                if item.get("er_commlike") != ""
                else ""
            )
        },
        {
            "name": "virus_detector",
            "value_func": lambda item, row_n, i2excel, name2idx: (
                f'=IF(COUNT(FILTER({col_name(name2idx["views"])}:{col_name(name2idx["views"])}, {col_name(name2idx["userlink"])}:{col_name(name2idx["userlink"])} = INDIRECT("{col_name(name2idx["userlink"])}"&ROW()))) = 1, 0, (INDIRECT("{col_name(name2idx["views"])}"&ROW()) - MEDIAN(FILTER({col_name(name2idx["views"])}:{col_name(name2idx["views"])}, {col_name(name2idx["userlink"])}:{col_name(name2idx["userlink"])} = INDIRECT("{col_name(name2idx["userlink"])}"&ROW())))) / (2 * (STDEV(FILTER({col_name(name2idx["views"])}:{col_name(name2idx["views"])}, {col_name(name2idx["userlink"])}:{col_name(name2idx["userlink"])} = INDIRECT("{col_name(name2idx["userlink"])}"&ROW())))  + 0.0000000001)))'
            )
        },
        {
            "name": "shares",
            "value_func": lambda item, row_n, i2excel, name2idx: item.get("shareCount", "")
        },
        {
            "name": "ER_shares_views",
            "value_func": lambda item, row_n, i2excel, name2idx: ( f'=TO_PERCENT({item.get("er_shares", "")})')
        },
        {
            "name": "duration",
            "value_func": lambda item, row_n, i2excel, name2idx: item.get("videoDuration", "")
        },
        {
            "name": "virus_status",
            "value_func": lambda item, row_n, i2excel, name2idx: (
                f'=IF(COUNTIF({col_name(name2idx["userlink"])}:{col_name(name2idx["userlink"])}, INDIRECT("{col_name(name2idx["userlink"])}"&ROW()))<4, "NO DATA", IF(INDIRECT("{col_name(name2idx["virus_detector"])}"&ROW())<-0.1, "LOW", IF(INDIRECT("{col_name(name2idx["virus_detector"])}"&ROW())<= 0.1, "AVERAGE", IF(INDIRECT("{col_name(name2idx["virus_detector"])}"&ROW())<=0.4, "GOOD", IF(INDIRECT("{col_name(name2idx["virus_detector"])}"&ROW())<=0.8, "BEST", "VIRUS")))))'
                )
        },
        {
            "name": "engagement_status",
            "value_func": lambda item, row_n, i2excel, name2idx: (
                f'=IF(AND(INDIRECT("{col_name(name2idx["er_commlike"])}"&ROW())<0.02,INDIRECT("{col_name(name2idx["ER_shares_views"])}"&ROW())<0.005), "LOW ER", IF(AND(INDIRECT("{col_name(name2idx["er_commlike"])}"&ROW())<=0.04,INDIRECT("{col_name(name2idx["ER_shares_views"])}"&ROW())<=0.01), "AVERAGE ER", "BEST ER"))'
                )
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
                f'=len(INDIRECT("{col_name(name2idx["caption"])}"&ROW()))'
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
                f'=IF(COUNT(FILTER({col_name(name2idx["views"])}:{col_name(name2idx["views"])}, {col_name(name2idx["userlink"])}:{col_name(name2idx["userlink"])} = INDIRECT("{col_name(name2idx["userlink"])}"&ROW()))) = 1, 0, (INDIRECT("{col_name(name2idx["views"])}"&ROW()) - MEDIAN(FILTER({col_name(name2idx["views"])}:{col_name(name2idx["views"])}, {col_name(name2idx["userlink"])}:{col_name(name2idx["userlink"])} = INDIRECT("{col_name(name2idx["userlink"])}"&ROW())))) / (2 * (STDEV(FILTER({col_name(name2idx["views"])}:{col_name(name2idx["views"])}, {col_name(name2idx["userlink"])}:{col_name(name2idx["userlink"])} = INDIRECT("{col_name(name2idx["userlink"])}"&ROW())))  + 0.0000000001)))'
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
        val = col_def["value_func"](item, row_number, col_name, name2idx)
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
        sheet_id = sheet.id

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
        #sheet.insert_rows(rows_to_insert, row=3, value_input_option='USER_ENTERED')
        #update existing filters

        sheet.insert_rows(rows_to_insert, row=3, value_input_option='USER_ENTERED')
        print("✅ Новая строка добавлена.")
        # try:
        #     #FILTER

        #     # 3️⃣ Считываем текущие фильтры
        #     service = build('sheets', 'v4', credentials=credentials)
        #     spreadsheet = service.spreadsheets().get(spreadsheetId=table_id).execute()
        #     sheet_info = next((s for s in spreadsheet['sheets'] if s['properties']['sheetId'] == sheet_id), None)

        #     if not sheet_info or "basicFilter" not in sheet_info:
        #         print("⚠️ Базовый фильтр не найден. Пропускаем обновление.")

        #     existing_filter = sheet_info["basicFilter"]
        #     print("🎯 Текущие фильтры перед обновлением:")
        #     print(json.dumps(existing_filter, indent=4, ensure_ascii=False))

        #     # 4️⃣ Сохраняем значения только для фильтруемых колонок
        #     criteria_columns = list(existing_filter.get("criteria", {}).keys())
        #     column_value_map = {}

        #     # Загружаем только нужные диапазоны для этих колонок
        #     ranges = [f"'TEST_FILTER'!{chr(65 + int(col))}2:{chr(65 + int(col))}" for col in criteria_columns]
        #     result = service.spreadsheets().values().batchGet(
        #         spreadsheetId=table_id,
        #         ranges=ranges
        #     ).execute()

        #     # Обрабатываем результат
        #     for idx, col in enumerate(criteria_columns):
        #         column_values = result.get("valueRanges", [])[idx].get("values", [])
        #         # Извлекаем уникальные значения, ограничиваем вывод
        #         unique_values = {val[0] for val in column_values if val}
        #         column_value_map[int(col)] = unique_values
        #         #print(f"📊 Колонка {col}: {list(unique_values)[:5]}... (показано 5 из {len(unique_values)})")

        #     # 5️⃣ Отключаем фильтры
        #     service.spreadsheets().batchUpdate(
        #         spreadsheetId=table_id,
        #         body={"requests": [{"clearBasicFilter": {"sheetId": sheet_id}}]}
        #     ).execute()
        #     #print("🚨 Фильтры отключены.")

        #     # 6️⃣ Добавляем новую строку
        #     header_row = sheet.row_values(1)
        #     new_row = ["" for _ in range(len(header_row))]
        #     try:
        #         virus_index = header_row.index("Вирусность")
        #         engagement_index = header_row.index("Вовлеченность")
        #         new_row[virus_index] = "NO DATA"
        #         new_row[engagement_index] = "LOW ER"
        #     except ValueError:
        #         print("⚠️ Столбцы 'Вирусность' или 'Вовлеченность' не найдены.")




        #     sheet.insert_rows(rows_to_insert, row=3, value_input_option='USER_ENTERED')
        #     print("✅ Новая строка добавлена.")




        #     # 7️⃣ Обновляем диапазон фильтра
        #     existing_filter["range"]["endRowIndex"] = sheet.row_count

        #     # 8️⃣ Восстанавливаем скрытые значения
        #     if "criteria" in existing_filter:
        #         for col_idx, criteria in existing_filter["criteria"].items():
        #             if "hiddenValues" in criteria:
        #                 current_hidden = set(criteria["hiddenValues"])
        #                 possible_values = column_value_map.get(int(col_idx), set())
        #                 # Добавляем только те скрытые значения, которые существуют
        #                 updated_hidden = current_hidden.intersection(possible_values)
        #                 existing_filter["criteria"][col_idx]["hiddenValues"] = list(updated_hidden)

        #     # 9️⃣ Восстанавливаем фильтры
        #     service.spreadsheets().batchUpdate(
        #         spreadsheetId=table_id,
        #         body={"requests": [{"setBasicFilter": {"filter": existing_filter}}]}
        #     ).execute()
        #     print("🔄 Фильтры восстановлены с обновлённым диапазоном.")
        # except Exception as e:
        #     print(f"Ошибка в процессе обработки в обновлении фильтров в ggl: {e}")

            
        print(f"Все данные успешно добавлены в таблицу")

    except Exception as e:
        print(f"Ошибка в процессе обработки в append_data_to_google_sheet в ggl: {e}")

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


