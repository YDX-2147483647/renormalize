from __future__ import annotations

from csv import DictReader
from typing import TYPE_CHECKING, Any, Final

if TYPE_CHECKING:
    from pathlib import Path

Entity: Final = dict[str, Any]


def load_entities(filepath: Path) -> list[Entity]:
    with filepath.open(encoding="utf-8") as f:
        reader = DictReader(f)
        return list(reader)
