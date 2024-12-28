import time
from faster_whisper import WhisperModel
import os
import json
import subprocess
import datetime
import requests
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
import utils.apify as apify
import utils.prompts as gpt
import utils.ggl as ggl

print('SERVER STARTED')
#print(dir(ggl))
app = FastAPI()


class UserItem(BaseModel):
  username: str = Field(..., alias="0")
  reelsNumber: str = Field(..., alias="2")
  viewsFilter: str = Field(..., alias="3")


class UserData(BaseModel):
  users: list[UserItem]


class ReelLinksData(BaseModel):
  urls: list[str]


class ReelLinks(BaseModel):
  username: str
  links: str


# Функция для получения хоста (начала) URL
def extract_host_from_url(url):
  from urllib.parse import urlparse
  parsed_url = urlparse(url)
  return parsed_url.netloc  # Возвращаем только хост (например, instagram.fcgh7-1.fna.fbcdn.net)


def convert_video_to_audio(video_path):
  """Конвертация видео в аудиофайл (WAV) с использованием FFmpeg и извлечение длительности."""
  audio_path = video_path.replace(".mp4", ".wav")
  try:
    # Конвертация видео в аудио с помощью FFmpeg
    command = [
        "ffmpeg", "-i", video_path, "-ac", "1", "-ar", "16000", "-y",
        audio_path
    ]
    # Перенаправляем стандартный вывод и вывод ошибок в /dev/null (или в subprocess.PIPE для подавления)
    with open(os.devnull, 'w') as devnull:
      subprocess.run(command, check=True, stdout=devnull, stderr=devnull)
    print(f"Конвертация выполнена: {audio_path}")

    # Проверяем, что файл создан
    if os.path.exists(audio_path):
      print(f"Аудиофайл успешно создан: {audio_path}")
    else:
      print(f"Ошибка: Аудиофайл {audio_path} не найден!")
      return None  # Если файл не найден

    return audio_path
  except subprocess.CalledProcessError as e:
    print(f"Ошибка при конвертации {video_path}: {e}")
    return None


def transcribe_audio(audio_path, model):
  try:
    #transcribe(word_timestamps=True)
    #link to repo https://github.com/SYSTRAN/faster-whisper
    segments, info = model.transcribe(audio_path, language=None)
    transcription = ""
    for segment in segments:
      transcription += segment.text
    return transcription
  except Exception as e:
    print(f"Ошибка при транскрибации {audio_path}: {e}")
    return None


def process_reel(shortCode, transcript_data, model, output_filename):
  video_path = transcript_data[shortCode]["video_path"]
  audio_path = convert_video_to_audio(video_path)

  if audio_path:
    transcript_data[shortCode]["audio_path"] = audio_path
    transcription = transcribe_audio(audio_path, model)
    if transcription:
      transcript_data[shortCode]["transcription"] = transcription
    else:
      transcript_data[shortCode]["transcription"] = "Ошибка транскрибации"
  else:
    transcript_data[shortCode]["transcription"] = "Ошибка конвертации"

  save_partial_transcription(transcript_data, output_filename)

  # Удаление файлов после обработки
  if os.path.exists(video_path):
    os.remove(video_path)
  if os.path.exists(audio_path):
    os.remove(audio_path)

  return transcript_data[shortCode]


def save_partial_transcription(reel_data, save_path_transcript):
  try:
    output = {
        "processing_time_seconds":
        0,  # Время добавим позже
        "transcriptions": [{
            "shortCode":
            shortCode,
            "video_path":
            reel_data[shortCode]["video_path"],
            "audio_path":
            reel_data[shortCode]["audio_path"],
            "transcription":
            reel_data[shortCode]["transcription"]
        } for shortCode in reel_data]
    }

    with open(f'{save_path_transcript}', "w", encoding="utf-8") as json_file:
      json.dump(output, json_file, ensure_ascii=False, indent=4)
    print(f"Транскрипция сохранена")
  except Exception as e:
    print(f"Ошибка при сохранении JSON: {e}")


def insert_transcription(extracted_data, output_data):
  # Создаем словарь для быстрого поиска по shortCode
  transcription_dict = {
      t['shortCode']: t['transcription']
      for t in output_data['transcriptions']
  }

  # Обновляем extracted_data
  for item in extracted_data:
    shortCode = item.get('shortCode')
    if shortCode in transcription_dict:
      item['transcription'] = transcription_dict[shortCode]

  return extracted_data


# Подключаем папку static для статических файлов
app.mount("/static", StaticFiles(directory="static"), name="static")


# Маршрут для корневого запроса, который возвращает HTML файл
@app.get("/", response_class=HTMLResponse)
async def read_index():
  with open("static/index.html") as f:
    html_content = f.read()
  return HTMLResponse(content=html_content)


