import re
from collections import Counter

# Входной список ссылок
links = '''https://www.instagram.com/reel/C-GIgCmPVXt/?igsh=endkOGJ3c3Bjc3k=
https://www.instagram.com/reel/DA_W3X7SPwK/?igsh=YnBucjU0dzZuc3Fs
https://www.instagram.com/reel/C_LJPvRuAPW/?igsh=MXRsZWRhN3Z0emhjcw==
https://www.instagram.com/reel/C-BFaEjSK6P/?igsh=NWNvZ3RwbXc3MGI1
https://www.instagram.com/mullerandcorealty/profilecard/?igsh=MmMxdXRidzE0Mngx
https://www.instagram.com/reel/C4Nhu2fJu99/?igsh=OHc1c20weDQwMDBu
https://www.instagram.com/reel/Cuh274Hv0I9/?igsh=MXhucGd4bW9yNHkxdg==
https://www.instagram.com/thebrokeagent/profilecard/?igsh=aGdmdGwyaHgwc2V5
https://www.instagram.com/reel/C5AJhgfrKWH/?igsh=MWQzc2tsZnhlNGY1Mg==
https://www.instagram.com/reel/C48_B2HOHaW/?igsh=cXVmM3dlMjFwb3F3
https://www.instagram.com/reel/C3YT5h9vQi5/?igsh=bXRtdGp3OWdpN3M4
'''
try:
    # Подсчет количества входящих ссылок
    total_links = len([line for line in links.strip().split('\n') if line.strip()])  # Подсчет ссылок

    # Извлечение usernames
    usernames = re.findall(r'(?:https?://(?:www\.)?instagram\.com/)([\w\.]+)', links)

    # Подсчет повторений
    username_counts = Counter(usernames)

    # Вывод всех извлеченных usernames
    print("\nВсе извлеченные usernames:")
    for user in usernames:
        print(user)

    # Вывод повторяющихся с количеством
    print("\nПовторяющиеся usernames и количество повторений:")
    for user, count in username_counts.items():
        if count > 1:
            print(f"{user}: {count}")

    # Уникальные usernames (все, но без дубликатов)
    unique_usernames = list(username_counts.keys())
    print("\nВсе уникальные usernames (без дубликатов):")
    print("\n".join(unique_usernames))

    # Вывод метрик
    print(f"\nКоличество входящих ссылок: {total_links}")  # Вывод количества ссылок
    print(f"Количество уникальных usernames: {len(username_counts)}")  # Вывод количества уникальных usernames

except Exception as e:
    print(f"Ошибка: {e}")