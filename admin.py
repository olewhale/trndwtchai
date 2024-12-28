import os
import subprocess
import psutil
import time
import multiprocessing
from http.server import SimpleHTTPRequestHandler, HTTPServer
import json

#emulator -avd Pixel_8_Pro_NoWin -no-window -no-boot-anim -no-snapshot
#appium --allow-insecure adb_shell

# Конфигурация
APPIUM_PORT = 4723
EMULATOR_NAME = "Pixel_8_Pro_NoWin"
HTTP_SERVER_PORT = 8000
STATIC_FOLDER = "static"

def is_process_running(name):
    for process in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            cmdline = process.info['cmdline']
            if cmdline and isinstance(cmdline, list) and name.lower() in ' '.join(cmdline).lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False

def is_appium_running(port):
    try:
        result = subprocess.check_output(f"curl http://localhost:{port}/status", shell=True, stderr=subprocess.DEVNULL)
        return "ready" in result.decode("utf-8")
    except:
        return False

def start_appium():
    print("Запускаю Appium...")
    subprocess.Popen(["appium", "--allow-insecure", "adb_shell"], shell=True)

def start_emulator():
    print("Запускаю эмулятор...")
    subprocess.Popen([
        "emulator",
        "-avd", EMULATOR_NAME,
        "-no-window",
        "-no-boot-anim",
        "-no-snapshot"
    ], shell=True)
    # subprocess.Popen([
    #     "emulator",
    #     "-avd", EMULATOR_NAME,
    #     "-no-window",
    #     "-no-boot-anim",
    #     "-no-snapshot",
    #     "-gpu", "off"
    # ], shell=True)

class CustomHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/status":
            appium_status = "🟢" if is_appium_running(APPIUM_PORT) else "🔴"
            emulator_status = "🟢" if is_process_running("emulator") else "🔴"
            status = {
                "appium": appium_status,
                "emulator": emulator_status
            }
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(status).encode("utf-8"))  # Корректный JSON
        elif self.path == "/" or self.path == "/admin":
            self.path = "/static/admin.html"
            return super().do_GET()
        else:
            return super().do_GET()

def start_http_server():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    print(f"Запуск HTTP-сервера на порту {HTTP_SERVER_PORT}")
    server_address = ('', HTTP_SERVER_PORT)
    httpd = HTTPServer(server_address, CustomHandler)
    httpd.serve_forever()

if __name__ == "__main__":
    print("Проверка статусов Appium и эмулятора...")

    if not is_appium_running(APPIUM_PORT):
        appium_process = multiprocessing.Process(target=start_appium)
        appium_process.start()
        time.sleep(5)

    if not is_process_running("emulator"):
        emulator_process = multiprocessing.Process(target=start_emulator)
        emulator_process.start()
        time.sleep(10)

    start_http_server()
