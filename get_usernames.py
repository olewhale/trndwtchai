import re
from collections import Counter

# Входной список ссылок
links = '''https://www.tiktok.com/@dylanschneider
https://www.tiktok.com/@hennyhermes
https://www.tiktok.com/@officialdjaaron
https://www.tiktok.com/@blakeproehl
https://www.tiktok.com/@kodemusic
https://www.tiktok.com/@jteazy.1
https://www.tiktok.com/@iamlevibloom
https://www.tiktok.com/@thelilgoatofficial
https://www.tiktok.com/@424kp
https://www.tiktok.com/@theofficialmkay
https://www.tiktok.com/@.damien
https://www.tiktok.com/@kandzfr
https://www.tiktok.com/@musicmaestro____
https://www.tiktok.com/@hoodstarjb
https://www.tiktok.com/@tj.se6
https://www.tiktok.com/@chydemusic
https://www.tiktok.com/@itsparkerjack
https://www.tiktok.com/@notkilldyll
https://www.tiktok.com/@__sweezy___
https://www.tiktok.com/@canadian_nosferatu
https://www.tiktok.com/@houndrel
https://www.tiktok.com/@tx2official
https://www.tiktok.com/@derekberry69
https://www.tiktok.com/@20tokens
https://www.tiktok.com/@tommyragen
https://www.tiktok.com/@_doan._
https://www.tiktok.com/@thenoahfinnce
https://www.tiktok.com/@kiralise
https://www.tiktok.com/@lolopopgurl
https://www.tiktok.com/@jversee
https://www.tiktok.com/@iamodeal
https://www.tiktok.com/@therevoir
https://www.tiktok.com/@sennoh_
https://www.tiktok.com/@thatguy_calvin
https://www.tiktok.com/@idkconundrum
https://www.tiktok.com/@zekecordle
https://www.tiktok.com/@dayglow
https://www.tiktok.com/@violentvira
https://www.tiktok.com/@southarcade
https://www.tiktok.com/@montelldeerofcharlotte
https://www.tiktok.com/@damona_offical
https://www.tiktok.com/@eliasgb.wav
https://www.tiktok.com/@rauemusic
https://www.tiktok.com/@benchesband
https://www.tiktok.com/@fritzhagermusic
https://www.tiktok.com/@off_tide
https://www.tiktok.com/@minuteaftermidnight
https://www.tiktok.com/@asdecemberfalls
https://www.tiktok.com/@notenoughspacefl
https://www.tiktok.com/@aoapunk
https://www.tiktok.com/@heartofesha
https://www.tiktok.com/@otukaaaa
https://www.tiktok.com/@malcolmtodddd
https://www.tiktok.com/@wesghost
https://www.tiktok.com/@loverbboiiii'''

# Instagram usernames extraction
try:
    # Подсчет количества входящих ссылок Instagram
    instagram_links = [line for line in links.strip().split('\n') if 'instagram.com' in line]
    total_instagram_links = len(instagram_links)

    # Извлечение usernames Instagram
    instagram_usernames = re.findall(r'(?:https?://(?:www\.)?instagram\.com/)([\w\.]+)', links)

    # Подсчет повторений Instagram
    instagram_username_counts = Counter(instagram_usernames)

    # Вывод всех извлеченных usernames Instagram
    print("\nВсе извлеченные usernames Instagram:")
    for user in instagram_usernames:
        print(user)

    # Вывод повторяющихся с количеством Instagram
    print("\nПовторяющиеся usernames Instagram и количество повторений:")
    for user, count in instagram_username_counts.items():
        if count > 1:
            print(f"{user}: {count}")

    # Уникальные usernames Instagram (все, но без дубликатов)
    unique_instagram_usernames = list(instagram_username_counts.keys())
    print("\nВсе уникальные usernames Instagram (без дубликатов):")
    print("\n".join(unique_instagram_usernames))

    # Вывод метрик Instagram
    print(f"\nКоличество входящих ссылок Instagram: {total_instagram_links}")
    print(f"Количество уникальных usernames Instagram: {len(instagram_username_counts)}")

except Exception as e:
    print(f"Ошибка Instagram: {e}")

# TikTok usernames extraction
try:
    # Подсчет количества входящих ссылок TikTok
    tiktok_links = [line for line in links.strip().split('\n') if 'tiktok.com' in line]
    total_tiktok_links = len(tiktok_links)

    # Извлечение usernames TikTok
    tiktok_usernames = re.findall(r'(?:https?://(?:www\.)?tiktok\.com/@)([\w\.]+)', links)

    # Подсчет повторений TikTok
    tiktok_username_counts = Counter(tiktok_usernames)

    # Вывод всех извлеченных usernames TikTok
    print("\nВсе извлеченные usernames TikTok:")
    for user in tiktok_usernames:
        print(user)

    # Вывод повторяющихся с количеством TikTok
    print("\nПовторяющиеся usernames TikTok и количество повторений:")
    for user, count in tiktok_username_counts.items():
        if count > 1:
            print(f"{user}: {count}")

    # Уникальные usernames TikTok (все, но без дубликатов)
    unique_tiktok_usernames = list(tiktok_username_counts.keys())
    print("\nВсе уникальные usernames TikTok (без дубликатов):")
    print("\n".join(unique_tiktok_usernames))

    # Вывод метрик TikTok
    print(f"\nКоличество входящих ссылок TikTok: {total_tiktok_links}")
    print(f"Количество уникальных usernames TikTok: {len(tiktok_username_counts)}")

except Exception as e:
    print(f"Ошибка TikTok: {e}")

#if usernames
# try:
#     # Подсчет количества входящих usernames
#     total_usernames = len([line for line in links.strip().split('\n') if line.strip()])  # Подсчет usernames

#     # Извлечение usernames (в данном случае они уже в нужном формате)
#     usernames_list = [line.strip() for line in links.strip().split('\n') if line.strip()]
    
#     # Подсчет повторений
#     username_counts = Counter(usernames_list)

#     # Вывод всех извлеченных usernames
#     print("\nВсе извлеченные usernames:")
#     for user in usernames_list:
#         print(user)

#     # Вывод повторяющихся с количеством
#     print("\nПовторяющиеся usernames и количество повторений:")
#     for user, count in username_counts.items():
#         if count > 1:
#             print(f"{user}: {count}")

#     # Уникальные usernames (все, но без дубликатов)
#     unique_usernames = list(username_counts.keys())
#     print("\nВсе уникальные usernames (без дубликатов):")
#     print("\n".join(unique_usernames))

#     # Вывод метрик
#     print(f"\nКоличество входящих usernames: {total_usernames}")  # Вывод количества usernames
#     print(f"Количество уникальных usernames: {len(username_counts)}")  # Вывод количества уникальных usernames

# except Exception as e:
#     print(f"Ошибка: {e}")