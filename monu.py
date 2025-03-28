import speech_recognition as sr
import pyttsx3
import wikipedia
import pywhatkit
import os
import datetime
import requests
import psutil
import pyautogui
import random

# Initialize text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 170)

# Speak function
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Initialize microphone
def initialize_microphone(device_index=5):  # Default to Intel Smart Sound Technology mic
    try:
        mic = sr.Microphone(device_index=device_index)
        # Test if microphone is working
        with mic as source:
            return mic
    except Exception as e:
        print(f"Error with primary mic: {str(e)}")
        try:
            # Fallback to Realtek mic
            return sr.Microphone(device_index=17)
        except Exception as e:
            print(f"Error with fallback mic: {str(e)}")
            return None

# Listen function
def listen():
    try:
        recognizer = sr.Recognizer()
        mic = initialize_microphone()
        
        if mic is None:
            speak("Microphone initialization failed. Please check your audio devices.")
            return ""

        with mic as source:
            print("Adjusting for ambient noise...")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            print("Ready to listen! Speak now...")
            try:
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
                print("Audio captured, processing...")
                
                try:
                    command = recognizer.recognize_google(audio, language='en-US')
                    print(f"Recognized: {command}")
                    return command.lower()
                except sr.UnknownValueError:
                    print("Could not understand the audio")
                except sr.RequestError as e:
                    print(f"Could not request results; {e}")
                return ""
                
            except sr.WaitTimeoutError:
                print("Listening timed out. No speech detected.")
                return ""
                
    except Exception as e:
        print(f"Error during speech recognition: {str(e)}")
        return ""

# Free Weather Report (using Open-Meteo API)
def get_weather(city):
    url = f"https://wttr.in/{city}?format=%C+%t"
    response = requests.get(url)
    if response.status_code == 200:
        weather_data = response.text
        speak(f"The weather in {city} is {weather_data}")
        print(weather_data)
    else:
        speak("Sorry, I couldn't fetch the weather details.")

# Free News Updates (Using BBC RSS)
def get_news():
    url = "https://feeds.bbci.co.uk/news/rss.xml"
    response = requests.get(url)
    if response.status_code == 200:
        from xml.etree import ElementTree as ET
        root = ET.fromstring(response.text)
        items = root.findall(".//item")[:5]  # Get top 5 news headlines
        speak("Here are the top 5 news headlines:")
        for i, item in enumerate(items):
            news_title = item.find("title").text
            speak(f"News {i+1}: {news_title}")
            print(news_title)
    else:
        speak("Sorry, I couldn't fetch the news.")

# Offline Chatbot
def offline_chatbot(user_input):
    responses = {
        "hello": "Hello! How can I help you?",
        "how are you": "I'm just a program, but I'm functioning perfectly!",
        "who made you": "I was created using Python by a programmer like you!",
        "what is your name": "I am your AI assistant.",
        "goodbye": "Goodbye! Have a nice day!"
    }
    return responses.get(user_input, "I'm not sure how to respond to that.")

# System Control Commands
def system_commands(command):
    if "volume up" in command:
        pyautogui.press("volumeup", presses=5)
        speak("Volume increased.")
    elif "volume down" in command:
        pyautogui.press("volumedown", presses=5)
        speak("Volume decreased.")
    elif "mute" in command:
        pyautogui.press("volumemute")
        speak("Volume muted.")
    elif "shutdown" in command:
        speak("Shutting down the system.")
        os.system("shutdown /s /t 5")
    elif "restart" in command:
        speak("Restarting the system.")
        os.system("shutdown /r /t 5")
    elif "sleep" in command:
        speak("Putting the system to sleep.")
        os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
    else:
        return False
    return True

# Execute commands
def execute_command(command):
    if "wikipedia" in command:
        query = command.replace("wikipedia", "").strip()
        speak("Searching Wikipedia...")
        result = wikipedia.summary(query, sentences=2)
        speak(result)
        print(result)

    elif "play" in command:
        song = command.replace("play", "").strip()
        speak(f"Playing {song} on YouTube...")
        pywhatkit.playonyt(song)

    elif "search" in command:
        query = command.replace("search", "").strip()
        speak(f"Searching for {query} on Google...")
        pywhatkit.search(query)

    elif "open notepad" in command:
        speak("Opening Notepad")
        os.system("notepad")

    elif "open calculator" in command:
        speak("Opening Calculator")
        os.system("calc")

    elif "open command prompt" in command or "open cmd" in command:
        speak("Opening Command Prompt")
        os.system("start cmd")

    elif "time" in command:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The current time is {current_time}")
        print(f"Time: {current_time}")

    elif "date" in command:
        today_date = datetime.date.today().strftime("%B %d, %Y")
        speak(f"Today's date is {today_date}")
        print(f"Date: {today_date}")

    elif "weather" in command:
        speak("Which city do you want the weather for?")
        city = listen()
        if city:
            get_weather(city)

    elif "news" in command:
        get_news()

    elif "exit" in command or "quit" in command:
        speak("Goodbye! Have a great day!")
        exit()

    elif system_commands(command):
        pass  # System command executed

    else:
        chatbot_response = offline_chatbot(command)
        speak(chatbot_response)
        print(chatbot_response)

# Main loop
if __name__ == "__main__":
    speak("Hello, I am your assistant. How can I assist you?")
    while True:
        user_command = listen()
        if user_command:
            execute_command(user_command)
