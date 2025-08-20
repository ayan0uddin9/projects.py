import pyttsx3
import datetime
import speech_recognition as sr



engine = pyttsx3.init()

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def getvoices():
    voices = engine.getProperty('voices')
    # print(voices[1].id)
    if voices == 1:
        engine.setProperty('voice', voices[0].id)
    
    if voices == 2:
        engine.setProperty('voice', voices[1].id)
    
    speak("hello this is jarvis")

def time():
        Time = datetime.datetime.now().strftime("%I:%M:%S")
        speak("the current time is:")
        speak(Time)

def date():
        year = int(datetime.datetime.now().year)
        month = int(datetime.datetime.now().month)
        date = int(datetime.datetime.now().day)
        speak("the current date is:")
        speak(year)
        speak(month)
        speak(date)

def wishme():
        speak("welcome back sir!")
        time()
        date()
        speak("jarvis at your service, please tell me how can i help you")
        wishme()
# def greeting():
#         hour = datetime.datetime.now().hour
#         if hour >= 6 and hour < 12:
#             speak("good morning sir!")
#         elif hour >= 12 and hour < 18:
#             speak("good afternoon sir!")
#         elif hour >= 18 and hour < 24:
#             speak("good evening sir!")
#         else:
#             speak("good night sir!")
    

        wishme()



# def wishme():
#         speak("welcome back sir!")
#         time()
#         date()
#         greeting()
#         speak("jarvis at your service, please tell me how can i help you")

        


    
# while True:
#     voice = int(input("Press 1 for male voice\nPress 2 for female voice\n"))
# #     speak(audio)
#     getvoices(voice)
def takeCommandCMD():
      query = input("please tell me how can i help you\n")
      return query

if __name__ == "__main__":
    wishme()
    while True:
        query = takeCommandCMD().lower()
        if 'time' in query:
            time()
        elif 'date' in query:
            date()
        elif 'offline' in query:
            quit()

    

    