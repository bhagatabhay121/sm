import cohere
from rich import print
from dotenv import dotenv_values
import subprocess
from asyncio import run
import keyboard
import asyncio
import pyautogui
import pygetwindow as gw
import subprocess
import requests
import time
from groq import Groq
import webbrowser 
from AppOpener import close, open as appopen
from pywhatkit import search, playonyt
from Backend. RealtimeSearchEngine import RealtimeSearchEngine 
from Backend. Chatbot import ChatBot
import os
import random




env_vars = dotenv_values(".env")

CohereAPIKey = env_vars.get("CohereAPIKey")

co = cohere.Client(api_key=CohereAPIKey)

funcs = [
    "exit","general","realtime","open","close","play",
    "generate image","system","content","google search",
    "youtube search","remainder"
]



Username = env_vars.get("Username")
Assistantname = env_vars.get("Assistantname")


DefaultMessage = f'''{Username} : Hello {Assistantname}, How are you?
{Assistantname} Welcome {Username}. I am doing well. How may i help you?'''
subprocesses = []
Functions = ["open", "close", "play", "system", "content", "google search", "youtube search"]





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
    time.sleep(5)
    active_window = gw.getActiveWindow()
    if "Xstream Play" in active_window.title:
        pyautogui.moveTo(1503, 179)
        pyautogui.click()
        pyautogui.write(Topic)
        pyautogui.press("enter")

        time.sleep(2)
        pyautogui.moveTo(270, 439)
        pyautogui.click()

        pyautogui.scroll(-500)
    

        pyautogui.moveTo(182,561)
    else:
        search(Topic) 
    #return True

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
    
    playonyt(command)


def OpenApp(app, sess=requests.session()):
    try:
        appopen(app, match_closest=True, output=True, throw_error=True)
        return True

    except:
        active_window = gw.getActiveWindow()

        if "Google Chrome" in active_window.title:
            if "first account" in app or "mera account" in app or "my account" in app:
                pyautogui.moveTo(636, 454)
                pyautogui.click()
                

            elif "second account" in app or "second account" in app:
                pyautogui.moveTo(839, 455)
                pyautogui.click()

            elif "new tab" in app:
                pyautogui.hotkey('ctrl','t')

            elif "Airtel stream" in app:
                pyautogui.moveTo(1301, 615)
                pyautogui.click()

            else:
                webbrowser.open("www."+app+".com")

           

        else:
            webbrowser.open("www."+app+".com")

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
    active_window = gw.getActiveWindow()
    

    if command == "bluetooth off" or command == "disconnect bluetooth" or command == "bluetooth":
        pyautogui.hotkey('win', 'a')
        keyboard.press_and_release("right")
        keyboard.press_and_release("enter")

    elif command == "wifi off" or command == "disconnect wifi" or command == "wifi":
        pyautogui.hotkey('win', 'a')
        keyboard.press_and_release("enter")

    elif "mute" in command:
        keyboard.press_and_release("volume mute")

    elif "unmute" in command:
        keyboard.press_and_release("volume unmute")
    elif "volume up" in command:
        keyboard.press_and_release("up")
        keyboard.press_and_release("volume up")
    elif "volume down" in command:
        keyboard.press_and_release("volume down")

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


messages = []

preamble = """
You are a very accurate Decision-Making Model, which decides what kind of a query is given to you.
You will decide whether a query is a 'general' query, a 'realtime' query, or is asking to perform any task or automation like 'open facebook, instagram', 'can you write a application and open it in notepad'
*** Do not answer any query, just decide what kind of query is given to you. ***
-> Respond with 'general ( query )' if a query can be answered by a llm model (conversational ai chatbot) and doesn't require any up to date information like if the query is 'who was akbar?' respond with 'general who was akbar?', if the query is 'how can i study more effectively?' respond with 'general how can i study more effectively?', if the query is 'can you help me with this math problem?' respond with 'general can you help me with this math problem?', if the query is 'Thanks, i really liked it.' respond with 'general thanks, i really liked it.' , if the query is 'what is python programming language?' respond with 'general what is python programming language?', etc. Respond with 'general (query)' if a query doesn't have a proper noun or is incomplete like if the query is 'who is he?' respond with 'general who is he?', if the query is 'what's his networth?' respond with 'general what's his networth?', if the query is 'tell me more about him.' respond with 'general tell me more about him.', and so on even if it require up-to-date information to answer. Respond with 'general (query)' if the query is asking about time, day, date, month, year, etc like if the query is 'what's the time?' respond with 'general what's the time?'.
-> Respond with 'realtime ( query )' if a query can not be answered by a llm model (because they don't have realtime data) and requires up to date information like if the query is 'who is indian prime minister' respond with 'realtime who is indian prime minister', if the query is 'tell me about facebook's recent update.' respond with 'realtime tell me about facebook's recent update.', if the query is 'tell me news about coronavirus.' respond with 'realtime tell me news about coronavirus.', etc and if the query is asking about any individual or thing like if the query is 'who is akshay kumar' respond with 'realtime who is akshay kumar', if the query is 'what is today's news?' respond with 'realtime what is today's news?', if the query is 'what is today's headline?' respond with 'realtime what is today's headline?', etc.
-> Respond with 'open (application name or website name)' if a query is asking to open any application like 'open facebook', 'open telegram', etc. but if the query is asking to open multiple applications, respond with 'open 1st application name, open 2nd application name' and so on.
-> Respond with 'close (application name)' if a query is asking to close any application like 'close notepad', 'close facebook', etc. but if the query is asking to close multiple applications or websites, respond with 'close 1st application name, close 2nd application name' and so on.
-> Respond with 'play (song name)' if a query is asking to play any song like 'play afsanay by ys', 'play let her go', etc. but if the query is asking to play multiple songs, respond with 'play 1st song name, play 2nd song name' and so on.
-> Respond with 'generate image (image prompt)' if a query is requesting to generate a image with given prompt like 'generate image of a lion', 'generate image of a cat', etc. but if the query is asking to generate multiple images, respond with 'generate image 1st image prompt, generate image 2nd image prompt' and so on.
-> Respond with 'reminder (datetime with message)' if a query is requesting to set a reminder like 'set a reminder at 9:00pm on 25th june for my business meeting.' respond with 'reminder 9:00pm 25th june business meeting'.
-> Respond with 'system (task name)' if a query is asking to mute, unmute, volume up, volume down , etc. but if the query is asking to do multiple tasks, respond with 'system 1st task, system 2nd task', etc.
-> Respond with 'content (topic)' if a query is asking to write any type of content like application, codes, emails or anything else about a specific topic but if the query is asking to write multiple types of content, respond with 'content 1st topic, content 2nd topic' and so on.
-> Respond with 'google search (topic)' if a query is asking to search a specific topic on google but if the query is asking to search multiple topics on google, respond with 'google search 1st topic, google search 2nd topic' and so on.
-> Respond with 'youtube search (topic)' if a query is asking to search a specific topic on youtube but if the query is asking to search multiple topics on youtube, respond with 'youtube search 1st topic, youtube search 2nd topic' and so on.
*** If the query is asking to perform multiple tasks like 'open facebook, telegram and close whatsapp' respond with 'open facebook, open telegram, close whatsapp' ***
*** If the user is saying goodbye or wants to end the conversation like 'bye jarvis.' respond with 'exit'.***
*** Respond with 'general (query)' if you can't decide the kind of query or if a query is asking to perform a task which is not mentioned above. ***
"""

