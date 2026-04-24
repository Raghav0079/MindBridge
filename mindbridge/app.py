"""Main Gradio application for MindBridge."""

from __future__ import annotations

import json
import os
from datetime import datetime
from typing import Generator, cast

import gradio as gr

from exercises import get_exercise, list_exercises
from mood_tracker import MoodTracker
from ollama_client import OllamaClient
from prompt import SYSTEM_PROMPT

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
MOOD_LOG_PATH = os.path.join(DATA_DIR, "mood_log.json")
JOURNAL_PATH = os.path.join(DATA_DIR, "journal.json")

OLLAMA_ERROR_MESSAGE = (
    "⚠️ MindBridge cannot connect to Gemma 4. Please make sure Ollama is running "
    "by opening a terminal and typing: ollama serve"
)

client = OllamaClient()
mood_tracker = MoodTracker(MOOD_LOG_PATH)

ChatMessage = dict[str, str]


def passthrough_history(history: list[ChatMessage]) -> list[ChatMessage]:
    """Return chat history unchanged for component wiring."""
    return history


def ensure_journal_store() -> None:
    """Create local journal file when it does not exist."""
    try:
        os.makedirs(DATA_DIR, exist_ok=True)
        if not os.path.exists(JOURNAL_PATH):
            with open(JOURNAL_PATH, "w", encoding="utf-8") as file:
                json.dump([], file)
    except OSError as exc:
        raise RuntimeError("Unable to initialize journal store.") from exc


def load_journal_entries() -> list[dict[str, str]]:
    """Read all journal entries from disk."""
    ensure_journal_store()
    try:
        with open(JOURNAL_PATH, "r", encoding="utf-8") as file:
            data = json.load(file)
            if not isinstance(data, list):
                return []

            entries: list[dict[str, str]] = []
            data_items = cast(list[object], data)
            for item in data_items:
                if isinstance(item, dict):
                    item_dict = cast(dict[str, object], item)
                    timestamp = str(item_dict.get("timestamp", ""))
                    entry = str(item_dict.get("entry", ""))
                    entries.append({"timestamp": timestamp, "entry": entry})
            return entries
    except (OSError, json.JSONDecodeError):
        return []


def save_journal_entries(entries: list[dict[str, str]]) -> None:
    """Write all journal entries to disk."""
    try:
        with open(JOURNAL_PATH, "w", encoding="utf-8") as file:
            json.dump(entries, file, ensure_ascii=True, indent=2)
    except OSError as exc:
        raise RuntimeError("Unable to save journal entry.") from exc


def format_mood_history() -> str:
    """Create a text summary for the most recent mood entries."""
    entries = mood_tracker.get_recent(7)
    if not entries:
        return "No mood entries yet."

    lines: list[str] = []
    for entry in entries:
        timestamp = str(entry.get("timestamp", ""))
        score = str(entry.get("score", ""))
        note = str(entry.get("note", "")).strip()
        line = f"- {timestamp}: {score}/5"
        if note:
            line += f" - {note}"
        lines.append(line)

    average = mood_tracker.get_average()
    lines.append(f"\nAverage mood: {average:.2f}/5")
    return "\n".join(lines)


def log_mood(score: int, note: str) -> tuple[str, str, str]:
    """Persist a mood check-in and return updated UI values."""
    try:
        mood_tracker.log_mood(score, note)
        return format_mood_history(), "Mood saved.", ""
    except RuntimeError:
        return format_mood_history(), "Could not save mood right now.", note


def save_journal_entry(entry_text: str) -> tuple[str, str]:
    """Save one journal entry and return empty textbox with status."""
    text = entry_text.strip()
    if not text:
        return "", "Please write something before saving."

    try:
        entries = load_journal_entries()
        entries.append(
            {
                "timestamp": datetime.now().isoformat(timespec="seconds"),
                "entry": text,
            }
        )
        save_journal_entries(entries)
        return "", "Journal entry saved."
    except RuntimeError:
        return entry_text, "Could not save your journal entry right now."


def add_exercise_to_chat(
    selected_name: str, chat_history: list[ChatMessage]
) -> list[ChatMessage]:
    """Add selected exercise details as an assistant message in chat."""
    if not selected_name or selected_name.strip() == "":
        return chat_history

    exercise = get_exercise(selected_name)
    if not exercise:
        chat_history.append(
            {"role": "assistant", "content": "I could not find that exercise."}
        )
        return chat_history

    raw_steps = exercise.get("steps", [])
    if isinstance(raw_steps, list):
        steps_source = cast(list[object], raw_steps)
        steps = [str(step) for step in steps_source]
    else:
        steps = []
    lines = [
        f"Here is {exercise.get('name', 'an exercise')}:",
        str(exercise.get("description", "")),
        "",
    ]
    for index, step in enumerate(steps, start=1):
        lines.append(f"{index}. {step}")

    chat_history.append({"role": "assistant", "content": "\n".join(lines)})
    return chat_history


