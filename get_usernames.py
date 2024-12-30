import re
from collections import Counter

# Входной список ссылок
links = '''https://www.instagram.com/melnikova.kids/
https://www.instagram.com/v.a.r.e.n.i.k0
https://www.instagram.com/marina.ankvab/reels/
https://www.instagram.com/ekaterina.berga/reels/
https://www.instagram.com/only_finance/reels/
https://www.instagram.com/enot_deutsch_club/reels/
https://www.instagram.com/nikonorovarepetitor/reels/
https://www.instagram.com/kidskey/
https://www.instagram.com/rocket.tech.school/
https://www.instagram.com/chessiland/reels/
https://www.instagram.com/sshimanskaya/
https://www.instagram.com/shkola.school/reels/
https://www.instagram.com/care_my_baby/reels/
https://www.instagram.com/deutschonline.b/reels/
https://www.instagram.com/deutschonline.a2/reels/
https://www.instagram.com/onlineschool1.ru/reels/
https://www.instagram.com/skysmart_parents/reels/
https://www.instagram.com/rebotica_edu/reels/
https://www.instagram.com/yndx.practicum/reels/
https://www.instagram.com/skillfactoryschool/reels/
https://www.instagram.com/chessfirst.online/reels/
https://www.instagram.com/algoritmika.study/reels/
https://www.instagram.com/letovoschool/reels/
https://www.instagram.com/itgen.io/reels/
https://www.instagram.com/foxford_edu/reels/
https://www.instagram.com/novakidschool/reels/
https://www.instagram.com/ivrit_with_meital/reels/
https://www.instagram.com/ivrit.with.michelle/reels/
https://www.instagram.com/anastasiakabalina/reels/
https://www.instagram.com/ivritsnikol_official/reels/
https://www.instagram.com/katarina_kot/reels/
https://www.instagram.com/canshecode/reels/
https://www.instagram.com/luke.and.english/
https://www.instagram.com/english.ilovesitcoms/reels/
https://www.instagram.com/valerymis/
https://www.instagram.com/kari_zhu/reels/
https://www.instagram.com/vikapika_usa/reels/
https://www.instagram.com/galabob/reels/
https://www.instagram.com/ludmila.petranovskaya/reels/
https://www.instagram.com/stillvasilisa/reels/
https://www.instagram.com/lavrikate/reels/
https://www.instagram.com/anna_buevi/
https://www.instagram.com/nastya.attention/reels/
https://www.instagram.com/interesnee.life/reels/
https://www.instagram.com/arina_iz_magazina/reels/
https://www.instagram.com/alena_lapenya/reels/
https://www.instagram.com/mrs.dubrovski/reels/
https://www.instagram.com/neuro_gimnastic/reels/
https://www.instagram.com/mesedu.bulach/reels/
https://www.instagram.com/eskorykh/reels/
https://www.instagram.com/podelki_detvora/reels/
https://www.instagram.com/dvizgenie_deti/reels/
https://www.instagram.com/neuro_teacher/reels/
https://www.instagram.com/nadezh_neuro/reels/
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