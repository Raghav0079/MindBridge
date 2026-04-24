# 🧠 MindBridge — Offline Mental Health Companion for Students

> A private, judgment-free mental health chat companion powered by Gemma 4, running fully offline via Ollama. No internet required. No data ever leaves your device.

---

## 🏆 Submission

- **Competition:** The Gemma 4 Good Hackathon (Kaggle × Google DeepMind)
- **Track:** Health & Sciences
- **Special Prize Target:** Ollama Prize
- **Demo Video:** [YouTube Link — add before submission]
- **Live Demo:** [Hugging Face Spaces Link — add before submission]

---

## 🎯 Problem Statement

Millions of students in India and across the developing world face anxiety, stress, and burnout with no access to mental health support. College counselors are scarce. Internet is unreliable. And privacy concerns stop many from seeking help online.

MindBridge solves this by running a compassionate, supportive AI companion **entirely on-device** — no cloud, no data collection, no subscription.

---

## ✨ Features

- 💬 **Chat-based companion** — empathetic, non-judgmental conversation
- 😊 **Mood check-in** — tracks how you feel at the start of each session
- 🌬️ **Coping exercises** — breathing techniques, grounding, journaling prompts
- 📓 **Journal** — private, local journaling with AI reflection
- 🔒 **100% offline** — powered by Gemma 4 via Ollama, zero data sent to cloud
- 🌐 **Works on low-end hardware** — runs on CPU with 16GB RAM

---

## 🛠️ Tech Stack

| Layer | Tool |
|---|---|
| Language Model | Google Gemma 4 (E4B) |
| Local Inference | Ollama |
| UI | Gradio |
| Backend | Python 3.10+ |
| Storage | Local JSON files |

---

## ⚙️ Setup Instructions

### 1. Prerequisites

- Python 3.10 or higher
- [Ollama](https://ollama.com) installed on your machine
- 16GB RAM minimum (runs CPU-only, no GPU needed)

### 2. Pull the Gemma 4 model

```bash
ollama pull gemma4:e4b
```

> This downloads ~9.6GB. Only needed once.

### 3. Clone this repository

```bash
git clone https://github.com/YOUR_USERNAME/mindbridge.git
cd mindbridge
```

### 4. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 5. Run MindBridge

```bash
python app.py
```

Then open your browser at: `http://localhost:7860`

---

## 📁 Project Structure

```
mindbridge/
├── app.py               # Gradio UI + main entry point
├── ollama_client.py     # Gemma 4 inference via Ollama API
├── prompt.py            # System prompt + companion personality
├── mood_tracker.py      # Session mood logging
├── exercises.py         # Coping exercises and journaling prompts
├── data/
│   ├── mood_log.json    # Local mood history
│   └── journal.json     # Local journal entries
├── requirements.txt
└── README.md
```

---

## 🔒 Privacy by Design

MindBridge is built with privacy as a core principle, not an afterthought:

- All conversations happen **locally** between you and Gemma 4
- No data is sent to any server or API
- No account or login required
- All mood logs and journal entries are stored as plain JSON on your own machine
- You can delete your data at any time by deleting the `data/` folder

---

## 🧠 How Gemma 4 Is Used

MindBridge uses **Gemma 4 E4B** running locally via Ollama's REST API (`http://localhost:11434`). The model is guided by a carefully crafted system prompt that:

- Establishes a warm, non-clinical, supportive tone
- Prevents the model from giving medical diagnoses
- Encourages users to seek professional help when needed
- Keeps conversations grounded, safe, and student-friendly

The companion uses Ollama's `/api/chat` endpoint with a rolling conversation history to maintain context within a session.

---

## 📸 Screenshots

> Add screenshots of the Gradio UI here before submission

---

## 🎬 Demo Video

> [YouTube Link — 3 minutes, shows the full user flow from mood check-in → conversation → coping exercise]

---

## ⚠️ Disclaimer

MindBridge is **not a replacement for professional mental health care**. It is a supportive tool designed to help students manage everyday stress and anxiety. If you are in crisis, please contact a mental health professional or a crisis helpline immediately.

**India Crisis Helpline:** iCall — 9152987821

---

## 📄 License

This project is licensed under **CC-BY 4.0** in accordance with the Gemma 4 Good Hackathon rules.

---

## 👤 Author

Built with ❤️ for the Gemma 4 Good Hackathon by Raghav Mishra . 
