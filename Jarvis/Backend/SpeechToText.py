import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import dotenv_values
import mtranslate as mt

# Load environment variables
env_vars = dotenv_values(".env")
InputLanguage = env_vars.get("InputLanguage")  # Default to English if not set

# Create Speech Recognition HTML
HtmlCode = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <title>Speech Recognition</title>
</head>
<body>
    <button id="start" onclick="startRecognition()">Start Recognition</button>
    <button id="end" onclick="stopRecognition()">Stop Recognition</button>
    <p id="output"></p>
    <script>
        const output = document.getElementById('output');
        let recognition;

        function startRecognition() {{
            recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
            recognition.lang = "{InputLanguage}";
            recognition.continuous = true;

            recognition.onresult = function(event) {{
                const transcript = event.results[event.results.length - 1][0].transcript;
                output.textContent += transcript + " ";
            }};

            recognition.onend = function() {{
                recognition.start();
            }};
            recognition.start();
        }}

        function stopRecognition() {{
            recognition.stop();
        }}
    </script>
</body>
</html>'''

# Save HTML file
os.makedirs("Data", exist_ok=True)
html_path = os.path.abspath("Data/Voice.html")
with open(html_path, "w") as f:
    f.write(HtmlCode)

current_dir = os.getcwd()

# Chrome WebDriver setup
chrome_options = Options()
chrome_options.add_argument("--use-fake-ui-for-media-stream")
chrome_options.add_argument("--use-fake-device-for-media-stream")

# REMOVE HEADLESS MODE (since speech recognition needs UI)
# chrome_options.add_argument("--headless=new")  # Commented out

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# Set Assistant Status
TempDirPath = rf"{current_dir}/Frontend/Files"

def SetAssistantStatus(Status):
    with open(rf"{TempDirPath}/Status.data", "w", encoding="utf-8") as file:
        file.write(Status)

# Modify Query Formatting
def QueryModifier(Query):
    new_query = Query.lower().strip()
    query_words = new_query.split()
    question_words = ["how", "what", "where", "when", "who", "why", "which", "whose", "whom", "can you", "what's"]

    if any(word + " " in new_query for word in question_words):
        if query_words[-1][-1] in ['.', '?', '!']:
            new_query = new_query[:-1] + "?"
        else:
            new_query += "?"

    return new_query.capitalize()

# Translate Text to English
def UniversalTranslator(Text):
    return mt.translate(Text, "en", "auto").capitalize()

# Speech Recognition Function
def SpeechRecognition():
    ak = html_path.replace('\\', '/')
    driver.get(f"file:///{ak}")
    driver.find_element(By.ID, "start").click()

    while True:
        try:
            Text = driver.find_element(By.ID, "output").text.strip()

            if Text:
                driver.find_element(By.ID, "end").click()
                
                if InputLanguage.lower().startswith("en"):
                    return QueryModifier(Text)
                else:
                    SetAssistantStatus("Translating ...")
                    return QueryModifier(UniversalTranslator(Text))

        except Exception as e:
            print(f"Error: {e}")
            break  # Exit loop if there's an error

# Main Execution
if __name__ == "__main__":
    while True:
        print("Listening... Speak now!")
        Text = SpeechRecognition()
        print("You said:", Text)
