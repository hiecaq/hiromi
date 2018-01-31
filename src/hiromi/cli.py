# -*- coding: utf-8 -*-
"""
    bgm_mal_immigration.cli
    ~~~~~~~~~~~~~~~~~~~~~~~

    The command line interface for bgm_mal_immigration

    :copyright: (c) 2017 by quinoa42.
    :license: MIT, see LICENSE for more details.
"""

import argparse
import json
import logging
import sys
import time

from pkg_resources import get_distribution

from bgmal import Bangumi, MyAnimeList

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
    parser_immigrate = subparsers.add_parser(
        'immigrate', help="Immigrate watched list from bangumi to MyAnimeList"
    )
    parser_immigrate.set_defaults(func=immigrate)
    acts = parser_immigrate.add_mutually_exclusive_group(required=True)
    acts.add_argument(
        '--bgm2mal', help="Immigrate from bgm to mal", action="store_true"
    )
    acts.add_argument(
        '--mal2bgm', help="Immigrate from mal to bgm", action="store_true"
    )
    parser_immigrate.add_argument(
        '-f',
        '--file',
        metavar="JSON",
        help="The user's config json file that will be used",
        type=str,
        default="config.json"
    )
    parser_immigrate.add_argument(
        '-o',
        '--output',
        metavar="SAVEFILE",
        help="Save the failed AnimeItems to a file",
        type=str,
        default="save.json"
    )
    parser_immigrate.add_argument(
        '-i',
        '--input',
        metavar="SAVEFILE",
        help="Read the previous failed AnimeItem file.",
        type=str,
        default=None
    )
    parser.add_argument(
        '-V',
        '--version', help='Show version and exit.', action='store_true',
        default=False
    )

    if len(argv) == 0:
        parser.print_help()
        sys.exit(1)

    args = vars(parser.parse_args(argv))
    if args['version']:
        args['func'] = lambda _: print(__version__)
    return args


def load_config(filename):
    with open(filename) as f:
        config = json.loads(f.read())

    a = MyAnimeList(config['mal']['account'], config['mal']['password'])
    b = Bangumi(config['bgm']['account'], config['bgm']['password'])
    return a, b


def immigrate(args):
    if args['bgm2mal']:
        dst, src = load_config(args['file'])
    else:
        src, dst = load_config(args['file'])

    if args['input']:
        with open(args['input']) as f:
            li = json.loads(f)
    else:
        li = src.watched_list()

    sucess, fail = [], []
    for i, item in enumerate(li):
        if i % 10 == 0:
            time.sleep(120)
        try:
            cond = dst.mark_as_watched(item)
        except Exception as e:
            cond = False
        if cond:
            sucess.append(item)
        else:
            fail.append(item)

    print(
        "sucess({0}): {1} \n fail({2}): {3}".format(
            len(sucess), sucess, len(fail), fail
        )
    )

    with open(args['output']) as f:
        f.write(json.dumps(fail))


def main():
    args = parse_args(sys.argv[1:])
    if 'func' in args:
        args['func'](args)


if __name__ == "__main__":
    main()
