# MindBridge

MindBridge is a private, offline mental health companion for students. It runs locally with Gradio + Python and uses a local Ollama model for chat.

## Current Workspace Layout

```text
.
├── README.md
├── prompts.txt
├── prompts2.txt
└── mindbridge/
	├── app.py
	├── exercises.py
	├── mood_tracker.py
	├── ollama_client.py
	├── prompt.py
	├── requirements.txt
	└── data/
		├── journal.json
		└── mood_log.json
```

## What The App Currently Includes

- Local chat UI (Gradio) with quick prompt buttons.
- Mood logging (1-5 scale + optional note) saved to local JSON.
- Mood history summary (last 7 entries + average score).
- Coping exercise selector with built-in exercises.
- Journal entry saving to local JSON.
- Crisis banner trigger when responses include iCall details.
- Offline/local model calls through Ollama at `http://localhost:11434`.

## Requirements

- Python 3.10+
- Ollama installed and running
- Gemma model pulled in Ollama (default in code: `gemma4:e4b`)

## Run Locally

From the workspace root:

```powershell
cd mindbridge
pip install -r requirements.txt
ollama pull gemma4:e4b
ollama serve
python app.py
```

Open: `http://127.0.0.1:7860`

## Data Storage

All local data is stored in:

- `mindbridge/data/mood_log.json`
- `mindbridge/data/journal.json`

No cloud database is used.

## Tech Stack

- Python
- Gradio
- Requests
- Local Ollama API
- JSON file storage

## Safety Note

MindBridge is a supportive companion, not a replacement for clinical care.
If someone is in crisis, the app guidance includes iCall: **9152987821**.
