# -*- coding: utf-8 -*-
"""
    bgm_mal_immigration.api
    ~~~~~~~~~~~~~~~~~~~~~~~

    Defines predefined ABCs as specifications and public
    used classes for this module

    :copyright: (c) 2017 by quinoa42.
    :license: MIT, see LICENSE for more details.
"""

import collections
from abc import ABC, abstractmethod


class LoginFailedException(Exception):
    pass


class AnimeWebsite(ABC):
    """AnimeWebsite is an ABC defined generally for potentially all
    shared features among Bangumi, MyAnimeList, etc
    """

    @abstractmethod
    def __init__(self, account, password):
        """Construct an AnimeWebsite object with given account and password

        :param str account: user's account
        :param str password: user's password

        """
        pass

    @abstractmethod
    def watched_list(self):
        """Return the watched list of anime

        :returns: A list of dict, with field str `title` and int `score`

        """
        pass

    @abstractmethod
    def search(self, title):
        """Return an ``AnimeItem`` object representing the anime entry
        of this search result.

        :param str title: the title user wish to search
        :returns: an ``AnimeItem`` object representing the search result
        :rtype: AnimeItem

        """
        pass

    @abstractmethod
    def mark_as_watched(self, anime_item):
        """Mark the given anime as watched with the given score, return true
        if this call succeeds.

        :param AnimeItem title: an AnimeItem that the user want to mark
                                as watched.
        :returns: true or false
        :rtype: bool

        """
        pass


AnimeItem = collections.namedtuple(
    'AnimeItem', ['title', 'score', 'userscore']
)
