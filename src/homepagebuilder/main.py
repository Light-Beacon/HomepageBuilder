"""构建器主入口"""
import argparse
from typing import Dict
from .core.config import is_debugging, init_full, force_debug, set_config
from .command import *

COMMAND_BINDING:Dict[str, CommandProcesser] = {}

def __bind_all_command(subparsers):
    for processer_class in CommandProcesser.__subclasses__():
        processer = processer_class(subparsers)
        COMMAND_BINDING[processer.name] = processer

def __applicate_auto_complete(parser):
    try:
        import argcomplete
        argcomplete.autocomplete(parser)
    except ImportError:
        pass

def main():
    """构建器主入口"""
    init_full()
    try:
        from .core.i18n import locale, LocalizedHelpFormatter
    except ImportError:
        print("[FATAL] Load i18n module failed.")
        return 1
    try:
        parser = argparse.ArgumentParser(
            add_help=False,
            formatter_class=LocalizedHelpFormatter
        )
        parser.add_argument('-h', '--help', action='help', help=locale('command.help'))
        subparsers = parser.add_subparsers(help=locale('command'), dest='command')
        __bind_all_command(subparsers)
        __applicate_auto_complete(parser)
        args = parser.parse_args()
        if args.logging_level:
            set_config('Logging.Level', args.logging_level)
        if args.debug:
            force_debug()
        COMMAND_BINDING[args.command].process(args)
    except KeyboardInterrupt:
        print(locale('command.interrupted'))
    except SystemExit:
        print(locale('command.system_exit'))
    except Exception as e:
        print(f"{e.__class__.__name__}: {e}")
        if is_debugging():
            raise e
        return 1
    return 0

if __name__ == '__main__':
    main()
