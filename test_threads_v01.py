import os
import time
import json
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed

from faster_whisper import WhisperModel
from tqdm import tqdm


def convert_video_to_audio(video_path: str) -> str:
    """
    Конвертация видеофайла (.mp4) в аудиофайл (.wav) при помощи ffmpeg.
    Возвращает путь к сконвертированному аудио.
    """
    audio_path = video_path.replace(".mp4", ".wav")
    try:
        command = [
            "ffmpeg", "-i", video_path, 
            "-ac", "1",  # моно
            "-ar", "16000",  # 16kHz
            "-y",  # перезапись без подтверждения
            audio_path
        ]
        # Запускаем ffmpeg, глушим вывод
        with open(os.devnull, 'w') as devnull:
            subprocess.run(command, check=True, stdout=devnull, stderr=devnull)

        if os.path.exists(audio_path):
            return audio_path
        else:
            print(f"Не удалось создать аудиофайл: {audio_path}")
            return ""
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при конвертации {video_path}: {e}")
        return ""


def transcribe_audio(audio_path: str, model: WhisperModel) -> str:
    """
    Транскрибация аудиофайла с помощью Faster Whisper (локальная модель).
    Возвращает полученный текст (строка).
    """
    if not os.path.exists(audio_path):
        return "Аудиофайл не найден"

    try:
        segments, info = model.transcribe(audio_path, language=None)
        transcription = "".join(segment.text for segment in segments)
        return transcription
    except Exception as e:
        print(f"Ошибка при транскрибации {audio_path}: {e}")
        return "Ошибка транскрибации"


def process_video(video_path: str, model: WhisperModel) -> dict:
    """
    Обёртка: конвертируем видео -> транскрибируем -> возвращаем результат.
    Результат: словарь вида {
        "video": <путь к видео>,
        "transcription": <строка с расшифровкой или сообщением об ошибке>
    }
    """
    audio_path = convert_video_to_audio(video_path)
    if audio_path:
        text = transcribe_audio(audio_path, model)
        # Удалим промежуточный аудиофайл
        if os.path.exists(audio_path):
            os.remove(audio_path)
    else:
        text = "Ошибка при конвертации"

    return {
        "video": video_path,
        "transcription": text
    }


def transcribe_reels_in_parallel(reels_folder: str = "reels", num_workers: int = 10):
    """
    Главная функция:
    - Находит все .mp4 в папке `reels_folder`
    - Запускает параллельную транскрибацию (ThreadPoolExecutor, num_workers)
    - Сохраняет результат в reels_transcriptions.json
    """
    # Создаем список всех .mp4 файлов в папке reels
    all_videos = []
    for file_name in os.listdir(reels_folder):
        if file_name.lower().endswith(".mp4"):
            full_path = os.path.join(reels_folder, file_name)
            all_videos.append(full_path)

    if not all_videos:
        print("В папке 'reels' нет видеофайлов (.mp4)")
        return

    print(f"Найдено видеофайлов: {len(all_videos)}")

    # Инициализируем модель
    print("Инициализация модели Whisper...")
    model = WhisperModel("small", device="cuda", compute_type="float16")
    # Если без GPU, можно сделать device="cpu".

    # Параллельное исполнение
    print(f"Начинаем транскрибацию в {num_workers} потоков...")
    start_time = time.time()

    results = []
    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        future_to_video = {
            executor.submit(process_video, v_path, model): v_path
            for v_path in all_videos
        }

        # Красивый прогресс-бар, пока выполняются задачи
        for future in tqdm(as_completed(future_to_video), 
                           total=len(future_to_video),
                           desc="Transcribing",
                           unit="video"):
            video_path = future_to_video[future]
            try:
                result_dict = future.result()
                results.append(result_dict)
            except Exception as e:
                print(f"Ошибка при обработке {video_path}: {e}")

    end_time = time.time()
    total_time = end_time - start_time

    # Сохраняем результаты в JSON
    output_file = os.path.join(reels_folder, "reels_transcriptions_thread_03.json")
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=4)

    print(f"\nГотово! Все транскрибации сохранены в '{output_file}'.")
    print(f"Затраченное время: {total_time:.2f} c")


if __name__ == "__main__":
    transcribe_reels_in_parallel("reels/test", num_workers=3)
