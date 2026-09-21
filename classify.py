#!/usr/bin/env python3
"""Ticket Classifier — rule-based classification of incoming user messages.

Reads messages from messages.txt (one message per line), classifies each
message into one of three categories (жалоба / справка / другое) and prints
a polite draft reply for every ticket.

Pure Python 3, standard library only (sys, pathlib).
"""

import sys
from pathlib import Path

# Keyword rules. Order matters: жалоба is checked first, then справка,
# everything else falls back to другое.
COMPLAINT_KEYWORDS = (
    "очеред", "холодн", "пропал", "пропала", "пропало",
    "wi-fi", "wifi", "вай-фай", "вайфай",
    "сломан", "сломал", "не работает", "не работает",
    "проблем", "ошибк", "сбо", "плохо", "грязн", "холодно",
)

REFERENCE_KEYWORDS = (
    "справк", "документ", "парковк", "где ", "где находится",
    "как получить", "как оформить", "как заказать", "выдать",
)

DRAFT_REPLIES = {
    "жалоба": (
        "Здравствуйте! Приносим извинения за доставленные неудобства. "
        "Ваша жалоба зарегистрирована и передана ответственным специалистам. "
        "Мы постараемся устранить проблему как можно скорее и сообщим о результате."
    ),
    "справка": (
        "Здравствуйте! Ваш запрос принят. Мы передали его в профильный отдел: "
        "справку/информацию подготовят и направят вам в ближайшее рабочее время."
    ),
    "другое": (
        "Здравствуйте! Спасибо за обращение. Ваш запрос передан оператору — "
        "мы свяжемся с вами для уточнения деталей и дальнейших действий."
    ),
}


def classify(text: str) -> str:
    """Return the category for a message based on keyword rules."""
    lowered = text.lower()
    if any(keyword in lowered for keyword in COMPLAINT_KEYWORDS):
        return "жалоба"
    if any(keyword in lowered for keyword in REFERENCE_KEYWORDS):
        return "справка"
    return "другое"


def load_messages(path: Path) -> list:
    """Read messages from file, strip whitespace, skip empty lines."""
    if not path.exists():
        print(f"Ошибка: файл {path} не найден.", file=sys.stderr)
        sys.exit(1)
    lines = path.read_text(encoding="utf-8").splitlines()
    return [line.strip() for line in lines if line.strip()]


def main() -> None:
    # Ensure Cyrillic output works on Windows consoles.
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    data_file = Path(__file__).resolve().parent / "messages.txt"
    messages = load_messages(data_file)

    for index, message in enumerate(messages, start=1):
        category = classify(message)
        reply = DRAFT_REPLIES[category]
        print(f"Тикет #{index}")
        print(f"  Сообщение: {message}")
        print(f"  Категория: {category}")
        print(f"  Черновик ответа: {reply}")
        print()


if __name__ == "__main__":
    main()