def process_data(account, days=1, links=[], scheme=0):
  start_time = time.time()
  print('process data started')

  if scheme == 0:
    users_data = ggl.get_table_data_as_json(account, 'DATA')

    if not users_data:
      print('No users')
      return

    reelsData = apify.instagram_user_scrapper(users_data, days=days)
    sorted_data, sortedReelsCount = apify.instagram_scrapper_filter_sorter(
        reelsData, users_data)

    if sortedReelsCount == 0:
      print('No new reels')
      return
  elif scheme == 1:
    account['username'] = account.get('username') + "_saves"
    #apify request
    reelsData = apify.instagram_reels_scrapper(links)
    sorted_data = reelsData
  '''
    ###TEST_ZONE Помогает использовать уже полученный json файл от apify. Не забудь убрать reelsData в комментинг
    ###TEST_ZONE
    with open("db/2/dr.chshtnv_apify_20241021_191953.json", "r", encoding="utf-8") as file:
        reelsData = json.load(file)
    ### /TEST_ZONE
    ### /TEST_ZONE
    '''
  # Генерируем имя файла только один раз
  now = datetime.datetime.now()
  date_time_str = now.strftime("%Y%m%d_%H%M%S")
  save_path = os.path.join('db', str(account['id']))
  os.makedirs(save_path, exist_ok=True)

  output_apify_filename = f"{account['username']}_apify_{date_time_str}.json"
  save_path_apify = os.path.join('db', str(account['id']),
                                 output_apify_filename)
  #Сохраняем apify данные в json файл
  with open(save_path_apify, "w", encoding="utf-8") as file:
    json.dump(reelsData, file, ensure_ascii=False, indent=4)

  extracted_data = apify.extracted_data_maker(sorted_data)

  deb = True
  if deb:
    print(json.dumps(extracted_data, ensure_ascii=False, indent=4))
    print("Done")
    return

  #return None
  transcript_data = download_reels(extracted_data)
  #model_size types - 'tiny', 'base', 'small', 'medium', 'large'
  model_size = "medium"
  model = WhisperModel(model_size, device="cpu", compute_type="int8")

  output_filename = f"{account['username']}_transcriptions_{date_time_str}.json"
  save_path_transcript = os.path.join('db', str(account['id']),
                                      output_filename)

  #Сохраняем пустой файл
  with open(save_path_transcript, "w", encoding="utf-8") as file:
    json.dump("", file, ensure_ascii=False, indent=4)

  for shortCode in transcript_data:
    try:
      transcript_data[shortCode] = process_reel(shortCode, transcript_data,
                                                model, save_path_transcript)
    except Exception as e:
      print(f"Ошибка при обработке {shortCode}: {e}")

  with open(save_path_transcript, "r", encoding="utf-8") as file:
    output_data = json.load(file)
  end_time = time.time()
  total_processing_time = end_time - start_time
  print(f"Общее время обработки: {total_processing_time:.2f} секунд")
  start_time = time.time()

  output_data["processing_time_seconds"] = total_processing_time

  # Удаляем поля video_path и audio_path из каждого элемента списка transcriptions
  for transcription in output_data["transcriptions"]:
    transcription.pop("video_path", None)
    transcription.pop("audio_path", None)

  with open(save_path_transcript, "w", encoding="utf-8") as file:
    json.dump(output_data, file, ensure_ascii=False, indent=4)

  results = insert_transcription(extracted_data, output_data)
  len_results = len(results)

  for index, item in enumerate(results, start=1):
    spez_common_answer = {}
    spez_original_answer = {}
    transcription = item.get('transcription')

    spez_common_answer = gpt.spez_common_script(transcription,
                                                item.get('caption'))
    item['topic'] = spez_common_answer.get('topic', '')
    item['theme'] = spez_common_answer.get('theme', '')

    print(f"--------- spez_original run for {index}/{len_results} ---------")
    #checking if the transcription is not empty
    if transcription != "Ошибка транскрибации":
      spez_original_answer = gpt.spez_original_script(transcription)

      print(json.dumps(spez_original_answer, ensure_ascii=False, indent=4))
      print("------------------")
      # Print gpt_answer type and value for debugging
      #print(f"gpt_answer type: {type(gpt_answer)}")
      #print(f"gpt_answer value: {gpt_answer}")
      try:
        #gpt_answer_dict = json.loads(str(gpt_answer))
        item['original_script'] = {}
        item['original_script']['hook'] = spez_original_answer.get('hook', '')
        item['original_script']['content'] = spez_original_answer.get(
            'content', '')
        item['original_script']['cta'] = spez_original_answer.get('cta', '')
        item['song'] = spez_original_answer.get('song', None)
        item['humor'] = spez_original_answer.get('humor', None)
      except json.JSONDecodeError:
        print("Error: String returned from spez_reelsmaker is not valid JSON")
        # Optionally handle the error, e.g., set defaults or skip
        continue
    else:
      try:
        item['original_script'] = {}
        item['original_script']['hook'] = '-'
        item['original_script']['content'] = '-'
        item['original_script']['cta'] = '-'
        item['song'] = 0
        item['humor'] = 0
      except json.JSONDecodeError:
        print("Error: String returned from spez_reelsmaker is not valid JSON")
        # Optionally handle the error, e.g., set defaults or skip
        continue
      print(f"No transcription found for item {item.get('shortCode')}")

  # Save JSON file with the specified naming convention
  result_filename = f"{account['username']}_result_{date_time_str}.json"
  save_path_result = os.path.join('db', str(account['id']), result_filename)

  os.makedirs(os.path.dirname(save_path_result), exist_ok=True)
  with open(save_path_result, "w", encoding="utf-8") as result_file:
    json.dump(results, result_file, ensure_ascii=False, indent=4)

  #Сюда надо добавить данные с второго агента
  for index, item in enumerate(results, start=1):
    spez_rewriter_answer = {}
    transcription = item.get('transcription')

    print(f"--------- spez_rewriter run for {index}/{len_results} ---------")
    #checking if the transcription is not empty
    if transcription != "Ошибка транскрибации":
      # Получаем уже сохранённые данные скрипта
      original_script = item.get('original_script', {})
      hook = original_script.get('hook', '')
      content = original_script.get('content', '')
      cta = original_script.get('cta', '')

      spez_rewriter_answer = gpt.spez_rewriter_script(
          {
              'hook': hook,
              'content': content,
              'cta': cta
          }, item.get('caption'))

      try:
        item['rewrited_script'] = {}
        item['rewrited_script']['hook'] = spez_rewriter_answer.get('hook', "-")
        item['rewrited_script']['content'] = spez_rewriter_answer.get(
            'content', "-")
        item['rewrited_script']['cta'] = spez_rewriter_answer.get('cta', "-")
        item['rewrited_script']['caption'] = spez_rewriter_answer.get(
            'caption', '')
      except json.JSONDecodeError:
        print("Error: String returned from spez_reelsmaker is not valid JSON")
        # Optionally handle the error, e.g., set defaults or skip
        continue
    else:
      spez_rewriter_answer = gpt.spez_rewriter_script({}, item.get('caption'))

      try:
        item['rewrited_script'] = {}
        item['rewrited_script']['hook'] = "-"
        item['rewrited_script']['content'] = "-"
        item['rewrited_script']['cta'] = "-"
        item['rewrited_script']['caption'] = spez_rewriter_answer.get(
            'caption', '')
      except json.JSONDecodeError:
        print("Error: String returned from spez_reelsmaker is not valid JSON")
        # Optionally handle the error, e.g., set defaults or skip
        continue
      print(f"No transcription found for item {item.get('shortCode')}")

  end_time = time.time()
  total_processing_time = end_time - start_time
  print(f"Общее время обработки: {total_processing_time:.2f} секунд")

  os.makedirs(os.path.dirname(save_path_result), exist_ok=True)
  with open(save_path_result, "w", encoding="utf-8") as result_file:
    json.dump(results, result_file, ensure_ascii=False, indent=4)
  ###

  #print(results)
  #json_results = json.dumps(results, indent=4) # эта строка преобразует список в json строку

  try:
    if scheme == 0:
      ggl.append_data_to_google_sheet(results, account["table_id"],
                                      'INSTAGRAM')
    elif scheme == 1:
      ggl.append_data_to_google_sheet(results, account["table_id"],
                                      'INSTAGRAM_SAVED')

    print(f"\nDONE\n\n")
    return "Process completed successfully!"
  except Exception as e:
    print(f"Ошибка в процессе обработки в ggl: {e}")


