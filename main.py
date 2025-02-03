import logging
import pytz
import datetime
import time
import main2

# Настройка логирования
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def run_script():
    logger.info("-------START---------")
    try:
        # Записываем время запуска
        barcelona_tz = pytz.timezone("Europe/Madrid")
        now = datetime.datetime.now(barcelona_tz)
        logger.info(f"Скрипт запущен в {now.strftime('%Y-%m-%d %H:%M:%S')}")
        # Ваша основная логика здесь
        main2.app_run()
    except Exception as e:
        logger.error(f"Ошибка выполнения: {str(e)}", exc_info=True)


def schedule_app_run(target_time_str, option="all"):
    while True:
        try:
            # Получаем текущее время в часовом поясе Барселоны
            barcelona_tz = pytz.timezone("Europe/Madrid")
            now = datetime.datetime.now(barcelona_tz)
            logger.info(
                f"Текущее время в Барселоне: {now.strftime('%Y-%m-%d %H:%M:%S')}"
            )

            # Преобразуем строку времени в объект datetime.time
            target_time = datetime.datetime.strptime(target_time_str,
                                                     "%H:%M").time()

            # Комбинируем текущую дату с целевым временем
            today_target_datetime = datetime.datetime.combine(
                now.date(), target_time)
            today_target_datetime = barcelona_tz.localize(
                today_target_datetime)

            # Если целевое время уже прошло сегодня, планируем на следующий день
            if today_target_datetime <= now:
                today_target_datetime += datetime.timedelta(days=1)

            # Вычисляем разницу во времени
            time_diff = (today_target_datetime - now).total_seconds()
            logger.info(
                f"Скрипт будет запущен в {today_target_datetime.strftime('%Y-%m-%d %H:%M:%S')}"
            )
            logger.info(f"Ожидание {time_diff} секунд")

            # Ожидаем до целевого времени
            time.sleep(time_diff)

            # Запускаем основную функцию
            logger.info("AFTER SLEEP")
            run_script(option)
            #break
        except Exception as e:
            logger.error(f"Ошибка планирования выполнения: {str(e)}",
                         exc_info=True)
            # Ждем 60 секунд перед повторной попыткой в случае ошибки
            time.sleep(60)



if __name__ == "__main__":


    x = 1

    if x == 0:
        print("Скрипт запущен")
        main2.app_run(option="one", account_id=30, range_days="0-21", scraping_type="tiktok")
        #main2.app_run(option="one", account_id=29, range_days="0-22", scraping_type="tiktok")
    elif x == 1:
        print("Скрипт запущен")
        main2.app_run(option="all", range_days="3-3", scraping_type="instagram")
    elif x == 2:
        print("Скрипт запущен")
        target_time_str = "20:00"  # Укажите желаемое время запуска в формате ЧЧ:ММ
        schedule_app_run(target_time_str, option="all")
