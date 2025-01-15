import re
from collections import Counter

# Входной список ссылок
links = '''https://www.instagram.com/markbarton_mb?igsh=djk0azVlbGlub29j
https://www.instagram.com/dr.alexeysitnikov?igsh=dzR6bWRoMmdwMWl5
https://www.instagram.com/irina_hakamada?igsh=NWphMnRnOXBrcXYy
https://www.instagram.com/yaroslav_samoylov?igsh=MnRsN3d4aTBleGh4
https://www.instagram.com/ivlieva_yulia?igsh=MWdvZ3NjZ2sxbjhkaw==
https://www.instagram.com/vikadmitrieva?igsh=MWc5b2RiemZuNXpmbQ==
https://www.instagram.com/petrosipov1?igsh=Yjd4NHozc3U1end3
https://www.instagram.com/solotatiana?igsh=cDRoZmg3ajZsb2cy
https://www.instagram.com/grebenuk.m?igsh=MXQxdXVobmdjbjVqZg==
https://www.instagram.com/sunlower?igsh=MTdlczl1OWhmM2tyaQ==
https://www.instagram.com/saidov_mikhail/profilecard/?igsh=MXZrc3gyM2U4MjA2bw==
https://www.instagram.com/dr.alexeysitnikov?igsh=dzR6bWRoMmdwMWl5
https://www.instagram.com/isaacpintosevich/profilecard/?igsh=MTBnbDh0NXJ5ZnB6eg==
https://www.instagram.com/irina_hakamada/profilecard/?igsh=bnAweDY3eHlyZGFs
https://www.instagram.com/mindspa_ru/profilecard/?igsh=Z2RjY2JoYWx3OHNt
https://www.instagram.com/grebenuk.m?igsh=MXQxdXVobmdjbjVqZg==
https://www.instagram.com/markbarton_mb?igsh=djk0azVlbGlub29j
https://www.instagram.com/labkovskiyofficial?igsh=MXZiOHN3dTFqcHlnYg==
https://www.instagram.com/sedakasparova?igsh=MTUxaHdrcGF0bTVvaQ==
https://www.instagram.com/sovetnikkk?igsh=MTZsaHVsMXcxd2U4eQ==
https://www.instagram.com/doctor_zubareva?igsh=ZnFiNGxmdWpxZ3kx
https://www.instagram.com/ab.money_?igsh=dWRkcmNic2RobG5u
https://www.instagram.com/sashabelair?igsh=MWZoc2JhYTZkZXVzdA==
https://www.instagram.com/alexandramitroshina?igsh=MXFtemIxbW9zeDR4eg==
https://www.instagram.com/aviasales?igsh=MXF3ZXJnbnpvZ21jbg==
https://www.instagram.com/sofi_progrev?igsh=ZzBjaWtxaXlvYnl3
https://www.instagram.com/volkovafinance?igsh=MWh5YXNjbXFqNjF3Zw==
https://www.instagram.com/saidov_mikhail?igsh=MXc1b2lqaGdqb3FnbQ==
https://www.instagram.com/designschool?igsh=djV0cDdsYXBhdGlk
https://www.instagram.com/gomzova.ekateriina?igsh=MXgzNDlueWNnaW0xOA==
https://www.instagram.com/rizhaya_v_zakone?igsh=MTI2NnRrNHl1M2Q5NA==
https://www.instagram.com/laskavaya.school?igsh=aG85NmRobTF0NmNr
https://www.instagram.com/vikadmitrieva?igsh=MTFqZmJ1aHQ0aDJxYg==
https://www.instagram.com/art.senatorov?igsh=MXBkdjJmZHg1b3lveg==
https://www.instagram.com/sunlower?igsh=MWZjaWt6eDhremZkaA==
https://www.instagram.com/stillvasilisa?igsh=amU1NHg4dTl4YWJm
https://www.instagram.com/schreinerkate?igsh=N2lodDdoaHo4dGF1
https://www.instagram.com/irina.lillo?igsh=YXg1Ymk4bjNxNGI2
https://www.instagram.com/maria.promam?igsh=MTRwMHd4MGhyazhqNQ==
https://www.instagram.com/maria.promam?igsh=MTRwMHd4MGhyazhqNQ==
https://www.instagram.com/satya.expert?igsh=MWRpMXozamR5ZHZlMg==
https://www.instagram.com/inna_de_almeida?igsh=MWpodGZxZ2M0dHd4ZQ==
https://www.instagram.com/vojevatov?igsh=MTlpdnRjdnJtdDY4ZQ==
https://www.instagram.com/krasikovofficial?igsh=dTVtd2poaTFqZWE0
https://www.instagram.com/valentin_shishkin_kinetika?igsh=dzd5ZDd6eXZiOTg4
https://www.instagram.com/sovetnikkk?igsh=cWYyeGl5MXY2ZWVm
https://www.instagram.com/veronik20011/profilecard/?igsh=MWt1cHVsMnR2dmUwMA==
https://www.instagram.com/alenashakh?igsh=MWttazI1ajVya3BleQ==
https://www.instagram.com/tatyana.drugova?igsh=MWNhOXZraHcyZDF1aA==
https://www.instagram.com/psycholog.alexandr.shahov?igsh=MWJnMWJpYTNvNzNlNQ==
https://www.instagram.com/doctor_komissarova?igsh=MWJ3eGJkaGk3dHp2aw==
https://www.instagram.com/katyakvasnikova?igsh=MXhxajlxMjB5ZTdsNw==
https://www.instagram.com/oskar_hartmann?igsh=NnEyazVyMTR6b28w
https://www.instagram.com/portnyagin?igsh=dGkzeWxoemU4a3Bu
https://www.instagram.com/una.tuna?igsh=MWEwcngwaHAydzlvbQ==
https://www.instagram.com/danyavollk?igsh=eHc4ajA5Yjhmemsx
https://www.instagram.com/arina_alexx?igsh=MXhvZnh3bHozcm5tOA==
https://www.instagram.com/viva_la_vika?igsh=MWZpamMzN3NwNjZzbw==
https://www.instagram.com/alenashakh?igsh=MWttazI1ajVya3BleQ==
https://www.instagram.com/mironovanastasiia?igsh=eGZpYzVvb3kwOGZ1
https://www.instagram.com/julz_brend?igsh=OWp2MjVqcjk1bDY0
https://www.instagram.com/irina.lillo?igsh=YXg1Ymk4bjNxNGI2
https://www.instagram.com/irina.lillo?igsh=YXg1Ymk4bjNxNGI2
https://www.instagram.com/be.psycholog?igsh=MWM5d2I3dWRyZGpucw==
https://www.instagram.com/tatakalnitskaya?igsh=Yzk0YWlhaHhxbHd3
https://www.instagram.com/kurpatov_official?igsh=djluODg3dHloc2E5
https://www.instagram.com/vladimir_yakovlev_vainer?igsh=ZGEwanY1YmhyMWFv
https://www.instagram.com/ludmila.petranovskaya?igsh=MWJrdzh3MXUyYmYxMA==
https://www.instagram.com/alexander_kolmanovsky?igsh=YzE1M3l2aXR0cHhw
https://www.instagram.com/luke.and.english?igsh=NzNkbm9tOGlqN2F2
https://www.instagram.com/nata_lienet?igsh=MXVtdGJqeGZzb3Zreg==
https://www.instagram.com/stanislav.kolchatov?igsh=MW1sNmxwMndlcGw5YQ==
https://www.instagram.com/drblondy?igsh=MTliOHhvdWdyb2lnaQ==
https://www.instagram.com/pavellachev?igsh=aXQzbW5iNDh0dWNq
https://www.instagram.com/lena_rindych?igsh=MXRocXg4bmkwM3Vhcw==
https://www.instagram.com/_katelubimova?igsh=MWRkbDIzb3poY2Zrdg==
https://www.instagram.com/maxbelov.live?igsh=OTdxemQ4end1dTVo
https://www.instagram.com/marichevva?igsh=MTJxdnExNTIyc3l1eg==
https://www.instagram.com/_d.yakovlev?igsh=aXJqN21kd2N0cGw3
https://www.instagram.com/sofi_progrev?igsh=ZWlxZmk5NjUydmJr
https://www.instagram.com/ramanava_knows?igsh=M21wbjV4YXl4cGtt
https://www.instagram.com/temalebedev?igsh=NXdjcGZneDkxaWRs
https://www.instagram.com/otvetoshnaya?igsh=MWFrbmVrcmJxaGptcg==
https://www.instagram.com/viktoriamastersaction?igsh=MTdraXl1bmYyejFqag==
https://www.instagram.com/kakcaxap?igsh=cmY4YjlianhsbG4w
https://www.instagram.com/motivator.1nc?igsh=MWFtNm9kMm8zYjVmcg==
https://www.instagram.com/motivession?igsh=MWVmbDRzYnF3bTV3ZA==
https://www.instagram.com/business_people_?igsh=bWo3ZXlvdWpka215
https://www.instagram.com/rm_motivator?igsh=MXBqYW5yNThqY3MxdQ==
https://www.instagram.com/misli_mudretsa?igsh=YnZqZGp0ZDdhYjM0
https://www.instagram.com/mudrec_govorit?igsh=MTdzcGNsOHlxaHdnYQ==
https://www.instagram.com/secrety_manipulatora?igsh=MThibXl2cHhkYmMxdw==
https://www.instagram.com/arsen_dzen?igsh=Z21objQ3enN4eWV5
https://www.instagram.com/sergiv_efko?igsh=aDVueWNxcnUxZ3Mz
https://www.instagram.com/moriarty.proff?igsh=MjQ0Y21hY2Nvczlv
https://www.instagram.com/lea.helps?igsh=MXg4NWlqanV6d2M3Yg==
https://www.instagram.com/memories_postcards?igsh=MXF3bTZsZG1tbHY0Yw==
https://www.instagram.com/iuliastration?igsh=MWhndTd3OXJpNWxuNw==
https://www.instagram.com/kataivisuals?igsh=MXZ5eHduZjBkZjNzZw==
https://www.instagram.com/strengthvisuals?igsh=MWNycm0yaW9qYjVyOA==
https://www.instagram.com/valuethe.mind?igsh=d2tqN3hzNmk4M2pw
https://www.instagram.com/kiririlll?igsh=OWZhZTA2eXRrZm9q
https://www.instagram.com/oliviaherrickdesign?igsh=MWZ4NTF2dW44cDRqaQ==
https://www.instagram.com/mindset.therapy?igsh=ODlhaGFjb3c1a3hw
https://www.instagram.com/danyavollk?igsh=N3dxamF4bHFlOGp1
https://www.instagram.com/sashabelair?igsh=MWZoc2JhYTZkZXVzdA==
https://www.instagram.com/alexandramitroshina?igsh=MXFtemIxbW9zeDR4eg==
https://www.instagram.com/anastasiakere?igsh=MW9lbmF3N3BzcDdxMQ==
https://www.instagram.com/mltsevaa?igsh=dzY3YnFpc2dqeDRo
https://www.instagram.com/alenadaleko?igsh=MWpzZWc4ZDFjMjlrdA==
https://www.instagram.com/aiza.fai?igsh=ejkzb3hjOGE0NWdt
https://www.instagram.com/sofi_progrev?igsh=MW5vanY2aHJjZ2hjZQ==
https://www.instagram.com/theivansergeev?igsh=MWV1bzU4bDl1OHJrcw==
https://www.instagram.com/walerism?igsh=YWlqZDhyZzZieTI4
https://www.instagram.com/entaipova?igsh=ZGNydzNtbG54eXc3
https://www.instagram.com/margo.savchuk?igsh=MWg1amF0cjhwanhpdA==
https://www.instagram.com/dimakhalilov1?igsh=d255Y3U5OHlodGg5
https://www.instagram.com/viva_la_vika?igsh=bmoyaW0zcmFjazU1
https://www.instagram.com/ramanava_knows?igsh=MXJ6aXRqOW5yajQ0ZA==
https://www.instagram.com/arina_alexx?igsh=MW9oaGd4OWd6eDdteA==
https://www.instagram.com/alexandramitroshina_life?igsh=d3IxaG9wbmRvenZt
https://www.instagram.com/alexandramitroshina?igsh=bG9rMGJ5b2kxcmdx
https://www.instagram.com/setters_education?igsh=MW1hOHBpZzFqeWFndQ==
https://www.instagram.com/mironova_mari?igsh=MmVmOXFpMDduZ20y
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