def app_run():
  with open("db/main/db.json", "r", encoding="utf-8") as file:
    table_list = json.load(file)

  switcher = 3  # This should be set appropriately as per your context

  match switcher:
    case 0:
      process_data(table_list["accounts"][6], days=1, scheme=0)
      pass
    case 1:
      for account in table_list["accounts"]:
        if account["id"] != 2:
          process_data(account, days=1, scheme=0)
      pass
    case 2:
      for account in table_list["accounts"]:
        if account["id"] > 0 and account["subscription"] != "stop":
          process_data(account, days=1, scheme=0)
    case 3:
      # For all accounts
      for account in table_list["accounts"]:
        if account["subscription"] != "stop":
          process_data(account, days=1, scheme=0)
    case 4:
      # Handle case where switcher is 4
      pass
    case _:
      # Handle unexpected cases
      pass

  #executor.submit(process_data, request, table_list[2], 10)
  #return None


links_list = ReelLinks(username="olegmazunin",
                       links='''
       ,
https://vt.tiktok.com/ZSj694xwV,
https://vt.tiktok.com/ZSj694EsJ,
https://www.instagram.com/reel/DB2UJCBRbii/?igsh=NXNsNThuZXk0YTly,
https://www.instagram.com/reel/DBweB0TIsMO/?igsh=MTN2aGVxOGdhNDVqbA==
''')

