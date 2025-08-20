import os
import random
import mimetypes
from datetime import datetime
from flask import Flask, render_template, request, jsonify, send_file, abort
import pyttsx3

# Optional voice support (PocketSphinx). App still works without it.
VOICE_READY = True
try:
    import speech_recognition as sr
except ImportError:
    VOICE_READY = False

app = Flask(__name__)

# ---------- CONFIG ----------
MUSIC_DIR = os.path.expanduser(r"~/Music")  # Change if you store music elsewhere
ALLOWED_EXTS = (".mp3", ".wav", ".flac", ".m4a", ".aac", ".ogg")

# Common Windows apps; extend as you like
APP_PATHS = {
    "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "notepad": "notepad.exe",
    "calc": "calc.exe",
}

# ---------- GLOBALS ----------
MEMORY = {}
MUSIC_LIBRARY = {}  # id -> absolute path
NEXT_TRACK_ID = 1

# ---------- UTILITIES ----------
def speak(text: str):
    # Speaks from your PC speakers (server-side), and returns text for UI
    engine = pyttsx3.init()
    engine.setProperty("rate", 170)
    print(f"Jarvis: {text}")
    engine.say(text)
    engine.runAndWait()

def scan_music():
    global MUSIC_LIBRARY, NEXT_TRACK_ID
    MUSIC_LIBRARY.clear()
    NEXT_TRACK_ID = 1
    if not os.path.isdir(MUSIC_DIR):
        return
    for root, _, files in os.walk(MUSIC_DIR):
        for f in files:
            if f.lower().endswith(ALLOWED_EXTS):
                MUSIC_LIBRARY[NEXT_TRACK_ID] = os.path.join(root, f)
                NEXT_TRACK_ID += 1

def pick_random_track():
    if not MUSIC_LIBRARY:
        return None, None, None
    track_id = random.choice(list(MUSIC_LIBRARY.keys()))
    path = MUSIC_LIBRARY[track_id]
    title = os.path.basename(path)
    return track_id, path, title

def open_application_by_name(name: str):
    key = name.strip().lower()
    if key in APP_PATHS:
        path = APP_PATHS[key]
        try:
            os.startfile(path)
            return True, "Opening application."
        except Exception as e:
            return False, f"Failed to open: {e}"
    return False, "I don't know that app."

def tell_date_time():
    now = datetime.now()
    return f"Today is {now.strftime('%A, %d %B %Y')}. The time is {now.strftime('%I:%M %p')}."

def tell_joke():
    jokes = [
        "Why don’t skeletons fight each other? They don’t have the guts.",
        "I told my computer I needed a break… it won’t stop sending KitKat ads.",
        "Why was the math book sad? Too many problems.",
        "Debugging: being the detective in a crime movie where you are also the murderer."
    ]
    return random.choice(jokes)

def solve_math(expr: str):
    try:
        # Extremely limited eval for safety
        result = eval(expr, {"__builtins__": {}}, {})
        return f"The answer is {result}"
    except Exception:
        return "I couldn't calculate that."

def remember_inline(text: str):
    # Supports: "remember name is Ayan" or "remember name Ayan"
    msg = text.strip()
    if " is " in msg:
        parts = msg.split(" is ", 1)
        key = parts[0].strip()
        value = parts[1].strip()
    else:
        parts = msg.split(maxsplit=1)
        if len(parts) == 2:
            key, value = parts[0].strip(), parts[1].strip()
        else:
            return "Please say like: remember name is Ayan."
    MEMORY[key] = value
    return f"Got it. I'll remember that {key} is {value}."

def recall_key(key: str):
    key = key.strip()
    if key in MEMORY:
        return f"You told me {key} is {MEMORY[key]}."
    return f"I don't remember anything about {key}."

