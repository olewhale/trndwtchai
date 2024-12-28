from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time, sys, os, json, re, random
from dotenv import load_dotenv
from datetime import datetime
from tqdm import tqdm

# Загружаем переменные из .env
load_dotenv()

lnks = [
    "https://www.instagram.com/p/DD7yXnDOTPc/",
    "https://www.instagram.com/p/DD7jEjmO1NX/",
    "https://www.instagram.com/p/DD7czL3O91I/",
    "https://www.instagram.com/p/DD7QL5rO0Zj/",
    "https://www.instagram.com/p/DD7GSTHMTDi/",
    "https://www.instagram.com/p/DD6zyslvPlZ/",
    "https://www.instagram.com/p/DD6zYLqOaPe/",
    "https://www.instagram.com/p/DD56_QbvOrt/",
    "https://www.instagram.com/p/DD5GbdwOW3m/",
    "https://www.instagram.com/p/DD4hGJdCgCu/",
    "https://www.instagram.com/p/DD4s-ZCTuI6/",
    "https://www.instagram.com/p/DD4hDsgOSpO/",
    "https://www.instagram.com/p/DD4P8bfCdxl/",
    "https://www.instagram.com/p/DD4P66giXdP/",
    "https://www.instagram.com/p/DD3VRwuM1b0/",
    "https://www.instagram.com/p/DD3PmFsTcEM/",
    "https://www.instagram.com/p/DD2ycF6OcFv/",
    "https://www.instagram.com/p/DD2wa5BB4qR/",
    "https://www.instagram.com/p/DD2f9a1yqJn/",
    "https://www.instagram.com/p/DD2XmR7OER5/",
    "https://www.instagram.com/p/DD2L3SxM0nq/",
    "https://www.instagram.com/p/DD19JOSMyvt/",
    "https://www.instagram.com/p/DD1wIM-PQj8/",
    "https://www.instagram.com/p/DD1rj1QO0iq/",
    "https://www.instagram.com/p/DD1oymGioTI/",
    "https://www.instagram.com/p/DD0mrdNzi5L/",
    "https://www.instagram.com/p/DDz52zgif6r/",
    "https://www.instagram.com/p/DDzot5dCywF/",
    "https://www.instagram.com/p/DDzXgkLid2S/",
    "https://www.instagram.com/p/DDzWXeMuo_c/",
    "https://www.instagram.com/p/DDzGYEainnR/",
    "https://www.instagram.com/p/DDyRNf3T4YK/",
    "https://www.instagram.com/p/DDx4lVrs0MW/",
    "https://www.instagram.com/p/DDxt3_GyKJv/",
    "https://www.instagram.com/p/DDxYX6TShzy/",
    "https://www.instagram.com/p/DDxRjrosnah/",
    "https://www.instagram.com/p/DDxD2qCCfW2/",
    "https://www.instagram.com/p/DDxAarwCRur/",
    "https://www.instagram.com/p/DDwyto_C2qO/",
    "https://www.instagram.com/p/DDwhXjXik9C/",
    "https://www.instagram.com/p/DDwXYJ_pL0Q/",
    "https://www.instagram.com/p/DDwI3ZBiNIp/",
    "https://www.instagram.com/p/DDvVS0oy-F7/",
    "https://www.instagram.com/p/DDurE5RxY4n/",
    "https://www.instagram.com/p/DDugaiYz5AP/",
    "https://www.instagram.com/p/DDuN6rWiRYr/",
    "https://www.instagram.com/p/DDuUxI4iWYr/",
    "https://www.instagram.com/p/DDuOw4zOizY/",
    "https://www.instagram.com/p/DDt8vypCW9c/",
    "https://www.instagram.com/p/DDuBOLVCwMb/",
    "https://www.instagram.com/p/DDt8xJ6CfRd/",
    "https://www.instagram.com/p/DDtv_PkOYrY/",
    "https://www.instagram.com/p/DDssoIXylyT/",
    "https://www.instagram.com/p/DDsjuWqBfz9/",
    "https://www.instagram.com/p/DDsgssAxpzH/",
    "https://www.instagram.com/p/DDsGOe9RxAZ/",
    "https://www.instagram.com/p/DDsFXe2pxM-/",
    "https://www.instagram.com/p/DDr7rnHO0ar/",
    "https://www.instagram.com/p/DDrxDLoTXI6/",
    "https://www.instagram.com/p/DDrrtjPi6gB/",
    "https://www.instagram.com/p/DDroehcu_oK/",
    "https://www.instagram.com/p/DDqKUnUM45j/",
    "https://www.instagram.com/p/DDqDqZgy2H6/",
    "https://www.instagram.com/p/DDpx9Y4SnBY/",
    "https://www.instagram.com/p/DDpRMRGN20P/",
    "https://www.instagram.com/p/DDpMR2xzTRt/",
    "https://www.instagram.com/p/DDpDYbIpsr8/",
    "https://www.instagram.com/p/DDn_Me2vi9q/",
    "https://www.instagram.com/p/DDnqWrVOsj6/",
    "https://www.instagram.com/p/DDnUwhXN_RS/",
    "https://www.instagram.com/p/DDmqeW1NwNN/",
    "https://www.instagram.com/p/DDmVoGrvWuu/",
    "https://www.instagram.com/p/DDmOwo5iV5f/",
    "https://www.instagram.com/p/DDlI1znz56l/",
    "https://www.instagram.com/p/DDkQJLmuPOv/",
    "https://www.instagram.com/p/DDkFab2TBO-/",
    "https://www.instagram.com/p/DDjruEeuVdN/",
    "https://www.instagram.com/p/DDjpdoGiVK7/",
    "https://www.instagram.com/p/DDiKtzcpL-a/",
    "https://www.instagram.com/p/DDiF_5YTNlA/",
    "https://www.instagram.com/p/DDh5XAARa66/",
    "https://www.instagram.com/p/DDhycqfx9ec/",
    "https://www.instagram.com/p/DDhpxUpzjhZ/",
    "https://www.instagram.com/p/DDhfJ6XPbB2/",
    "https://www.instagram.com/p/DDhFWnfT4cU/",
    "https://www.instagram.com/p/DDg0OQmCxKk/",
    "https://www.instagram.com/p/DDgRXlUxI1w/",
    "https://www.instagram.com/p/DDf90mls8dH/",
    "https://www.instagram.com/p/DDf4KfpPcnu/",
    "https://www.instagram.com/p/DDfpnMhtJyO/",
    "https://www.instagram.com/p/DDfDJtYvstL/",
    "https://www.instagram.com/p/DDe6zpBT3th/",
    "https://www.instagram.com/p/DDewwEvuz89/",
    "https://www.instagram.com/p/DDeZWmvO6RV/",
    "https://www.instagram.com/p/DDeIim9CsvK/",
    "https://www.instagram.com/p/DDdQ3zrt8gf/",
    "https://www.instagram.com/p/DDdPfOxSG3y/",
    "https://www.instagram.com/p/DDdBMmJtejR/",
    "https://www.instagram.com/p/DDcYSPszlXl/",
    "https://www.instagram.com/p/DDcIQlApRpu/",
    "https://www.instagram.com/p/DDbvBsSAuL9/",
    "https://www.instagram.com/p/DDbjvPRirir/",
    "https://www.instagram.com/p/DDa76hMz-sM/",
    "https://www.instagram.com/p/DDawWYzO68S/",
    "https://www.instagram.com/p/DDarbkqtfE2/",
    "https://www.instagram.com/p/DDarWocSM2j/",
    "https://www.instagram.com/p/DDaSr3Syo0B/",
    "https://www.instagram.com/p/DDZjKEOzoQX/",
    "https://www.instagram.com/p/DDZTzzTiu1L/",
    "https://www.instagram.com/p/DDY-ucciVE2/",
    "https://www.instagram.com/p/DDYn6iSRIzd/",
    "https://www.instagram.com/p/DDYSPkRTr0s/",
    "https://www.instagram.com/p/DDYJKUYNPQT/",
    "https://www.instagram.com/p/DDYIsqBsQcX/"
]


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
            print(f'------START-REEL-{i}----')
            url = item.get("url").replace('/p/', '/reel/')
            print(f'reels url for share: {url}')
            # Периодическая очистка кэша Instagram
            if i in (10, 40, 80, 100, 120, 140, 160, 180):
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
                'args': [ 'start', '-n', 'com.instagram.android/com.instagram.mainactivity.MainActivity']
        })
        time.sleep(3)
        for i, item in tqdm(enumerate(links, start=1), total=len(links), desc="Process get shares:", unit="reel", file=sys.stdout):
            
            url = item.replace('/p/', '/reel/')
            print(f'--START-REEL-{i}--- reels url for share: {url}')
            # Периодическая очистка кэша Instagram
            if i in (25, 50, 75, 100, 125, 150, 175, 200, 225, 250, 275, 300, 325, 350, 375, 400, 425, 450, 475, 500, 525, 550, 575, 600, 625, 650, 675, 700, 725, 750, 775, 800, 825, 850, 875, 900, 925, 950, 975, 1000):
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
                    json.dump(shares, result_file, ensure_ascii=False, indent=4)
                print(f"Saved intermediate reels data to {filename}")
                time.sleep(3)
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
                
                
                # Ожидание загрузки страницы с небольшой рандомизацией
                delay = random.uniform(5, 7)
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
                    shares.append(reshare_number)

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
    result_filename = f"vart_result_20241224.json"
    save_path_result = os.path.join('db', 'manual', result_filename)

    fetch_reels_shares_manual(lnks, driver, result_filename, save_path_result)
            


#execute_shares_scraping_manual()
