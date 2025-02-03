from kivy.uix.effectwidget import Translate
from AppOpener import close, open as appopen
from webbrowser import open as webopen
from pywhatkit import search, playonyt
from dotenv import dotenv_values
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from rich import print
from groq import Groq
import webbrowser 
import pyautogui
import subprocess
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium import webdriver
import requests
import time
import os
from webdriver_manager.chrome import ChromeDriverManager
import keyboard
import asyncio

env_vars = dotenv_values(".env")

GroqAPIKey = env_vars.get("GroqAPIKey")

classes = ["zCubwf", "hgKElc", "LTKOO sY7ric", "ZOLcW", "gsrt vk_bk FzvWSb YwPhnf", "pclqee", "tw-Data-text tw-text-small tw-ta", "IZ6rdc", "05uR6d LTKOO", "vlzY6d", "webanswers-webanswers_table_webanswers-table", "dDoNo ikb4Bb gsrt", "sXLa0e", "LWkfKe", "VQF4g", "qv3Wpe", "kno-rdesc", "SPZz6b"]
# Define a user-agent for making web requests.
useragent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'
#Initialize the Groq client with the API key.
client = Groq(api_key=GroqAPIKey)

# Predefined professional responses for user interactions.
professional_responses = [
    "Your satisfaction is my top priority; feel free to reach out if there's anything else I can help you with.",
    "I'm at your service for any additional questions or support you may need-don't hesitate to ask.",
]

messages = []
# System message to provide context to the chatbot.
SystemChatBot = [{"role": "system", "content": f"Hello, I am Abhay. You're a content writter. You have to write a content like letter,codes, application, essays, notes, songs, poems etc."}]

def GoogleSearch(Topic):
    search(Topic) 
    return True

def Content(Topic):
    def OpenNotePad(File):
        default_text_editor = "notepad.exe"
        subprocess.Popen([default_text_editor, File])

    def ContentWriterAI(prompt):
        messages.append({"role":"user", "content": f"{prompt}"})

        completion = client.chat.completions.create(
            model="mixtral-8x7b-32768",
            messages=SystemChatBot + messages,
            max_tokens=2048,
            temperature=0.7,
            top_p=1,
            stream=True,
            stop=None
        )

        Answer = ""

        for chunk in completion:
            if chunk.choices[0].delta.content:
                Answer += chunk.choices[0].delta.content

        Answer = Answer.replace("</s>", "")

        messages.append({"role":'assistant', "content": Answer})
        return Answer
    
    Topic: str = Topic.replace("Content", "")
    ContentByAI = ContentWriterAI(Topic)

    with open(rf"Data\{Topic.lower().replace(' ','')}.txt", "w", encoding="utf-8") as file:
        file.write(ContentByAI)
        file.close()

    OpenNotePad(rf"Data\{Topic.lower().replace(' ','')}.txt")
    return True

def YouTubeSearch(Topic):
    Url4Search = f"https://www.youtube.com/results?search_query={Topic}"
    webbrowser.open(Url4Search)
    return True

def PlayYoutube(command):
    if command == "song" or command == "recommended video":
        def play_recommended():
            try:
                recommended_videos = driver.find_elements(By.XPATH, '//*[@id="dismissible"]//a[@id="thumbnail"]')
                if recommended_videos:
                    recommended_videos[0].click()
                    
                else:
                    keyboard.press_and_release("l")
            except:
                pass


    elif command == "next video" or command == "next":
        pyautogui.hotkey('shift', 'n')

    elif command == "video" or command == "song" or command == "play":
        keyboard.press_and_release("space")

    elif command == "first video":
        pyautogui.moveTo(560, 405)
        pyautogui.click()

    elif command == "second video":
        pyautogui.moveTo(1147, 394)
        pyautogui.click()

    elif command == "third video":
        pyautogui.moveTo(1715, 374)
        pyautogui.click()
        

    elif command == "short" or command == "short feed" or command == "short video" or command == "shorts":
        pyautogui.moveTo(110, 263)
        pyautogui.click()

    elif command == "skip ad":
        pyautogui.moveTo(1164, 703)
        pyautogui.click()

    else:
        playonyt(command)

