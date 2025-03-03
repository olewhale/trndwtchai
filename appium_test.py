from concurrent.futures import ThreadPoolExecutor
from appium import webdriver
from appium.options.android import UiAutomator2Options
import random
import os
import time
from dotenv import load_dotenv
import logging

#appium --allow-insecure adb_shell -p 4723
#appium --allow-insecure adb_shell -p 4725

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("process_logs.log", mode="w", encoding="utf-8")
    ]
)

load_dotenv()

def init_driver(device_name, port):
    """Инициализация Appium-драйвера"""
    options = UiAutomator2Options()
    options.platform_name = 'Android'
    options.automation_name = 'UiAutomator2'
    options.device_name = device_name
    options.udid = device_name  # Явно указываем UDID для привязки к эмулятору
    options.app_package = 'com.instagram.android'
    options.app_activity = '.main.MainActivity'
    options.no_reset = True
    options.full_reset = False
    options.uiautomator2_server_launch_timeout = 60000
    options.adb_exec_timeout = 60000
    
    server_url = f"http://localhost:{port}"  # Базовый маршрут для Appium v2
    logging.info(f"[{device_name}] Попытка подключения к {server_url}")
    try:
        driver = webdriver.Remote(server_url, options=options)
        logging.info(f"[{device_name}] Подключено к устройству с UDID: {driver.capabilities['udid']}")
        return driver
    except Exception as e:
        logging.error(f"[{device_name}] Ошибка инициализации драйвера: {e}")
        raise

def send_instagram_link_to_device(device_name, port, instagram_url):
    """Синхронная отправка ссылки на устройство"""
    driver = None
    try:
        driver = init_driver(device_name, port)
        logging.info(f"[{device_name}] Appium драйвер инициализирован")

        # Проверка текущего пакета и запуск Instagram, если он не активен
        current_package = driver.current_package
        if current_package != 'com.instagram.android':
            driver.start_activity('com.instagram.android', '.main.MainActivity')
            logging.info(f"[{device_name}] Принудительный запуск Instagram")
        
        time.sleep(5)  # Даём время на запуск приложения

        # Преобразование URL в reel-формат
        reel_url = instagram_url if 'reel' in instagram_url else instagram_url.replace('/p/', '/reel/')
        logging.info(f"[{device_name}] Подготовленный URL: {reel_url}")

        # Отправка deep link
        driver.execute_script('mobile: deepLink', {
            'url': reel_url,
            'package': 'com.instagram.android',
            'waitForLaunch': True
        })
        logging.info(f"[{device_name}] Ссылка {reel_url} отправлена через deepLink")

        delay = random.uniform(4, 6)
        time.sleep(delay)  # Синхронное ожидание
        logging.info(f"[{device_name}] Ожидание {delay:.2f} сек завершено")

    except Exception as e:
        logging.error(f"[{device_name}] Ошибка: {str(e)}")

    finally:
        if driver:
            try:
                driver.quit()
                logging.info(f"[{device_name}] Драйвер закрыт")
            except Exception as e:
                logging.error(f"[{device_name}] Ошибка при закрытии драйвера: {e}")

def open_link_on_two_devices():
    """Параллельное открытие ссылок на двух устройствах с использованием потоков"""
    devices = [
        {"name": "emulator-5554", "port": "4723", "instagram_url": "https://www.instagram.com/p/DEz2COYvOBJ/"},
        {"name": "emulator-5556", "port": "4725", "instagram_url": "https://www.instagram.com/p/DEN4xTgNwxB/"}
    ]
    
    # Используем ThreadPoolExecutor для параллельного запуска на двух ядрах
    with ThreadPoolExecutor(max_workers=2) as executor:
        futures = [
            executor.submit(send_instagram_link_to_device, device["name"], device["port"], device["instagram_url"])
            for device in devices
        ]
        # Ожидаем завершения всех потоков
        for future in futures:
            try:
                future.result()  # Получаем результат или исключение из потока
            except Exception as e:
                logging.error(f"Ошибка в потоке: {e}")

def main():
    """Основная функция"""
    try:
        open_link_on_two_devices()
        print("Ссылки открыты на обоих устройствах")
    except Exception as e:
        logging.error(f"Ошибка в main: {e}")

if __name__ == "__main__":
    main()