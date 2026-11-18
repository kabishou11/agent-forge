"""Synthetic fixture with the bounded tag-parsing repair applied."""


def split_tags(raw: str) -> list[str]:
    parts = [part.strip() for part in raw.split(",")]
    return [part for part in parts if part]