# ---------- COMMAND ROUTER ----------
def process_command(command: str):
    if not command:
        return {"reply": "Say or type a command.", "speak": True}

    cmd = command.lower().strip()

    # Greetings
    if any(w in cmd for w in ["hello", "hi", "hey"]):
        reply = "Hello Ayan, nice to talk to you."
        speak(reply)
        return {"reply": reply, "speak": False}

    # Time / Date
    if "time" in cmd or "date" in cmd:
        reply = tell_date_time()
        speak(reply)
        return {"reply": reply, "speak": False}

    # Open apps: "open chrome", "open notepad", "open calc"
    if cmd.startswith("open "):
        app_name = cmd.replace("open ", "", 1).strip()
        ok, msg = open_application_by_name(app_name)
        if ok:
            speak(msg)
        return {"reply": msg, "speak": False}

    # Play music
    if "play music" in cmd or cmd == "music":
        if not MUSIC_LIBRARY:
            scan_music()
        track_id, _, title = pick_random_track()
        if track_id is None:
            reply = "No music files found in your Music folder."
            speak(reply)
            return {"reply": reply, "speak": False}
        reply = f"Playing {title}"
        speak(reply)
        return {"reply": reply, "speak": False, "music": {"id": track_id, "title": title}}

    # Math: "calculate 2+2", "calc 12/3"
    if cmd.startswith("calculate ") or cmd.startswith("calc "):
        expr = command.split(" ", 1)[1]
        reply = solve_math(expr)
        speak(reply)
        return {"reply": reply, "speak": False}

    # Joke
    if "joke" in cmd:
        reply = tell_joke()
        speak(reply)
        return {"reply": reply, "speak": False}

    # Remember: "remember name is Ayan" or "remember name Ayan"
    if cmd.startswith("remember "):
        rest = command.split(" ", 1)[1]
        reply = remember_inline(rest)
        speak(reply)
        return {"reply": reply, "speak": False}

    # Recall: "recall name" or "what is name"
    if cmd.startswith("recall "):
        key = command.split(" ", 1)[1]
        reply = recall_key(key)
        speak(reply)
        return {"reply": reply, "speak": False}
    if cmd.startswith("what is "):
        key = command.replace("what is ", "", 1)
        reply = recall_key(key)
        speak(reply)
        return {"reply": reply, "speak": False}

    # Exit
    if "quit" in cmd or "exit" in cmd:
        reply = "I won't shut down the server, but I'll be right here when you need me."
        speak(reply)
        return {"reply": reply, "speak": False}

    reply = "I'm not programmed for that yet."
    speak(reply)
    return {"reply": reply, "speak": False}

# ---------- ROUTES ----------
@app.route("/")
def index():
    # Initial scan on first load
    if not MUSIC_LIBRARY:
        scan_music()
    return render_template("index.html", voice_ready=VOICE_READY)

@app.post("/api/command")
def api_command():
    data = request.get_json(silent=True) or {}
    command = data.get("command", "")
    result = process_command(command)
    return jsonify(result)

@app.get("/api/voice")
def api_voice():
    if not VOICE_READY:
        return jsonify({"ok": False, "error": "Voice not available. Install SpeechRecognition and pocketsphinx."}), 400
    try:
        r = sr.Recognizer()
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source, duration=0.5)
            audio = r.listen(source, phrase_time_limit=5)
        try:
            text = r.recognize_sphinx(audio)
            return jsonify({"ok": True, "text": text})
        except Exception as e:
            return jsonify({"ok": False, "error": f"Couldn't understand: {e}"}), 400
    except Exception as e:
        return jsonify({"ok": False, "error": f"Microphone error: {e}"}), 400

@app.get("/music/stream/<int:track_id>")
def music_stream(track_id):
    path = MUSIC_LIBRARY.get(track_id)
    if not path or not os.path.isfile(path):
        abort(404)
    mime, _ = mimetypes.guess_type(path)
    try:
        return send_file(path, mimetype=mime or "audio/mpeg", as_attachment=False, conditional=True)
    except Exception:
        abort(500)

@app.get("/api/music/next")
def api_music_next():
    if not MUSIC_LIBRARY:
        scan_music()
    track_id, _, title = pick_random_track()
    if track_id is None:
        return jsonify({"ok": False, "error": "No music files found."}), 404
    return jsonify({"ok": True, "music": {"id": track_id, "title": title}})

if __name__ == "__main__":
    # Run on localhost
    app.run(host="127.0.0.1", port=5000, debug=False)

# jarvis