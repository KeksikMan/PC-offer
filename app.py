import json
import os
import datetime
import time

import pyautogui as pg


def cancel_shutdown(request):
    os.system(request)

    message = "Хорошие новости! Выключение было отменено"
    pg.alert(text=message, title='Отмена', button='OK')
def shutdown_time_staff(request, message):
    mod_request = f"{request} /c \"{message}\" "
    os.system(mod_request)
def shutdown_time(request):
    time = int(request[15:])
    if time >= 60:
        minute = time // 60
        if minute >= 60:
            hour = minute // 60
            message = f"Через  {hour}час {minute-hour*60}мин {time-minute*60}сек компьютер будет отключен, пупсик"
            shutdown_time_staff(request, message)
        else:
            message = f"Через  {minute}мин {time-minute*60}сек компьютер будет отключен, пупсик"
            shutdown_time_staff(request, message)
    else:
        message = f"Через {time} сек компьютер будет отключен, пупсик"
        shutdown_time_staff(request, message)
def set_value(path, value):
    with open("config.json", "r") as config:
        json_dict = json.load(config)
    with open("config.json", "w") as config:
        json_dict[path] = value
        json.dump(json_dict, config, indent=2)
def execute_request(request):
    if type(request) == str:
        print(request)

        if "shutdown" in request:
            if "shutdown /a" == request:
                cancel_shutdown(request)
            else:
                shutdown_time(request)
        elif "auto-mode" in request:
            if request == "auto-mode on":
                set_value("auto-mode", True)
            else:
                set_value("auto-mode", False)
        elif "set-time" in request:
            set_value("time-off", request[9:])
        elif "server" == request:
            os.system("python file_server.py")
        elif "file" in request:
            set_value("file", request[5:])


def time_check():
    while True:
        hour_now = datetime.datetime.now().time().hour
        minute_now = datetime.datetime.now().time().minute

        with open("config.json", "r") as config:
            json_dict = json.load(config)

        if json_dict["auto-mode"]:

            time_config = int(json_dict["time-off"])

            hour_off = time_config // 60
            minute_off = time_config - hour_off * 60

            if hour_now > hour_off:
                shutdown_time("shutdown -s -t 20")
            elif hour_now == hour_off:
                if minute_off - minute_now <= 30:
                    shutdown_time(f"shutdown -s -t {60 * (minute_off - minute_now)}")
            elif hour_now < hour_off and hour_off - hour_now == 1:
                if 60 - minute_now + minute_off <= 30:
                    shutdown_time(f"shutdown -s -t {60 * (60 - minute_now + minute_off)}")

        time.sleep(60)