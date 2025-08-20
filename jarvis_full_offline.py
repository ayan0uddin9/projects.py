import pyttsx3
from datetime import datetime
import os
import random
import pandas as pd
import numpy as np

# Try to load speech recognition, else fallback to keyboard only
try:
    import speech_recognition as sr
    mic_available = True
except ImportError:
    mic_available = False

# ---------- SPEAK ----------
def speak(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 170)
    print(f"Jarvis: {text}")
    engine.say(text)
    engine.runAndWait()

# ---------- LISTEN ----------
def listen():
    if mic_available:
        try:
            recognizer = sr.Recognizer()
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                print("🎤 Listening...")
                audio = recognizer.listen(source)
            try:
                command = recognizer.recognize_sphinx(audio)
                print(f"🗣 You said: {command}")
                return command.lower()
            except Exception:
                speak("Didn't catch that. Type your command instead.")
                return input("Type your command: ").lower()
        except Exception:
            speak("Mic not available. Switching to keyboard.")
            return input("Type your command: ").lower()
    else:
        return input("Type your command: ").lower()

# ---------- FUNCTIONS ----------
def tell_date_time():
    now = datetime.now()
    speak(f"Today is {now.strftime('%A, %d %B %Y')}. The time is {now.strftime('%I:%M %p')}.")

def open_application(path):
    if os.path.exists(path):
        os.startfile(path)
        speak("Opening application.")
    else:
        speak("Application not found.")

def play_random_music():
    music_folder = os.path.expanduser(r"~/Music")
    music_files = []
    for root, dirs, files in os.walk(music_folder):
        for file in files:
            if file.lower().endswith((".mp3", ".wav", ".flac")):
                music_files.append(os.path.join(root, file))
    if music_files:
        song = random.choice(music_files)
        os.startfile(song)
        speak(f"Playing {os.path.basename(song)}")
    else:
        speak("No music files found in your Music folder.")

def solve_math(expr):
    try:
        result = eval(expr, {"__builtins__": {}})
        speak(f"The answer is {result}")
    except Exception:
        speak("I couldn't calculate that.")

def tell_joke():
    jokes = [
        "Why don’t skeletons fight each other? They don’t have the guts.",
        "Why did the computer go to the doctor? It caught a virus.",
        "Why was the math book sad? Too many problems."
    ]
    speak(random.choice(jokes))

# ---------- SIMPLE MEMORY ----------
memory = {}

def remember_item(key, value):
    memory[key] = value
    speak(f"Got it. I’ll remember that {key} is {value}.")

def recall_item(key):
    if key in memory:
        speak(f"You told me {key} is {memory[key]}.")
    else:
        speak(f"I don't remember anything about {key}.")

# ---------- MAIN ----------
def main():
    speak("Jarvis online. How can I help you, Ayan?")
    tell_date_time()

    while True:
        command = listen()

        if not command:
            continue

        if "time" in command or "date" in command:
            tell_date_time()
        elif "hello" in command:
            speak("Hello Ayan, nice to talk to you.")
        elif "open" in command:
            if "chrome" in command:
                open_application(r"C:\Program Files\Google\Chrome\Application\chrome.exe")
            elif "notepad" in command:
                open_application("notepad.exe")
            else:
                speak("I don't know that app.")
        elif "play music" in command:
            play_random_music()
        elif "calculate" in command:
            expr = input("Enter math expression: ")
            solve_math(expr)
        elif "joke" in command:
            tell_joke()
        elif "remember" in command:
            speak("What should I remember?")
            key = input("Key: ").lower()
            speak("What’s the value?")
            value = input("Value: ")
            remember_item(key, value)
        elif "recall" in command:
            speak("What do you want me to recall?")
            key = input("Key: ").lower()
            recall_item(key)
        elif "quit" in command or "exit" in command:
            speak("Goodbye Ayan.")
            break
        else:
            speak("Not programmed for that yet.")

if __name__ == "__main__":
    main()

# jarvis    