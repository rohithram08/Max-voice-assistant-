import pyttsx3
import speech_recognition as sr
from datetime import datetime, timedelta
import sched
import time
import re
import requests
from weather import get_current_location, get_weather, get_weather_by_location
from ht import get_health_tips
from selenium_web import Inflow
from YT_auto import youtube
from News import *
import randfacts
from jokes import joke
from download import *
import os
import sys
from poetry import *
from resume_builder import *

# Initialize text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 180)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)  # Set to default voice

# Assistant setup
assistant_name = "Max"
s = sched.scheduler(time.time, time.sleep)
reminders = {}

# Initialize the speech recognizer
r = sr.Recognizer()

def speak(text):
    """Converts text to speech."""
    engine.say(text)
    engine.runAndWait()

def listen_to_voice(timeout=10):
    """Listens for voice input and returns recognized text."""
    with sr.Microphone() as source:
        r.energy_threshold = 4000
        r.adjust_for_ambient_noise(source, duration=1)
        print("Listening...")
        try:
            audio = r.listen(source, timeout=timeout, phrase_time_limit=5)
            text = r.recognize_google(audio)
            print(text)
            return text.lower()
        except sr.WaitTimeoutError:
            speak("I didn't hear anything. Please try again.")
            return None
        except sr.UnknownValueError:
            speak("Sorry, I didn't catch that. Could you please repeat?")
            return None
        except sr.RequestError as e:
            speak(f"Could not request results from Google Speech Recognition service; {e}")
            return None

def run_voice_assistant():
    global active
    active = False

    while True:
        if not active:
            print(f"Say 'wakeup {assistant_name}' to start.")
            speak(f"Say 'wakeup {assistant_name}' to start.")
            text = listen_to_voice()
            if text and f"wake up {assistant_name.lower()}" in text:
                active = True
                speak(f"Hello! {wish_me()} I am {assistant_name}, your voice assistant. How are you?")
                response_to_greeting = listen_to_voice()
                if response_to_greeting and "what about you" in response_to_greeting:
                    speak("I am having a good day!")
                speak("I am here to assist you. What can I do for you?")
        else:
            text = listen_to_voice()
            if text:
                if f"sleep mode {assistant_name.lower()}" in text:
                    speak(f"{assistant_name} going to sleep mode. Goodbye!")
                    active = False
                    sys.exit()
                handle_command(text)


def handle_command(text):
    """Processes commands based on the recognized text."""
    if f"sleep mode {assistant_name.lower()}" in text:
        speak(f"{assistant_name} going to sleep mode. Goodbye!")
        print(f"{assistant_name} going to sleep mode. Goodbye!")
        return
    elif "about you" in text:
        about_max()
    elif "your name" in text:
        speak(f"I am {assistant_name} , your friendly voice assistant.")
    elif "open google" in text:
        try:
            os.system("start https://www.google.com")
            speak("Opening Google.")
        except Exception as e:
            print(f"Error: {str(e)}")
            speak(f"Sorry, I couldn't open Google due to an error: {str(e)}")
    elif "wikipedia" in text:
        handle_wikipedia_request()
    elif "youtube" in text:
        handle_youtube_request()
    elif "news" in text:
        speak("Sure , I will read the news for you.")
        arr = news()
        for item in arr:
            print(item)
            speak(item)
    elif "fact" in text:
        handle_fact_request()
    elif "joke" in text:
        handle_joke_request()
    elif "weather" in text:
        handle_weather_request(text)
    elif "date" in text or "time" in text:
        handle_date_time_request(text)
    elif "remind me" in text:
        set_reminder(text)
    elif "health tips" in text:
        speak("Sure, here are some health tips.")
        get_health_tips()
    elif "calculate" in text:
        result = calculate(text)
        speak(result)
        print(result)
    elif "download" in text:
        handle_download_request(text)
    elif "open" in text.lower():
        query = text.lower().replace("open", "").strip()
        open_app(query)
    elif "poem" in text or "poetry" in text:
        handle_poetry_request()
    elif "resume" in text:
        build_resume()
    else:
        speak("I'm sorry, I can't do that yet.")
        

def open_app(app_name):
    try:
        print(f"Opening {app_name}...")
        speak(f"Sure, sir. Opening {app_name} now.")
        os.startfile(app_name)
    except Exception as e:
        error_message = f"Sorry, I could not open {app_name} due to an error: {e}"
        print(error_message)
        speak(error_message)

def handle_wikipedia_request():
    """Handles Wikipedia search requests."""
    speak("Sure, which topic should I look up?")
    print("Sure, which topic should I look up?")
    info = listen_to_voice()
    if info:
        speak(f"Searching {info} in Wikipedia")
        print(f"Searching {info} in Wikipedia")
        assist = Inflow()
        assist.get_info(info)
        assist.listen_for_exit_command()

