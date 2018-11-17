#!/usr/bin/env python
import argparse
import logging
from functools import partial
from subprocess import Popen

from keybind import VERSION_STR, KeyBinder, configure_logging


def main():

    arg_parser = argparse.ArgumentParser(prog='keybind', description='Global key binding made easy')
    arg_parser.add_argument('--version', action='version', version=VERSION_STR)

    arg_parser.add_argument('-k', nargs='*', help='Binding rule. "KEY=program"', action='append')
    arg_parser.add_argument(
        '--sniff', help='Intercept all keys. Use wisely, keep mouse ready.', action='store_true', default=False)
    arg_parser.add_argument('--debug', help='Print out debug info', action='store_true', default=False)

    parsed_args = arg_parser.parse_args()
    parsed_args = vars(parsed_args)

    configure_logging(logging.DEBUG if parsed_args['debug'] else None)

    keymap = {}

    def run(what):
        prc = Popen(what, shell=True)
        prc.communicate()

    keys = parsed_args['k']

    if parsed_args['sniff']:
        KeyBinder.activate()

    elif keys:

        for rule in keys:
            key, _, cmd = rule[0].partition('=')

            if key.isdigit():
                key = int(key)

            keymap[key] = partial(run, what=cmd) if cmd else None

        KeyBinder.activate(keymap)


if __name__ == '__main__':
    main()
