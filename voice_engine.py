import pyttsx3
import json
import queue
import sys
import sounddevice as sd
from vosk import Model, KaldiRecognizer

# --- 1. OFFLINE TEXT-TO-SPEECH ---
engine = pyttsx3.init()
engine.setProperty('rate', 175)

def speak(text):
    engine.say(text)
    engine.runAndWait()

# --- 2. LOAD OFFLINE SPEECH RECOGNITION MODEL ---
try:
    # This looks for the "model" folder you downloaded
    model = Model("model")
    recognizer = KaldiRecognizer(model, 16000)
except Exception:
    print("❌ ERROR: Offline 'model' folder not found.")
    print("Please download vosk-model-small-en-us, extract it, rename it to 'model', and put it in this folder.")
    sys.exit(1)

# Audio queue for processing
q = queue.Queue()

def callback(indata, frames, time, status):
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))

# --- 3. THE OFFLINE LISTENER ---
def listen():
    """Listens completely locally without timing out."""
    with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                           channels=1, callback=callback):
        while True:
            data = q.get()
            if recognizer.AcceptWaveform(data):
                # Parse the JSON response from Vosk
                result = json.loads(recognizer.Result())
                command = result.get("text", "")
                
                # If a word was actually spoken, return it
                if command:
                    return command.lower()