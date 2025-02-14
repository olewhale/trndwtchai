import os
import asyncio
import requests
from dotenv import load_dotenv
from telegram import Bot

# Загружаем переменные окружения из .env
load_dotenv()

# Получаем токен бота из .env
TELEGRAM_BOT_API = os.getenv("TELEGRAM_BOT_API")

if not TELEGRAM_BOT_API:
    raise ValueError("Токен бота не найден в .env файле!")

def get_chat_id_from_username(username):
    """
    Получает chat_id по Telegram username, если бот уже получал сообщения от пользователя.

    Аргументы:
    - username (str): Username пользователя без @.

    Возвращает:
    - int: chat_id пользователя, если найден.
    - None: если chat_id не найден.
    """
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_API}/getUpdates"

    response = requests.get(url)
    data = response.json()

    if not data.get("ok"):
        print("Ошибка при получении обновлений:", data)
        return None

    for update in data.get("result", []):
        if "message" in update:
            user = update["message"]["from"]
            if user.get("username") == username:
                return user.get("id")  # Это и есть chat_id

    print(f"Пользователь {username} не найден в обновлениях.")
    return None

async def send_message(bot, chat_id, reels_count=None, tiktok_count=None, table_link=""):
    """Асинхронно отправляет сообщение с информацией о загруженных данных."""
    try:
        message_parts = ["В таблицу добавлено:"]
        
        if reels_count:
            message_parts.append(f"🟣 {reels_count} reels")
        
        if tiktok_count:
            message_parts.append(f"🔴 {tiktok_count} tiktok")

        if table_link:
            message_parts.append(f"[Ссылка на таблицу]({table_link})")

        message = "\n".join(message_parts)

        await bot.send_message(chat_id=chat_id, text=message, parse_mode="Markdown", disable_web_page_preview=True)
        print("Сообщение успешно отправлено.")
    except Exception as e:
        print(f"Ошибка при отправке сообщения в send_message: {e}")

def send_table_update(results, account):
    try:
        username = account.get('username_tg', '').lstrip('@')  # Удаляем @, если он есть
        if not username:
            print("Ошибка: username_tg отсутствует в аккаунте.")
            return

        # Получаем chat_id синхронно через getUpdates
        chat_id = get_chat_id_from_username(username)

        if not chat_id:
            print(f"Не удалось получить chat_id для {username}. Сообщение не отправлено.")
            return

        print(f"Chat ID найден: {chat_id}, username: {account['username']}")

        bot = Bot(token=TELEGRAM_BOT_API)

        reels_count = sum(1 for result in results if result.get('platform') == 'instagram')
        tiktok_count = sum(1 for result in results if result.get('platform') == 'tiktok')
        table_link = f"https://docs.google.com/spreadsheets/d/{account['table_id']}"

        # Запускаем асинхронную отправку сообщения
        asyncio.run(send_message(bot, chat_id, reels_count, tiktok_count, table_link))
    except Exception as e:
        print(f"Ошибка при отправке сообщения в send_table_update: {e}")
