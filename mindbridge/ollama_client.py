"""Client wrapper for local Ollama chat API."""

from __future__ import annotations

from typing import Any

import requests


class OllamaClient:
    """Provides convenience methods for checking and using a local Ollama model."""

    def __init__(
        self, base_url: str = "http://localhost:11434", model: str = "gemma4:e4b"
    ) -> None:
        """Initialize an Ollama client with base URL and model name."""
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.session = requests.Session()

    def is_available(self) -> bool:
        """Return True when Ollama server is reachable, otherwise False."""
        try:
            response = self.session.get(self.base_url, timeout=3)
            return response.status_code < 500
        except requests.RequestException:
            return False

    def chat(self, messages: list[dict[str, str]]) -> str:
        """Send chat history to Ollama and return the assistant text reply."""
        endpoint = f"{self.base_url}/api/chat"
        payload: dict[str, Any] = {
            "model": self.model,
            "messages": messages,
            "stream": False,
        }

        try:
            response = self.session.post(endpoint, json=payload, timeout=120)
            response.raise_for_status()
            data = response.json()
            message = data.get("message", {})
            content = message.get("content", "")
            return content.strip() if isinstance(content, str) else ""
        except requests.RequestException as exc:
            raise RuntimeError(
                "Could not connect to Ollama at http://localhost:11434. "
                "Please ensure Ollama is running."
            ) from exc
        except ValueError as exc:
            raise RuntimeError("Received an invalid response from Ollama.") from exc
