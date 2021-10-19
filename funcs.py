import pyttsx3
import speech_recognition as sr
import os
from fuzzywuzzy import fuzz
import datetime
import win32com.client as wincl
import time
import anekdot
import browser
import calc
import convert
import translate
opts = {"alias": ("гдз", "решебник", "ответы"),
        "tbr": ('скажи', 'расскажи', 'покажи', 'сколько', 'произнеси', 'как','сколько','поставь','переведи', "засеки",'запусти','сколько будет'),
        "cmds":
            {"ctime": ('текущее время', 'сейчас времени', 'который час', 'время'),
             'startStopwatch': ('запусти секундомер', "включи секундомер", "начини"),
             'stopStopwatch': ('останови секундомер', "выключи секундомер", "прекрати"),
             "stupid1": ('расскажи анекдот', 'рассмеши меня', 'ты знаешь анекдоты', "шутка"),
             "calc": ('прибавить','умножить','разделить','степень','вычесть','поделить','х','+','-','/'),
             "shutdown": ('выключи', 'выключить', 'отключение', 'отключи', 'выключи компьютер'),
             "conv": ("валюта", "конвертер","доллар",'руб','евро'),
             "internet": ("открой", "вк", "гугл", "сайт", 'вконтакте', "ютуб"),
             "translator": ("переводчик","translate", "переведи"),
             "deals": ("дела","делишки", 'сам')}}
startTime = 0
speak_engine = pyttsx3.init()
voices = speak_engine.getProperty('voices')
speak_engine.setProperty('voice', voices[2].id)
r = sr.Recognizer()
m = sr.Microphone(device_index=1)
voice = "str"


def speak(what):
    print(what)
    speak = wincl.Dispatch("SAPI.SpVoice")
    speak.Speak(what)


def callback(recognizer, audio):
    try:
        global voice
        voice = recognizer.recognize_google(audio, language="ru-RU").lower()

        print("Распознано: " + voice)


        cmd = voice

        for x in opts['alias']:
            cmd = cmd.replace(x, "").strip()

        for x in opts['tbr']:
            cmd = cmd.replace(x, "").strip()
        voice = cmd
            # распознаем и выполняем команду
        cmd = recognize_cmd(cmd)
        execute_cmd(cmd['cmd'])


    except sr.UnknownValueError:
        print("Голос не распознан!")
    except sr.RequestError as e:
        print("Неизвестная ошибка, проверьте интернет!")
def listen():
    with m as source:
        r.adjust_for_ambient_noise(source)
    stop_listening = r.listen_in_background(m, callback)
    while True: time.sleep(0.1)


def recognize_cmd(cmd):
    RC = {'cmd': '', 'percent': 0}
    for c, v in opts['cmds'].items():
        for x in v:
            vrt = fuzz.ratio(cmd, x)
            if vrt > RC['percent']:
                RC['cmd'] = c
                RC['percent'] = vrt
    return RC


def execute_cmd(cmd):
    global startTime
    if cmd == 'ctime':
        now = datetime.datetime.now()
        speak("Сейчас {0}:{1}".format(str(now.hour), str(now.minute)))
    elif cmd == 'shutdown':
        os.system('shutdown -s')
        speak("Выключаю...")
    elif cmd == 'calc':
        calc.calculator()
    elif cmd == 'conv':
        convert.convertation()
    elif cmd == 'translator':
        translate.translate()
    elif cmd == 'stupid1':
        anekdot.fun()
    elif cmd == 'internet':
        browser.browser()
    elif cmd == 'startStopwatch':
        speak("Секундомер запущен")
        startTime = time.time()
    elif cmd == "stopStopwatch":
        if startTime != 0:
            Time = time.time() - startTime
            speak(f"Прошло {round(Time // 3600)} часов {round(Time // 60)} минут {round(Time % 60, 2)} секунд")
            startTime = 0
        else:
            speak("Секундомер не включен")
    elif cmd == 'deals':
        speak("Голова пока цела. Я имею ввиду процессор.")
    else:
        print("Команда не распознана")
