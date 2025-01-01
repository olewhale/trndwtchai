from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time, sys, os, json, re, random
from dotenv import load_dotenv
from datetime import datetime
from tqdm import tqdm
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import fromstring
import logging

# Настройка логирования с UTF-8
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),  # Логи в консоль
        logging.FileHandler("process_logs.log", mode="w", encoding="utf-8")  # Логи в файл с UTF-8
    ]
)

# Загружаем переменные из .env
load_dotenv()

lnks_string2 = '''https://www.instagram.com/p/DEHOUZ1NOVc/
https://www.instagram.com/p/DEHKcsmtKp8/
https://www.instagram.com/p/DEHJynktBE1/
https://www.instagram.com/p/DEHIL94tIku/
https://www.instagram.com/p/DEHHgsNoz6t/
https://www.instagram.com/p/DEG4_B8TMhJ/
https://www.instagram.com/p/DEGJvoPK190/
https://www.instagram.com/p/DEGDFEyMH6f/
https://www.instagram.com/p/DEF3pLBsU6e/
https://www.instagram.com/p/DEF102tMl3-/
https://www.instagram.com/p/DEFuaIfsSoW/
https://www.instagram.com/p/DEFswiqCzhL/
https://www.instagram.com/p/DEFrz5-u6Fz/
https://www.instagram.com/p/DEFrHbnMU1M/
https://www.instagram.com/p/DEFpzZ8uYeO/
https://www.instagram.com/p/DEFmlxoI-_o/
https://www.instagram.com/p/DEFnRMOM8tB/
https://www.instagram.com/p/DEFjtanqsQg/
https://www.instagram.com/p/DEFgixtIJ32/
https://www.instagram.com/p/DEFfKZNN6Tb/
https://www.instagram.com/p/DEFcWIAtkLb/
https://www.instagram.com/p/DEFYh2ntVar/
https://www.instagram.com/p/DEFXWkeIko0/
https://www.instagram.com/p/DEFJ795spc0/
https://www.instagram.com/p/DEFFAuAoSJI/
https://www.instagram.com/p/DEE9Re1syDF/'''

