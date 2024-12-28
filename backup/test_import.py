#from utils.ggl import append_data_to_google_sheet
import utils.ggl as ggl
import json

print(dir(ggl))

json_r = [{
    'account_url': 'https://www.instagram.com/hamza_automates',
    'username': 'hamza_automates',
    'url': 'https://www.instagram.com/p/DAcMa4eRx-5/',
    'timestamp': '2024-09-28 00:24:23',
    'videoUrl':
    'https://scontent-ord5-2.cdninstagram.com/o1/v/t16/f1/m86/8645A235DBC9DBEE5FCB806B0A8C819C_video_dashinit.mp4?stp=dst-mp4&efg=eyJxZV9ncm91cHMiOiJbXCJpZ193ZWJfZGVsaXZlcnlfdnRzX290ZlwiXSIsInZlbmNvZGVfdGFnIjoidnRzX3ZvZF91cmxnZW4uY2xpcHMuYzIuNzIwLmJhc2VsaW5lIn0&_nc_cat=105&vs=894782448761332_270924382&_nc_vs=HBksFQIYUmlnX3hwdl9yZWVsc19wZXJtYW5lbnRfc3JfcHJvZC84NjQ1QTIzNURCQzlEQkVFNUZDQjgwNkIwQThDODE5Q192aWRlb19kYXNoaW5pdC5tcDQVAALIAQAVAhg6cGFzc3Rocm91Z2hfZXZlcnN0b3JlL0dLVERlUnZBWDFqdFAyNGZBRXNkaWMtb0FVY2JicV9FQUFBRhUCAsgBACgAGAAbABUAACaGi%2FrE1cS5PxUCKAJDMywXQFLIgxJul40YEmRhc2hfYmFzZWxpbmVfMV92MREAdf4HAA%3D%3D&_nc_rid=1265e6fb17&ccb=9-4&oh=00_AYCnkh9129VsGStZvbBfI-nG6495E5iMikgcADMvmJ3tVA&oe=67063F21&_nc_sid=10d13b',
    'shortCode': 'DAcMa4eRx-5',
    'caption':
    'Completely Automate LinkedIn #automation #automate #linkedin #software #saas #agency #make #workflow #agency #hamzabaig #highlevel #gohighlevel #code #programmer #ai #openai #chatgpt #makemoneyonline #sidehustle #fyp #smma',
    'commentsCount': 371,
    'likesCount': 647,
    'videoPlayCount': 23557,
    'videoDuration': 75.21,
    'engagement': '0.0432143312',
    'transcription':
    " These five circles have the power to generate you $500 every single month and the reason is that because they're actually a social media automation. It uses AI to generate LinkedIn posts 24-7 on autopilot for all of your clients. And it's also one that I've personally built and sold. So it starts off by watching blog articles for any recent updates about their industry and it sends that information to chat GPT. This GPT assistant specifically is trained to be a fantastic social media manager and comes up with the best copy. We then send that output content to Dali which is open AI's image generation model and create a content image for our post. We then extract that image using the HTTP function and then we send them both to LinkedIn that we create an organization image post using both the content and the image that we generate and we can schedule it to be posted. This can happen multiple times a day 24-7 all year round for your clients. And this is just one example of hundreds of different automations that you can build and sell to local businesses near you. Now if you want to access to this automation then comment the word content in the comment section below. But if you want to learn exactly how you can start building automations like this in general for any kind of local business and you want to get started with this as a business model because you know that this is the future. Then head over to my profile, click the link in my bio to apply to my automation incubator. It's a 100% free resource where I teach you exactly how to get started with automations and build them from scratch. We just passed 14,000 members making us the fastest scoring and biggest automation community on planet Earth. So I hope to see you inside.",
    'category': 'Бизнес и технологии',
    'topic':
    'Как создание автоматизаций с использованием ИИ может приносить ежемесячный доход и быть продано местным предприятиям',
    'translatedCaption':
    'Задумывались над тем, как превратить ваши видео в увлекательные контентные части?\\n\\nВот мой процесс:\\n\\n👉🏼Запишите обучающее видео длительностью 10 минут.\\n\\n👉🏼Используйте автоматизацию, чтобы преобразовать его в подробный блог-пост.\\n\\n👉🏼Воспользуйтесь AI для генерации заголовков и подписей для карусели.\\n\\n👉🏼Загрузите всё в Airtable.\\n\\n👉🏼Запланируйте и опубликуйте на нескольких платформах.\\n\\nВсё это так просто! Пусть автоматизация и AI выполняют тяжелую работу, пока вы сосредоточены на создании более ценного контента.\\n\\n~ Q\\n\\n#taskautomation',
    'original': {
        'hook':
        "These five circles have the power to generate you $500 every single month and the reason is that because they're actually a social media automation.",
        'content':
        "It uses AI to generate LinkedIn posts 24-7 on autopilot for all of your clients. And it's also one that I've personally built and sold. So it starts off by watching blog articles for any recent updates about their industry and it sends that information to chat GPT. This GPT assistant specifically is trained to be a fantastic social media manager and comes up with the best copy. We then send that output content to Dali which is open AI's image generation model and create a content image for our post. We then extract that image using the HTTP function and then we send them both to LinkedIn that we create an organization image post using both the content and the image that we generate and we can schedule it to be posted. This can happen multiple times a day 24-7 all year round for your clients.",
        'call_to_action':
        "Now if you want to access to this automation then comment the word content in the comment section below. But if you want to learn exactly how you can start building automations like this in general for any kind of local business and you want to get started with this as a business model because you know that this is the future. Then head over to my profile, click the link in my bio to apply to my automation incubator. It's a 100% free resource where I teach you exactly how to get started with automations and build them from scratch. We just passed 14,000 members making us the fastest scoring and biggest automation community on planet Earth."
    },
    'adapted': {
        'hook':
        "These five circles have the power to generate you $500 every single month and the reason is that because they're actually a social media automation.\n1. Эти пять кругов могут приносить вам $500 каждый месяц благодаря социальной медиа автоматизации.\n2. Узнайте, как 5 простых кругов могут обеспечивать ваш постоянный доход в $500 ежемесячно благодаря автоматизации соцсетей.\n3. Откройте секрет социально-медийной автоматизации, которая может генерировать $500 в месяц с помощью пяти шагов.",
        'content':
        'Мы предлагаем высокоэффективные решения для автоматизации социальных сетей, которые круглосуточно создают посты для LinkedIn с помощью ИИ. Эта система, созданная и опробованная мной, начинает с анализа блогов на предмет новых индустриальных обновлений, отправляет нужную информацию в chat GPT для создания лучшего контента, а затем использует Dali для генерации соответствующих изображений. Затем контент и изображение интегрируются и публикуются в LinkedIn, создавая актуальные организационные посты. Эта автоматизация ученика нацелена на бизнесы, стремящиеся быть на шаг впереди, и может быть адаптирована для индивидуальных нужд ваших клиентов.',
        'call_to_action':
        'Если вы хотите получить доступ к этой автоматизации, пишите "контент" в комментариях. Желаете узнать, как можно начинать создавать такие автоматизации для местного бизнеса и запустить это как бизнес-модель? Переходите в мой профиль, чтобы подать заявку в наш "инкубатор автоматизации" — бесплатный ресурс, обучающий всему процессу создания автоматизаций с нуля. Мы уже превысили отметку в 14,000 участников, становясь самой быстрорастущей и масштабной автоматизационной общиной на планете. Жду вас внутри!'
    }
}]
# Тестовый вызов функции
#json_results = json.dumps(json_r, indent=4)
ggl.append_data_to_google_sheet(json_r)
