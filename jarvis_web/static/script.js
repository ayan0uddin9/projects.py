const logEl = document.getElementById("log");
const inputEl = document.getElementById("commandInput");
const sendBtn = document.getElementById("sendBtn");
const voiceBtn = document.getElementById("voiceBtn");
const audioEl = document.getElementById("audio");
const nowPlayingEl = document.getElementById("nowPlaying");
const nextSongBtn = document.getElementById("nextSongBtn");

function appendLog(role, text) {
  const div = document.createElement("div");
  div.className = `msg ${role}`;
  div.textContent = text;
  logEl.prepend(div);
}

async function sendCommand(text) {
  if (!text.trim()) return;
  appendLog("you", text);
  inputEl.value = "";
  try {
    const res = await fetch("/api/command", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({ command: text })
    });
    const data = await res.json();
    appendLog("jarvis", data.reply || "...");
    if (data.music && data.music.id) {
      const url = `/music/stream/${data.music.id}`;
      audioEl.src = url;
      audioEl.play().catch(() => {});
      nowPlayingEl.textContent = `Now playing: ${data.music.title}`;
    }
  } catch (e) {
    appendLog("jarvis", "Network error while sending command.");
  }
}

sendBtn.addEventListener("click", () => {
  sendCommand(inputEl.value);
});

inputEl.addEventListener("keydown", (e) => {
  if (e.key === "Enter") sendCommand(inputEl.value);
});

voiceBtn.addEventListener("click", async () => {
  if (voiceBtn.dataset.enabled !== "1") {
    appendLog("jarvis", "Voice not available. Install SpeechRecognition and pocketsphinx.");
    return;
  }
  voiceBtn.disabled = true;
  voiceBtn.textContent = "Listening...";
  appendLog("jarvis", "Listening via PC microphone...");
  try {
    const res = await fetch("/api/voice");
    const data = await res.json();
    if (data.ok) {
      appendLog("you", data.text);
      await sendCommand(data.text);
    } else {
      appendLog("jarvis", data.error || "Couldn't understand.");
    }
  } catch (e) {
    appendLog("jarvis", "Voice error.");
  } finally {
    voiceBtn.disabled = false;
    voiceBtn.textContent = "Listen";
  }
});

nextSongBtn.addEventListener("click", async () => {
  try {
    const res = await fetch("/api/music/next");
    const data = await res.json();
    if (data.ok) {
      const { id, title } = data.music;
      const url = `/music/stream/${id}`;
      audioEl.src = url;
      audioEl.play().catch(() => {});
      nowPlayingEl.textContent = `Now playing: ${title}`;
      appendLog("jarvis", `Playing ${title}`);
    } else {
      appendLog("jarvis", data.error || "No music found.");
    }
  } catch (e) {
    appendLog("jarvis", "Error picking a song.");
  }
});