lnks_string = '''https://www.instagram.com/p/DEN4xTgNwxB/
https://www.instagram.com/p/DENmR-QxR9J/
https://www.instagram.com/p/DENgZg8NWp0/
https://www.instagram.com/p/DENaE-kvETJ/
https://www.instagram.com/p/DEPDqGkzTT4/
https://www.instagram.com/p/DERvOZgzUgx/
https://www.instagram.com/p/DER2J_ZzmBP/
https://www.instagram.com/p/DEMgRhBiUGP/
https://www.instagram.com/p/DEL9xUnvip5/
https://www.instagram.com/p/DEK3N4AIxoW/
https://www.instagram.com/p/DEKoQCkMHa3/
https://www.instagram.com/p/DEKcjXZsx5C/
https://www.instagram.com/p/DEKYZI8TK1r/
https://www.instagram.com/p/DEKVhU4zVCU/
https://www.instagram.com/p/DESKtpZzxsZ/
https://www.instagram.com/p/DEJ6Df_z6yO/
https://www.instagram.com/p/DEJ4XnytsrM/
https://www.instagram.com/p/DEJWlividJG/
https://www.instagram.com/p/DEJWHKPiXnl/
https://www.instagram.com/p/DEIXloMoqbt/
https://www.instagram.com/p/DEH-b-EzTt-/
https://www.instagram.com/p/DEH3lDtzepB/
https://www.instagram.com/p/DEHmxDiOjO1/
https://www.instagram.com/p/DEKHtfezEI9/
https://www.instagram.com/p/DEHwqDFz5nW/
https://www.instagram.com/p/DEHQ9WnSzr-/
https://www.instagram.com/p/DEHOUZ1NOVc/
https://www.instagram.com/p/DEGOQOBtus0/
https://www.instagram.com/p/DEF7ZstvRE8/
https://www.instagram.com/p/DEFuqj7Cu9L/
https://www.instagram.com/p/DEFsHYYtu0g/
https://www.instagram.com/p/DEFnZfxRQv4/
https://www.instagram.com/p/DEFd3b8Mh0V/
https://www.instagram.com/p/DEFXDzxTRQC/
https://www.instagram.com/p/DEHp2Fez-Ou/
https://www.instagram.com/p/DEKjPk5z-Ci/
https://www.instagram.com/p/DEFL2y7ThbN/
https://www.instagram.com/p/DEKcVhOz2EM/
https://www.instagram.com/p/DEE22iqNfXK/
https://www.instagram.com/p/DEE3TJBT4rO/
https://www.instagram.com/p/DEEds-bIsW3/
https://www.instagram.com/p/DEDp_FxTsDA/
https://www.instagram.com/p/DEDd7XmN_0P/
https://www.instagram.com/p/DEDaJwNs6HE/
https://www.instagram.com/p/DEDQpjMR0ir/
https://www.instagram.com/p/DEC9YtByrnI/
https://www.instagram.com/p/DEH3mBGTVlN/
https://www.instagram.com/p/DECs4GOM5QV/
https://www.instagram.com/p/DEFFCLQzf3P/
https://www.instagram.com/p/DEHcDOiT7M3/
https://www.instagram.com/p/DEE-Ocqzoh5/
https://www.instagram.com/p/DECK-syvz-l/
https://www.instagram.com/p/DECIGXVitOa/
https://www.instagram.com/p/DECHhAVSA9E/
https://www.instagram.com/p/DEBpl86vdrr/
https://www.instagram.com/p/DEAuQoAuG0t/
https://www.instagram.com/p/DEAmulGtxmo/
https://www.instagram.com/p/DEAUNAgz5gc/
https://www.instagram.com/p/DECLrInTQz4/
https://www.instagram.com/p/DEAHp7ls_9q/
https://www.instagram.com/p/DEADEeONril/
https://www.instagram.com/p/DEACI4Vi5oL/
https://www.instagram.com/p/DD_0MyWCL--/
https://www.instagram.com/p/DD_lhL7tlcD/
https://www.instagram.com/p/DD_izlMonyU/
https://www.instagram.com/p/DD-AhPXt5fu/
https://www.instagram.com/p/DD9yaOExQm2/
https://www.instagram.com/p/DD9xn3zy9oV/
https://www.instagram.com/p/DD9sAw-zNSI/
https://www.instagram.com/p/DD9Uhyxta8w/
https://www.instagram.com/p/DD9TAZ-uZay/
https://www.instagram.com/p/DD8x2McIT0Y/
https://www.instagram.com/p/DD8Gqfmz9iF/
https://www.instagram.com/p/DD7xO-XCi7t/
https://www.instagram.com/p/DD7w0SdPqCO/
https://www.instagram.com/p/DD7l_91RyF1/
https://www.instagram.com/p/DD7jaO9utqN/
https://www.instagram.com/p/DD7ekF6tJqY/
https://www.instagram.com/p/DD7cc4Ru9X6/
https://www.instagram.com/p/DD7VKT_IMm0/
https://www.instagram.com/p/DD7POYbNrzj/
https://www.instagram.com/p/DD7G-sPz3Su/
https://www.instagram.com/p/DD68ml7Mp85/
https://www.instagram.com/p/DD6L9CQoo5w/
https://www.instagram.com/p/DD596KqoW8d/
https://www.instagram.com/p/DD4225CNxuf/
https://www.instagram.com/p/DD4teZLSQRn/
https://www.instagram.com/p/DD4ksg9Icqc/
https://www.instagram.com/p/DD4gjrrz5jl/
https://www.instagram.com/p/DD4HvnRTsc9/
https://www.instagram.com/p/DD4CtQWukB1/
https://www.instagram.com/p/DD3_xt-N_wS/
https://www.instagram.com/p/DD3zikrShkm/
https://www.instagram.com/p/DD3xRF_t9EK/
https://www.instagram.com/p/DD3uGhDyUQ1/
https://www.instagram.com/p/DD3hy9YSQXE/
https://www.instagram.com/p/DD2N6hrNvJj/
https://www.instagram.com/p/DD2DCj8T68j/
https://www.instagram.com/p/DD198kkTUXM/
https://www.instagram.com/p/DD12aD_C1-C/
https://www.instagram.com/p/DD1r1N1NtLK/
https://www.instagram.com/p/DD1V4m6yV2I/
https://www.instagram.com/p/DD07JFXpDtc/
https://www.instagram.com/p/DD0cMqPCbuh/
https://www.instagram.com/p/DD0X8FCyKdx/
https://www.instagram.com/p/DDzzcEayWZ6/
https://www.instagram.com/p/DDziIdaR-uB/
https://www.instagram.com/p/DDztu4Tx7xY/
https://www.instagram.com/p/DDzrm_KtwUA/
https://www.instagram.com/p/DDzrRIgPlgY/
https://www.instagram.com/p/DDzAD2MNgmt/
https://www.instagram.com/p/DDyyPQrCCxO/
https://www.instagram.com/p/DDyt5OovKsb/
https://www.instagram.com/p/DDylHN8t7M8/
https://www.instagram.com/p/DDyKHquirjC/
https://www.instagram.com/p/DDyJ6uJxNWF/
https://www.instagram.com/p/DDxnBi3CHiW/
https://www.instagram.com/p/DDxma20s_AA/
https://www.instagram.com/p/DDxhmOUiwzz/
https://www.instagram.com/p/DDxYXJ3PN23/
https://www.instagram.com/p/DDxJzxjtsAq/
https://www.instagram.com/p/DDw_UWroBMo/
https://www.instagram.com/p/DDw1-t-TsJO/
https://www.instagram.com/p/DDw02JeRVZB/
https://www.instagram.com/p/DDwu8F4NBu4/
https://www.instagram.com/p/DDwVpXKvFY3/
https://www.instagram.com/p/DDv8O_3SHMJ/
https://www.instagram.com/p/DDvLzFyAoMe/
https://www.instagram.com/p/DDunoyavU02/
https://www.instagram.com/p/DDugHJny5Tg/
https://www.instagram.com/p/DDuTPkezHEY/
https://www.instagram.com/p/DDtzVI0SlUO/
https://www.instagram.com/p/DDs9fA7NWgK/
https://www.instagram.com/p/DDs63FDPyo0/
https://www.instagram.com/p/DDsOmwcyk08/
https://www.instagram.com/p/DDp7yFMpGJ0/
https://www.instagram.com/p/DDr6DgZR77q/
https://www.instagram.com/p/DDr2tEPS2zb/
https://www.instagram.com/p/DDrpiLXyg60/
https://www.instagram.com/p/DDrVbznoxcq/
https://www.instagram.com/p/DDq8IjeqYa6/
https://www.instagram.com/p/DDqvmxZIOLB/'''

