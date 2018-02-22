# -*- coding: utf-8 -*-
"""
    bgm_mal_immigration.mal
    ~~~~~~~~~~~~~~~~~~~~~~~

    Deal with the MAL APIs

    :copyright: (c) 2017 by quinoa42.
    :license: MIT, see LICENSE for more details.
"""

import json
import logging
import re
import time
from functools import lru_cache

import requests
from bs4 import BeautifulSoup

from hiromi.cache import period_cache

from .api import AnimeItem, AnimeWebsite, LoginFailedException

logger = logging.getLogger(__name__)

ANIME_VALUES = """\
<?xml version="1.0" encoding="UTF-8"?>
<entry>
<episode>{episode}</episode>
<status>{status}</status>
<score>{userscore}</score>
<storage_type></storage_type>
<storage_value></storage_value>
<times_rewatched></times_rewatched>
<rewatch_value></rewatch_value>
<date_start></date_start>
<date_finish></date_finish>
<priority></priority>
<enable_discussion></enable_discussion>
<enable_rewatching></enable_rewatching>
<comments></comments>
<tags></tags>
</entry>\
"""


class IllegalPasswordException(Exception):
    pass


def _search(title):
    """Search and return an ``AnimeItem`` object representing the result.

    :param str title: the title user wish to search.
    :returns: an dict contains interesting informations.

    """
    r = requests.get(
        'https://myanimelist.net/search/prefix.json',
        params={
            'type': 'anime',
            'keyword': title
        }
    )
    r.raise_for_status()
    data = json.loads(r.text)
    # assume the first one is the closest result
    return data['categories'][0]['items'][0]


class MyAnimeList(AnimeWebsite):
    """Manipulate the MAL api"""

    def __init__(self, account, password):
        """Construct a MyAnimeList object with given account and password

        :param str account: user's email address
        :param str password: user's password

        """
        self._account = account
        if (':' in password or '<' in password):
            raise IllegalPasswordException(
                "Error: password with ':' or '<' "
                "cannot be used for API authentation."
            )
        self._password = password
        self.username = self._get_username()

    def _get_username(self):
        """Get the username of this user.
        :returns: username
        :rtype: str

        """
        url = 'https://myanimelist.net/api/account/verify_credentials.xml'
        r = requests.get(url, auth=(self._account, self._password))
        soup = BeautifulSoup(r.content, 'lxml')
        try:
            r.raise_for_status()
        except Exception as e:
            logger.error("logging failed: %s", e)
            raise LoginFailedException()
        else:
            username = soup.find('username').string
            return username

    @period_cache("mal", period=3600)
    def watched_list(self):
        """Return the watched list of anime

        :returns: a list of anime entries, described in dict of name and score

        """
        return self._get_list(2)

    def watching_list(self):
        """Return the watching list of anime

        :returns: a list of anime entries, described in dict of name and score

        """
        return self._get_list(1)

    def _get_list(self, status):
        """Return the list of anime for given status

        :param int status: the status of this list, 2 for completed and 1 for
                            current watching

        :returns: a list of anime entries, described in dict of name and score

        """
        r = requests.get(
            "https://myanimelist.net/animelist"
            "/{0}?status={1}".format(self.username, status)
        )
        r.raise_for_status()
        soup = BeautifulSoup(r.content, 'lxml')
        try:
            items = soup.find(class_='list-table')['data-items']
        except Exception as e:
            print(e)
            time.sleep(5)
            r = requests.get(
                "https://myanimelist.net/animelist"
                "/{0}?status=2".format(self.username)
            )
            r.raise_for_status()

        items = soup.find(class_='list-table')['data-items']
        data = json.loads(items)
        return [
            AnimeItem(
                title=entry['anime_title'],
                score=None,
                #  title=_get_info(
                #      'https://myanimelist.net' + entry['anime_url'],
                #      'Japanese'
                #  ),
                #  score=_get_score(
                #      'https://myanimelist.net' + entry['anime_url']
                #  ),
                userscore=entry['score'],
                episode=entry['anime_num_episodes'],
                status=entry['num_watched_episodes'],
                id=entry['anime_id']
            ) for entry in data
        ]

    def search(self, title):
        """Search and return an ``AnimeItem`` object representing the result.

        :param str title: the title user wish to search.
        :returns: an ``AnimeItem`` object representing the search result.
        :rtype: AnimeItem

        """
        item = _search(title)
        return item
        return AnimeItem(
            title=_get_info(item['url'], 'Japanese'),
            score=float(item['payload']['score']),
            userscore=None,
            episode=int(_get_info(item['url'], 'Episodes')),
            status=None,
            id=item['id']
        )

    def mark_as_watched(self, anime_item):
        """Mark the given anime as watched with the given score, return true
        if this call succeeds.

        :param AnimeItem title: an AnimeItem that the user want to mark
        as watched.
        :returns: true or false
        :rtype: bool

        """
        time.sleep(0.5)

        item = _search(anime_item.title)
        url = 'https://myanimelist.net/api/animelist/add/{0}.xml'.format(
            item['id']
        )
        try:
            episode = int(_get_info(item['url'], 'Episodes'))
        except ValueError as e:
            return False
        r = requests.get(
            url,
            auth=(self._account, self._password),
            params={
                'data':
                    ANIME_VALUES.format(
                        episode=episode, userscore=anime_item.userscore,
                        status=2
                    )
            }
        )
        # OMG it actually return 400 Client Error if the anime is watched
        if not r.status_code == 400:
            r.raise_for_status()
            return True

        return False


@lru_cache(maxsize=3)
def _get_page(url):
    """Get the japanese name of the anime in this url.

    :param str url: The given url of this anime.
    :returns: the name of this anime.
    :rtype: str

    """

    time.sleep(0.5)

    r = requests.get(url)
    r.raise_for_status()
    soup = BeautifulSoup(r.content, "lxml")
    return soup


def _get_score(url):
    soup = _get_page(url)
    return float(
        soup.find('div', attrs={
            'data-title': 'score'
        }).string.strip()
    )


def _get_info(url, information):
    """TODO: Docstring for _get_info.

    :param url: TODO
    :param information: TODO
    :returns: TODO

    """

    def is_target(x):
        target = x.find('span', class_='dark_text')
        return target is not None and target.string == information + ":"

    soup = _get_page(url)

    info = list(
        filter(
            is_target,
            soup.find_all('div', class_=re.compile('spaceit(_pad)?'))
        )
    )

    return (
        info[-1].contents[-1].strip()
        if len(info) > 0 else soup.find('span', attrs={
            'itemprop': 'name'
        }).string
    )
