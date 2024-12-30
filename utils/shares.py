from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time, sys, os, json, re, random
from dotenv import load_dotenv
from datetime import datetime
from tqdm import tqdm
import xml.etree.ElementTree as ET
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


# Загружаем переменные из .env
load_dotenv()

lnks_string = '''https://www.instagram.com/p/DEHOUZ1NOVc/
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

# Разделяем строку на массив ссылок
lnks = lnks_string.strip().split('\n')


def login_to_instagram ():
    INSTAGRAM_USERNAME = os.getenv('INSTAGRAM_USERNAME')
    INSTAGRAM_PASSWORD = os.getenv('INSTAGRAM_PASSWORD')

    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.platform_version = "13"
    options.device_name = "Pixel_8_Pro"
    options.app_package = "com.instagram.android"
    options.app_activity = "com.instagram.mainactivity.MainActivity"
    options.no_reset = True
    options.new_command_timeout = 300

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
        time.sleep(5)
        

        for i, item in enumerate(reels_data):
            url = item.get("url").replace('/p/', '/reel/')
            print(f'------START-REEL-{i}----reels url for share: {url}')
            # Периодическая очистка кэша Instagram
            if i % 25 == 0:  # Проверяем, делится ли i на 25
                driver.execute_script('mobile: shell', {
                    'command': 'am',
                    'args': ['force-stop', 'com.instagram.android']
                })
                time.sleep(5)
                print('Cache was cleared')

                # Сохраняем промежуточные результаты
                #write a data
                os.makedirs(os.path.dirname(save_path_result), exist_ok=True)
                with open(save_path_result, "w", encoding="utf-8") as result_file:
                    json.dump(reels_data, result_file, ensure_ascii=False, indent=4)
                print(f"Saved intermediate reels data to {filename}")
                time.sleep(1)

            # Открываем Reels через deeplink
            try:
                driver.execute_script('mobile: shell', {
                    'command': 'am',
                    'args': ['start', '-a', 'android.intent.action.VIEW', '-d', url]
                })
                
                
                # Ожидание загрузки страницы с небольшой рандомизацией
                delay = random.uniform(4, 6)
                #print(f'delay:{delay}')
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

                    #<debug>
                    # filen = f"page_s_start_{i}.xml"
                    # with open(filen, "w", encoding="utf-8") as f:
                    #    f.write(page_source)
                    #</debug>

                except Exception as e:
                    print(f"Ошибка при поиске элемента решера: {e}")
                    item['shareCount'] = -1

            except Exception as e:
                print(f"Ошибка при открытии Reels: {e}")
                item['shareCount'] = -1

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

def fetch_reels_shares_manual(links, driver, result_filename, save_path_result):
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
    

def execute_shares_scraping(reels_data, result_filename, save_path_result):
    instagram_running, driver = login_to_instagram()

    if instagram_running:
        scraped_data = fetch_reels_shares(reels_data, driver, result_filename, save_path_result)
        return scraped_data

def execute_shares_scraping_manual():
    instagram_running, driver = login_to_instagram()
    result_filename = f"vart_result_20241224.json"
    save_path_result = os.path.join('db', 'manual', result_filename)

    fetch_reels_shares_manual(lnks, driver, result_filename, save_path_result)
            


#execute_shares_scraping_manual()