# Разделяем строку на массив ссылок
lnks = lnks_string.strip().split('\n')


def login_to_instagram ():
    INSTAGRAM_USERNAME = os.getenv('INSTAGRAM_USERNAME')
    INSTAGRAM_PASSWORD = os.getenv('INSTAGRAM_PASSWORD')

    # Настройка опций для сессии
    options = UiAutomator2Options()
    options.platform_name = 'Android'
    options.device_name = 'emulator-5554'
    options.app_package = 'com.instagram.android'
    options.app_activity = '.activity.MainTabActivity'
    options.no_reset = True
    options.uiautomator2_server_launch_timeout = 60000

    driver = webdriver.Remote("http://localhost:4723", options=options)


    try:

        username_xpath = '//android.widget.FrameLayout[@resource-id="com.instagram.android:id/layout_container_main"]/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.widget.FrameLayout[1]/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[1]/android.view.ViewGroup/android.view.ViewGroup/android.widget.EditText'
        password_xpath = '//android.widget.FrameLayout[@resource-id="com.instagram.android:id/layout_container_main"]/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.widget.FrameLayout[1]/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[2]/android.view.ViewGroup/android.widget.EditText'
        login_button_xpath = '//android.widget.Button[@content-desc="Log in"]/android.view.ViewGroup'
        save_button_xpath = '//android.widget.Button[@content-desc="Save"]/android.view.ViewGroup'
        allow_notify_xpath = '//android.widget.TextView[@resource-id="com.android.permissioncontroller:id/permission_message"]'
        allow_notify_button_xpath = '//android.widget.Button[@resource-id="com.android.permissioncontroller:id/permission_deny_button"]'

        # Set the media volume to 0
        driver.execute_script('mobile: shell', {
            'command': 'cmd',
            'args': ['media_session', 'volume', '--set', '0']
        })
        time.sleep(1)
        
        
        # Проверяем наличие поля логина
        username_elements = driver.find_elements(AppiumBy.XPATH, username_xpath)
        if username_elements:
            # Поле логина найдено, значит вводим логин/пароль и логинимся
            username_field = username_elements[0]
            username_field.send_keys(INSTAGRAM_USERNAME)
            time.sleep(1)

            # Аналогично для пароля
            password_elements = driver.find_elements(AppiumBy.XPATH, password_xpath)
            if password_elements:
                password_field = password_elements[0]
                password_field.send_keys(INSTAGRAM_PASSWORD)
                time.sleep(1)
            else:
                print("Поле пароля не найдено, не можем ввести пароль")
            
            # Нажимаем кнопку Log in (если она есть)
            login_button_elements = driver.find_elements(AppiumBy.XPATH, login_button_xpath)
            if login_button_elements:
                login_button = login_button_elements[0]
                login_button.click()
                print("Выполняем вход в аккаунт...")
                time.sleep(10)
            else:
                print("Кнопка логина не найдена")
        else:
            print("Поле username не найдено, пропускаем ввод логина/пароля")

        # После логина или пропуска ищем кнопку Save
        save_button_elements = driver.find_elements(AppiumBy.XPATH, save_button_xpath)
        if save_button_elements:
            time.sleep(10)
            save_button = save_button_elements[0]
            save_button.click()
            print("Нажали на кнопку 'Save'")
            time.sleep(10)
        else:
            # Кнопка Save не найдена, переходим к следующему шагу
            print("Кнопка 'Save' не найдена, следующий шаг...")
        
        allow_notify_elements = driver.find_elements(AppiumBy.XPATH, allow_notify_xpath)
        allow_not_notify_button_elements = driver.find_elements(AppiumBy.XPATH, allow_notify_button_xpath)
        if allow_notify_elements and allow_not_notify_button_elements:
            time.sleep(10)
            allow_not_button = allow_not_notify_button_elements[0]
            allow_not_button.click()
            print("Нажали на кнопку DontAllow'")
            time.sleep(3)
        else:
            # Кнопка dontallow не найдена, переходим к следующему шагу
            print("Кнопка dontallow не найдена, следующий шаг...")
        
        instagram_running = True
        print("Instagram app is running")



    except Exception as e:
        print(f"Ошибка: {e}")
        instagram_running = False
    finally:
        #driver.quit()
        #print('----driver quit')
        return instagram_running, driver