def send_message(
    user_message: str,
    chat_history: list[ChatMessage],
    llm_messages: list[ChatMessage],
) -> Generator[tuple[str, list[ChatMessage], list[ChatMessage]], None, None]:
    """Handle one chat turn with a temporary thinking placeholder."""
    message = user_message.strip()
    if not message:
        yield "", chat_history, llm_messages
        return

    chat_history.append({"role": "user", "content": message})
    llm_messages.append({"role": "user", "content": message})

    chat_history.append({"role": "assistant", "content": "Thinking..."})
    yield "", chat_history, llm_messages

    try:
        reply, elapsed = client.chat(llm_messages)
        final_reply = (
            f"{reply}\n\n_Replied in {elapsed}s on CPU via Gemma 4_"
            if reply
            else "I'm having trouble thinking right now. Please try again in a moment."
        )
    except RuntimeError:
        final_reply = (
            "I'm having trouble thinking right now. Please try again in a moment."
        )

    chat_history[-1] = {"role": "assistant", "content": final_reply}
    llm_messages.append({"role": "assistant", "content": final_reply})
    yield "", chat_history, llm_messages


def check_for_crisis(chat_history: list[ChatMessage]) -> dict[str, object]:
    """Show a crisis support banner when the latest assistant response includes iCall."""
    if not chat_history:
        return gr.update(visible=False)

    last = chat_history[-1]
    content = str(last.get("content", "")).lower()
    if "9152987821" in content or "icall" in content:
        return gr.update(
            value=(
                "🆘 If you are in crisis, please call iCall now: **9152987821** "
                "(Mon-Sat, 8am-10pm). You are not alone."
            ),
            visible=True,
        )
    return gr.update(visible=False)


