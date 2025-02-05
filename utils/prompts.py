import os
from pydantic import BaseModel, Field
from typing import List
from openai import OpenAI
import json
from dotenv import load_dotenv

# Загружаем переменные из .env
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)


class OriginalData(BaseModel):
  hook: str
  content: str
  call_to_action: str


class AdaptedData(BaseModel):
  hook: str = Field(
      ...,
      description=
      "Should be a multi-line string with 5 hooks separated by newlines")
  content: str
  call_to_action: str


class TransformData(BaseModel):
  category: str
  topic: str
  translatedCaption: str = Field(...,
                                 description="This is a translated caption")
  original: OriginalData
  adapted: AdaptedData

class OriginalScript(BaseModel):
  hook: str = Field(
    ..., description="An engaging opening statement text that captures the viewer's attention with the most catchy and meaningful load. Consists of more than 3 words. Example: 'I should be charging for what I am about to tell you!', 'Heres how to get your (desired result) in X steps'. If you see that some words may not have the right meaning, please correct them. This text is from an audio transcription and it may not have accurately transcribed the audio into text."
  )
  content: str = Field(
    ...,
    description=
    "The main content or narrative of the transcription. It should make sense. If you see that some words may not have the right meaning, please correct them. This text is from an audio transcription and it may not have accurately transcribed the audio into text."
  )
  cta: str = Field(
    ...,
    description=
    "A call to action for the audience. Example:'Follow for more (industry) education!','DM me for the link', 'Comment WORD and I send you the link'. It should make sense. If you see that some words may not have the right meaning, please correct them. This text is from an audio transcription and it may not have accurately transcribed the audio into text.")
  song: int = Field(
    ...,
    description=
    "Flag indicating whether the transcription is a song (1) or a not a song (0)."
  )
  humor: int = Field(
    ...,
    description=
    "Flag indicating whether the transcription have a humor (1) or does't have a humor (0)."
  )

class CommonInfo(BaseModel):
  topic: str = Field(
      ...,
      description=
      "The topic of the transcription. It may include predetermined options or a new topic if none of the options fit."
  )
  theme: str = Field(
      ...,
      description="A brief description of the theme of the transcription.")


class RewritedScript(BaseModel):
  hook: str = Field(
      ...,
      description=
      "A list of hooks generated for the video based on the transcription. Must be like 1. hook1\n2. hook2\n3. hook3\n4. hook4\n5. hook5")
  content: str = Field(...,
                       description="The translated content from the original.")
  cta: str = Field(
      ...,
      description="A list of call-to-action phrases generated for the video. Must be like 1. cta1\n2. ctak2\n3. ctak3")
  caption: str = Field(...,
                       description="The translated caption from the original.")



