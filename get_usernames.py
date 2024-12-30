import re
from collections import Counter

# Входной список ссылок
links = '''
https://www.instagram.com/advokat_kuschnir?igsh=OGJ6eHRvd2RibXdz
https://www.instagram.com/antimakler?igsh=aG90Z2tudXEyank5
https://www.instagram.com/juhnsteuerberater?igsh=MWdna3lrZDZwcmhiaw==
https://www.instagram.com/juristgermanii?igsh=OTdpZ2NlYWh0YWRh
https://www.instagram.com/mariarusde?igsh=MTB6OTBtOGppZnhiMw==
https://www.instagram.com/juliainberlin_?igsh=MWR5aXQ2cXRoYmE0dw==
https://www.instagram.com/germany.explores?igsh=MXBmNmE0cWF1MzY0Mw==
https://www.instagram.com/berlin.explore?igsh=eDVvMGhrN2sxdWp2
https://www.instagram.com/visitberlin?igsh=enNyb3Jqam92cTAx
https://www.instagram.com/berlinglimmers?igsh=cWFwODNlcG51NGR0
https://www.instagram.com/berlin_de?igsh=MW05MWVhNmU2YzUwZQ==
https://www.instagram.com/natalia.in.berlin?igsh=Nzg1b3A1OW1ibmgw
https://www.instagram.com/polina___berlin?igsh=NHdyOWN4MWt6eGlu
https://www.instagram.com/berlinxperience?igsh=MWNweWJzdG83ZG9ocw==
https://www.instagram.com/berlin_forever_berlin?igsh=MWUya2MxeWc2cHpldQ==
https://www.instagram.com/explores.berlin?igsh=anI0MjVwNHZwdGk3
https://www.instagram.com/gastroberlin?igsh=ejJlNWRlM3NqMmhn
https://www.instagram.com/koeln_de?igsh=eHE1dXFoa3Fwa2dq
https://www.instagram.com/koelnerdomofficial?igsh=MWJ3ZTU0cno0ZG9jaQ==
https://www.instagram.com/geheimtippkoeln?igsh=NnNjcHFnbzBtZWU4
https://www.instagram.com/podslushano.de?igsh=bHZ0b2g0NG11Yjhm
https://www.instagram.com/placestobe_munich?igsh=b3I0YzYxcTUxd2h5
https://www.instagram.com/daysofmunich?igsh=MXcwNGt0ZXF1YjV5eg==
https://www.instagram.com/genussverliebt_?igsh=MWJ6a3M2OTUzcGE0YQ==
https://www.instagram.com/inlovewith_adventure?igsh=YnFjM3JqaDhzZ25s
https://www.instagram.com/hamburg?igsh=MTBiajNlY2tnaWkwMQ==
https://www.instagram.com/heuteinhamburg.byhaspa?igsh=MTdtbzNyeDBqaHF3Zw==
https://www.instagram.com/sabrinaxfavs?igsh=MWJ0YTN0dmd6MmVkdA==
https://www.instagram.com/frankfurt.de?igsh=MTV0cWF3d3VmbTRoMQ==
https://www.instagram.com/frankfurttipp?igsh=MTBleWk1a3hocHU1cQ==
https://www.instagram.com/frankfurt__aktuell?igsh=MTJ1YnV5cmF1amh0
https://www.instagram.com/frankfurt.vibe?igsh=c2dmZDR5N3dlcGow
https://www.instagram.com/germanytourism?igsh=aTA0NXE0bjlqODJv
https://www.instagram.com/margaritkaaa?igsh=Mm10dnV6NWJ6ejQz
https://www.instagram.com/alusha.life?igsh=MXV2NGI5aGxuNTRxeA==
https://www.instagram.com/mayson_berliner?igsh=ejZjcmFjMzBxOHdh
https://www.instagram.com/berlin_forever_berlin?igsh=MWUya2MxeWc2cHpldQ==
https://www.instagram.com/munichinside?igsh=cnF2N3dwNTFlZDNo
https://www.instagram.com/hamburg_de?igsh=MXgycWhkaWh3YTFhMw==
https://www.instagram.com/geheimtipphamburg?igsh=dWhmb2R1M2w3Mnk1
https://www.instagram.com/visitfrankfurt?igsh=MTd5cmg0b2t3OGhxcw==
https://www.instagram.com/frau_iz_sibiri?igsh=MTRibDYwcHJwdGx5YQ==
https://www.instagram.com/nemusli?igsh=MWI4aTUyYTZ1NnhkYg==
https://www.instagram.com/tanya_from_kharkiv?igsh=ODNycmhyZXc0cXdi
https://www.instagram.com/anastasia_germany_de?igsh=MTI0aWNhcDFvMGV2ZQ==
https://www.instagram.com/anako.vg?igsh=MW9nMTE0NnY1Z3Fvcg==
https://www.instagram.com/viki.victoriia?igsh=MTkwYXZyMmVvamUweQ==
https://www.instagram.com/tykowkaaa?igsh=MW5icGpqaGV2cmR3Yg==
https://www.instagram.com/garik_scharit?igsh=NDN0amdxNTQ5c2N5
https://www.instagram.com/herr_iz_sibiri?igsh=MThtNGRjbWlxMmY5NA==
https://www.instagram.com/dashabenz?igsh=MTY2YzZsdTRtNTFtdw==
https://www.instagram.com/karisha_kaa?igsh=MWg5YTFjYjZwMXgwNQ==
https://www.instagram.com/d.kdzh?igsh=MXJlM3B1ZzlvdnBlYg==
https://www.instagram.com/xenia_hl?igsh=MTdiNWt4cjhiZHc3dQ==
https://www.instagram.com/mutti_bunti?igsh=ZDF1dmZsZXF2ZHk5
https://www.instagram.com/kak_ja_stala_frau?igsh=d25qNnNsOTFpdXV1
https://www.instagram.com/kati_dusseldorf?igsh=Nnc4czh6ODI0ZHVy
https://www.instagram.com/intermigro?igsh=cXh3am5jYnh3Z3J4
https://www.instagram.com/iryna_talavyria?igsh=ZDJzOWd0b3UxZTFi
https://www.instagram.com/jetminds.company?igsh=dms5N3psdHN5ZTM5
https://www.instagram.com/zhenya_murat?igsh=MWwwMXMyeTN5azczZA==
https://www.instagram.com/ka4a_in_berlin?igsh=OGlxMHNjN3A5N3lz
https://www.instagram.com/iunskaya?igsh=MTFvdGE2bDVpZGhnYw==
https://www.instagram.com/lena_reisen.de?igsh=MWo1am1jbWc3ajBqaA==
https://www.instagram.com/alina.foodi?igsh=MnI4MmxubGJnbHRo
https://www.instagram.com/strraus?igsh=MXkyYzBpNHh1NzB5ag==
https://www.instagram.com/angelika_falkov?igsh=MWJnYWRkbGpzdDgzag==
https://www.instagram.com/arina_germany?igsh=bGpoeWppNHBiNTk2
https://www.instagram.com/uslugi.de?igsh=eWZrcGRsbmFvMTYw
https://www.instagram.com/vascha_dascha?igsh=MWJrZTB1cmp6cnJkcQ==
https://www.instagram.com/alexeyhummel?igsh=MW1hNG05N3lmdTl5aw==
https://www.instagram.com/agilefluent?igsh=dHI5bmh4ZnRjdmx2
https://www.instagram.com/ep_advisory?igsh=MXVtbzRhOWY2dHE3bQ==
https://www.instagram.com/alena_in_deutschland?igsh=d3BoOGIxNjY2NmFx
https://www.instagram.com/nizza_nikka?igsh=Z21vcTF6dTFzczhy
https://www.instagram.com/elza.travels?igsh=MXQ3M3kwZDB2a2M5NA==
https://www.instagram.com/anastasiia_bdnrk?igsh=NzNuOTlrMnRpNGlv
https://www.instagram.com/germany.bound?igsh=dDJkZ2sybmtvZWI2
https://www.instagram.com/irish_man_in_germany?igsh=MTR0cHF4dTZlc253ZQ==
https://www.instagram.com/simplegermany?igsh=MTZxMWszdGZrbmtmMg==
https://www.instagram.com/just_germanthings?igsh=cmd2bTI2dzFncXU1
https://www.instagram.com/schatzi5551?igsh=MXcyaXliMzZ3eXJsaw==
https://www.instagram.com/olyapro.online?igsh=MXRkYnkwdTc4aDEyOA==
https://www.instagram.com/saprykina.daria_?igsh=MXU2Mm02bGg4cXR2eg==
https://www.instagram.com/d.kdzh?igsh=MXJlM3B1ZzlvdnBlYg==
https://www.instagram.com/vitadeutschland?igsh=OGhiYTA3NHA0Z28x
https://www.instagram.com/oksana_kharaman?igsh=Y3YwOTV6am04c28w
https://www.instagram.com/inga_lamouroux?igsh=dDA4eXhzenViYnh1
https://www.instagram.com/samara_academy?igsh=aDJpY2s4N241eXhj
https://www.instagram.com/kotova.de?igsh=aTFwczRqMmNwMG1i
https://www.instagram.com/buchhaltung_onlineakademie?igsh=M3kwc2I3eno4eHI5
https://www.instagram.com/youngmasha?igsh=MTN5cWg1MXc4MHdo
https://www.instagram.com/nadyameleshko?igsh=b2p1dGY5eGpubHZp
https://www.instagram.com/germany_expat_life?igsh=MWkwM3ZzeDl6MW80
https://www.instagram.com/foreign_ki_duniya?igsh=bjJoZW50Zjd2NWlo
https://www.instagram.com/buchhaltung_onlineakademie?igsh=M3kwc2I3eno4eHI5
https://www.instagram.com/agilefluent?igsh=dHI5bmh4ZnRjdmx2
https://www.instagram.com/engels.ira?igsh=cWVnY2t5Y2pyY2xr
https://www.instagram.com/reisekg?igsh=MWZvZ2d1dzVjbGZlOA==
https://www.instagram.com/job.agentur_germany?igsh=MWxtbjI1eHQ0YWFmZA==
https://www.instagram.com/uyenninh/reels/
https://www.instagram.com/irinabanaru/
https://www.instagram.com/itcareerhub?igsh=bTV5bWJtbHNuaWZq
https://www.instagram.com/intermigro?igsh=MTY5MjVzc3V0b2Vudg==
https://www.instagram.com/nemusli?igsh=NTdic3d2Z2QyaDJ4
https://www.instagram.com/mutti_bunti?igsh=NG5hNnFudzA0Z3g3
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