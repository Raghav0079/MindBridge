"""Coping exercise catalog for MindBridge."""

from __future__ import annotations


EXERCISES: dict[str, dict[str, object]] = {
    "box_breathing": {
        "name": "Box Breathing",
        "description": "A simple breathing cycle to calm your nervous system.",
        "steps": [
            "Inhale slowly through your nose for 4 counts.",
            "Hold your breath gently for 4 counts.",
            "Exhale slowly through your mouth for 4 counts.",
            "Hold again for 4 counts, then repeat for 4 rounds.",
        ],
    },
    "grounding_54321": {
        "name": "5-4-3-2-1 Grounding",
        "description": "Use your senses to bring yourself back to the present moment.",
        "steps": [
            "Name 5 things you can see around you.",
            "Name 4 things you can feel or touch.",
            "Name 3 things you can hear right now.",
            "Name 2 things you can smell.",
            "Name 1 thing you can taste or appreciate.",
        ],
    },
    "progressive_muscle_relaxation": {
        "name": "Progressive Muscle Relaxation",
        "description": "Release body tension by tightening and relaxing muscle groups.",
        "steps": [
            "Start at your feet and tense the muscles for 5 seconds.",
            "Release and notice the difference for 10 seconds.",
            "Move upward through legs, stomach, hands, shoulders, and face.",
            "End with three slow breaths and relaxed posture.",
        ],
    },
    "gratitude_journaling": {
        "name": "Gratitude Journaling",
        "description": "Shift focus by writing three things you are grateful for today.",
        "steps": [
            "Open your notebook or phone notes.",
            "Write 3 things that went okay or felt meaningful today.",
            "For each one, add one sentence on why it matters to you.",
            "Read them once slowly before closing.",
        ],
    },
    "body_scan": {
        "name": "Body Scan Meditation",
        "description": "Notice sensations in your body without judging them.",
        "steps": [
            "Sit or lie down comfortably and close your eyes if safe.",
            "Bring attention to your toes, then slowly move upward.",
            "Notice tension, warmth, or discomfort in each area.",
            "Breathe into tense spots and soften your muscles.",
            "Finish with one deep breath and open your eyes.",
        ],
    },
}


def get_exercise(name: str) -> dict[str, object]:
    """Return one exercise by internal key or display name."""
    normalized = name.strip().lower().replace(" ", "_")

    if normalized in EXERCISES:
        return EXERCISES[normalized]

    for exercise in EXERCISES.values():
        title = str(exercise.get("name", "")).strip().lower()
        if title == name.strip().lower():
            return exercise

    return {}


def list_exercises() -> list[str]:
    """Return a list of exercise display names."""
    return [str(exercise["name"]) for exercise in EXERCISES.values()]
