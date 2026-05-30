# 🧠 ELIAS: Explainable Logic Intelligent Automation System

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Offline](https://img.shields.io/badge/Environment-100%25%20Offline-success)
![Security](https://img.shields.io/badge/Security-Biometric%20FaceID-red)
![License](https://img.shields.io/badge/License-MIT-green)

**ELIAS** is a highly secure, 100% offline, voice-driven desktop automation agent. Unlike traditional cloud-based assistants (Siri, Alexa) that suffer from network latency and severe data privacy risks, ELIAS processes all Natural Language Processing (NLP) locally. It bridges the gap between acoustic speech recognition and physical operating system execution using Robotic Process Automation (RPA) and fuzzy-matching logic.

Designed for high-security environments, clinical workstations, and users with motor impairments, ELIAS provides superhuman desktop navigation capabilities without ever connecting to the internet.

---

## ✨ Key Features

* **Biometric Facial Security:** The system remains locked and deaf until it positively identifies the authorized owner using 128-D facial embeddings and Euclidean distance mapping.
* **Zero-Latency Offline NLP:** Utilizes the Vosk API to extract Mel-Frequency Cepstral Coefficients (MFCCs) and translate speech to text entirely on the local CPU.
* **Deterministic Fuzzy Matching:** Implements the Levenshtein Distance algorithm as a phonetic spell-checker to correct misheard commands (e.g., auto-correcting "open X L" to "open Excel").
* **Physical Desktop Actuation (RPA):** Bypasses standard OS APIs to inject low-level hardware interrupts, allowing ELIAS to type dictated documents at 200+ WPM, navigate tabs, and auto-save files.
* **Multithreaded Architecture:** Maintains a responsive, modern CustomTkinter dashboard while the microphone loop continuously runs in a daemon thread.

---

## 📂 System Architecture & File Structure

The project is built on a highly modular architecture, separating sensory input from logical routing and physical execution.

### `app.py` (The Front-End Router)
The central hub of the application. It launches the `CustomTkinter` GUI, handles the asynchronous multithreading for the audio loop, and acts as the primary traffic controller between the user's voice and the system's brain.

### `security.py` (The Biometric Gatekeeper)
Triggered upon launch, this module accesses the webcam via OpenCV. It utilizes Histogram of Oriented Gradients (HOG) to detect faces, calculates a 128-point biometric map, and compares it against the authorized `owner.jpg`. The microphone only activates if the match threshold (< 0.6) is met.

### `voice_engine.py` (The Ears & Mouth)
The acoustic engine. It uses `sounddevice` to capture raw audio waveforms and feeds them into the local Vosk model to extract text. It also utilizes `pyttsx3` to provide offline audio feedback (text-to-speech) back to the user.

### `file_system.py` (The Brain & Logic)
The cognitive routing center. This file houses the "Extreme Phonetic Alias Dictionaries." It receives transcribed text, calculates the Levenshtein distance to account for acoustic errors, and deterministically maps the intent to specific Windows shell commands or execution paths.

### `rpa_engine.py` (The Hands & Execution)
The physical actuator. Built using `PyAutoGUI`, this module takes verified commands and simulates physical human actions—pressing hotkeys (Ctrl+T, Alt+F4), scrolling, navigating with arrow keys, and typing out full dictated documents automatically.

---

## 🚀 Installation & Setup

### Prerequisites
1. Python 3.8+ installed on your local machine.
2. A working webcam and microphone.
3. The offline Vosk language model.

### Step-by-Step Guide
1. **Clone the repository:**
```bash
   git clone [https://github.com/YourUsername/ELIAS.git](https://github.com/YourUsername/ELIAS.git)
   cd ELIAS
Install the required libraries:

Bash
   pip install customtkinter opencv-python face_recognition pyaudio sounddevice vosk pyttsx3 pyautogui Levenshtein
Set up the Offline Model:

Download the vosk-model-small-en-us from the official Vosk website.

Extract the folder, rename it strictly to model, and place it in the root directory of this project.

Set up Biometrics:

Take a clear photo of your face, name it owner.jpg, and place it in the root directory.

Run the application:

Bash
   python app.py
🛣️ Future Roadmap
Cross-Platform Support: Transitioning RPA hooks to fully support macOS and Linux environments.

SLM Integration: Replacing hardcoded alias dictionaries with localized Small Language Models (e.g., Llama-3-8B via Ollama) to allow for complex, conversational intent parsing while maintaining absolute privacy.

Low-Light Resilience: Implementing adaptive histogram equalization for the biometric scanner to operate in pitch-black environments.