def build_demo() -> gr.Blocks:
    """Build and return the MindBridge Gradio app."""
    ensure_journal_store()
    available = client.is_available()

    if available:
        print("✅ Connected to Gemma 4 via Ollama")
    else:
        print("⚠️ Could not connect to Ollama. Is it running?")

    startup_status = "" if available else OLLAMA_ERROR_MESSAGE
    welcome_message: ChatMessage = {
        "role": "assistant",
        "content": (
            "Hi! I'm MindBridge, your private mental health companion. "
            "This is a safe space - everything you share stays on your device "
            "and is never sent anywhere. How are you feeling today?"
        ),
    }

    with gr.Blocks(title="MindBridge") as demo:
        gr.Markdown("# 🧠 MindBridge")
        gr.Markdown("Your private mental health companion")
        gr.Markdown(
            "`Gemma 4 E4B via Ollama` - 100% offline · No data leaves your device"
        )

        startup_notice = gr.Markdown(startup_status)
        crisis_banner = gr.Markdown("", visible=False)

        chat_state = gr.State(value=[welcome_message])
        llm_state = gr.State(value=[{"role": "system", "content": SYSTEM_PROMPT}])

        chatbot = gr.Chatbot(
            label="MindBridge Chat",
            height=500,
            value=[welcome_message],
            type="messages",
        )

        gr.Markdown("**Quick prompts:**")
        with gr.Row():
            btn_anxious = gr.Button("😰 I'm feeling anxious", size="sm")
            btn_stressed = gr.Button("😤 I'm stressed", size="sm")
            btn_lonely = gr.Button("😔 I feel lonely", size="sm")
            btn_sleep = gr.Button("😴 I can't sleep", size="sm")

        def send_quick(
            msg: str, chat_history: list[ChatMessage], llm_messages: list[ChatMessage]
        ) -> Generator[tuple[str, list[ChatMessage], list[ChatMessage]], None, None]:
            return send_message(msg, chat_history, llm_messages)

        with gr.Row():
            user_input = gr.Textbox(
                label="Message", placeholder="Share what you are feeling...", scale=8
            )
            send_button = gr.Button("Send", variant="primary", scale=1)

        with gr.Row():
            mood_slider = gr.Slider(
                minimum=1,
                maximum=5,
                value=3,
                step=1,
                label="How are you feeling right now? (1=😔 2=😟 3=😐 4=🙂 5=😊)",
            )
            mood_note = gr.Textbox(
                label="Optional mood note", placeholder="What is on your mind?"
            )
            mood_button = gr.Button("Log Mood", variant="secondary")
        mood_status = gr.Markdown("")

        with gr.Accordion("Coping Exercises", open=False):
            exercise_dropdown = gr.Dropdown(
                choices=list_exercises(), label="Choose an exercise"
            )
            exercise_button = gr.Button("Load Exercise")

        with gr.Accordion("My Mood History", open=False):
            mood_history = gr.Textbox(
                label="Last 7 entries",
                value=format_mood_history(),
                lines=8,
                interactive=False,
            )

        with gr.Accordion("Journal", open=False):
            journal_box = gr.Textbox(label="Write a private journal entry", lines=6)
            journal_button = gr.Button("Save Entry")
            journal_status = gr.Markdown("")

        gr.Markdown(
            "MindBridge runs entirely on your device. Your conversations are private."
        )

        mood_button.click(
            fn=log_mood,
            inputs=[mood_slider, mood_note],
            outputs=[mood_history, mood_status, mood_note],
        )

        exercise_button.click(
            fn=add_exercise_to_chat,
            inputs=[exercise_dropdown, chat_state],
            outputs=[chat_state],
        ).then(
            fn=passthrough_history,
            inputs=[chat_state],
            outputs=[chatbot],
        )

        send_event = send_button.click(
            fn=send_message,
            inputs=[user_input, chat_state, llm_state],
            outputs=[user_input, chat_state, llm_state],
        )
        send_event.then(fn=passthrough_history, inputs=[chat_state], outputs=[chatbot])
        send_event.then(
            fn=check_for_crisis, inputs=[chat_state], outputs=[crisis_banner]
        )

        submit_event = user_input.submit(
            fn=send_message,
            inputs=[user_input, chat_state, llm_state],
            outputs=[user_input, chat_state, llm_state],
        )
        submit_event.then(
            fn=passthrough_history, inputs=[chat_state], outputs=[chatbot]
        )
        submit_event.then(
            fn=check_for_crisis, inputs=[chat_state], outputs=[crisis_banner]
        )

        anxious_event = btn_anxious.click(
            fn=send_message,
            inputs=[
                gr.State(value="I'm feeling anxious and don't know why."),
                chat_state,
                llm_state,
            ],
            outputs=[user_input, chat_state, llm_state],
        )
        anxious_event.then(
            fn=passthrough_history, inputs=[chat_state], outputs=[chatbot]
        )
        anxious_event.then(
            fn=check_for_crisis, inputs=[chat_state], outputs=[crisis_banner]
        )

        stressed_event = btn_stressed.click(
            fn=send_message,
            inputs=[
                gr.State(value="I'm really stressed right now."),
                chat_state,
                llm_state,
            ],
            outputs=[user_input, chat_state, llm_state],
        )
        stressed_event.then(
            fn=passthrough_history, inputs=[chat_state], outputs=[chatbot]
        )
        stressed_event.then(
            fn=check_for_crisis, inputs=[chat_state], outputs=[crisis_banner]
        )

        lonely_event = btn_lonely.click(
            fn=send_message,
            inputs=[
                gr.State(value="I feel lonely and isolated."),
                chat_state,
                llm_state,
            ],
            outputs=[user_input, chat_state, llm_state],
        )
        lonely_event.then(
            fn=passthrough_history, inputs=[chat_state], outputs=[chatbot]
        )
        lonely_event.then(
            fn=check_for_crisis, inputs=[chat_state], outputs=[crisis_banner]
        )

        sleep_event = btn_sleep.click(
            fn=send_message,
            inputs=[
                gr.State(value="I can't sleep and it's affecting everything."),
                chat_state,
                llm_state,
            ],
            outputs=[user_input, chat_state, llm_state],
        )
        sleep_event.then(fn=passthrough_history, inputs=[chat_state], outputs=[chatbot])
        sleep_event.then(
            fn=check_for_crisis, inputs=[chat_state], outputs=[crisis_banner]
        )

        journal_button.click(
            fn=save_journal_entry,
            inputs=[journal_box],
            outputs=[journal_box, journal_status],
        )

        if not available:
            startup_notice.value = OLLAMA_ERROR_MESSAGE

    print("🚀 MindBridge is running at http://localhost:7860")
    return demo


demo = build_demo()


if __name__ == "__main__":
    demo.launch(server_name="127.0.0.1", server_port=7860)
