from csv import DictReader
from typing import Any, Final

Entity: Final = dict[str, Any]


def load_entities(filename) -> list[Entity]:
    with open(filename, 'r', encoding='utf-8') as f:
        reader = DictReader(f)
        return [row for row in reader]
