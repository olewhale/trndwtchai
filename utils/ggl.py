from re import S
from fastapi.params import Query
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv
import os, sys

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
            "username", "trigger", "viewsFilter_K", "reels_count"
        ]

        # Get all records with expected headers
        records = sheet.get_all_records(expected_headers=expected_headers)

        # Convert records to JSON format, filtering out rows with "off" triggers
        users_data = []
        for record in records:
            if record.get("trigger") == "on":
                try:
                    user_data = {
                        "username": record.get("username"),
                        "viewsFilter":
                        int(record.get("viewsFilter_K", 0)) * 1000,
                        "reels_count": int(record.get("reels_count", 0))
                    }
                    users_data.append(user_data)
                except ValueError:
                    print(f"Skipping row with invalid data: {record}")
        return users_data
    except Exception as e:
        print(f"Ошибка в процессе get_table_data_as_json: {e}")
        return []


def append_data_to_google_sheet(json_results, table_id, list_name, scheme=0):
    try:
        print('Starting collect data for google sheet')
        # Step 1: Set up Google Sheets API credentials
        scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive.file",
            "https://www.googleapis.com/auth/drive"
        ]
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            'static/reelstranscription-a94a4b07252e.json', scope)
        client = gspread.authorize(credentials)

        # Step 2: Open the Google Sheet
        google_sheet_url = f'https://docs.google.com/spreadsheets/d/{table_id}/edit?usp=sharing'
        sheet = client.open_by_url(google_sheet_url).worksheet(list_name)

        # Step 3: Проверяем значение в A3
        cell_value = sheet.cell(3, 1).value
        if cell_value is None or not cell_value.isdigit():
            new_number = 1  # Если там пусто или не число, ставим 1
        else:
            new_number = int(cell_value) + 1  # Если там есть число, то +1

        # Step 4: Собираем все данные в список строк
        rows_to_insert = []
        for i, item in enumerate(json_results):
            # Разделяем строку на строки
            txt = item.get("translatedCaption", "")
            translated_caption = txt.replace("\\n\\n", "\n\n")
            song_notification = ""
            humor_notification = ""
            if item.get("song") == 1:
                song_notification = '''>>>ВОЗМОЖНО ЭТО ТЕКСТ ПЕСНИ<<<
                '''
            if item.get("humor") == 1:
                humor_notification = '''>>>ВОЗМОЖНО ЕСТЬ ЮМОР<<<
                '''
            original_script = f'''{song_notification}#HOOK
{item["original_script"].get("hook", "")}

#CONTENT
{item["original_script"].get("content", "")}

#CTA
{item["original_script"].get("cta", "")}

#CAPTION
{item.get("caption", "")}'''

            rewrited_script = f'''{song_notification}{humor_notification}#HOOK
{item["rewrited_script"].get("hook", "")}

#CONTENT
{item["rewrited_script"].get("content", "")}

#CTA
{item["rewrited_script"].get("cta", "")}

#CAPTION
{item["rewrited_script"].get("caption", "")}'''
            if scheme == 0:
                values = {
                    "A":
                    new_number,  # account_url
                    "B":
                    f'=HYPERLINK("{item.get("account_url", "")}", "{item.get("username", "")}")',  # username and url
                    "C":
                    item.get("url", ""),  # url,
                    "D":
                    item.get("timestamp", ""),  # timestamp
                    "E":
                    item.get("topic", ""),  # topic
                    "F":
                    item.get("theme", ""),  # theme
                    "G":
                    item["original_script"].get("hook", ""),  # hook
                    "H":
                    "",  # text_hook # TODO: add text_hook
                    "I":
                    item.get("caption", ""),  # caption
                    "J":
                    '=len(INDIRECT("I"&ROW()))',  # video_type
                    "K":
                    item.get("videoPlayCount", ""),  # playCount
                    "L":
                    item.get("likesCount", ""),  # likes
                    "M":
                    item.get("commentsCount", ""),  # comments
                    "N":
                    f'=TO_PERCENT({item.get("engagement", "-")})' if
                    item.get("engagement") != "-" else "-",  # engagement
                    "O":
                    '=IF(COUNT(FILTER(K:K, B:B = INDIRECT("B"&ROW()))) = 1, 0, (INDIRECT("K"&ROW()) - MEDIAN(FILTER(K:K, B:B = INDIRECT("B"&ROW())))) / (2 * STDEV(FILTER(K:K, B:B = INDIRECT("B"&ROW())))))',  #virus_detector
                    "P":
                    item.get("shareCount", ""),  # shares
                    "Q":
                    '=IF(OR(INDIRECT("P"&ROW())="", INDIRECT("K"&ROW())="", INDIRECT("P"&ROW())="-", NOT(ISNUMBER(INDIRECT("P"&ROW())))), "NoN", INDIRECT("P"&ROW())/INDIRECT("K"&ROW()))',  # ER shares/views
                    "R":
                    item.get("videoDuration", ""),  # duration
                    "S":
                    original_script,  # script
                    "T":
                    rewrited_script,  # script_adapted
                    "U":
                    '',  # adapted_script
                    "V":
                    '',  # storyboard
                    "W":
                    '',  # used
                }
            elif scheme == 2:
                err_shares = item.get("sharesCount", -1) / item.get(
                    "likesCount", -1)
                values = {
                    "A":
                    new_number,  # account_url
                    "B":
                    f'=HYPERLINK("{item.get("account_url", "")}", "{item.get("username", "")}")',  # username and url
                    "C":
                    item.get("url", ""),  # url,
                    "D":
                    item.get("timestamp", ""),  # timestamp
                    "E":
                    item.get("topic", ""),  # topic
                    "F":
                    item.get("theme", ""),  # theme
                    "G":
                    item["original_script"].get("hook", ""),  # hook
                    "H":
                    "",  # text_hook # TODO: add text_hook
                    "I":
                    item.get("caption", ""),  # caption
                    "J":
                    '=len(INDIRECT("I"&ROW()))',  # video_type
                    "K":
                    item.get("videoPlayCount", ""),  # playCount
                    "L":
                    item.get("likesCount", ""),  # likes
                    "M":
                    item.get("commentsCount", ""),  # comments
                    "N":
                    item.get("shareCount", ""),  # shares
                    "O":
                    item.get("collectCount", ""),  # saves
                    "P":
                    f'=TO_PERCENT({item.get("engagement", "1")})'
                    if item.get("engagement") != "-" else
                    "-",  # engagement shares/plays
                    "Q":
                    f'=TO_PERCENT({err_shares})',  # engagement
                    "R":
                    '=IF(COUNT(FILTER(K:K, B:B = INDIRECT("B"&ROW()))) = 1, 0, (INDIRECT("K"&ROW()) - MEDIAN(FILTER(K:K, B:B = INDIRECT("B"&ROW())))) / (2 * STDEV(FILTER(K:K, B:B = INDIRECT("B"&ROW())))))',  #virus_detector
                    "S":
                    item.get("videoDuration", ""),  # duration
                    "T":
                    original_script,  # script
                    "U":
                    rewrited_script,  # script_adapted
                    "V":
                    '',  # adapted_script
                    "W":
                    '',  # storyboard
                    "X":
                    '',  # used
                }

            # Convert dictionary values to a list for appending to the sheet
            row_to_insert = [values[col] for col in sorted(values.keys())]
            rows_to_insert.append(row_to_insert)

            # Увеличиваем номер для следующей строки
            new_number += 1

            print(f'Запись {i + 1} добавлена в список для отправки')

        # Step 5: Вставляем все данные одним запросом
        rows_to_insert.reverse(
        )  # Reverse the list to insert in the correct order
        sheet.insert_rows(rows_to_insert,
                          row=3,
                          value_input_option='USER_ENTERED')
        print(f"Все данные успешно добавлены в таблицу")

    except Exception as e:
        print(f"Ошибка в процессе обработки в ggl: {e}")

    print("Done!")


# Example usage
#table_id = "1C9bpCjytr-J1kruMLzt0X-omxQW0s0MJHyOvDILjtYs"
#list_name = "Data"
#json_results = get_table_data_as_json(table_id, list_name)
#print(json.dumps(json_results, indent=1))