def handle_youtube_request():
    """Handles YouTube video requests."""
    vid = youtube()
    if vid:
        speak(f"Playing {vid} on YouTube")
        assist = Inflow()  
        assist.play(vid)
        assist.youtube()

def handle_fact_request():
    """Provides a random fact."""
    fact = randfacts.get_fact()
    speak(f"Did you know that, {fact}")
    print(fact)

def handle_joke_request():
    """Tells a joke."""
    speak("Here's a joke for you.")
    j = joke()
    print(j[0])
    speak(j[0])
    print(j[1])
    speak(j[1])

def handle_weather_request(text):
    """Provides weather information based on the command."""
    response_prefix = "Currently, "
    if "current" in text:
        current_location = get_current_location()
        if current_location:
            current_temp, current_desc = get_weather(current_location[0], current_location[1])
            if current_temp and current_desc:
                speak(response_prefix + f"the temperature is {current_temp}°C with {current_desc}")
            else:
                speak("I'm sorry, I couldn't retrieve the current weather information.")
        else:
            speak("I'm sorry, I couldn't determine your current location.")
    elif "location of" in text:
        location = text.split("location of")[1].strip()
        location_temp, location_desc = get_weather_by_location(location)
        if location_temp and location_desc:
            speak(response_prefix + f"in {location}, it is {location_temp}°C with {location_desc}")
        else:
            speak(f"I'm sorry, I couldn't retrieve the weather information for {location}.")

def handle_date_time_request(text):
    """Provides the current date or time based on the command."""
    today_date = datetime.now()
    if "date" in text and "time" in text:
        speak(f"Today is {today_date.strftime('%d')} of {today_date.strftime('%B')}. It's currently {today_date.strftime('%I:%M:%S %p')}")
    elif "date" in text:
        speak(f"Today is {today_date.strftime('%d')} of {today_date.strftime('%B')}")
    elif "time" in text:
        speak(f"It's currently {today_date.strftime('%I:%M:%S %p')}")

def wish_me():
    """Returns a greeting based on the current time."""
    hour = int(datetime.now().hour)
    if hour < 12:
        return "Good morning"
    elif hour < 18:
        return "Good afternoon"
    else:
        return "Good evening"

def calculate(text):
    """Calculates the result of a mathematical expression."""
    try:
        match = re.findall(r"[0-9+\-*/.]+", text)
        if match:
            calculation = "".join(match)
            result = eval(calculation)
            return f"The result is {result}."
        else:
            return "Invalid calculation."
    except Exception as e:
        return f"Error: {e}"

def about_max():
    """Provides information about the assistant."""
    details_about_max = [
        "I am Max, your voice assistant.",
        "I can help you with a variety of tasks such as checking the weather, setting reminders, and playing music.",
        "I am designed to make your daily tasks easier and more enjoyable.",
        "My goal is to provide assistance through voice commands and make your experience as seamless as possible."
    ]
    for detail in details_about_max:
        speak(detail)
        time.sleep(1)

def parse_time(text):
    """Parses time duration from the text and returns total seconds."""
    time_units = {'second': 1, 'minute': 60, 'hour': 3600}
    time_regex = r'(\d+)\s*(seconds?|minutes?|hours?)'
    matches = re.findall(time_regex, text)
    if matches:
        total_seconds = sum(int(num) * time_units[unit.rstrip('s')] for num, unit in matches)
        return total_seconds
    else:
        raise ValueError("No time specified")

def set_reminder(text):
    """Sets a reminder based on the command."""
    def reminder(message):
        print(f"Reminder: {message}")
        speak(f"Reminder: {message}")

    if "remind me to" in text:
        try:
            parts = text.split("remind me to")
            reminder_msg = parts[1].strip()
            time_part = text.split()[-2:]
            if len(time_part) == 2:
                units = {"second": 1, "minute": 60, "hour": 3600}
                if time_part[1].rstrip('s') in units:
                    reminder_time = int(time_part[0]) * units[time_part[1].rstrip('s')]
                    s.enter(reminder_time, 1, reminder, (reminder_msg,))
                    reminder_time_delta = timedelta(seconds=reminder_time)
                    reminder_datetime = datetime.now() + reminder_time_delta
                    speak(f"Reminder set for: {reminder_msg} at {reminder_datetime.strftime('%I:%M %p')}.")
                else:
                    speak("Invalid time unit specified.")
            else:
                speak("Could not understand the time duration.")
        except Exception as e:
            print(f"Error: {str(e)}")
            speak(f"I'm sorry, there was an error setting the reminder: {str(e)}")

def handle_download_request(text):
    """Handles download requests."""
    pass

run_voice_assistant()