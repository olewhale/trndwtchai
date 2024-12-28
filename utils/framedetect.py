from scenedetect import VideoManager, SceneManager
from scenedetect.detectors import ContentDetector
import os
import subprocess
from tqdm import tqdm  # Импортируем tqdm для прогресс-бара

# Функция для извлечения пятого кадра шота с помощью ffmpeg
def extract_fifth_frame_ffmpeg(video_path, scenes, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Добавляем прогресс-бар для отображения процесса обработки шотов
    for i, (start_time, _) in enumerate(tqdm(scenes, desc="Extracting frames", unit="shot")):
        # Формируем команду для ffmpeg, чтобы извлечь пятый кадр через 5 кадров после начала шота
        timecode = start_time.get_timecode()  # Время в формате HH:MM:SS.mmm
        frame_path = os.path.join(output_dir, f'shot_{i+1}.jpg')

        # Команда ffmpeg для извлечения пятого кадра по времени
        command = [
            'ffmpeg',
            '-ss', timecode,  # Устанавливаем время начала
            '-i', video_path,  # Путь к видеофайлу
            '-vf', 'select=eq(n\,4)',  # Выбираем пятый кадр (нумерация начинается с нуля)
            '-frames:v', '1',  # Извлечь только один кадр
            '-q:v', '2',  # Качество изображения (0 - наилучшее, 31 - наихудшее)
            '-y', frame_path  # Путь для сохранения кадра
        ]

        # Выполняем команду ffmpeg
        subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# Основная функция для поиска шотов и извлечения кадров
def get_fifth_frame_of_each_shot(video_path, output_dir):
    # Создаем VideoManager и SceneManager
    video_manager = VideoManager([video_path])
    scene_manager = SceneManager()

    # Добавляем детектор смены контента
    scene_manager.add_detector(ContentDetector(threshold=30))

    # Загружаем видео
    video_manager.start()

    # Определяем сцены
    scene_manager.detect_scenes(frame_source=video_manager)
    scenes = scene_manager.get_scene_list()

    # Извлекаем пятый кадр каждого шота с помощью ffmpeg
    extract_fifth_frame_ffmpeg(video_path, scenes, output_dir)

    # Освобождаем ресурсы
    video_manager.release()

# Путь к видео и директория для сохранения кадров
video_path = 'video/video1.mp4'  # Укажите путь к вашему видеофайлу
output_dir = 'video/output_frames'

# Запуск процесса
get_fifth_frame_of_each_shot(video_path, output_dir)