def spez_common_script(post_text, caption):

  system_role = '''
#ROLE
Ты копирайтер, который обрабатывает текст из транскрибированного видео файла.
Видео файл - это Instagram reels, Youtube shorts или TikTok видео.
Транскрибация может состоять из:
1. закадрового голоса(например специалист говорит о чем-то)
2. просто момента из жизни человека
3. текста песни
и тд
  '''

  spez_original_instruction = f'''
#TASK
Классифицируй и опиши тему текста transcription(транскрипция может быть несовсем точно транскрибирована) и caption из видео файла(Instagram reels, tik tok or Youtube shorts), следуя структурированным шагам.

# Steps

## Шаг 0
- Определи язык из `INPUT` и сохрани его в переменную `language_original`.

## Шаг 1
- Определи, к какому топику из списка topics относится транскрипция. Если подходящего топика нет, придумай новый.
  Строка должна быть на `language_original` языке.
  ```
  topics = ["Деньги", "Отношения", "Секс", "Путешествия", "Мотивация", "Психология", "История из жизни", "Маркетинг", "Питание", "Спорт", "Продуктивность", "Лайфхаки", "Советы", "Юмор", "Дети", "Родители", "Интересные приложения и сайты", "Полезные сервисы", "Фишки", "ИИ", "Автоматизация бизнеса", "Материнство", "Туризм", "Здоровье", "Медицина"]
  ```

## Шаг 2
- Напиши кратко тему транскрипции и сохрани это в переменной `theme` на `language_original` языке.
  '''
  #topics = ["Деньги", "Отношения", "Секс", "Путешествия", "Мотивация", "Психология", "История из жизни", "Маркетинг", "Питание", "Спорт", "Продуктивность", "Лайфхаки", "Советы", "Юмор", "Дети", "Родители", "Интересные приложения и сайты", "Полезные сервисы", "Фишки", "ИИ", "Автоматизация бизнеса", "Материнство", "Туризм", "Здоровье", "Медицина"]
  #topics = ["Money", "Relationships", "Sex", "Travel", "Motivation", "Psychology", "Life story", "Marketing", "Nutrition", "Sports", "Productivity", "Life hacks", "Tips", "Humor", "Children", "Parents", "Interesting apps and websites", "Useful services", "Tricks", "AI", "Business automation", "Motherhood", "Tourism", "Health", "Medicine"]

  
  try:
    completion = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[{
            "role":
            "system",
            "content":
            f'''
            caption =
            {system_role}

            {spez_original_instruction}
          '''
        }, {
            "role":
            "user",
            "content":
            f'''
#INPUT:
##If you see that some words may not have the right meaning in transcription variable, please correct them. This text is from an audio transcription and it may not have accurately transcribed the audio into text.
transcription = "{post_text}"
caption = "{caption}"
            '''
        }],
        temperature=0,
        max_tokens=5000,
        response_format=CommonInfo)
    #research_paper = completion.choices[0].message.parsed

    #print(research_paper)

    commonData = completion.choices[0].message.parsed
    #originalData_json = originalData.model_dump_json() if originalData else {}
    #print(research_paper_json)

    # Проверяем значение атрибута song напрямую
    #if originalData.song == 1:
    #  return {'song_text': 'Возможно, это песня'}

    # Преобразуем объект модели в JSON-словарь
    return commonData.dict()

  except Exception as e:
    print(f"Ошибка: {e}")
    return {"error": "Ошибка при вызове OpenAI API"}

def spez_original_script(post_text):

  system_role = '''
#ROLE
Ты копирайтер, который обрабатывает текст из транскрибированного видео файла.
Видео файл - это Instagram reels, Youtube shorts или TikTok видео.
Транскрибация может состоять из:
1. закадрового голоса(например специалист говорит о чем-то)
2. просто момента из жизни человека
3. текста песни
4. ...
  '''

  spez_original_instruction = f'''
#TASK
Определи, классифицируй и оцени текстовую транскрипцию из видео файла(Instagram reels, tiktok or Youtube shorts), следуя структурированным шагам.

# Steps

## Шаг 1
- Определи язык из `INPUT` и сохрани его в переменную `language_original`.

## Шаг 2
- Если  содержит полноценный сценарий для видео или текст закадрового голоса, раздели текст на части: `hook`, `content`, `cta`.
  - `hook`- Первая часть текста с самой цепляющей и смысловой нагрузкой. Состоит более чем из 5 слов. Начинается с самого первого слова переменной transcription. 
  - `content`- Вторая часть текста с смысловой нагрузкой или рассказом. Состоит более чем из 5 слов.
  - `cta` - Текст, призывающий к действию, если он есть и имеет смысловую нагрузку. Состоит более чем из 5 слов.
- Если текст малоинформативен или короткий (1-3 слов) или просто описывает звуки, используй: `hook = "-"`, `content = "-"`, `cta = "-"`. 

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

###Пример-Call-to-action:
- Напиши слово "Яблоко" и я отправлю тебе...
- Переходи ко мне в профиль...
- Пиши комментарий/Ставь лайк...
- Перешли этот рилс своему другу...

## Шаг 3
- БЕРЕМ ИНФОРМАЦИЮ ИЗ TRANSCRIPTION
- Если это транскрипция песни: `song = 1`.
- Если это не транскрипция песни: `song = 0`.

## Шаг 4
- БЕРЕМ ИНФОРМАЦИЮ ИЗ TRANSCRIPTION
- Если это видео содержит юмор\шутки\мем: `humor = 1`.
- Если это видео несодержит юмор\шутки\мем: `humor = 0`.

# Output Format
Вывод должен содержать переменные: `hook`, `content`, `cta`, `song`, `humor`.

# Notes

- СТРОГО иди по шагам.
- Все шаги осуществляются на `language_original` языке, шаг 3 также на этом языке.
- ВАЖНО! Ты обязан определить весь текст из INPUT в `hook`, `content`, `cta`!
  '''

  try:
    completion = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[{
            "role":
            "system",
            "content":
            f'''
            caption =
            {system_role}

            {spez_original_instruction}
          '''
        }, {
            "role":
            "user",
            "content":
            f'''
#INPUT:
transcription = "{post_text}"
            '''
        }],
        temperature=0,
        max_tokens=15000,
        response_format=OriginalScript)
    #research_paper = completion.choices[0].message.parsed

    #print(research_paper)

    originalData = completion.choices[0].message.parsed
    #originalData_json = originalData.model_dump_json() if originalData else {}
    #print(research_paper_json)

    # Проверяем значение атрибута song напрямую
    #if originalData.song == 1:
    #  return {'song_text': 'Возможно, это песня'}

    # Преобразуем объект модели в JSON-словарь
    return originalData.dict()

  except Exception as e:
    print(f"Ошибка: {e}")
    return {"error": "Ошибка при вызове OpenAI API"}


