import re
from collections import Counter

# Входной список ссылок
links = '''https://www.instagram.com/v_alekseev?igsh=OG9maXduMmVzc3M3
https://www.instagram.com/bulatkhamidullin1?igsh=OGFwMml6aHN4NXQ1
https://www.instagram.com/krasnovsn?igsh=MXhzY2lobzNuazlsbg==
https://www.instagram.com/afanasyevnf?igsh=MTR3NWY5cmpqbGt2MQ==
https://www.instagram.com/academy.camopazvitiya?igsh=a2h2bHYzNG40bXUx
https://www.instagram.com/nmiac1?igsh=bjhuOHQ4ZXZlYTQ3
https://www.instagram.com/elmira_shoinbekova?igsh=eHp0Nng0ZnR3MzE=
https://www.instagram.com/danilova.tanyaa?igsh=MWN1cm1ncHM1M3hocg==
https://www.instagram.com/ilnaznabiullin?igsh=MW9yZTIyaXh5a3FnbQ==
https://www.instagram.com/mtokovinin?igsh=MTRuMDV6MmNlcmk4
https://www.instagram.com/agabekovartem?igsh=czZpMGM5bG5xbWgx
https://www.instagram.com/marketing.masha?igsh=NHdybjQ5b2Jnandx
https://www.instagram.com/atlanty_club?igsh=bmJlbnh1YjJ4M216
https://www.instagram.com/sikorskaya_mari?igsh=bzhjNG1qbDZyanZ3
https://www.instagram.com/andrelazarev_official?igsh=MXVieGxxazc1czRzOA==
https://www.instagram.com/mondaydotcom?igsh=MTVvNmtoaTR2YzdwdA==
https://www.instagram.com/moneymindsetmami?igsh=MTNsbDk4Z2ZqOTBrYQ==
https://www.instagram.com/german_roistat?igsh=dm0xdjJxMHY5cW8x
https://www.instagram.com/moskotin?igsh=emgyZjVnazRqdjB1
https://www.instagram.com/anyakamenets?igsh=YXoyNzd0emQ4d3Bw
https://www.instagram.com/vitalygolitzyn?igsh=ZWo5Zm5rcGFoYTEz
https://www.instagram.com/kaisark_?igsh=MXU3enY5MG9iMDg1aQ==
https://www.instagram.com/solovyov_maxim?igsh=dTg0NHdxMDNoY21u
https://www.instagram.com/ivanavramenko?igsh=NmFzOGMzdDE1NXp5
https://www.instagram.com/khodzhaev_azam?igsh=MW11ZDd6N3RoYjdmeQ==
https://www.instagram.com/oleg.dymshakov?igsh=ZnIxdHFhcTh3M2Mw
https://www.instagram.com/alisagolovneva?igsh=NmUzb285eTQ0dG5s
https://www.instagram.com/korolkov.life?igsh=MWlrenB0bHNzNG1lZw==
https://www.instagram.com/maxim_batyrev?igsh=MW50MnJhNXVndmFocg==
https://www.instagram.com/shakir_gataulin?igsh=MXBkZW5tdW4ybHVr
https://www.instagram.com/tsay.dm?igsh=eW45NG9razFiMm9x
https://www.instagram.com/valerya.mikhaylova?igsh=MXA0ZG0xMDd4Nzk5eg==
https://www.instagram.com/hamzaiten?igsh=bDh4MzZ3bjdjcWg3
https://www.instagram.com/diana_ivashchenko_?igsh=ZTlxbzlrM2ZhN2Jl
https://www.instagram.com/jeksen_jvteam?igsh=MTNqNmVzcGk2eG1mbw==
https://www.instagram.com/luda_dell?igsh=c3Q3NDRyZzl2ZzE3
https://www.instagram.com/vlad.bermuda?igsh=NGJudG9idjAzeWs4
https://www.instagram.com/motivationenergy1?igsh=MXYzejhqbjIyb3Bi
https://www.instagram.com/berdanoff?igsh=MWRndHE1ZDN0aTl5ZA==
https://www.instagram.com/viktor.kuznetsov.18?igsh=c2YzY200eTN5amlj
https://www.instagram.com/aigul_bahralinova?igsh=MTc2OG03Z3gxZHV3Mw==
https://www.instagram.com/margarita_lushkina?igsh=MXR5aDg0cm52cGR4MQ==
https://www.instagram.com/bznsmentor?igsh=MWppdTJ6Nm9iM2Znag==
https://www.instagram.com/pavel_sales?igsh=dG40M3IxMnhoMW1i
https://www.instagram.com/petrochenkow?igsh=MTFoZnI1ZnRkbnR2OA==
https://www.instagram.com/chernyak_yevgeny?igsh=MWZobGdiNXdkeWJzcQ==
https://www.instagram.com/stashkevichyan?igsh=MWl6anJmNnY5dDdjdA==
https://www.instagram.com/salesforce?igsh=b3Y4b3JoZGJrczRr
https://www.instagram.com/stefan_studio?igsh=MWdycndpZ2JsZW9veA==
https://www.instagram.com/club_miliarderov?igsh=MTVmYTIxN216Y3M1aw==
https://www.instagram.com/ali_nadjuzah?igsh=MW13ZjVyMDdkcDdudw==
https://www.instagram.com/hubspot?igsh=NWh4Z3h2azZyMzl0
https://www.instagram.com/osfetisova?igsh=MTl6NjBiMDhsbDhwcA==
https://www.instagram.com/katerina_ukolova_life?igsh=MXYxMGsyZ29sYjVjMg==
https://www.instagram.com/moscow_vv?igsh=eDhndjBkOXlnNXNy
https://www.instagram.com/trendwatching_com?igsh=cDdwaWprcGIyN2E=
https://www.instagram.com/mariafonina?igsh=MTRhMnVkY3o1bWZxcg==
https://www.instagram.com/nikitakonev?igsh=MXN0amczdW5pNDJxaQ==
https://www.instagram.com/daria_gomziakova?igsh=MTN6NWE2eml0aHk0MQ==
https://www.instagram.com/market.prosto?igsh=Y3lkZGV3bXNzeTZi
https://www.instagram.com/masli.ce?igsh=MW83b3JoaWVtaGFsYw==
https://www.instagram.com/silauma?igsh=YXIwdmptN21xd3By
https://www.instagram.com/chistyakov_george?igsh=MXBpdG1qejQxZG04Zg==
https://www.instagram.com/grits.partners?igsh=MW1saTc1MDd4amk0cA==
https://www.instagram.com/podless.vladimirs?igsh=MW9jamExdjdtZDZpeA==
https://www.instagram.com/vladidas?igsh=amhpbzNmcGM0N295
https://www.instagram.com/alexyanovsky?igsh=ZzgyMmIzMDh2YnZu
https://www.instagram.com/kutergin?igsh=eHg3ZGI1bWxwaG9j
https://www.instagram.com/bakalchuk_vladislav?igsh=MXE0cTUyY2dvd25tMg==
https://www.instagram.com/alexanderorlovbulldozer?igsh=MWl3czdxcnN6cWZhbQ==
https://www.instagram.com/kumar_mussayev?igsh=MWVlMDFjbW01cTVjYw==
https://www.instagram.com/kurakinbz?igsh=MWxxcGE5eTBkdTh1bA==
https://www.instagram.com/vladimiryakuba?igsh=MTNoZTlmMXlwc3F5cg==
https://www.instagram.com/mednikova.promanagement?igsh=MWgyN2RrZXZ6a2Rmag==
https://www.instagram.com/margulan.books?igsh=aGZ4bDd0Y2Y1N20x
https://www.instagram.com/truspro_business?igsh=anNiaDd3eWoyeG04
https://www.instagram.com/lada_pro_online?igsh=dzl3Y2o5ZDdtMmJ5
https://www.instagram.com/dashkiev?igsh=enF0ZDRxZnl1NzJr
https://www.instagram.com/sokolovskiy?igsh=bWNuaTByajAzanJz
https://www.instagram.com/portnyagin?igsh=c2R6MzdwenYyNm16
https://www.instagram.com/alexvisotsky?igsh=ZDRsdDZhNGc2Zm5y
https://www.instagram.com/zin_irin?igsh=MXF4NnE2aWEwbm1vcw==
https://www.instagram.com/rybakov_igor?igsh=Z2xoaDN5bGIxNTRt
https://www.instagram.com/pavelgitelman?igsh=MW92emIxc3dpODZ6MA==
https://www.instagram.com/way_of_millionaire?igsh=Y3pydTNnZHU4dWc5
https://www.instagram.com/denisenko.911?igsh=eXc0eTc0N2dhZ2M5
https://www.instagram.com/ladapopova?igsh=MWpveHIyY2dyYnY1dg==
https://www.instagram.com/_d.yakovlev?igsh=MTduYmQ3b3JxMGZ2Mg==
https://www.instagram.com/dmitry_levitsky?igsh=MWpzZ2s4djhoank1dw==
https://www.instagram.com/alexmerzliakov?igsh=MWMycXhzNnhqcmc2OQ==
https://www.instagram.com/olegcloser?igsh=bWt1bmRoZm05cTgx
https://www.instagram.com/margulan.motivation_?igsh=NGJ1dmZreXdqM3hz
https://www.instagram.com/julz_brend?igsh=MTViMzdlMnBrc2xjOQ==
https://www.instagram.com/mvoronin?igsh=eGV3dGpjNHYwcGZj
https://www.instagram.com/michael_kuchment?igsh=ZzRhNzdlbTNwb3V0
https://www.instagram.com/demesick?igsh=Z25vYnI1ZnZqaDRv
https://www.instagram.com/imanov_gusein?igsh=bnZjbnN0eHZpczM=
https://www.instagram.com/avetov?igsh=bzRuYnppOWVrNTVy
https://www.instagram.com/ismailov__arsen?igsh=MWFmN3Fmc2Mzc2twbw==
https://www.instagram.com/karakozov01?igsh=MXMyMXdiM3MxdXVubg==
https://www.instagram.com/yusup.karada?igsh=bTNtd295OHpqbGM1
https://www.instagram.com/mann_igor?igsh=ZHJsNGI0cWwzYmQ1
https://www.instagram.com/askardolgikh?igsh=MTUyczh5N29qcmdteA==
https://www.instagram.com/wealt_famous?igsh=N2ZqY3VjanRvamR6
https://www.instagram.com/olegtorbosov?igsh=djFuZTQ1NmpubHRx
https://www.instagram.com/valentin_vtv?igsh=dXZnMGJ0OWM1d3Nm
https://www.instagram.com/agrudin?igsh=MTl1emk5Ymg0NTVnMw==
https://www.instagram.com/margo_bylinina?igsh=MTZ4bTR4OTh2cmlhcw==
https://www.instagram.com/jane_star?igsh=MWFzYjZ6MDRybnhtbg==
https://www.instagram.com/rinadzhi?igsh=cXFjYWc4MG04Mmhv
https://www.instagram.com/nastasya.andrevna?igsh=dXRyMHZkcGNxcDVm
https://www.instagram.com/finance_rules?igsh=czZuanp4MHRqNXFx
https://www.instagram.com/isaacpintosevich?igsh=dXB3aWJ4ZXNkcGV5
https://www.instagram.com/aidahmetov_ali?igsh=MWNscnV2c3J1b2loMQ==
https://www.instagram.com/ruzhina_evelina?igsh=MWFrOWVsaGtwZXpwcQ==
https://www.instagram.com/miliarder.team?igsh=MTF6aTZtNnRsMWc0bQ==
https://www.instagram.com/oskar_hartmann?igsh=YmFveHJ6MnA3cnRk
https://www.instagram.com/abduramanovrifat?igsh=MTBmYjBtdDdoaTF1NQ==
https://www.instagram.com/mvfedorenko?igsh=MTQ0bGxmZGozbnN4aw==
https://www.instagram.com/business.vine?igsh=ZnlmNnJza2VxcXpk
https://www.instagram.com/anna_filina_hrfeedback?igsh=MWExcWR2bGMwcHhtMg==
https://www.instagram.com/ilena.salieva?igsh=MXdicjZjYmhhM2p6cQ==
https://www.instagram.com/vladkozyra?igsh=bWpxNm41b2t4bTVr
https://www.instagram.com/lucky.info?igsh=OWQ0NWdmaThwZXlz
https://www.instagram.com/kurchanov_evgeny?igsh=NmpyeG92ajI1amdr
https://www.instagram.com/sabi.beis?igsh=bm9wNzRiZ2pycHJq
https://www.instagram.com/finance_rush?igsh=b2FjbTQ2cHN2b2c=
https://www.instagram.com/radislavgandapas?igsh=djZ1dnMwN25mOXUy
https://www.instagram.com/corporate_mystic?igsh=MTJkZWd6YzE1cmMzcw==
https://www.instagram.com/arthur.muradov.official?igsh=YXdrYWRmb2ZkdGEw
https://www.instagram.com/jeka_balles?igsh=amE0eWI3bWZ4MXdw
https://www.instagram.com/faisomlab?igsh=ZDIwOHl6bWV6ZGx3
https://www.instagram.com/motivatortvoy?igsh=anI3czc3NTBua2N5
https://www.instagram.com/alexandramitroshina?igsh=MWg5eGdobWVpenp3Yw==
https://www.instagram.com/mikhail.timochko?igsh=bWV5ZXlmZDg2MzJi
https://www.instagram.com/motiv.person?igsh=dnRkOGxoMjJtaXJp
https://www.instagram.com/artemkey_new?igsh=dGNyMWltNnh1bDNw
https://www.instagram.com/ekaterina.lbragimova?igsh=MXY1dmNjNGx6b2tkeA==
https://www.instagram.com/margulan52weeks?igsh=N3UwMnd2ZGJkZjVk
https://www.instagram.com/yura.muradyan?igsh=MXg2bHZrZjYwNXNidg==
https://www.instagram.com/businessstage?igsh=b2U3cHFhZGI0ZW5s
https://www.instagram.com/ayazshabutdinov?igsh=MW9icWZrdW9iZGtkcA==
https://www.instagram.com/saidmurod_davlatov?igsh=eGVyc2RkbndtaDk0
https://www.instagram.com/tonyrobbins?igsh=YWJlMzRvNHYwY2hi
https://www.instagram.com/philguzenuk?igsh=MW5yZnUxazRldzI1OA==
https://www.instagram.com/motiv_strong?igsh=d3Bmdjlka2xxaGMw
https://www.instagram.com/petrosipov1?igsh=MXVmcXJyZzhoMnE0Zg==
https://www.instagram.com/hakamaton?igsh=MXZ5bjhuczI0ZWRxbA==
https://www.instagram.com/grebenuk.m?igsh=MTV0OTZsOWg2bzl0Yw==
https://www.instagram.com/art.senatorov?igsh=MXZqYmw0cnB1ZGt4cw==
https://www.instagram.com/dr.alexeysitnikov?igsh=NXExNWNwaHlncnlx
https://www.instagram.com/sashbrin?igsh=MTdpeXlrNWQ0MDdqNg==
https://www.instagram.com/garyvee?igsh=MTZ6ZDlvaGN3eGt4cQ==
https://www.instagram.com/margulan_seissembai?igsh=MWN3cXpmbDFqdzlubw==
https://www.instagram.com/yevgeny_motivation?igsh=MWZneTZwMHBvanJ2Yw==
https://www.instagram.com/artemkey_new?igsh=dGNyMWltNnh1bDNw
https://www.instagram.com/arthur.muradov.official?igsh=YXdrYWRmb2ZkdGEw
https://www.instagram.com/_d.yakovlev?igsh=MTduYmQ3b3JxMGZ2Mg==
https://www.instagram.com/peka_pohudel?igsh=NDR6cHZxc2lpYm14
https://www.instagram.com/daria_gomziakova?igsh=MTN6NWE2eml0aHk0MQ==
https://www.instagram.com/tsay.dm?igsh=eW45NG9razFiMm9x
https://www.instagram.com/sabi.beis?igsh=bm9wNzRiZ2pycHJq
https://www.instagram.com/nargiz.batyrshayeva?igsh=eHlkb2Vmc3d5OXFq
https://www.instagram.com/tleuhanov?igsh=aXViN21wa3ozMjRy
https://www.instagram.com/rus_libirry?igsh=MW81NTdrYXp2bHpmaw==
https://www.instagram.com/derbis_xo?igsh=Y3JrcDUxMmJjbmQ5
https://www.instagram.com/manshuk_kerey?igsh=NmVxNnh4cnA5MDJj
https://www.instagram.com/hamzaiten?igsh=bDh4MzZ3bjdjcWg3
https://www.instagram.com/vladimiryakuba?igsh=MTNoZTlmMXlwc3F5cg==
https://www.instagram.com/jeka_balles?igsh=amE0eWI3bWZ4MXdw
https://www.instagram.com/vadym_vb?igsh=MTlvcDM5ejVjZWRncQ==
https://www.instagram.com/artem_vb?igsh=a2VmM3R1NnM1czJ1
https://www.instagram.com/jan_voskresensky?igsh=ejgwdWdjM2pwODg2
https://www.instagram.com/pruddan?igsh=ZnUzNWo2aXZpY2Y=
https://www.instagram.com/business_nastroy?igsh=MnAzcmZtdDU4MnJm
https://www.instagram.com/andreyneginskiy?igsh=MThlOGI5anBtb3lqOQ==
https://www.instagram.com/kalinin?igsh=MXR2aDUyaXI4ZG41cA==
https://www.instagram.com/velizhanini?igsh=djZodjE0YXg5cm9k
https://www.instagram.com/sofi_progrev?igsh=OWY0b2Y3czRwbjc5
https://www.instagram.com/_olliko_?igsh=bGU0eTZhMjM1cXJn
https://www.instagram.com/mynova_oksana?igsh=MTJscnFxY2R3OGF5Zg==
https://www.instagram.com/ana.mavricheva?igsh=bmFjeng1bDRjNW9u
https://www.instagram.com/julls_target?igsh=MXVxcWNleW9lajQ4
https://www.instagram.com/ruslana_vetrenko?igsh=MWd5cmo3bDM1MXBkaw==
https://www.instagram.com/igor_shazhko?igsh=MXRjdDY1dW9zYzVvaw==
https://www.instagram.com/kaznacheeva_pro?igsh=MW02cmJibmcxN2I0Ng==
https://www.instagram.com/adamova_project?igsh=MWZmNWxrY2ZsOWs1eg==
https://www.instagram.com/artemtime?igsh=MWd1YzF4NWt4NGVkbQ==
https://www.instagram.com/kovaleva.ti?igsh=MTJ5aDM2ZmsyeDdkMg==
https://www.instagram.com/sergey_bukanov?igsh=azUyeDJiazMzdmpt
https://www.instagram.com/dmitry_beleshko?igsh=MXRpaDNycmhwdHI1cg==
https://www.instagram.com/ira_chelysheva?igsh=MXE0MXlzYmt3ZXBleg==
https://www.instagram.com/egoza_zhe?igsh=a3lwcm1oNjY0eXVr
https://www.instagram.com/pogodina_expert?igsh=MTIzbHVpemxuZmhmNg==
https://www.instagram.com/marina_book?igsh=MWQxemVlczB2c3Y1bQ==
https://www.instagram.com/kidimova?igsh=MXh0OWwybW9wMWR1Ng==
https://www.instagram.com/eleonora_marketing?igsh=MTUxc2w2dWwwYzdweg==
https://www.instagram.com/iznutri.agency?igsh=MXFhMTV5b3ZtMHl2cA==
https://www.instagram.com/koshelkova.angelina?igsh=dnhtd3R2MmhxOW9o
https://www.instagram.com/julia_rodochinskaya?igsh=MTBydGdza3pmNnI5Zg==
https://www.instagram.com/convert_monster?igsh=ODRuNmxwdXZoeGpr
https://www.instagram.com/ayazhan.sarsenova?igsh=MWN3ZmtiYm9ybHpqZw==
https://www.instagram.com/ban4ukov?igsh=d2IwbHBveTd4ZmNt
https://www.instagram.com/vadim.sorokin?igsh=ZWhmdmxxcnF0MnFj
https://www.instagram.com/nagyz_abzhanov?igsh=ejF2cnNxOGJvazI3
https://www.instagram.com/businesspro.inc?igsh=NWZhYzR3djVremNq
https://www.instagram.com/vadimkompaniiets?igsh=MWZtczN6ZnBqY2xsYg==
https://www.instagram.com/ilia.paliy?igsh=Z2xzZDY0aW9zYTJs
https://www.instagram.com/metlitsky_content?igsh=MWx6OHA5dWt0YmJpMg==
https://www.instagram.com/minimasneva?igsh=cmpmM2l3ODV5a2lk
https://www.instagram.com/lera_rumaa?igsh=bWhjNmRrdHd3bHJ5
https://www.instagram.com/vladidas?igsh=amhpbzNmcGM0N295
https://www.instagram.com/tvoy_shanks?igsh=Z2hscjhmcWsxZDll
https://www.instagram.com/trushina?igsh=MTV6YjU0MHo4OG9pbA==
https://www.instagram.com/tot_samy_sulimov?igsh=MXR3ZWNwaWtqY3ozMw==
https://www.instagram.com/topbizidei?igsh=YnBnbnh4bG90anM2
https://www.instagram.com/timergaleevaofficial?igsh=eWgyN2JjY2d5dnoy
https://www.instagram.com/temki.est?igsh=Z3FnaDl3dXJiZjRr
https://www.instagram.com/tatiana.bratsun?igsh=MWVqenRjeGNybDE4cA==
https://www.instagram.com/sidorenko_pro?igsh=MWttbzl3Z3hnbGljYQ==
https://www.instagram.com/shayekin_ruslan?igsh=MTM3aWVlN25pNXpjeA==
https://www.instagram.com/sharipov_islambek?igsh=N3gzOHYyN2Vlb2J3
https://www.instagram.com/samitovm?igsh=ZmVsNG84OTgyaDlz
https://www.instagram.com/sabina_sanber?igsh=a3Y4Y3ZpanNlbWt1
https://www.instagram.com/rudakovap?igsh=ZjVobnRjcjJnYmEx
https://www.instagram.com/profbalance?igsh=OWFwNjFmZzV2b2Rz
https://www.instagram.com/polyanskayaa?igsh=bzZrMzc3bmMyMmJt
https://www.instagram.com/nastya_startnow?igsh=MThjMnRleXJ4czczeA==
https://www.instagram.com/nurs_mag?igsh=cGx4cm9iNnkxMzZ2
https://www.instagram.com/nastya.acsy?igsh=azZsN3VtcThqYTIy
https://www.instagram.com/maxchir?igsh=OWp6MzR3N3p1a2p6
https://www.instagram.com/maakooveev?igsh=MTNhYnhrdXQ3MGl4Zg==
https://www.instagram.com/lina_gorbatenko?igsh=MWRtaTU5MXNsZjlpbQ==
https://www.instagram.com/lauravaigorova?igsh=MTltanZ6d2E0bnl2cg==
https://www.instagram.com/kyrbangaliev?igsh=MnVlcWNtN29qYWlq
https://www.instagram.com/kotov.evgen?igsh=bHhpYWd0M2lxNDAx
https://www.instagram.com/kate_lustenko?igsh=MW5yNDh5ejE1YmplaQ==
https://www.instagram.com/igor_stoyanov?igsh=MTltNzE4Y2prem4xcw==
https://www.instagram.com/facelessformula.ai?igsh=dW5qMHJyajZ2bG5o
https://www.instagram.com/evgeny_a_frolov?igsh=MWl1b3VyZmg3ZjE0Nw==
https://www.instagram.com/evgeniy_svesh?igsh=MTgwemsxcWZpY2Y2Yw==
https://www.instagram.com/emil.corp?igsh=ZjlpOGdjOHd6N2d6
https://www.instagram.com/e.v.rakhimov?igsh=MW53cWtzeTRqYnlleA==
https://www.instagram.com/artem__gura?igsh=MXZ2MjZwdjJjcHB1dA==
https://www.instagram.com/asadulla?igsh=MTBrYWdnZDYxZXg5MA==
https://www.instagram.com/antonthegod?igsh=cWh2cTE4bG1jczBx
https://www.instagram.com/alina_telling?igsh=bjY0eDd6ZnZ6bGh3
https://www.instagram.com/allo.viktory?igsh=MWc2cXpkZnFqcXYxdQ==
https://www.instagram.com/neprostomaksim?igsh=MWptNDZuZzdwMnk4Mg==
https://www.instagram.com/aza_ai_expert?igsh=MTAyaWRhczMxNjQ1MQ==
https://www.instagram.com/romankumarvias?igsh=MXRzNjBnZDJuMWljNw==
https://www.instagram.com/wealthrevolution.in?igsh=bWRzMW9lemM0OWZ3
https://www.instagram.com/vusithembekwayo?igsh=MWFhZDA3bWtiN255aA==
https://www.instagram.com/visionary.voyage?igsh=anN2eTI4ZHF3c2Ey
https://www.instagram.com/tonyrobbins?igsh=YWJlMzRvNHYwY2hi
https://www.instagram.com/timarmoo?igsh=dDE1ZXJjZm0yZnZh
https://www.instagram.com/thirdnetwork?igsh=MTFpdzgwdHRydGRtbw==
https://www.instagram.com/theyounetworkhq?igsh=aXh2OHZ2dTNjbGR6
https://www.instagram.com/thestartupshow.in?igsh=NGdsejFwNWozMXF1
https://www.instagram.com/theschoolofhardknockz?igsh=MXJsdmVib3k4cjl0cQ==
https://www.instagram.com/thelazyceo?igsh=aG1tYml1dDk5eGU4
https://www.instagram.com/the_propertyboss?igsh=Z3lrcmFsazU4dGNr
https://www.instagram.com/stevenguo.io?igsh=Z3JxM3ZhNDN1czE2
https://www.instagram.com/startupbell?igsh=emVhOGhrdDR6eDVw
https://www.instagram.com/starter_story?igsh=Z3JiOHM2YWs5MjRh
https://www.instagram.com/skillspowers?igsh=MWNzamxjNDQ1d3IzbA==
https://www.instagram.com/simonsquibb?igsh=b3BrZnh0OWM0N3Z2
https://www.instagram.com/simonsinek?igsh=MXZ1d2d3YmhwM2pkbA==
https://www.instagram.com/shashank_udupa?igsh=MWszOXZoaDljdnZtag==
https://www.instagram.com/santwinder_singh_waraich?igsh=MWdzcm9mOHY4MHBkbA==
https://www.instagram.com/run.startup?igsh=MXhiMmY2ZTgyemhxaw==
https://www.instagram.com/profit?igsh=bm9lc2l1dGI4YWN3
https://www.instagram.com/profgalloway?igsh=MTMxd3ZpbHZtNGlzcQ==
https://www.instagram.com/pashamoga?igsh=aXpsbTZkeDBlYWs5
https://www.instagram.com/momikereel?igsh=MTZydm9qOXp4ZnptMQ==
https://www.instagram.com/millionairessence?igsh=Y2Q1Y2NmbHB3NXYw
https://www.instagram.com/mattyr_ecom?igsh=MWg4cGw1Y2Nkc2JseQ==
https://www.instagram.com/marketing.psychology?igsh=Z2RxbWVxOTZ2dTk0
https://www.instagram.com/the.marketing.maestro?igsh=MXJ1YXZtaTF5cXd2OQ==
https://www.instagram.com/marketing.growmatics?igsh=Y3dmN2VsNnU2bnQ2
https://www.instagram.com/maria.wendt?igsh=d2FyNHhzaXc5OWE5
https://www.instagram.com/chasingfreedomwithjuls?igsh=bXMxZjhsMnY4eGJn
https://www.instagram.com/makeithappen?igsh=MTR3aHFubmhtdGczMw==
https://www.instagram.com/leilahormozi?igsh=MXR5ZHVsZ2d5cW5nNQ==
https://www.instagram.com/jun_yuh?igsh=MWozbjlvem55NjlmOA==
https://www.instagram.com/joshuagilesfirebrand?igsh=MW5iZjk0NHAxejlpOA==
https://www.instagram.com/investmentjoy?igsh=MXZib2gxdGhzZWh1OQ==
https://www.instagram.com/howtobeentrepreneur?igsh=MWZsZm92NzNraDRwcw==
https://www.instagram.com/sweatystartup?igsh=MWYyMmczMnZodms5Zw=='''

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