def swipe_up(driver, duration=500):
    """
    Выполняет свайп вверх на мобильном устройстве с небольшим рандомным смещением стартовой точки.

    :param driver: Объект WebDriver Appium
    :param duration: Длительность свайпа в миллисекундах
    """
    # Получаем размеры экрана устройства
    window_size = driver.get_window_size()
    
    # Добавляем небольшую рандомизацию к стартовой точке
    start_x = window_size['width'] // 2 + random.randint(-10, 10)  # Смещение ±10 пикселей по ширине
    start_y = int(window_size['height'] * 0.8) + random.randint(-10, 10)  # Смещение ±10 пикселей по высоте
    end_y = int(window_size['height'] * 0.2) + random.randint(-10, 10)    # Смещение ±10 пикселей по высоте

    # Создаем объект PointerInput для сенсорных действий
    touch_input = PointerInput("touch", "finger")

    # Создаем последовательность действий для свайпа
    actions = ActionBuilder(driver, mouse=touch_input)
    actions.pointer_action.move_to_location(start_x, start_y)
    actions.pointer_action.pointer_down()
    actions.pointer_action.pause(duration / 1000)  # Пауза в секундах
    actions.pointer_action.move_to_location(start_x, end_y)
    actions.pointer_action.pointer_up()
    actions.perform()

    print(f"Свайп вверх выполнен: ({start_x}, {start_y}) -> ({start_x}, {end_y}).")

