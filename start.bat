@echo off
REM Переходим в папку со скриптом
cd C:\AAA\Projects\trndwch\mfai_neuro_reels_writer

REM Запускаем admin.py в отдельном окне
start python admin.py

REM Активируем виртуальное окружение
call venv_win\Scripts\activate.bat

REM Небольшая задержка, чтобы admin.py успел запуститься
timeout /t 10 /nobreak >nul

REM Запускаем main.py в текущем окне
python main.py

REM Деактивируем виртуальное окружение (опционально)
REM deactivate