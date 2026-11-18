"""Synthetic fixture with a deliberately bounded tag-parsing defect."""


def split_tags(raw: str) -> list[str]:
    parts = [part.strip() for part in raw.split(",")]
    return [part for part in parts if part][:1]