def perform_random_swipes(driver):
    """
    Выполняет от 1 до 3 рандомных свайпов вверх с интервалом от 0.5 до 1 секунд.
    Возвращает общее время выполнения свайпов.
    """
    swipe_count = random.randint(1, 2)  # Случайное количество свайпов
    print(f"Выполняется {swipe_count} свайпов вверх.")
    
    total_time = 0  # Общее время выполнения свайпов

    for _ in range(swipe_count):
        duration = random.randint(300, 500)  # Длительность свайпа 400–700 мс
        swipe_up(driver, duration=duration)
        interval = random.uniform(0.5, 1)  # Интервал между свайпами
        total_time += duration / 1000 + interval  # Обновляем общее время
        time.sleep(interval)

    return total_time

def get_reshare_number_from_xml(driver):
    """
    Извлекает число репостов (Reshare number) из XML-источника.

    :param driver: Объект WebDriver Appium
    :return: Число репостов или None, если не найдено
    """
    try:
        # Получаем XML-источник
        page_source = driver.page_source

        # Парсим XML
        root = ET.fromstring(page_source)

        # Ищем элемент с нужным атрибутом "content-desc"
        for element in root.iter():
            content_desc = element.attrib.get("content-desc", "")
            if "Reshare number is" in content_desc:
                # Извлекаем число из строки
                match = re.search(r"Reshare number is(\d+)", content_desc)
                if match:
                    return int(match.group(1))  # Возвращаем число как int

        print("Reshare number not found.")
        return None
    except Exception as e:
        print(f"Ошибка при парсинге XML: {e}")
        return None

def fetch_reels_shares(reels_data, driver, result_filename, save_path_result):

    try:
        # Убедись, что Appium сервер запущен по указанному адресу
        driver.execute_script('mobile: shell', {
            'command': 'am',
            'args': ['kill-all']
        })
        driver.press_keycode(3)  # Кнопка Home для выхода на рабочий экран
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"sharesCount_{timestamp}.json"
        time.sleep(4)
        random_divisor = random.randint(10, 20)  # Устанавливаем начальное значение делителя
        

        for i, item in tqdm(enumerate(reels_data, start=1), total=len(reels_data), desc="Process get shares:", unit="reel", file=sys.stdout):
            url = item.get("url").replace('/p/', '/reel/')
            print(f'------START-REEL-{i}----reels url for share: {url}')
            # Периодическая очистка кэша Instagram
            if i % 50 == 0:  # Проверяем, делится ли i на 25
                driver.execute_script('mobile: shell', {
                    'command': 'am',
                    'args': ['force-stop', 'com.instagram.android']
                })
                time.sleep(5)
                print('Cache was cleared')

                driver.execute_script('mobile: shell', {
                        'command': 'am',
                        'args': [ 'start', '-n', 'com.instagram.android/com.instagram.mainactivity.MainActivity']
                })
                time.sleep(3)


            success = False  # Флаг успешного выполнения
            for attempt in range(2):  # Две попытки для каждого item
                try:
                    # Открытие ссылки в Instagram
                    driver.execute_script('mobile: deepLink', {
                        'url': url,
                        'package': 'com.instagram.android'
                    })
                    
                    # Ожидание загрузки страницы с небольшой рандомизацией
                    delay = random.uniform(3, 4)
                    time.sleep(delay)
                    # Попытка найти элемент решера с таймаутом
                    try:
                        
                        page_source = driver.page_source
                        # Используем регулярное выражение для поиска строки с числом 
                        match = re.search(r'content-desc="Reshare number is(\d+)"', page_source)

                        if match:
                            reshare_number = match.group(1)  # Извлекаем число
                            print(f"Reshare number: {reshare_number}")
                        else:
                            reshare_number = "-1"
                            print("Reshare number not found")

                        #Сохраняем данные в массив
                        item['shareCount'] = reshare_number
                        success = True
                        break  # Если успешно, выходим из цикла попыток

                    except Exception as e:
                        print(f"Ошибка при поиске элемента решера: {e}")
                        item['shareCount'] = -1

                except Exception as e:
                    print(f"Ошибка при открытии Reels: {e}")
                    item['shareCount'] = -1

                if not success and attempt == 0:  # Если первая попытка не удалась
                    print("Первая попытка не удалась, повторяем...")
                    time.sleep(3)  # Небольшая пауза перед повторной попыткой
            
            #write a data after each reels
            os.makedirs(os.path.dirname(save_path_result), exist_ok=True)
            with open(save_path_result, "w", encoding="utf-8") as result_file:
                json.dump(reels_data, result_file, ensure_ascii=False, indent=4)

            # Логика рандомного выполнения свайпов
            if i % random_divisor == 0:
                swipe_time = perform_random_swipes(driver)
                print(f"Завершение свайпов, общее время ожидания: {swipe_time:.2f} секунд.")
                time.sleep(swipe_time)  # Ждём завершения свайпов

                # Обновляем делитель после выполнения свайпов
                random_divisor = random.randint(10, 20)

        #write a data
        os.makedirs(os.path.dirname(save_path_result), exist_ok=True)
        with open(save_path_result, "w", encoding="utf-8") as result_file:
            json.dump(reels_data, result_file, ensure_ascii=False, indent=4)
        print(f"Saved final reels data to {filename}")

    except Exception as e:
        print(f"Общая ошибка в процессе: {e}")
        return reels_data

    finally:
        # Гарантированно закрываем драйвер
        try:
            driver.quit()
            return reels_data
        except:
            pass

