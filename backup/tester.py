import time
import json
from queue import Queue
from threading import Thread

# Очередь для данных
data_queue = Queue()
database = []

# Функция задачи
def task(task_id, data):
    print(f"Начало задачи {task_id}")
    time.sleep(1)  # Эмуляция работы
    data_queue.put({"task_id": task_id, "data": data})
    print(f"Задача {task_id} завершена")

# Поток для обработки очереди
def process_queue():
    while True:
        item = data_queue.get()
        if item is None:  # Сигнал остановки
            break
        database.append(item)
        print(f"Данные добавлены: {item}")
        data_queue.task_done()

# Основная функция
def main():
    # Запуск потока для обработки очереди
    processor = Thread(target=process_queue, daemon=True)
    processor.start()

    # Запуск задач
    tasks = [(1, "data for task 1"), (2, "data for task 2"), (3, "data for task 3"), (4, "data for task 4")]
    threads = [Thread(target=task, args=(task_id, data)) for task_id, data in tasks]

    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    # Завершаем очередь
    data_queue.put(None)  # Сигнал остановки
    processor.join()

    # Сохраняем в JSON
    with open("database.json", "w") as file:
        json.dump(database, file, indent=4)
    print("Данные сохранены в database.json")

if __name__ == "__main__":
    main()