def spez_rewriter_script(original, caption, language):

  system_role = '''
#ROLE
Ты опытный копирайтер, который обрабатывает текст из транскрибированного видео файла разделенный на hook_original, content_original и call-to-action_original.
Видео файл - это Instagram reels, Youtube shorts или TikTok видео.
Транскрибация может состоять из:
1. закадрового голоса(например специалист говорит о чем-то)
2. просто момента из жизни человека
3. текста песни
и тд
  '''

  spez_rewriter_instruction = f'''
#TASK
#Твоя задача:
##Шаг1
Придумай 5 хук для этого видео на основе TRANSCRIPTION(hook_original, content_original и call-to-action_original) и примеров вирусных Hook. Обязательно вывести все 5 придуманных хуков. Если hook_original = "-", то hook1 = '-'.
  1. hook1: Переведи hook_original на {language} язык. Если его нет, ставим "-". Если hook_original уже на {language} языке, то оставляем его на {language} языке.
  2. hook2: Придумай на основе примеров лучших хуков из раздела "Примеры лучших хуков на русском" и смысла TRANSCRIPTION. Выбери подходящий. На {language} язык. 
  3. hook3: Придумай на основе примеров лучших хуков из раздела "Примеры лучших хуков на русском" и смысла TRANSCRIPTION. Выбери подходящий. На {language} язык. 
  4. hook4: Придумай на основе примеров лучших хуков из раздела "Примеры лучших хуков на русском" и смысла TRANSCRIPTION. Выбери подходящий. На {language} язык. 
  5. hook5: Придумай на основе примеров лучших хуков из раздела "Примеры лучших хуков на русском" и смысла TRANSCRIPTION. Выбери подходящий. На {language} язык. 


###Примеры лучших хуков на русском:
#### Категория: Ошибки и неправильные действия
1. 3 действия, которые делать категорически нельзя, если вы хотите...
2. Вы 100% делаете эти ошибки, когда...
3. Ошибка, из-за которой у вас никогда не получится...
4. Всё это время вы делали... неправильно
5. Осторожно! Этими действиями вы можете сильно навредить своему...
6. Неочевидные вещи, которые мешают вам...
7. Вы никогда не сможете..., если...
8. Как вы вредите своему... всего одним простым действием
9. Ты никогда не станешь [кем-то], если не поймёшь это.
10. Ты никогда в жизни не станешь хорошим [блогером], если не сделаешь это.

#### Категория: Неожиданные и шокирующие факты
1. Вы не поверите, но настоящая причина... это...
2. Вы 100% никогда не думали об... с этой стороны
3. Я была в шоке, когда узнала, что про этот способ... почти никто не знает
4. Это, наверное, самое странное, что вы услышите о..., но я обязан это сказать
5. Вам обманывают, когда говорят, что...

#### Категория: Причины и последствия
1. Вот почему... не работает
2. Всё это время вы делали... неправильно
3. 5 ужасных последствий..., которые напрочь отобьют у вас желание...
4. Сейчас я назову причину, почему у вас не получается...

#### Категория: Лайфхаки и советы
1. Как...? Вы точно не знали про этот лайфхак
2. Вам должно быть стыдно, если вы занимаетесь... и не знаете про...
3. Делюсь малоизвестной фишкой, как можно...
4. Я обязана поделиться с вами этим проверенным лайфхаком, как...
5. Проверенный способ..., даже если...
6. Если вы уже замучились..., то... есть один лайфхак, как...

#### Категория: Шаги и инструкции
1. Алгоритм действий на случай, если вы...
2. Пошаговая инструкция, как...
3. Проверенная схема, как...
4. Просто действуйте по этой инструкции и...
5. Сейчас покажу, как можно...

#### Категория: Привычки и ежедневные действия
1. Делайте эти действия, и вы заметите, как...
2. 5 ежедневных привычек, которые помогли мне...
3. Благодаря этой простой привычке вы...
4. Вы навсегда забудете про..., если начнёте...
5. Вот три упражнения, которые ты должен включить в свою тренировку, если ты новичок.

#### Категория: Преимущества и возможности
1. 5 убедительных причин заняться...
2. ТОП-5 книг, которые помогут вам...
3. Эти книги изменят вашу жизнь...
4. Вы больше никогда не захотите... после этой информации

#### Категория: Вопросы и интрига
1. А вы уже слышали, что...?
2. Что делать, если...?
3. Сколько нужно..., чтобы...?

##Шаг2
  Не копируй, а перепиши content_original на {language} язык. Важно оставить все смыслы и объем текста. Если content_original = "-", то content = '-'
  
##Шаг3
  Напиши 3 call-to-action(cta) на {language} язык.
  1. cta1: Просто переведи call-to-action_original на {language} язык. Если call-to-action_original = '-', то придумай на основе примеров лучших cta, используя {language} язык.
  2. cta2: придумай на основе следующего примера - "Пиши коммент «(слово по тематике)» и я отправлю (написать, что отправим(обычно какой-то лид-магнит))!" но на {language} язык.
  3. cta3: придумай на основе примеров лучших cta но на {language} язык.

###Примеры лучших call-to-action:
  1. Подпишись, чтобы узнать больше о (сфера)!
  2. Хочешь узнать больше о (продукт/услуга)? Переходи по ссылке в моем профиле.
  3. Сохрани этот пост, чтобы не забыть!
  4. Подпишись, чтобы знать больше о (сфера)!
  5. Пиши коммент «(слово по тематике)» и я отправлю (написать, что отправим(обычно какой-то лид-магнит))!
  6. Пиши коммент «(слово по тематике)» и я пришлю ссылку!
  7. Хочешь видеть больше такого контента? Обязательно подпишись!
  8. Хочешь такие же результаты? Напиши мне «X» для записи на индивидуальную консультацию!
  9. Поделись этим с лучшим другом/мамой/партнером по гольфу!
  10. Если полезно - подпишись. Я публикую такие материалы каждый день!
  11. Хочешь больше информации? Нажми на мое выделенное (название highlights)!
  12. Ссылка в профиле, переходи!
  13. Подробности в хайлтайтсах/шапке профиля! И не забудь подписаться!

##Шаг4
  caption_translated = Перевод caption_original на {language} язык
  Запрещается переводить хэштеги. Просто скопируй хэштеги

#Specifics
  - выполняй строго по шагам. Ничего не пропускай
  - Все пиши на {language} языке

#OUTPUT
  hook = [hook1, hook2, hook3, hook4, hook5]
  content = content_translated
  cta = [cta1, cta2, cta3]
  caption = caption_translated
  '''

  spez_rewriter_instruction_if_no_transcript = f'''
#TASK
#Твоя задача:
caption_translated = Переведи caption_original на {language} язык.
Запрещается переводить хэштеги. Просто скопируй хэштеги

#Specifics
  - Все пиши на {language} языке

#OUTPUT
  hook = '-'
  content = '-'
  cta = '-'
  caption = caption_translated
  '''

  if original == {}:
    spez_rewriter_instruction = spez_rewriter_instruction_if_no_transcript
  else:
    spez_rewriter_instruction = spez_rewriter_instruction

  try:
    completion = client.beta.chat.completions.parse(
        model="gpt-4o-2024-11-20",
        messages=[{
            "role":
            "system",
            "content":
            f'''
            caption =
            {system_role}

            {spez_rewriter_instruction}
          '''
        }, {
            "role":
            "user",
            "content":
            f'''
#INPUT:
Transcription = (
"hook_original" : "{original.get('hook')}",
"content_original" : "{original.get('content')}",
"call-to-action_original" : "{original.get('cta')}"
)

##CAPTION
caption = {caption}
            '''
        }],
        temperature=0.5,
        max_tokens=15000,
        response_format=RewritedScript)
    #research_paper = completion.choices[0].message.parsed

    #print(research_paper)

    rewritedData = completion.choices[0].message.parsed

    # Преобразуем объект модели в JSON-словарь
    return rewritedData.dict()

  except Exception as e:
    print(f"Ошибка: {e}")
    return {"error": "Ошибка при вызове OpenAI API"}


