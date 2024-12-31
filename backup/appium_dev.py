from appium import webdriver
from appium.options.android import UiAutomator2Options
import time

# Настройка опций для сессии
options = UiAutomator2Options()
options.platform_name = 'Android'
options.device_name = 'emulator-5554'
options.app_package = 'com.instagram.android'
options.app_activity = '.activity.MainTabActivity'
options.no_reset = True

# Инициализация драйвера
driver = webdriver.Remote("http://localhost:4723", options=options)

# Ожидание загрузки приложения
time.sleep(2)

# Открытие ссылки в Instagram
driver.execute_script('mobile: deepLink', {
    'url': 'https://www.instagram.com/reel/DEHOUZ1NOVc/',
    'package': 'com.instagram.android'
})

# Ожидание для наблюдения результата
time.sleep(10)

# Завершение сессии
driver.quit()