def fetch_reels_shares_manual_INPROGRESS(links, driver, result_filename, save_path_result):
    shares =[]
    try:
        # Убедись, что Appium сервер запущен по указанному адресу
        driver.execute_script('mobile: shell', {
            'command': 'am',
            'args': ['kill-all']
        })
        driver.press_keycode(3)  # Кнопка Home для выхода на рабочий экран
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"sharesCount_manual_{timestamp}.json"

        time.sleep(3)
        driver.execute_script('mobile: shell', {
            'command': 'am',
            'args': [
                'start',
                '-n', 'com.instagram.android/com.instagram.mainactivity.MainActivity'
            ]
        })
        time.sleep(3)
        for i, item in tqdm(enumerate(links, start=1), total=len(links), desc="Process get shares:", unit="reel", file=sys.stdout):
            
            url = item.replace('/p/', '/reel/')
            print(f'--START-REEL-{i}--- reels url for share: {url}')
            # Периодическая очистка кэша Instagram
            if i % 50 == 0:  # Проверяем, делится ли i на 25
                driver.execute_script('mobile: shell', {
                    'command': 'am',
                    'args': ['force-stop', 'com.instagram.android']
                })
                time.sleep(5)
                print('Cache was cleared')

                driver.execute_script('mobile: shell', {
                        'command': 'am',
                        'args': [ 'start', '-n', 'com.instagram.android/com.instagram.mainactivity.MainActivity']
                })
                time.sleep(3)

            # Открываем Reels через deeplink
            try:
                driver.execute_script('mobile: shell', {
                    'command': 'am',
                    'args': ['start', '-a', 'android.intent.action.VIEW', '-d', url]
                })
                
                
                # старая версия ожидания - Ожидание загрузки страницы с небольшой рандомизацией
                delay = random.uniform(4, 6)
                time.sleep(delay)
                #page_source = driver.page_source

                

                # По совету чатгпт
                # Ожидание загрузки страницы вместо time.sleep
                # try:
                #     WebDriverWait(driver, 15).until(
                #         lambda d: 'Reshare number is' in d.page_source
                #     )
                #     page_source = driver.page_source
                # except Exception as e:
                #     print(f"Ошибка при ожидании загрузки: {e}")
                #     page_source = ""

                # Попытка найти элемент решера с таймаутом
                page_source = ""
                try:
                    logging.info("Получение исходного XML страницы...")
                    WebDriverWait(driver, 15).until(
                        lambda d: 'Reshare number is' in d.page_source
                    )
                    page_source = driver.page_source
                    logging.info("XML страницы успешно получен.")
                except Exception as e:
                    print(f"Ошибка при ожидании загрузки страницы: {e}")

                try:
                    # Парсим XML с помощью ElementTree
                    root = ET.fromstring(page_source)
                    logging.info("XML страницы успешно распарсен.")

                    # XPath-like поиск родительского элемента
                    parent_xpath = ".//androidx.recyclerview.widget.RecyclerView/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup[2]/android.view.ViewGroup[1]/android.view.ViewGroup[2]"
                    parent_element = root.find(parent_xpath)

                    if parent_element is None:
                        logging.error("Родительский элемент не найден.")
                        raise ValueError("Родительский элемент не найден.")

                    logging.info("Родительский элемент успешно найден.")

                    # Поиск дочерних элементов
                    logging.info("Получение дочерних элементов родительского элемента...")
                    child_elements = list(parent_element)

                    logging.info(f"Найдено {len(child_elements)} дочерних элементов.")

                    # Перебор дочерних элементов для поиска "Reshare number is"
                    reshare_number = "-1"
                    for index, child in enumerate(child_elements):
                        content_desc = child.attrib.get("content-desc")  # Получаем атрибут content-desc
                        logging.info(f"Дочерний элемент {index + 1}/{len(child_elements)}: content-desc = {content_desc}")
                        if content_desc and "Reshare number is" in content_desc:
                            # Извлекаем число из content-desc
                            match = re.search(r'Reshare number is(\d+)', content_desc)
                            if match:
                                reshare_number = match.group(1)
                                logging.info(f"Найдено число репостов: {reshare_number}")
                                break  # Число найдено, выходим из цикла

                    logging.info(f"Количество репостов: {reshare_number}")
                    # element = WebDriverWait(driver, 15).until(
                    #     EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "Reshare number is"))
                    # )
                    # element = driver.find_element(
                    #     AppiumBy.ANDROID_UIAUTOMATOR,
                    #     'new UiSelector().descriptionContains("Reshare number is")'
                    # )
                    # # Получение значения атрибута content-desc
                    # content_desc = element.get_attribute("content-desc")
                    # # Извлечь число с помощью регулярного выражения
                    # match = re.search(r"Reshare number is (\d+)", content_desc)
                    
                    # #match = re.search(r'content-desc="Reshare number is(\d+)"', page_source)

                    # if match:
                    #     reshare_number = match.group(1)  # Извлекаем число
                    #     print(f"Reshare number: {reshare_number}")
                    # else:
                    #     reshare_number = "-1"
                    #     print("Reshare number not found")

                    # #Сохраняем данные в массив
                    # shares.append(reshare_number)

                    #<debug>
                    # filen = f"page_s_start_{i}.xml"
                    # with open(filen, "w", encoding="utf-8") as f:
                    #    f.write(page_source)
                    #</debug>

                except Exception as e:
                    print(f"Ошибка при поиске элемента решера: {e}")
                    shares.append("-1")

            except Exception as e:
                print(f"Ошибка при открытии Reels: {e}")
                shares.append("-1")
                            # Сохраняем промежуточные результаты
            #write a data after each reels
            os.makedirs(os.path.dirname(save_path_result), exist_ok=True)
            with open(save_path_result, "w", encoding="utf-8") as result_file:
                json.dump(shares, result_file, ensure_ascii=False, indent=4)

        #write a data
        #os.makedirs(os.path.dirname(save_path_result), exist_ok=True)
        #with open(save_path_result, "w", encoding="utf-8") as result_file:
        #    json.dump(shares, result_file, ensure_ascii=False, indent=4)
        print(f"Saved final reels data to {filename}")

    except Exception as e:
        print(f"Общая ошибка в процессе: {e}")
        return None

    finally:
        # Гарантированно закрываем драйвер
        try:
            driver.quit()
            return None
        except:
            pass

