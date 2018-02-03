# -*- coding: utf-8 -*-
"""
    hiromi.cli
    ~~~~~~~~~~~~~~~~~~~~~~~

    The command line interface for hiromi

    :copyright: (c) 2018 by quinoa42.
    :license: MIT, see LICENSE for more details.
"""

import argparse
import logging
import sys
import colorama

from pkg_resources import get_distribution

from .immigrate import add_parser_immigrate
from .watchlist import add_parser_list

logger = logging.getLogger(__name__)

__version__ = get_distribution("hiromi").version


def parse_args(argv):
    """TODO: Docstring for Pars.

    :param list argv: list of str representing the CLI arguments
    :returns: a dict of parsed arguments

    """
    parser = argparse.ArgumentParser(
        description="Command line anime tracker.", allow_abbrev=False
    )
    subparsers = parser.add_subparsers()
    add_parser_immigrate(subparsers)
    add_parser_list(subparsers)
    parser.add_argument(
        '-V',
        '--version',
        help='Show version and exit',
        action='store_true',
        default=False
    )

    if len(argv) == 0:
        parser.print_help()
        sys.exit(1)

    args = vars(parser.parse_args(argv))
    if args['version']:
        args['func'] = lambda _: print(__version__)
    return args


def main():
    colorama.init()
    args = parse_args(sys.argv[1:])
    if 'func' in args:
        args['func'](args)
    colorama.deinit()


if __name__ == "__main__":
    main()
