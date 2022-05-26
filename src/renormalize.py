import logging
from glob import glob
from os.path import isfile, basename, splitext, join, dirname
from os import rename

from typing import NamedTuple, Optional
from util import Entity


class Suspect(NamedTuple):
    reason: str
    entity: Entity


def match(file_basename: str, entities: list[Entity]) -> Optional[Entity]:
    suspects: list[Suspect] = []

    for entity in entities:
        for key, value in entity.items():
            if value in file_basename:
                suspects.append(Suspect(
                    reason=key,
                    entity=entity
                ))
                break

    if len(suspects) == 0:
        logging.warning(f"未匹配到任何人：“{file_basename}”。")
        return None

    if len(suspects) > 1:
        messages = [f"{s.entity['name']}（{s.reason}）" for s in suspects]
        logging.warning(f"匹配到多人：{'、'.join(messages)}。")

    return suspects[0].entity


def format(pattern: str, entity: Entity) -> str:
    for key, value in entity.items():
        pattern = pattern.replace(f":{key}", value)

    return pattern


class Plan(NamedTuple):
    src: str
    dst: str


def renormalize_plan(pattern: str, pathname_or_files: str | list[str], entities: list[Entity]) -> list[Plan]:
    files = glob(pathname_or_files) if type(
        pathname_or_files) == str else pathname_or_files
    logging.debug(f"{files=}")
    if len(files) == 0:
        logging.warning(f"未找到任何文件：“{pathname_or_files}”。")

    plans: list[Plan] = []

    for src in files:
        assert isfile(src), f"“{src}”不是文件。"

        src_basename, ext = splitext(basename(src))
        entity = match(src_basename, entities)

        if entity is not None:
            dst_basename = format(pattern, entity)

            if src_basename == dst_basename:
                logging.info(f"已符合模式：“{src}”。")
            else:
                plans.append(Plan(
                    src=src,
                    dst=join(dirname(src), dst_basename + ext)
                ))

    return plans


def execute(plans: list[Plan]) -> None:
    for p in plans:
        rename(p.src, p.dst)
        logging.info(f"Rename “{p.src}” → “{p.dst}”.")
