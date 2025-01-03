import re
from collections import Counter

# Входной список ссылок
links = '''https://www.instagram.com/labellakath/
https://www.instagram.com/chinito_pacas/
https://www.instagram.com/deivpr/
https://www.instagram.com/estevie/
https://www.instagram.com/gonzy/
https://www.instagram.com/_jasiel.nunez/
https://www.instagram.com/juniorzamoraofficial/
https://www.instagram.com/saikobeibe/
https://www.instagram.com/xaviiiofficiall/
https://www.instagram.com/yamisafdie/
https://www.instagram.com/aidanbissett/
https://www.instagram.com/alexanderstewart/
https://www.instagram.com/bludnymph/
https://www.instagram.com/its.emei/
https://www.instagram.com/isabel.s.larosa/
https://www.instagram.com/matthansenmusic/
https://www.instagram.com/megsmithlol/
https://www.instagram.com/mettenarrative/
https://www.instagram.com/itssnowwife/
https://www.instagram.com/teddyswims/
https://www.instagram.com/amariamcgee/
https://www.instagram.com/ibebellah/
https://www.instagram.com/chxrry/
https://www.instagram.com/elmiene/
https://www.instagram.com/jordanward/
https://www.instagram.com/khamari/
https://www.instagram.com/lekan.official/
https://www.instagram.com/leonthomas/
https://www.instagram.com/naomisharon/
https://www.instagram.com/tyla/
https://www.instagram.com/applesage/
https://www.instagram.com/baritaliaa/
https://www.instagram.com/chappellroan/
https://www.instagram.com/thefrostchildren/
https://www.instagram.com/hangrammm/
https://www.instagram.com/hemlockesprings/
https://www.instagram.com/provoker.zone/
https://www.instagram.com/signcrushesmotorist48/
https://www.instagram.com/w.aterbaby/
https://www.instagram.com/whirrwhoreforlyfe/
https://www.instagram.com/310babii/
https://www.instagram.com/41themovement_/
https://www.instagram.com/babydrill/
https://www.instagram.com/bigxthaplug/
https://www.instagram.com/hunxho/
https://www.instagram.com/laybankz/
https://www.instagram.com/odumodublvck/
https://www.instagram.com/_skillababy/
https://www.instagram.com/thatmexicanot/
https://www.instagram.com/veezeworst/'''

#if links
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