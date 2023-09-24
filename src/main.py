import logging
from argparse import ArgumentParser, Namespace
from os.path import dirname, join, realpath

from renormalize import execute, renormalize_plan
from util import load_entities


def prepare_parser() -> ArgumentParser:
    parser = ArgumentParser(description="重整文件名")
    parser.add_argument(
        "pattern",
        help="重整后的文件名模式，如“作业-:id-:name”",
    )
    parser.add_argument(
        "pathname",
        help="要重整的文件夹（glob.glob 的 pathname 参数），例如“./作业/*”",
    )
    parser.add_argument(
        "--dry-run",
        help="只显示重整计划，不实际更改",
        default=False,
        action="store_true",
    )
    parser.add_argument(
        "--entities",
        help="entities.csv 的路径",
        default="<from_config>",
        nargs=1,
    )
    parser.add_argument(
        "--verbose",
        help="打印详细信息",
        default=False,
        action="store_true",
    )
    parser.add_argument(
        "--debug",
        help="打印调试信息",
        default=False,
        action="store_true",
    )

    return parser


def apply_args(args: Namespace) -> Namespace:
    if args.entities == "<from_config>":
        args.entities = join(realpath(dirname(__file__)), "../config/entities.csv")

    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
    elif args.verbose:
        logging.basicConfig(level=logging.INFO)

    return args


if __name__ == "__main__":
    parser = prepare_parser()
    args = parser.parse_args()
    args = apply_args(args)

    entities = load_entities(args.entities)
    plans = renormalize_plan(args.pattern, args.pathname, entities)

    if args.dry_run:
        print("Plans:")
        for p in plans:
            print(" " * 2, p.src, "→", p.dst)

        print("Dry run, nothing done.")
    else:
        execute(plans)
