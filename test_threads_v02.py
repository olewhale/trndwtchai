import os
import json
import time
import shutil
import logging
import tempfile
import subprocess
import multiprocessing

from tqdm import tqdm
from concurrent.futures import ProcessPoolExecutor, as_completed

from faster_whisper import WhisperModel

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s"
)
logger = logging.getLogger("transcriber_processpool")

# Устанавливаем метод запуска процессов для совместимости с CUDA
multiprocessing.set_start_method('spawn', force=True)

class WorkerState:
    """Класс для хранения состояния воркера (модель, временные файлы)"""
    def __init__(self):
        self.model = None
        self.temp_dir = None

def init_worker(
    model_size: str,
    device: str,
    compute_type: str
):
    """
    Инициализатор воркера с обработкой ошибок и временной директорией
    """
    global worker_state
    worker_state = WorkerState()
    
    try:
        logger.info(f"Инициализация модели {model_size} на {device}")
        worker_state.model = WhisperModel(
            model_size,
            device=device,
            compute_type=compute_type
        )
        worker_state.temp_dir = tempfile.mkdtemp(prefix="whisper_wav_")
        logger.info(f"Временная директория создана: {worker_state.temp_dir}")
    except Exception as e:
        logger.error(f"Ошибка инициализации: {str(e)}")
        raise

def cleanup_worker():
    """Очистка временных файлов при завершении воркера"""
    global worker_state
    if worker_state.temp_dir and os.path.exists(worker_state.temp_dir):
        shutil.rmtree(worker_state.temp_dir)
        logger.info(f"Очищена временная директория: {worker_state.temp_dir}")

def decode_to_wav(
    video_path: str,
    sample_rate: int = 16000,  # Увеличена частота для улучшения качества
    hwaccel: str = None
) -> str:
    """
    Конвертация с использованием аппаратного ускорения и проверкой ошибок
    """
    try:
        output_filename = f"temp_{os.getpid()}_{time.time()}.wav"
        wav_path = os.path.join(worker_state.temp_dir, output_filename)
        
        cmd = [
            'ffmpeg', '-y',
            '-i', video_path,
            '-vn', '-ac', '1',
            '-ar', str(sample_rate),
            '-acodec', 'pcm_s16le',
            wav_path
        ]
        
        if hwaccel:
            cmd.insert(1, '-hwaccel')
            cmd.insert(2, hwaccel)

        subprocess.run(
            cmd,
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE
        )
        return wav_path
    except Exception as e:
        logger.error(f"Ошибка конвертации {video_path}: {str(e)}")
        return ""

def transcribe_audio(audio_path: str, language: str = None) -> str:
    """
    Транскрипция с обработкой ошибок и тайм-аутом
    """
    global worker_state
    try:
        if not os.path.exists(audio_path):
            return "Ошибка: аудиофайл не найден"

        start_time = time.time()
        segments, _ = worker_state.model.transcribe(
            audio_path,
            language=language,
            beam_size=5,  # Увеличен размер луча для повышения точности
            vad_filter=True  # Включение фильтрации голосовой активности
        )
        transcription = " ".join([seg.text for seg in segments])
        logger.info(f"Транскрибировано {os.path.basename(audio_path)} за {time.time()-start_time:.1f}с")
        return transcription
    except Exception as e:
        logger.error(f"Ошибка транскрипции: {str(e)}")
        return "Ошибка транскрипции"
    finally:
        try:
            os.remove(audio_path)
        except:
            pass

def worker_pipeline(video_path: str, **kwargs):
    """
    Конвейер обработки с улучшенным управлением ресурсами
    """
    try:
        wav_path = decode_to_wav(video_path, **kwargs)
        if not wav_path:
            return {"video": video_path, "error": "Ошибка конвертации"}
        
        return {
            "video": video_path,
            "transcription": transcribe_audio(wav_path, kwargs.get('language')),
            "processing_pid": os.getpid()
        }
    except Exception as e:
        logger.error(f"Критическая ошибка в worker_pipeline: {str(e)}")
        return {"video": video_path, "error": str(e)}

def process_videos_with_process_pool(
    folder_mp4: str,
    out_file: str = "results.json",
    model_size: str = "small",
    device: str = "cuda",
    compute_type: str = "float16",
    language: str = None,
    hwaccel: str = "cuda",  # По умолчанию использовать аппаратное ускорение
    sample_rate: int = 16000,
    max_workers: int = 4  # Оптимально для большинства GPU
):
    """
    Оптимизированный обработчик с контролем памяти и улучшенным логированием
    """
    start_time = time.time()
    videos = [os.path.join(folder_mp4, f) for f in os.listdir(folder_mp4) if f.endswith('.mp4')]
    
    if not videos:
        logger.error("Нет видео для обработки")
        return

    logger.info(f"Начата обработка {len(videos)} видео с параметрами:")
    logger.info(f"Модель: {model_size}, Устройство: {device}, Тип вычислений: {compute_type}")
    logger.info(f"Воркеров: {max_workers}, Частота дискретизации: {sample_rate} Гц")

    results = []
    with ProcessPoolExecutor(
        max_workers=max_workers,
        initializer=init_worker,
        initargs=(model_size, device, compute_type)
    ) as executor:
        futures = {executor.submit(worker_pipeline, video, 
                    sample_rate=sample_rate,
                    hwaccel=hwaccel,
                    language=language): video for video in videos}

        for future in tqdm(as_completed(futures), total=len(futures), desc="Обработка"):
            try:
                results.append(future.result(timeout=300))  # Таймаут 5 минут на обработку
            except Exception as e:
                video = futures[future]
                logger.error(f"Таймаут обработки {video}: {str(e)}")
                results.append({"video": video, "error": "Таймаут обработки"})

    with open(out_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    logger.info(f"Обработка завершена за {time.time()-start_time:.2f} сек. Результаты сохранены в {out_file}")

if __name__ == "__main__":
    process_videos_with_process_pool(
        folder_mp4="reels/test",
        out_file="reels/test/results.json",
        model_size="small",
        device="cuda",
        compute_type="float16",
        language="ru",
        hwaccel="cuda",
        max_workers=4  # Оптимальное значение для большинства GPU
    )