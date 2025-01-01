import re
from collections import Counter

# Входной список ссылок
links = '''
vladidas
viva_la_vika
valentin_vtv
tvoy_shanks
truspro_business
trushina
tot_samy_sulimov
topbizidei
timergaleevaofficial
temki.est
tatiana.bratsun
svetlana_fin_restorer
sudarev_gleb
sidorenko_pro
shayekin_ruslan
sharipov_islambek
shakir_gataulin
sashbrin
samitovm
sabina_sanber
rybakov_igor
rudakovap
rinadzhi
rays.consulting
profin_advice
profbalance
polyanskayaa
petrochenkow
peter_gremyakin
pavellinkin
pavel_sales
osmanoff_kz
oskar_hartmann
olegcloser
oleg_ipo
nurs_mag
nastya.acsy
nastasya.andrevna
mvoronin
mvfedorenko
motif.tj
michael_kuchment
maxchir
market.prosto
margulan_seissembai
maakooveev
lina_gorbatenko
lauravaigorova
kyrbangaliev
kotov.evgen
kate_lustenko
julz_brend
juliemarkovamovie
jeka_balles
ira_podrez
imanov_gusein
igor_stoyanov
hrd.denis
grebenuk.m
forbes.russia
facelessformula.ai
evgeny_a_frolov
evgeniy_svesh
emil.corp
eleonora_marketing
e.v.rakhimov
duisepayev
dmitriy_sadomskiy
dim_zubr
dashkiev
cw_svaor
crypt0_sfera
burak__dasha
buhgalter.116
boris_zarkov
billion.mp
avetov
asadulla
artem__gura
ariel.pmu
antonthegod
anna.glavbuh
allo.viktory
alina_telling
alexvisotsky
alexandramitroshina
alex.chistyakov
aidahmetov_ali
abduramanovrifat
a.grigorets
damir.reels
salim_almazov
dias_serekbay
polinatopa
neprostomaksim
filippov_iliaa
aza_ai_expert
tany_bo
bellsborough
themixed_reality
dobrokotov
dm_smore
elvira_saraeva
shcherbinin.alexander.01
inntellme
aroundasky
s.belyak
ananian.ai
nastia_dvizh
polina_ai.tech
neuroschool_ai
nargiz_vibes
den_magdanov
kreida.alina
vasiliy.okhotnikov
pivazyan_
incubeai
evgenialight.ai
dushnila.design
zhiphotos
iilusechek
not_morozov
darya_creator
yulia.dati
truelera
vasilyryazanov
cybermind.academy
hanproai
pashu_ai
directoreels
ruslan.neiro
fink_gpt
egorkuzminxr
ilia.paliy
igorbabkoff_ai
aironzak
neuro.gera
kub_studio
aisashbrin
vladkozyra
russgamzatov
neural.anna
lada_pro_online
bonnieandslide
prokofev_artem
kiselevatut
kossolapov_igor
ivan_parfentev
art.senatorov
dasha_cher
wealthrevolution.in
vusithembekwayo
visionary.voyage
tonyrobbins
timarmoo
thirdnetwork
theyounetworkhq
thestartupshow.in
theschoolofhardknockz
thelazyceo
the_propertyboss
stevenguo.io
startupbell
starter_story
skillspowers
simonsquibb
simonsinek
shashank_udupa
santwinder_singh_waraich
run.startup
profit
profgalloway
pashamoga
ourfuturehq
olesia_cake_
mytechceo
money.minds8
momikereel
millionairessence
maurits_neo
mattyr_ecom
marketing.psychology
marketing.growmatics
maria.wendt
makeithappen
luciferburns.888
leilahormozi
kristinasubbotina.esq
kimeyskorner
k.alexmathew
jun_yuh
joshuagilesfirebrand
iyyappan_rajendran
itsrohitkumar
investupmedia
investmentjoy
intend.marketing
infouniverse
howtobeentrepreneur
hormozi
harshhhgautam
grow.kwik
goodworkmb
geoffreywoo
garyvee
fourevamedia
foundr
entrepreneursonig
entrepreneurbeingentrepreneur
emmagrede
daveramsey
codiesanchez
casarthakahuja
businessbeingbusiness
business_ideastosuccess
bossbabesmind
askmichia
amandasibiya
alexlieb
abhisheksri022
sweatystartup
yan_lapotkov
panfil_
pankratova916
20vchq
247_wall_st
7emenov
Learnrealbusiness
advised.tips
ai_finance_guru
alexlieb
alongsidefi
art.senatorov
artemkey_new
backstagewithmillionaires
bankless
borsfinance
builders.central
businessblurb
busirizz
capitalset
cashunatehindi
cheeverscloses
chronicrealityofficial
cookinfos
danspena
derrickpwhitehead
dironsourcing1
discodigits
doodhwaladaily
dylanpage.ning
earthsmotive
ecomheroes_media
elite.matrix
engvall.arts
enniskey_
entreprohooper
fffacts.fffashion
flowbank
fortune500
fortunemag
foundercentral_
foundr
foundstory.in
frank.hrelia
futurefocushq
gareth.biz
goldsilverdotcom
gritcapital
hot.spotmedia
https://www.instagram.com/acquired.fm/
humphreytalks
humzazafar
iam_romeobach
insiderbusiness
instantgyyan
intelligentcryptocurrency
ironhawkfinancial
jakonokoi
jellyroll615
john.china.sourcing
laconicbiographies
leilahormozi
lukebelmarwisdom
luxury_life_2023
marketing.vidyalaya
marketingovermarketing
marketingparas
maxbellona
miravalstudios
myfirstmilpod
nityaurdhva
notvivekshharma
officialjoelkaplan
optionsswing
ourfuturepod
pancodores
razvanpb
realrayanmalik
ree2mz
roastsigma
thefeedski
'''
# try:
#     # Подсчет количества входящих ссылок
#     total_links = len([line for line in links.strip().split('\n') if line.strip()])  # Подсчет ссылок

#     # Извлечение usernames
#     usernames = re.findall(r'(?:https?://(?:www\.)?instagram\.com/)([\w\.]+)', links)

#     # Подсчет повторений
#     username_counts = Counter(usernames)


#     # Вывод всех извлеченных usernames
#     print("\nВсе извлеченные usernames:")
#     for user in usernames:
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
#     print(f"\nКоличество входящих ссылок: {total_links}")  # Вывод количества ссылок
#     print(f"Количество уникальных usernames: {len(username_counts)}")  # Вывод количества уникальных usernames

# except Exception as e:
#     print(f"Ошибка: {e}")


try:
    # Подсчет количества входящих usernames
    total_usernames = len([line for line in links.strip().split('\n') if line.strip()])  # Подсчет usernames

    # Извлечение usernames (в данном случае они уже в нужном формате)
    usernames_list = [line.strip() for line in links.strip().split('\n') if line.strip()]
    
    # Подсчет повторений
    username_counts = Counter(usernames_list)

    # Вывод всех извлеченных usernames
    print("\nВсе извлеченные usernames:")
    for user in usernames_list:
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
    print(f"\nКоличество входящих usernames: {total_usernames}")  # Вывод количества usernames
    print(f"Количество уникальных usernames: {len(username_counts)}")  # Вывод количества уникальных usernames

except Exception as e:
    print(f"Ошибка: {e}")