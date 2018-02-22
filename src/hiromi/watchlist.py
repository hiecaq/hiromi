# -*- coding: utf-8 -*-
"""
    hiromi.watchlist
    ~~~~~~~~~~~~~~~~~~~~~~~

    The list subcommand for hiromi

    :copyright: (c) 2018 by quinoa42.
    :license: MIT, see LICENSE for more details.
"""

from .config import ConfigManager
import json
from colorama import Fore, Style


def add_parser_list(subparsers):
    parser_list = subparsers.add_parser(
        'list', help="List local or remote watchlist"
    )
    parser_list.set_defaults(func=watchlist)
    parser_list.add_argument(
        '-t',
        '--target',
        metavar="SRC",
        help="The source from which watchlist will be printed",
        type=str,
        default="local"
    )
    parser_list.add_argument(
        '-f',
        '--file',
        metavar="JSON",
        help="The user's config json file that will be used",
        type=str,
        default="local"
    )
    parser_list.add_argument(
        '-o',
        '--output',
        metavar="SAVEFILE",
        help="Save the failed AnimeItems to a file",
        type=str,
        default="save.json"
    )
    parser_list.add_argument(
        '--finished',
        help="Show the watched collection",
        action="store_true"
    )


def watchlist(args):
    """Print watchlist.

    :param args: TODO
    :returns: TODO

    """
    src = ConfigManager(args['file']).load_config(args['target'])

    watchlist = src.watched_list() if args['finished'] else src.watching_list()
    for item in watchlist:
        print(f"{Fore.GREEN}{item.title:\u3000<20}{Style.RESET_ALL}"
              f"{item.status}/{item.episode}\t{Fore.RED}"
              f"{item.userscore}{Style.RESET_ALL} ({item.score})")
