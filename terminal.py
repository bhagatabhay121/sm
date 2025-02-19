
from Backend. Model import FirstLayerDMM
from Backend. RealtimeSearchEngine import RealtimeSearchEngine 
from Backend. Automation import Automation
from Backend. Chatbot import ChatBot
from dotenv import dotenv_values
from asyncio import run
from time import sleep
import subprocess
import os

env_vars = dotenv_values(".env")

Username = env_vars.get("Username")
Assistantname = env_vars.get("Assistantname")


DefaultMessage = f'''{Username} : Hello {Assistantname}, How are you?
{Assistantname} Welcome {Username}. I am doing well. How may i help you?'''
subprocesses = []
Functions = ["open", "close", "play", "system", "content", "google search", "youtube search"]

def MainExecution():
    TaskExecution = False
    ImageExecution = False 
    ImageGenerationQuery = ""
    Query = input("enter command: ")
    if Query != "":
        Decision = FirstLayerDMM(Query)
        print("")
        print(f"Decision: {Decision}") 
        print("")
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
                elif "realtime" in Queries:
                    QueryFinal = Queries.replace("realtime ", "")
                    Answer = RealtimeSearchEngine(QueryFinal)
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