### TEST_ZONE
### TEST_ZONE
### TEST_ZONE

text_test = '''
Here's an automation that you can sell to a Chinese restaurant for $399 every single month and it's going to get them customers on autopilot while helping them with all of these things right here. It starts off when the customer scans a QR code on the table labeled signup for a free appetizer. The customer then fills out a form on a landing page asking for their personal information. It looks something like this. Now that was step one, but here's the value. It could be birthdays, weekly specials, holidays and promotional offers, events, but the bottom line is local restaurants need the power of direct marketing to speak directly to their customers. Now if you want access to a step by step tutorial on exactly how you can build this out for a local restaurant near you, then comment the word restaurant in the comment section below. If you want to learn how you can build automations in general for any kind of local business, then head over to my profile, click the link in my bio to apply to my automation incubator. We're currently the biggest automation community on planet earth and I'll see you inside
'''

caption_test = '''
Chinese Restaurants are entering the future #chinese #restaurant #automation #automate #saas #agency #build #workflow #smma #agency #highlevel #ghl #hamzabaig #reels #fyp #viral #learn
'''

#original = spez_original_script(text_test, caption_test)

original = {
    "topic": "Маркетинг",
    "theme":
    "Автоматизация для китайских ресторанов, которая помогает привлекать клиентов.",
    "hook":
    "Here's an automation that you can sell to a Chinese restaurant for $399 every single month...",
    "content":
    "It starts off when the customer scans a QR code on the table labeled signup for a free appetizer. The customer then fills out a form on a landing page asking for their personal information. It looks something like this. Now that was step one, but here's the value. It could be birthdays, weekly specials, holidays and promotional offers, events, but the bottom line is local restaurants need the power of direct marketing to speak directly to their customers.",
    "cta":
    "If you want access to a step by step tutorial on exactly how you can build this out for a local restaurant near you, then comment the word restaurant in the comment section below. If you want to learn how you can build automations in general for any kind of local business, then head over to my profile, click the link in my bio to apply to my automation incubator.",
    "song": 0
}

#print(original_text)
#rewriter = spez_rewriter_script(original, caption_test)

#print(json.dumps(original, ensure_ascii=False, indent=4))
#print(json.dumps(rewriter, ensure_ascii=False, indent=4))

### /TEST_ZONE
### /TEST_ZONE
### /TEST_ZONE