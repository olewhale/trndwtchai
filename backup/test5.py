import time
from concurrent.futures import ThreadPoolExecutor, as_completed

def subtask(sub_id):
    """
    Это имитация небольшой подзадачи: просто 'спит' 1 секунду.
    """
    time.sleep(1)
    return f"[{sub_id}] завершено"

def big_task(name):
    """
    "Большая" задача. Внутри неё мы параллельно запускаем несколько subtask.
    """
    print(f"Начало большой задачи {name}")

    results = []
    # Во внутреннем пуле будем обрабатывать сабзадачи
    with ThreadPoolExecutor(max_workers=3) as inner_executor:
        future_list = []
        for i in range(5):
            sub_id = f"{name}-sub{i}"
            # Запускаем сабпроцесс
            future = inner_executor.submit(subtask, sub_id)
            future_list.append(future)

        # Собираем результаты сабпроцессов
        for future in as_completed(future_list):
            results.append(future.result())

    print(f"Завершена большая задача {name}, результаты: {results}")
    return results

def main():
    """
    В этой функции мы создаём пул (внешний) и параллельно запускаем 2 big_task.
    """
    with ThreadPoolExecutor(max_workers=2) as outer_executor:
        future_a = outer_executor.submit(big_task, "PROCESS_A")
        future_b = outer_executor.submit(big_task, "PROCESS_B")

        for future in as_completed([future_a, future_b]):
            print("Результат верхнего уровня:", future.result())

if __name__ == "__main__":
    main()
