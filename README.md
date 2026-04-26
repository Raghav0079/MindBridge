# 🧠 MindBridge

> A private, offline mental health companion for Indian students — powered by Gemma 4, running entirely on your device.

![Python](https://img.shields.io/badge/Python-3.10+-blue) ![License](https://img.shields.io/badge/License-CC--BY%204.0-green) ![Ollama](https://img.shields.io/badge/Runs%20on-Ollama-purple) ![Offline](https://img.shields.io/badge/100%25-Offline-orange)

---

## The Problem

Over **150 million Indians** need mental health support, yet fewer than 1 in 10 ever receive it. For students aged 18–25, the barriers are especially steep: stigma, cost, waitlists, and the very real fear that conversations will not stay private. Existing AI-based tools send your data to the cloud, require subscriptions, or are built for Western contexts and miss the nuances of Indian student life — hostel pressure, family expectations, competitive exams, and career anxiety.

**MindBridge was built to change that.**

---

## What MindBridge Does

MindBridge is a fully offline, privacy-first mental health companion that:

- **Listens and responds** with warmth using Gemma 4 running locally via Ollama — no internet required after setup
- **Tracks your mood** over time with a 1–5 scale and optional notes, stored locally
- **Guides you through coping exercises** — box breathing, 5-4-3-2-1 grounding, progressive muscle relaxation, body scan, and gratitude journaling
- **Provides a private journal** — entries never leave your device
- **Responds to crisis signals** — if distress is detected, it warmly surfaces the iCall helpline (9152987821), India's free, confidential counselling service
- **Speaks your context** — the system prompt is tailored for Indian student life, not a generic Western audience

---

## Why Gemma 4 + Ollama

This project is a direct entry for the **Ollama Special Technology Prize** in the Gemma 4 Good Hackathon.

Gemma 4 running via Ollama (`gemma4:e4b`) was chosen deliberately:

- **Edge deployment** — runs on a student's laptop CPU, no GPU required
- **True privacy** — no API calls, no telemetry, no data leaving the device
- **Accessibility** — works without a stable internet connection, critical in tier-2/3 Indian cities and college hostels with unreliable Wi-Fi
- **Lightweight footprint** — the E4B variant keeps memory usage low enough for everyday hardware

The entire AI inference happens at `http://localhost:11434`. Your words never travel further than your own machine.

---

## Features

| Feature | Details |
|---|---|
| 💬 AI Chat | Gemma 4 via Ollama, streamed locally |
| 📊 Mood Tracker | 1–5 scale with notes, last 7 entries + average |
| 🧘 Coping Exercises | 5 guided exercises, loaded into chat on demand |
| 📓 Private Journal | Text entries saved to local JSON, never synced |
| 🆘 Crisis Detection | Auto-surface iCall (9152987821) when needed |
| 🔒 100% Offline | Zero cloud dependencies after initial model pull |
| ⚡ Quick Prompts | One-tap buttons for common emotional states |

---

## Tech Stack

| Layer | Technology |
|---|---|
| Language Model | Gemma 4 E4B via Ollama |
| UI | Gradio 5.x |
| Backend | Python 3.10+ |
| Storage | Local JSON files |
| HTTP | Requests (Ollama API) |
| Platform | Cross-platform (Windows, macOS, Linux) |

---

## Getting Started

### Prerequisites

- Python 3.10 or higher
- [Ollama](https://ollama.com) installed and running

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/Raghav0079/MindBridge.git
cd MindBridge

# 2. Install dependencies
cd mindbridge
pip install -r requirements.txt

# 3. Pull the Gemma 4 model
ollama pull gemma4:e4b

# 4. Start Ollama (in a separate terminal)
ollama serve

# 5. Launch MindBridge
python app.py
```

Open your browser at: **http://127.0.0.1:7860**

---

## Project Structure

```
MindBridge/
├── README.md
├── LICENSE
├── prompts.txt
├── prompts2.txt
└── mindbridge/
    ├── app.py              # Gradio UI and event wiring
    ├── exercises.py        # Coping exercise catalog
    ├── mood_tracker.py     # Local mood log (JSON)
    ├── ollama_client.py    # Ollama API wrapper
    ├── prompt.py           # Gemma 4 system prompt
    ├── requirements.txt
    └── data/
        ├── journal.json    # Private journal (local only)
        └── mood_log.json   # Mood history (local only)
```

---

## Privacy & Safety

**All data stays on your device.** MindBridge writes only to:
- `mindbridge/data/mood_log.json`
- `mindbridge/data/journal.json`

No analytics, no telemetry, no cloud sync — ever.

**MindBridge is a supportive companion, not a clinical tool.** It does not diagnose, treat, or prescribe. If you or someone you know is in crisis:

> 🆘 **iCall Helpline: 9152987821** — Free, confidential counselling, Monday–Saturday, 8am–10pm IST

---

## Impact Track Alignment

MindBridge targets two Impact Track categories:

- **Digital Equity & Inclusivity** — Works offline in low-connectivity environments, designed for the Indian student demographic, zero cost to run after setup
- **Health & Sciences** — Bridges the mental health access gap using local AI, lowers the barrier to first-contact support

---

## License

This project is licensed under the **Creative Commons Attribution 4.0 International (CC BY 4.0)** license. See [LICENSE](LICENSE) for full terms.

---

## Acknowledgements

- [Google Gemma 4](https://ai.google.dev/gemma) — the open model powering MindBridge
- [Ollama](https://ollama.com) — local model serving
- [iCall](https://icallhelpline.org) — India's student mental health helpline
- [Gradio](https://gradio.app) — rapid UI framework

---

*Built for the Gemma 4 Good Hackathon — Ollama Special Technology Track*