link_download = [{
    "shortCode":
    "123",
    "videoUrl":
    "https://api.apify.com/v2/key-value-stores/50tg9kjLu1eq5oXha/records/video-cheddar-20241030145419-7431582142942989614"
}]


#@app.put("/sendreels")
#def update_reels(request: ReelLinks):
def update_reels(request):
  print(f"Received URLs: {request}")
  request_links = str(request.links)
  # Normalize the separators to make link extraction easier
  data = request_links.replace(',', '\n').replace('\\n', '\n')

  # Split into list and strip whitespace
  links = [link.strip() for link in data.split('\n') if link.strip()]

  # Separate Instagram and TikTok links
  instagram_links = [
      link.replace('reel', 'p') for link in links
      if 'instagram.com/reel' in link
  ]
  tiktok_links = [link for link in links if 'tiktok' in link]

  # Prepare the response dictionary
  request_dict = {
      "username": request.username,
      "instagram_links": instagram_links,
      "tiktok_links": tiktok_links
  }

  print(json.dumps(request_dict, indent=4, ensure_ascii=False))

  # Путь к файлу
  file_path = "db/main/db.json"
  directory = os.path.dirname(file_path)

  # Проверяем, существует ли директория
  if not os.path.exists(directory):
    os.makedirs(directory)  # Создаем директорию, если она не существует

  # Открываем файл после проверки/создания директории
  with open(file_path, "r", encoding="utf-8") as file:
    table_list = json.load(file)

  # Получение username из запроса
  username = request_dict.get('username')

  # Поиск соответствующего table_id для данного username в списке аккаунтов
  account = next(
      (acc
       for acc in table_list['accounts'] if acc['username_tg'] == username),
      None)

  debug = True
  if debug:
    return

  # Проверка на наличие соответствующего аккаунта и вывод результатов
  if account:
    print(
        f"Found table_id for {username}: {account.get('id')} : {account.get('table_id')}"
    )  # Использование переменной account вместо несуществующей table_id

    #process_data(account, links=request_dict.get('instagram_links'), scheme=1)
    process_data(account, links=request_dict.get('tiktok_links'), scheme=2)
  else:
    print(f"No matching table_id found for {username}")

  return {"status": "updated", "data": request}


def download_reels(data):
  # Создаем папку с датой
  now = datetime.datetime.now()
  date_time_folder = now.strftime("%Y%m%d")
  save_directory = f'reels_test/{date_time_folder}'
  os.makedirs(save_directory, exist_ok=True)

  # Словарь для хранения шорткодов и путей к видео
  reel_data = {}

  # Функция для скачивания видео
  def attempt_download(video_url, save_path):
    try:
      response = requests.get(video_url, stream=True)
      if response.status_code == 200:
        # Записываем файл
        with open(save_path, 'wb') as video_file:
          for chunk in response.iter_content(chunk_size=1024):
            if chunk:
              video_file.write(chunk)
        print(f"Видео файл сохранен: {save_path}")
        return True  # Если успешно скачали, возвращаем True
      else:
        print(f"Ошибка загрузки: {response.status_code}")
        return False
    except Exception as e:
      print(f"Ошибка при загрузке: {e}")
      return False

  # Основной процесс скачивания с проверкой и заменой хоста
  for item in data:
    shortCode = item.get('shortCode')
    original_url = item.get('videoUrl')
    video_file_name = f'{shortCode}.mp4'
    file_path = os.path.join(save_directory, video_file_name)

    # Пробуем скачать с оригинальной ссылки
    success = attempt_download(original_url, file_path)

    if success:
      # Сохраняем информацию о скачанном видео
      reel_data[shortCode] = {
          "video_path": file_path,
          "audio_path":
          None,  # Для аудиофайла, который будет сгенерирован позже
          "transcription":
          None  # Для транскрипции, которая будет сгенерирована позже
      }
    else:
      print(f"Не удалось скачать видео для шорткода: {shortCode}")

  return reel_data


if __name__ == "__main__":
  #import uvicorn
  #uvicorn.run(app, host="0.0.0.0", port=8000)
  #app_run()

  ###TEST
  download_reels(link_download)
  #update_reels(links_list)
  ###/TEST

  #main()
