# -*- coding: utf-8 -*-
"""
    hiromi.immigrate
    ~~~~~~~~~~~~~~~~~~~~~~~

    The immigrate subcommand for hiromi

    :copyright: (c) 2018 by quinoa42.
    :license: MIT, see LICENSE for more details.
"""

import json
import time

from .config import ConfigManager


def add_parser_immigrate(subparsers):
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


def immigrate(args):
    conf_m = ConfigManager(args['file'])
    a, b = conf_m.load_config('mal'), conf_m.load_config('bgm')
    if args['bgm2mal']:
        dst, src = a, b
    else:
        src, dst = b, a

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
