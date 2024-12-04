import speech_recognition as sr
import webbrowser
import pyttsx3
import pyjokes
import musicLibrary
import requests
from openai import OpenAI
from gtts import gTTS
import pygame
import os
import psutil

recognizer = sr.Recognizer()
engine = pyttsx3.init() 
newsapi = "<Your Key Here>"

def speak(text):
    engine.say(text)
    engine.runAndWait()
    engine.setProperty('rate', 170)  # Speed of speech
    # engine.setProperty('pitch', 120)  # Adjust pitch (not supported on all systems)
    engine.setProperty('volume', 5.0)  # Volume (0.0 to 1.0)


# def speak(text):
#     tts = gTTS(text)
#     tts.save('jarvis.mp3') 

#     # Initialize Pygame mixer
#     pygame.mixer.init()

#     # Load the MP3 file
#     pygame.mixer.music.load('jarvis.mp3')

#     # Play the MP3 file
#     pygame.mixer.music.play()

#     # Keep the program running until the music stops playing
#     while pygame.mixer.music.get_busy():
#         pygame.time.Clock().tick(10)
    
#     pygame.mixer.music.unload()
#     os.remove("jarvis.mp3") 

def system_status():
    battery = psutil.sensors_battery()
    cpu_usage = psutil.cpu_percent(interval=1)
    disk_usage = psutil.disk_usage('/').percent
    status = f"Battery is at {battery.percent}%. CPU usage is at {cpu_usage}%. Disk usage is at {disk_usage}%."
    speak(status)

def tell_joke():
    joke = pyjokes.get_joke()
    speak(joke)

reminders = []

def add_reminder(reminder):
    reminders.append(reminder)
    speak("Reminder added.")

def check_reminders():
    if reminders:
        for idx, reminder in enumerate(reminders, start=1):
            speak(f"Reminder {idx}: {reminder}")
    else:
        speak("You have no reminders.")

# def aiProcess(command):
#     client = OpenAI(api_key="<Your Key Here>",
#     )

#     completion = client.chat.completions.create(
#     model="gpt-3.5-turbo",
#     messages=[
#         {"role": "system", "content": "You are a virtual assistant named jarvis skilled in general tasks like Alexa and Google Cloud. Give short responses please"},
#         {"role": "user", "content": command}
#     ]
#     )

#     return completion.choices[0].message.content

def get_weather(city):
    api_key = "<Your OpenWeatherMap API Key>"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        weather = data['weather'][0]['description']
        temperature = data['main']['temp']
        speak(f"The current weather in {city} is {weather} with a temperature of {temperature} degrees Celsius.")
    else:
        speak("I couldn't fetch the weather information.")

def open_file(file_name):
    for root, dirs, files in os.walk("D:\\"):  # Adjust path for your system
        if file_name in files:
            os.startfile(os.path.join(root, file_name))
            speak(f"Opening {file_name}")
            return
    speak("File not found.")
def open_application(app_name):
    apps = {
        "notepad": "notepad.exe",
        "calculator": "calc.exe",
        "chrome": r"C:\Users\ayush verma.DESKTOP-DJ04K8V\AppData\Local\Google\Chrome\Application\chrome.exe",
        "vscode": r"C:\Users\ayush verma.DESKTOP-DJ04K8V\AppData\Local\Programs\Microsoft VS Code\Code.exe"
    }
    if app_name in apps:
        try:
            os.startfile(apps[app_name])
            speak(f"Opening {app_name}.")
        except FileNotFoundError:
            speak(f"Could not find the application path for {app_name}. Please check the path.")
    else:
        speak("Application not found.")
def power_action(action):
    actions = {
        "shutdown": "shutdown /s /t 1",
        "restart": "shutdown /r /t 1",
        "lock": "rundll32.exe user32.dll,LockWorkStation"
    }
    if action in actions:
        os.system(actions[action])
        speak(f"System will {action} shortly.")
    else:
        speak("Action not recognized.")
def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = musicLibrary.music[song]
        webbrowser.open(link)
    elif "set reminder" in c.lower():
        reminder = c.lower().replace("set reminder", "").strip()
        add_reminder(reminder)
    elif "check reminders" in c.lower():
        check_reminders()
    elif "joke" in c.lower():
        tell_joke()
    elif "system status" in c.lower():
        system_status()
    elif "open file" in c.lower():
        file_name = c.lower().replace("open file", "").strip()
        open_file(file_name)
    elif "open" in c.lower():
        app_name = c.lower().replace("open", "").strip()
        open_application(app_name)
    elif "news" in c.lower():
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}")
        if r.status_code == 200:
            # Parse the JSON response
            data = r.json()
            
            # Extract the articles
            articles = data.get('articles', [])
            
            # Print the headlines
            for article in articles:
                speak(article['title'])
    elif "shutdown" in c.lower() or "restart" in c.lower() or "lock" in c.lower():
        action = c.lower().strip()
        power_action(action)
    elif "sleep laptop" in c.lower():
        speak("Putting your laptop to sleep. Goodbye!")
        if os.name == "nt":  # Windows
            os.system("rundll32.exe powrprof.dll,SetSuspendState Sleep")
        elif os.name == "posix":  # macOS or Linux
            os.system("pmset sleepnow")  # macOS
            os.system("systemctl suspend")  # Linux
    elif "weather" in c.lower():
        city = c.lower().split("in")[-1].strip()
        get_weather(city)
    else:
        # Let OpenAI handle the request
        # output = aiProcess(c)
        # speak(output) 
        pass





if __name__ == "__main__":
    speak("Initializing Jarvis....")
    while True:
        # Listen for the wake word "Jarvis"
        # obtain audio from the microphone
        r = sr.Recognizer()
         
        print("recognizing...")
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = r.listen(source, timeout=2, phrase_time_limit=1)
            word = r.recognize_google(audio)
            if(word.lower() == "jarvis"):
                speak("How can I assist you today?")
                # Listen for command
                with sr.Microphone() as source:
                    print("Jarvis Active...")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)

                    processCommand(command)


        except Exception as e:
            print("Error; {0}".format(e))



