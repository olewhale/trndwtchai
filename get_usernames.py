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
https://www.instagram.com/egoyan_anna?igsh=MWRtamkyNjczMTFucQ==
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
https://www.instagram.com/margulan_seissembai?igsh=dDloYTByYmh2Znps
https://www.instagram.com/anyclass.faceonline?igsh=MWFzZ3pzZDk2eWh3aQ==
https://www.instagram.com/igor_vorontsovv?igsh=MXcwMGpwbGg2MnJ4dw==
https://www.instagram.com/alenashakh?igsh=MWttazI1ajVya3BleQ==
https://www.instagram.com/tatyana.drugova?igsh=MWNhOXZraHcyZDF1aA==
https://www.instagram.com/julz_brend?igsh=OWp2MjVqcjk1bDY0
https://www.instagram.com/psycholog.alexandr.shahov?igsh=MWJnMWJpYTNvNzNlNQ==
https://www.instagram.com/nikolay_anatolievich_vasilenko?igsh=ZjUyanNicmsyeTEw
https://www.instagram.com/gur_am?igsh=MXZpdDdsbGZ1eW0zcw==
https://www.instagram.com/doctor_komissarova?igsh=MWJ3eGJkaGk3dHp2aw==
https://www.instagram.com/abramov_ivan?igsh=MWN5b3llZ2s1b3VzMw==
https://www.instagram.com/retrogradnymercury?igsh=MWtobGEyczc0N3Zw
https://www.instagram.com/katyakvasnikova?igsh=MXhxajlxMjB5ZTdsNw==
https://www.instagram.com/oskar_hartmann?igsh=NnEyazVyMTR6b28w
https://www.instagram.com/lada_krasikova?igsh=Y2ZlOHptc2JqeGJu
https://www.instagram.com/nastya.pixy?igsh=MmNoajA2Z3JiN2Zj
https://www.instagram.com/portnyagin?igsh=dGkzeWxoemU4a3Bu
https://www.instagram.com/una.tuna?igsh=MWEwcngwaHAydzlvbQ==
https://www.instagram.com/danyavollk?igsh=eHc4ajA5Yjhmemsx
https://www.instagram.com/arina_alexx?igsh=MXhvZnh3bHozcm5tOA==
https://www.instagram.com/viva_la_vika?igsh=MWZpamMzN3NwNjZzbw==
https://www.instagram.com/alenashakh?igsh=MWttazI1ajVya3BleQ==
https://www.instagram.com/mariafonina?igsh=MWw5cThrOGIwc2tkZA==
https://www.instagram.com/dina_dinameet?igsh=MXEzbGRkMzhnM2h5ZQ==
https://www.instagram.com/mironovanastasiia?igsh=eGZpYzVvb3kwOGZ1
https://www.instagram.com/julz_brend?igsh=OWp2MjVqcjk1bDY0
https://www.instagram.com/anna_gorod?igsh=MXc5eWhjcGdqdWFuNg==
https://www.instagram.com/irina.lillo?igsh=YXg1Ymk4bjNxNGI2
https://www.instagram.com/irina.lillo?igsh=YXg1Ymk4bjNxNGI2
https://www.instagram.com/be.psycholog?igsh=MWM5d2I3dWRyZGpucw==
https://www.instagram.com/vintovkina_arina?igsh=MWhzbHJ6Ynd4dHVxNw==
https://www.instagram.com/anna_akinina?igsh=dmJraTU1amZ4YnZz
https://www.instagram.com/tatakalnitskaya?igsh=Yzk0YWlhaHhxbHd3
https://www.instagram.com/kurpatov_official?igsh=djluODg3dHloc2E5
https://www.instagram.com/vladimir_yakovlev_vainer?igsh=ZGEwanY1YmhyMWFv
https://www.instagram.com/ludmila.petranovskaya?igsh=MWJrdzh3MXUyYmYxMA==
https://www.instagram.com/vipsauna?igsh=a3Y1djNveXA1bGUy
https://www.instagram.com/alexander_kolmanovsky?igsh=YzE1M3l2aXR0cHhw
https://www.instagram.com/luke.and.english?igsh=NzNkbm9tOGlqN2F2
https://www.instagram.com/philguzenuk?igsh=M3hhZWJrd3JwMW5x
https://www.instagram.com/nata_lienet?igsh=MXVtdGJqeGZzb3Zreg==
https://www.instagram.com/stanislav.kolchatov?igsh=MW1sNmxwMndlcGw5YQ==
https://www.instagram.com/drblondy?igsh=MTliOHhvdWdyb2lnaQ==
https://www.instagram.com/pavellachev?igsh=aXQzbW5iNDh0dWNq
https://www.instagram.com/lena_rindych?igsh=MXRocXg4bmkwM3Vhcw==
https://www.instagram.com/maria_logvinova?igsh=cmd2cXBsZm94OGt0
https://www.instagram.com/maria_logvinova?igsh=cmd2cXBsZm94OGt0
https://www.instagram.com/lubyatinka?igsh=a2ZscDJqajczeWJ2
https://www.instagram.com/_katelubimova?igsh=MWRkbDIzb3poY2Zrdg==
https://www.instagram.com/maxbelov.live?igsh=OTdxemQ4end1dTVo
https://www.instagram.com/ten_rays?igsh=ZXE3em5xdDM0MmQ=
https://www.instagram.com/taro.irena?igsh=MTZ6cHl1d3Z1NWpjZg==
https://www.instagram.com/anna__grinkova?igsh=ZWxibWU1ZTg0NW5x
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