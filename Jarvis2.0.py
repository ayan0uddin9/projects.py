import datetime
import pyttsx3
import speech_recognition as sr
import tkinter as tk
from threading import Thread

# Initialize speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)
engine.setProperty('voice', engine.getProperty('voices')[1].id)  # Change index for different voice

def speak(message):
    engine.say(message)
    engine.runAndWait()

def get_time_and_date():
    now = datetime.datetime.now()
    date_str = now.strftime("%A, %d %B %Y")
    time_str = now.strftime("%I:%M %p")
    return f"Hello Ayan. Today is {date_str}, and the time is {time_str}."

def jarvis_action():
    message = get_time_and_date()
    speak(message)
def jarvis_action():
    message = get_time_and_date()
    speak(message)

def listen_for_wake_word():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for wake word 'Jarvis'...")
        while True:
            try:
                audio = recognizer.listen(source)
                command = recognizer.recognize_google(audio).lower()
                if "jarvis" in command:
                    print("Wake word detected!")
                    jarvis_action()
            except sr.UnknownValueError:
                pass
            except sr.RequestError:
                print("Speech recognition service error")

def start_listening():
    Thread(target=listen_for_wake_word, daemon=True).start()

# GUI setup
app = tk.Tk()
app.title("Jarvis Assistant")
app.geometry("300x150")
app.configure(bg="#1e1e1e")

label = tk.Label(app, text="Jarvis is online", font=("Arial", 14), fg="white", bg="#1e1e1e")
label.pack(pady=10)

button = tk.Button(app, text="Speak Time & Date", command=jarvis_action, bg="#007acc", fg="white", font=("Arial", 12))
button.pack(pady=10)

start_listening()
app.mainloop()
# jarvis_action()


