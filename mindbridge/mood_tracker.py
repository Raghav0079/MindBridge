"""Simple mood tracking utilities backed by local JSON storage."""

from __future__ import annotations

import json
import os
from datetime import datetime


class MoodTracker:
    """Stores and retrieves local mood check-in entries."""

    def __init__(self, data_path: str) -> None:
        """Create a tracker and ensure backing storage exists."""
        self.data_path = data_path
        self._ensure_store()

    def _ensure_store(self) -> None:
        """Create required directories and mood log file when missing."""
        directory = os.path.dirname(self.data_path)
        try:
            os.makedirs(directory, exist_ok=True)
            if not os.path.exists(self.data_path):
                with open(self.data_path, "w", encoding="utf-8") as file:
                    json.dump([], file)
        except OSError as exc:
            raise RuntimeError(
                f"Unable to initialize mood store at {self.data_path}"
            ) from exc

    def _read_entries(self) -> list[dict[str, object]]:
        """Read all mood entries from disk."""
        try:
            with open(self.data_path, "r", encoding="utf-8") as file:
                data = json.load(file)
                return data if isinstance(data, list) else []
        except FileNotFoundError:
            self._ensure_store()
            return []
        except (json.JSONDecodeError, OSError):
            return []

    def _write_entries(self, entries: list[dict[str, object]]) -> None:
        """Persist all mood entries to disk."""
        try:
            with open(self.data_path, "w", encoding="utf-8") as file:
                json.dump(entries, file, ensure_ascii=True, indent=2)
        except OSError as exc:
            raise RuntimeError("Unable to save mood entry.") from exc

    def log_mood(self, score: int, note: str) -> None:
        """Append a mood entry with timestamp, score, and optional note."""
        safe_score = max(1, min(5, int(score)))
        entry: dict[str, object] = {
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "score": safe_score,
            "note": note.strip(),
        }
        entries = self._read_entries()
        entries.append(entry)
        self._write_entries(entries)

    def get_recent(self, n: int) -> list[dict[str, object]]:
        """Return the most recent n mood entries."""
        entries = self._read_entries()
        if n <= 0:
            return []
        return entries[-n:]

    def get_average(self) -> float:
        """Return the average mood score across all entries."""
        entries = self._read_entries()
        if not entries:
            return 0.0

        total = 0
        count = 0
        for entry in entries:
            score = entry.get("score")
            if isinstance(score, int):
                total += score
                count += 1

        return float(total) / count if count else 0.0
