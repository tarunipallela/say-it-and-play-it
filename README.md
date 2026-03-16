# 🎮 Say It & Play It – A Real-Time Voice-Controlled Game Experience

A fun, interactive **Python-based game where your voice becomes the controller.**  
Developed as part of our **Innovative Product Development (IPD)** project.

Inspired by the classic **Chrome Dino game**, this project demonstrates how **speech recognition can be used to control gameplay in real time**, making gaming more **interactive, accessible, and futuristic.**

---

# 🚀 Overview

**Say It & Play It** is an AI-powered mini-game where players control the character **entirely using voice commands** such as:

- **Jump**
- **Pause**
- **Resume**
- **Reset**
- **Exit**

The project explores how **voice interfaces can replace traditional input methods like keyboards**, opening doors to **hands-free gaming experiences**.

---

# 🧠 Features

🎤 **Real-Time Voice Recognition**  
Control the game using your microphone.

🦾 **Hands-Free Gameplay**  
No keyboard or mouse required.

⚡ **Instant Voice Response**  
Voice commands trigger immediate game actions.

🌐 **Offline Functionality**  
The game works completely offline.

🧩 **Customizable Commands**  
Developers can easily modify voice commands, assets, and logic.

🏃 **Character Sprint Mode**  
The character can perform **speed bursts for faster gameplay.**

⏸️ **Pause & Resume Commands**  
Players can **pause or resume the game using voice commands.**

🐲 **Beast Mode (Dynamic Difficulty)**  
Once the score crosses a **threshold**, the game enters **Beast Mode** where:

- Score multiplier becomes **x2**
- Game intensity increases

🏆 **Improved Scoring System**  
Score increases **only when an obstacle is successfully avoided**, ensuring fair gameplay.

---

# 🏗️ System Architecture

Player Voice → 🎧 Speech Recognition → 🧠 Command Processor  → 🎮 Game Engine (Pygame)

---

# 🧰 Technologies Used

| Component | Technology |
|----------|-----------|
| Programming Language | Python 3 |
| Game Engine | Pygame |
| Voice Recognition | SpeechRecognition |
| Text-to-Speech | pyttsx3 |
| IDE | VS Code |
| Version Control | GitHub |

---

# 🚀 Installation & Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/deepikaparasa6/sayit-playit.git
cd sayit-playit
```

### 2️⃣ Create a Virtual Environment

```bash
python -m venv myenv
```


### 3️⃣ Activate the Virtual Environment

```bash
myenv\Scripts\activate #windows
source myenv/bin/activate #macOS/Linux
```


### 4️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 5️⃣ Run the Game

```bash
python test_main2.py
```

⚠️ Make sure your microphone is connected and working properly.

## 🎮 Gameplay Commands

| Voice Command | Description | Effect in Game |
|---------------|-------------|----------------|
| Jump | Voice command to jump over obstacles | Character jumps |
| Pause | Stops the game temporarily | Game pauses |
| Resume | Continues the paused game | Game resumes |
| Exit   | Exits the game            | Game Exits    |
| Reset  | Resets the game to start position  | Game resets |

---

### Future Scope

🎯 Multilingual Voice Commands


Support commands in multiple languages.

🧠 Adaptive AI Gameplay


Game difficulty adapts based on player behavior.

🌍 Mobile Version


Voice + gesture-controlled mobile gaming experience.


---

###  Developed As Part Of

Innovative Product Development (IPD):


Exploring AI-powered interactive gaming using speech recognition.


---