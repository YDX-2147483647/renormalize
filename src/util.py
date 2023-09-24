from __future__ import annotations

from csv import DictReader
from typing import Any, Final

Entity: Final = dict[str, Any]


def load_entities(filename: str) -> list[Entity]:
    with open(filename, encoding="utf-8") as f:
        reader = DictReader(f)
        return list(reader)
