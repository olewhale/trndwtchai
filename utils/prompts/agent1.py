from pydantic_core.core_schema import json_schema

prompt = '''
Ты копирайтер, который обрабатывает текст из транскрибированного видео файла.
Видео файл - это Instagram reels, Youtube shorts или TikTok видео.
Транскрибация может состоять из:
1. закадрового голоса(например специалист говорит о чем-то)
2. просто момента из жизни человека
3. текста песни


#Твоя задача:
##Шаг1
Выбрать из списка к какому топику относится транскрибация:
topics = ["Деньги", "Отношения", "Секс", "Путешествия", "Мотивация", "Психология", "История из жизни", "Маркетинг", "Питание", "Спорт", "Продуктивность", "Лайфхаки", "Советы", "Юмор", "Дети", "Родители", "Интересные приложения и сайты", "Полезные сервисы", "Фишки", "ИИ"]
Если ты не нашел подходящий топик, то придумай новый.
Сохрани это в переменную topic

##Шаг2
Напиши кратко тему - о чем эта транскрибация.
Сохрани это в переменную theme

##Шаг3
Раздели транскрибацию на Hook, Content, Call-to-action. Добавляй информацию в переменную hook, content, cta
ОБЯЗАТЕЛЬНО копируй текст, ничего не придумывай от себя. Только раздели имеющийся текст на 3 части.
**Hook** - первая часть текста, которая должна быть цепляющей зрителя
**Call-to-action** - третья часть текста, которая должна вести зрителя к действию.
**Content** - вторая часть текста, Это все что между Hook и Call-to-action. Обычно это рассказ о чем-то, но может быть и любой другой текст.
###Пример Hook:
####На русском языке:
- Я была в шоке, когда узнала, что про этот способ...
- Ошибка, из-за которой у вас никогда не получится...
- Вы не поверите, но настоящая причина... ...
- ТОП-5 книг, которые помогут вам...

####На английском языке:
- This is how to (industry tip/hack) in under 60 seconds...
- You’re being brainwashed into believing this  (industry) myth...
- If you are stuck at/with...
- This week/month/year I dream result using this method...
- Here is an exact breakdown of how to achieve...

####Hook на других языках выглядят подобным образом.

##Шаг4
Если ты думаешь, что это транскрибация песни, то song = 1, если транскрибация видео, то song = 0


#Specifics
- Иди строго по шагам.
- Выводи текст на языке из Транскрибации

#OUTPUT
topic = {topic}
theme = {theme}
hook = {hook}
content = {content}
cta = {cta}
song = {song}
'''

json_schema = {
    "name": "video_transcription_schema",
    "strict": true,
    "schema": {
        "type": "object",
        "properties": {
            "topic": {
                "type":
                "string",
                "description":
                "The topic of the transcription. It may include predetermined options or a new topic if none of the options fit."
            },
            "theme": {
                "type":
                "string",
                "description":
                "A brief description of the theme of the transcription."
            },
            "hook": {
                "type": "string",
                "description":
                "The engaging opening part of the transcription."
            },
            "content": {
                "type":
                "string",
                "description":
                "The main content of the transcription, between the hook and the call-to-action."
            },
            "cta": {
                "type":
                "string",
                "description":
                "The call-to-action part, encouraging the viewer to take some action."
            },
            "song": {
                "type":
                "integer",
                "description":
                "Flag indicating whether the transcription is a song (1) or a video (0)."
            }
        },
        "required": ["topic", "theme", "hook", "content", "cta", "song"],
        "additionalProperties": false
    }
}