def fetch_reels_shares_manual(links, driver, result_filename, save_path_result):
    shares =[]
    try:

        # Убедись, что Appium сервер запущен по указанному адресу
        driver.execute_script('mobile: shell', {
            'command': 'am',
            'args': ['kill-all']
        })
        driver.press_keycode(3)  # Кнопка Home для выхода на рабочий экран
        logging.info("kill all apps")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"sharesCount_manual_{timestamp}.json"

        time.sleep(5)
        random_divisor = random.randint(3, 5)  # Устанавливаем начальное значение делителя
    

        for i, item in tqdm(enumerate(links, start=1), total=len(links), desc="Process get shares:", unit="reel", file=sys.stdout):
            url = item.replace('/p/', '/reel/')
            print(f'--START-REEL-{i}--- reels url for share: {url}')
            # Периодическая очистка кэша Instagram
            if i % 50 == 0:  # Проверяем, делится ли i на 25
                driver.execute_script('mobile: shell', {
                    'command': 'am',
                    'args': ['force-stop', 'com.instagram.android']
                })
                logging.info("Force-stop inst")
                time.sleep(3)
                print('Cache was cleared')

                driver.execute_script('mobile: shell', {
                        'command': 'am',
                        'args': [ 'start', '-n', 'com.instagram.android/com.instagram.mainactivity.MainActivity']
                })
                logging.info("start instagram again")
                time.sleep(3)
            
            success = False  # Флаг успешного выполнения
            for attempt in range(2):  # Две попытки для каждого item
                try:
                    # Открытие ссылки в Instagram
                    driver.execute_script('mobile: deepLink', {
                        'url': url,
                        'package': 'com.instagram.android'
                    })
                    logging.info("Open Link")
                    # Ожидание загрузки страницы с небольшой рандомизацией
                    delay = random.uniform(2, 4)
                    time.sleep(delay)

                    try:
                        page_source = driver.page_source
                        # Используем регулярное выражение для поиска строки с числом
                        logging.info("Get page source")
                        match = re.search(r'content-desc="Reshare number is(\d+)"', page_source)
                        logging.info("Found the shares")
                        if match:
                            reshare_number = match.group(1)  # Извлекаем число
                            print(f"Reshare number: {reshare_number}")
                        else:
                            reshare_number = "-1"
                            print("Reshare number not found")

                        #Сохраняем данные в массив
                        shares.append(reshare_number)
                        success = True
                        break  # Если успешно, выходим из цикла попыток

                    except Exception as e:
                        print(f"Ошибка при поиске элемента решера: {e}")
                        shares.append("-1")

                except Exception as e:
                    print(f"Ошибка при открытии Reels: {e}")
                    shares.append("-1")

                if not success and attempt == 0:  # Если первая попытка не удалась
                    print("Первая попытка не удалась, повторяем...")
                    time.sleep(3)  # Небольшая пауза перед повторной попыткой

            # Сохраняем промежуточные результаты
            os.makedirs(os.path.dirname(save_path_result), exist_ok=True)
            with open(save_path_result, "w", encoding="utf-8") as result_file:
                json.dump(shares, result_file, ensure_ascii=False, indent=4)

            # Логика рандомного выполнения свайпов
            if i % random_divisor == 0:
                swipe_time = perform_random_swipes(driver)
                print(f"Завершение свайпов, общее время ожидания: {swipe_time:.2f} секунд.")
                time.sleep(swipe_time)  # Ждём завершения свайпов

                # Обновляем делитель после выполнения свайпов
                random_divisor = random.randint(3, 5)


        #write a data
        os.makedirs(os.path.dirname(save_path_result), exist_ok=True)
        with open(save_path_result, "w", encoding="utf-8") as result_file:
           json.dump(shares, result_file, ensure_ascii=False, indent=4)
        print(f"Saved final reels data to {filename}")

    except Exception as e:
        print(f"Общая ошибка в процессе: {e}")
        return None

    finally:
        # Гарантированно закрываем драйвер
        try:
            driver.quit()
            return None
        except:
            pass

def execute_shares_scraping(reels_data, result_filename, save_path_result):
    instagram_running, driver = login_to_instagram()

    if instagram_running:
        scraped_data = fetch_reels_shares(reels_data, driver, result_filename, save_path_result)
        return scraped_data

def execute_shares_scraping_manual():
    instagram_running, driver = login_to_instagram()
    logging.info("Logged to instagram.")
    result_filename = f"kumarsolo_result_20241231.json"
    save_path_result = os.path.join('db', 'manual', result_filename)
    
    logging.info("Run fetch reels")
    fetch_reels_shares_manual(lnks, driver, result_filename, save_path_result)
            


#execute_shares_scraping_manual()