def press_key(shortcut):
    global driver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    body = driver.find_element(By.TAG_NAME, 'body')
    body.send_keys(shortcut)

def OpenApp(app, sess=requests.session()):
    try:
        appopen(app, match_closest=True, output=True, throw_error=True)
        return True

    except:
        pass

def CloseApp(app):
    if "chrome" in app:
        pass

    else:
        try:
            close(app, match_closest=True, output=True, throw_error=True)
            return True
        except:
            return False

def System(command):
    def mute():
        keyboard.press_and_release("volume mute")

    def unmute():
        keyboard.press_and_release("volume unmute")

    def volume_up():
        keyboard.press_and_release("volume up")

    def volume_down():
        keyboard.press_and_release("volume down")

    def homescreen():
        keyboard.press_and_release("win + d")

    def stop_video():
        keyboard.press_and_release("space")
        

    def mini_player():
        keyboard.press_and_release("i")

    def full_screen():
        keyboard.press_and_release("f")

    if command == "mute":
        mute()

    elif command == "mini player" or command == "show in mini player":
        mini_player()

    elif command == "fullscreen" or command == "open in full screen" or command == "full screen":
        full_screen()

    elif command == "unmute":
        unmute()
    elif command == "volume up":
        keyboard.press_and_release("up")
        volume_up()
    elif command == "volume down":
        volume_down()

    elif command == "home screen" or command == "minimize window":
        homescreen()

    elif command == "stop video" or command == "stop youtube video" or command == "start video":
        stop_video()

    elif command == "skip video" or command == "skip youtube video":
        keyboard.press_and_release("l")

    elif command == "click on first video":
        pyautogui.moveTo(560, 405)
        pyautogui.click()

    elif command == "click on second video":
        pyautogui.moveTo(1147, 395)
        pyautogui.click()

    elif command == "click on third video":
        pyautogui.moveTo(1715, 374)
        pyautogui.click()


    elif command == "click on short" or command == "click on short feed" or command == "click on short video" or command == "click on shorts":
        pyautogui.moveTo(110, 263)
        pyautogui.click()

    elif command == "skip advertisement" or command == "skip the ad" or command == "ad skip":
        pyautogui.moveTo(1164, 703)
        pyautogui.click()

    elif command == "scroll the video" or command == "scroll video" or command == "scroll":
        pyautogui.scroll(-500)

    elif command == "bluetooth off" or command == "disconnect bluetooth" or command == "bluetooth":
        pyautogui.hotkey('win', 'a')
        time.sleep(1)
        keyboard.press_and_release("left")
        
        

    return True

async def TranslateAndExecute(commands: list[str]):
    funcs = []

    for command in commands:
        if command.startswith("open "):
            if "open it" in command:
                pass

            if "open file" == command:
                pass

            else:
                fun = asyncio.to_thread(OpenApp, command.removeprefix("open "))
                funcs.append(fun)

        elif command.startswith(" "):
            pass

        elif command.startswith("general "):
            pass

        elif command.startswith("realtime "):
            pass

        elif command.startswith("close "):
            fun = asyncio.to_thread(CloseApp, command.removeprefix("close "))
            funcs.append(fun)

        elif command.startswith("play "):
            fun = asyncio.to_thread(PlayYoutube, command.removeprefix("play "))
            funcs.append(fun)

        elif command.startswith("content "):
            fun = asyncio.to_thread(Content, command.removeprefix("content "))
            funcs.append(fun)

        elif command.startswith("google search "):
            fun = asyncio.to_thread(GoogleSearch, command.removeprefix("google search "))
            funcs.append(fun)

        elif command.startswith("youtube search "):
            fun = asyncio.to_thread(YouTubeSearch, command.removeprefix("youtube search "))
            funcs.append(fun)

        elif command.startswith("system "):
            fun = asyncio.to_thread(System, command.removeprefix("system "))
            funcs.append(fun)


        else:
            print(f"No Function Found For {command}")

    results = await asyncio.gather(*funcs)

    for result in results:
        if isinstance(result, str):
            yield result
        else:
            yield result

async def Automation(commands: list[str]):
    async for result in TranslateAndExecute(commands):
        pass

    return True