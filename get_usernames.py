import re
from collections import Counter

# Входной список ссылок
links = '''https://www.instagram.com/bigbrofabio?igsh=eXVwZnZkMzR1MzZo
https://www.instagram.com/kryscina?igsh=ZXZicXQ0OTl4eGlx
https://www.instagram.com/berlinclubmemes?igsh=MWMwbWUxbnViNXhpOA==
https://www.instagram.com/jackitup_careers?igsh=dTRiemQzMzVyZWx6
https://www.instagram.com/just_germanthings?igsh=MTV5dXN3eGR6Y2IxcA==
https://www.instagram.com/payalineurope?igsh=MWdjdXVkM2w3OWN3cQ==
https://www.instagram.com/frau_iz_sibiri?igsh=MTB4bWQ2aGVkbTY4eA==

https://www.instagram.com/sertouch_in_germany?igsh=bWwzbXo3eHRmbWY2
https://www.instagram.com/steffiestravelbook?igsh=OTI4bjVsZGsxZDh5
https://www.instagram.com/ringbahn_roulette?igsh=MTIzYXJ4amMwYTV2Mw==

https://www.instagram.com/buchhaltung_onlineakademie/
https://www.instagram.com/briusartem?igsh=MWdsMjE0bWV2c3A3bQ==
https://www.instagram.com/duolingodeutschland?igsh=MWx0c2pmYmxzMHdkcw==
https://www.instagram.com/deutsch_mit_jhanvi?igsh=aTV3aGwwZzd6a3Ix
https://www.instagram.com/danielingermany?igsh=cHlpbXhqanR6cWZ5
https://www.instagram.com/tykowkaaa?igsh=Nnp6Nzk1ZGxrbWZp
https://www.instagram.com/uyenninh?igsh=MTBnejRtMDRqNG9hbQ==
https://www.instagram.com/foreign_ki_duniya?igsh=M29jbTlvNDE5Y2p5
https://www.instagram.com/berlintipsbyjuan?igsh=ZnIzM213aHg4MWpx
https://www.instagram.com/clarambecker/

https://www.instagram.com/lingua__deutsch?igsh=Mnc2M2xxNWF3YnQ5
https://www.instagram.com/katerynazini?igsh=ZjAwZjFkeHBrZnh3
https://www.instagram.com/__.shinebhagat_?igsh=bWpiNzEwenZ0YjZp
https://www.instagram.com/advokat_kuschnir?igsh=MW52bTJ0Z3dnaGx3ag==
https://www.instagram.com/natalia.in.berlin?igsh=MXZyNjExaTNscTBpZA==
https://www.instagram.com/nukivanlent?igsh=MTh3czI0MGlsMmcxMg==
https://www.instagram.com/marioadrion?igsh=Zm53dzQwOGtzb3g=
https://www.instagram.com/valechek_?igsh=bHBwdWJ1MXpzeWxk
https://www.instagram.com/realbatiwutschi?igsh=MTg5MGMyZ3czeW9hdw==
https://www.instagram.com/annie_ingermany?igsh=a3FveWZqZG5kOWFo
https://www.instagram.com/sharonanntitus?igsh=emRmemVoZjM0bjl2
https://www.instagram.com/travelaroundberlin?igsh=MTR5dHVqbmE1b2NobQ==
https://www.instagram.com/tipberlin?igsh=YXhla2Y2cnhsanVr
https://www.instagram.com/lucierauschnabel?igsh=Ymt2bnR0ZmNuamlx
https://www.instagram.com/vmrose?igsh=M2VwcXg1enl3YXhw
https://www.instagram.com/geissregina_?igsh=MWxrY2dkYmdnM285Yw==
https://www.instagram.com/berlin_de?igsh=Y2JqdjZvNmRwbGY1
https://www.instagram.com/dirkkreuter?igsh=ZmEwa3BzYmoyMXVo
https://www.instagram.com/juristgermanii?igsh=NWkxdTJjdW0yaDVw
https://www.instagram.com/settle.in.germany?igsh=MXg2bHk1em5jYXh0ZA==
https://www.instagram.com/wot_trainings?igsh=cWhjaTcwbDM2NGQ5
https://www.instagram.com/moataz_elaraby?igsh=MXZ1am1pMHZvNGMxdg==
https://www.instagram.com/michelle.friedberg?igsh=eGl5MGducjdpcGw1
https://www.instagram.com/vadimalesya_key?igsh=OXcwODVxbGQxN2t0
https://www.instagram.com/hh.deutsch?igsh=M2xzc3JzanY0bDE4
https://www.instagram.com/aittr.de?igsh=MXhkenA3ZG9jMjJ0Zw==
https://www.instagram.com/wunder.deutsch?igsh=MWJjdmk5c25sYnZibQ==
https://www.instagram.com/easygermanvideos?igsh=MTc5b2JzNjlwaWpvOQ==
https://www.instagram.com/easygermanvideos?igsh=MTc5b2JzNjlwaWpvOQ==
https://www.instagram.com/nukivanlent?igsh=MTh3czI0MGlsMmcxMg==
https://www.instagram.com/avantiina?igsh=cm4yZDF1b2xzZ2Ey
https://www.instagram.com/carolinepreussde?igsh=MTE2NDk5OGtkcDQ4ag==
https://www.instagram.com/ayyetay?igsh=YmFtYzN0Y2p4dTFt
https://www.instagram.com/haofx?igsh=eDJuMDYyeGNscjdz

https://www.instagram.com/germanbitesize?igsh=Zzg1NTgwcHJmMm94
https://www.instagram.com/careerspace.app?igsh=Z2pvbTRqcjlnZWh0

https://www.instagram.com/deutsch_eins?igsh=bG0zbmdteWsxcDF1
https://www.instagram.com/germanwithstory?igsh=a3BtcHIzZGVvOXMy
https://www.instagram.com/deutschag?igsh=Y3gyYW9ybzI5b3Ju
https://www.instagram.com/panfil_?igsh=MWxsdTMzZ2JzbWljdw==
https://www.instagram.com/viva_la_vika?igsh=ZDgyMmptaDMwbzRk
https://www.instagram.com/itcareerhub?igsh=MTNuZTY4anRkcDk1bA==
https://www.instagram.com/mutti_bunti?igsh=MTR3eDBldHlpNG80eg==
https://www.instagram.com/tim.sokolov_?igsh=M290dml6NnV5YmRx
https://www.instagram.com/gesunde.finanzen.de?igsh=d2ZvZjZ6ZTFkZGgz
https://www.instagram.com/deutsch_sovet?igsh=MWpsdGt2aW1nMGlkaw==
https://www.instagram.com/skidki_de?igsh=MXBoZjdhYjFpN2E4eg==
https://www.instagram.com/germany.expert?igsh=MWI5ZzUwMGc4NWRvNA==
https://www.instagram.com/berlin.explore?igsh=b3lnaDg1azI0aHJ3
https://www.instagram.com/berlinglimmers?igsh=bmo2ZmI0Zm9td292
https://www.instagram.com/its.kmo_?igsh=MWZyMHZpYmR3bHRyOQ==
https://www.instagram.com/_robbiethompson?igsh=Mmp6ODRuYmt6c3Zy
https://www.instagram.com/kostandiina?igsh=dHQ3bHhqeG1id3R6
https://www.instagram.com/learn.german.fast?igsh=MW1pMWZmenFtamFzaQ==
https://www.instagram.com/deutschland_de?igsh=MXBqaHlxeXZzOTNmcA==
https://www.instagram.com/michelle.friedberg?igsh=eGl5MGducjdpcGw1
https://www.instagram.com/journeyby_jacq/
'''

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