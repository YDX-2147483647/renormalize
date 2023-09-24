from __future__ import annotations

import logging
from glob import glob
from os import rename
from os.path import basename, dirname, isfile, join, splitext
from typing import TYPE_CHECKING, NamedTuple

from tqdm import tqdm

if TYPE_CHECKING:
    from util import Entity


class Suspect(NamedTuple):
    reason: str
    entity: Entity


def match(file_basename: str, entities: list[Entity]) -> Entity | None:
    suspects: list[Suspect] = []

    for entity in entities:
        for key, value in entity.items():
            if value in file_basename:
                suspects.append(Suspect(reason=key, entity=entity))
                break

    if len(suspects) == 0:
        logging.warning(f"未匹配到任何人：“{file_basename}”。")
        return None

    if len(suspects) > 1:
        messages = [f"{s.entity['name']}（{s.reason}）" for s in suspects]
        logging.warning(f"匹配到多人：{'、'.join(messages)}。")

    return suspects[0].entity


def format_basename(pattern: str, entity: Entity) -> str:
    for key, value in entity.items():
        pattern = pattern.replace(f":{key}", value)

    return pattern


class Plan(NamedTuple):
    src: str
    dst: str


def renormalize_plan(
    pattern: str, pathname_or_files: str | list[str], entities: list[Entity]
) -> list[Plan]:
    logging.debug(f"{pathname_or_files=}")
    logging.debug(f"{type(pathname_or_files)=}")
    files = (
        glob(pathname_or_files)
        if isinstance(pathname_or_files, str)
        else pathname_or_files
    )
    logging.debug(f"{files=}")
    if len(files) == 0:
        logging.warning(f"未找到任何文件：“{pathname_or_files}”。")

    plans: list[Plan] = []

    for src in tqdm(files, desc="Generate plans", unit="files", colour="blue"):
        assert isfile(src), f"“{src}”不是文件。"

        src_basename, ext = splitext(basename(src))
        entity = match(src_basename, entities)

        if entity is not None:
            dst_basename = format_basename(pattern, entity)

            if src_basename == dst_basename:
                logging.info(f"已符合模式：“{src}”。")
            else:
                plans.append(Plan(src=src, dst=join(dirname(src), dst_basename + ext)))

    return plans


def execute(plans: list[Plan]) -> None:
    for p in tqdm(plans, desc="Execute plans", unit="files", colour="green"):
        rename(p.src, p.dst)
        logging.info(f"Rename “{p.src}” → “{p.dst}”.")
