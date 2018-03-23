# -*- coding: utf-8 -*-
"""
    hiromi.update
    ~~~~~~~~~~~~~

    Incrementing watching status for hiromi

    :copyright: (c) 2018 by quinoa42.
    :license: MIT, see LICENSE for more details.
"""

from bgmal import AnimeItem

from .config import ConfigManager


def add_parser_update(subparsers):
    parser_update = subparsers.add_parser(
        'update', help="Increment the target anime's watching status by 1"
    )
    parser_update.set_defaults(func=update)
    parser_update.add_argument(
        '-f',
        '--file',
        metavar="JSON",
        help="The user's config json file that will be used",
        type=str,
        default="local"
    )
    parser_update.add_argument(
        'anime',
        metavar="ANIME",
        help="A regex that matching the anime wished to update",
        type=str
    )


def update(args):
    src = ConfigManager(args['file']).load_config('local')
    item = AnimeItem(args['anime'], None, None, None, None, None)
    if not src.increment_status(item):
        print("The update failed. Please check your input.")