ChatHistory = [
    {"role":"User", "message":"how are you?"},
    {"role":"Chatbot", "message":"general how are you?"},
    {"role":"User", "message":"do you like pizza?"},
    {"role":"Chatbot", "message":"general do you like pizza?"},
    {"role":"User", "message":"open chrome and tell me about mahatma gandhi."},
    {"role":"Chatbot", "message":"open chrome, general tell me about mahatma gandhi"},
    {"role":"User", "message":"open chrome and firefox"},
    {"role":"Chatbot", "message":"open chrome, open firefox"},
    {"role":"User", "message":"what is today's date and by the way remaind me that i have a dancing performance on 5th august"},
    {"role":"Chatbot", "message":"general what is today's date and by the way remaind 11:00 pm 5th aug dancing performance"},
    {"role":"User", "message":"chat with me"},
    {"role":"Chatbot", "message":"general chat with me"},
]

def FirstLayerDMM(prompt: str = "test"):
    messages.append({"role":"user", "content":f"{prompt}"})

    stream = co.chat_stream(
        model="command-r-plus",
        message=prompt,
        temperature=0.7,
        chat_history=ChatHistory,
        prompt_truncation="OFF",
        connectors=[],
        preamble=preamble
    )

    response = ""

    for event in stream:
        if event.event_type == "text-generation":
            response += event.text

    response = response.replace("\n", "")
    response = response.split(",")

    response = [i.strip() for i in response]

    temp = []

    for task in response:
        for func in funcs:
            if task.startswith(func):
                temp.append(task)

    response = temp

    if "{query}" in response:
        newresponse = FirstLayerDMM(prompt=prompt)

    else:
        return response
    
def Re():
    print("real search")

def MainExecution():
    TaskExecution = False
    ImageExecution = False 
    ImageGenerationQuery = ""
    Query = input(">>> ")

    if Query != "":
        Decision = FirstLayerDMM(Query)

        ak = random.choice(Decision)
        

        if "realtime" in ak:
            QueryFinal = ak.replace("realtime ", "")
            Answer = RealtimeSearchEngine(QueryFinal)
            print("Jarvis: "+Answer)
            return True
        
        else:
            pass
        G = any([i for i in Decision if i.startswith("general")])
        R = any([i for i in Decision if i.startswith("realtime")])
        Mearged_query = " and " .join(
            [" ".join(i.split()[1:]) for i in Decision if i.startswith("general") or i.startswith("realtime")]
        )
        for queries in Decision:
            if "generate " in queries:
                ImageGenerationQuery = str(queries) 
                ImageExecution = True
        for queries in Decision:
            if TaskExecution == False:
                if any(queries.startswith(func) for func in Functions):
                    run(Automation(list(Decision))) 
                    TaskExecution = True


        if ImageExecution == True:
            print("wait for a moment")
            print("I am generating this, tell me another command")
            with open(r"Frontend\Files\ImageGeneration.data", "w") as file: 
                file.write(f"{ImageGenerationQuery},True")
            try:
                p1 = subprocess.Popen(['python', r'Backend\ImageGeneration.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE,stdin=subprocess.PIPE, shell=False)
                
            except Exception as e:
                print(f"Error: {e}")

        if G and R or R:
            Answer = RealtimeSearchEngine(Mearged_query)
            return True
        else:
            for Queries in Decision:
                if "general" in Queries:
                    QueryFinal = Queries.replace("general ", "")
                    Answer = ChatBot(QueryFinal)
                    print("Jarvis: "+Answer)
                    return True
                

                elif "exit" in Queries:
                    QueryFinal = "Okay, Bye!"
                    Answer = ChatBot(QueryFinal) 
                    print("Jarvis: "+Answer)
                    os._exit(1)

    else:
        print("Type some command")

if __name__ == "__main__":
    while True:
        MainExecution()
