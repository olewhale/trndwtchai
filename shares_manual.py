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

with open('db/31/akademika_apify_20250224_223650_copy2.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

print(f'Len: {len(data)}')
# Получаем все 'url' из элементов в data
lnks = [item['url'] for item in data if 'url' in item]  # Извлекаем 'url' из каждого элемента

# # Форматируем строки в нужный формат
# lnks_string = '\n'.join(urls)  # Объединяем URLs в одну строку, разделяя их новой строкой

# Пример вывода
print(lnks)


#for only shares
# lnks_string = '''https://www.instagram.com/p/DEN4xTgNwxB/
# https://www.instagram.com/p/DENmR-QxR9J/
# https://www.instagram.com/p/DENgZg8NWp0/
# https://www.instagram.com/p/DDr2tEPS2zb/
# https://www.instagram.com/p/DDrpiLXyg60/
# https://www.instagram.com/p/DDrVbznoxcq/
# https://www.instagram.com/p/DDq8IjeqYa6/
# https://www.instagram.com/p/DDqvmxZIOLB/'''

# # Разделяем строку на массив ссылок
# lnks = lnks_string.strip().split('\n')


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
        
        '''
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
                print(" - INSTAGRAM SHARES - Поле пароля не найдено, не можем ввести пароль")
            
            # Нажимаем кнопку Log in (если она есть)
            login_button_elements = driver.find_elements(AppiumBy.XPATH, login_button_xpath)
            if login_button_elements:
                login_button = login_button_elements[0]
                login_button.click()
                print(" - INSTAGRAM SHARES - Выполняем вход в аккаунт...")
                time.sleep(10)
            else:
                print(" - INSTAGRAM SHARES - Кнопка логина не найдена")
        else:
            print(" - INSTAGRAM SHARES - Поле username не найдено, пропускаем ввод логина/пароля")

        # После логина или пропуска ищем кнопку Save
        save_button_elements = driver.find_elements(AppiumBy.XPATH, save_button_xpath)
        if save_button_elements:
            time.sleep(10)
            save_button = save_button_elements[0]
            save_button.click()
            print(" - INSTAGRAM SHARES - Нажали на кнопку 'Save'")
            time.sleep(10)
        else:
            # Кнопка Save не найдена, переходим к следующему шагу
            print(" - INSTAGRAM SHARES - Кнопка 'Save' не найдена, следующий шаг...")
        
        allow_notify_elements = driver.find_elements(AppiumBy.XPATH, allow_notify_xpath)
        allow_not_notify_button_elements = driver.find_elements(AppiumBy.XPATH, allow_notify_button_xpath)
        if allow_notify_elements and allow_not_notify_button_elements:
            time.sleep(10)
            allow_not_button = allow_not_notify_button_elements[0]
            allow_not_button.click()
            print(" - INSTAGRAM SHARES - Нажали на кнопку DontAllow'")
            time.sleep(3)
        else:
            # Кнопка dontallow не найдена, переходим к следующему шагу
            print(" - INSTAGRAM SHARES - Кнопка dontallow не найдена, следующий шаг...")
        '''
        instagram_running = True
        print(" - INSTAGRAM SHARES - Instagram app is running")



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

def fetch_reels_shares(reels_data, driver, shares_filename, save_path_shares):
    
    sharesCountResults = {}
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
                            reshare_number = int(match.group(1))  # Извлекаем число
                            print(f"Reshare number: {reshare_number}")
                        else:
                            reshare_number = -1
                            error = "ISSUE: NO RESHARES"
                            print(f"\033[91m{error}\033[0m")

                        success = True
                        break  # Если успешно, выходим из цикла попыток

                    except Exception as e:
                        print(f"\033[91mОшибка при поиске элемента решера: {e}\033[0m")
                        reshare_number = -1

                except Exception as e:
                    print(f"\033[91mОшибка при открытии Reels: {e}\033[0m")
                    reshare_number = -1

                if not success and attempt == 0:  # Если первая попытка не удалась
                    print("\033[36mПервая попытка не удалась, повторяем...\033[0m")
                    time.sleep(3)  # Небольшая пауза перед повторной попыткой
            
            # Добавляем данные в словарь sharesCountData
            sharesCountResults[item['shortCode']] = reshare_number
            
            os.makedirs(os.path.dirname(save_path_shares), exist_ok=True)
            with open(save_path_shares, "w", encoding="utf-8") as result_file:
                json.dump(sharesCountResults, result_file, ensure_ascii=False, indent=4)

            # Логика рандомного выполнения свайпов
            if i % random_divisor == 0:
                swipe_time = perform_random_swipes(driver)
                print(f"Завершение свайпов, общее время ожидания: {swipe_time:.2f} секунд.")
                time.sleep(swipe_time)  # Ждём завершения свайпов

                # Обновляем делитель после выполнения свайпов
                random_divisor = random.randint(10, 20)

    except Exception as e:
        print(f"Общая ошибка в процессе: {e}")
        return sharesCountResults

    finally:
        # Гарантированно закрываем драйвер
        try:
            driver.quit()
            return sharesCountResults
        except:
            pass

def fetch_reels_shares_manual_INPROGRESS(links, driver, shares_filename, save_path_shares):
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
                    reshare_number = "0"
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
                    #     reshare_number = 0
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
                    shares.append(0)

            except Exception as e:
                print(f"Ошибка при открытии Reels: {e}")
                shares.append(0)
                            # Сохраняем промежуточные результаты
            #write a data after each reels
            os.makedirs(os.path.dirname(save_path_shares), exist_ok=True)
            with open(save_path_shares, "w", encoding="utf-8") as result_file:
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

def fetch_reels_shares_manual(links, driver, shares_filename, save_path_shares):
    shares =[]
    try:

        # Убедись, что Appium сервер запущен по указанному адресу
        driver.execute_script('mobile: shell', {
            'command': 'am',
            'args': ['kill-all']
        })
        driver.press_keycode(3)  # Кнопка Home для выхода на рабочий экран
        logging.info("kill all apps")

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
                            reshare_number = 0
                            print("Reshare number not found")

                        #Сохраняем данные в массив
                        shares.append(reshare_number)
                        success = True
                        break  # Если успешно, выходим из цикла попыток

                    except Exception as e:
                        print(f"Ошибка при поиске элемента решера: {e}")
                        shares.append(0)

                except Exception as e:
                    print(f"Ошибка при открытии Reels: {e}")
                    shares.append(0)

                if not success and attempt == 0:  # Если первая попытка не удалась
                    print("Первая попытка не удалась, повторяем...")
                    time.sleep(3)  # Небольшая пауза перед повторной попыткой

            # Сохраняем промежуточные результаты
            os.makedirs(os.path.dirname(save_path_shares), exist_ok=True)
            with open(save_path_shares, "w", encoding="utf-8") as shares_file:
                json.dump(shares, shares_file, ensure_ascii=False, indent=4)

            # Логика рандомного выполнения свайпов
            if i % random_divisor == 0:
                swipe_time = perform_random_swipes(driver)
                print(f"Завершение свайпов, общее время ожидания: {swipe_time:.2f} секунд.")
                time.sleep(swipe_time)  # Ждём завершения свайпов

                # Обновляем делитель после выполнения свайпов
                random_divisor = random.randint(3, 5)


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

def execute_shares_scraping(reels_data, result_filename, save_path_share_results):
    instagram_running, driver = login_to_instagram()

    if instagram_running:
        scraped_data = fetch_reels_shares(reels_data, driver, result_filename, save_path_share_results)
        return scraped_data




def execute_shares_scraping_manual():
    instagram_running, driver = login_to_instagram()
    logging.info("Logged to instagram.")
    result_filename = f"kumarsolo_result_20241231.json"
    save_path_result = os.path.join('db', 'manual', result_filename)
    
    logging.info("Run fetch reels")
    fetch_reels_shares_manual(lnks, driver, result_filename, save_path_result)
            


execute_shares_scraping_manual()
