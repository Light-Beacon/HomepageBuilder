"""构建器主入口"""
import argparse
from typing import Dict
from .core.config import init_full, force_debug
from .command import *

COMMAND_BINGDING:Dict[str, CommandProcesser] = {}

def __bind_all_command(subparsers):
    for processer_class in CommandProcesser.__subclasses__():
        processer = processer_class(subparsers)
        COMMAND_BINGDING[processer.name] = processer

def main():
    """构建器主入口"""
    try:
        init_full()
        parser = argparse.ArgumentParser()
        subparsers = parser.add_subparsers(help='Command', dest='command')
        __bind_all_command(subparsers)
        args = parser.parse_args()
        if args.debug:
            force_debug()
        COMMAND_BINGDING[args.command].process(args)
    except Exception as e:
        print(f"{e.__class__.__name__}: {e}")
        return 1
    return 0

if __name__ == '__main__':
    main()
