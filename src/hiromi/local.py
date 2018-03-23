import json
from time import sleep

from bgmal import AnimeItem, AnimeWebsite
from hiromi.cache import period_cache


class Hiromi(AnimeWebsite):
    """AnimeWebsite is an ABC defined generally for potentially all
    shared features among Bangumi, MyAnimeList, etc
    """

    def __init__(self, getBgm, getMal):
        """Construct an AnimeWebsite object with given account and password

        """
        self._getBgm = getBgm
        self._getMal = getMal

    def watched_list(self):
        """Return the watched list of anime

        :returns: A list of dict, with field str `title` and int `score`

        """
        pass

    def watching_list(self):
        @period_cache("local", period=1800)
        def from_scratch():
            bgm = self._getBgm()
            mal = self._getMal()
            mal_animes = mal.watching_list()
            bgm_animes = bgm.watching_list()
            d = {'bgm': [], 'mal': [], 'failed': []}
            for anime in mal_animes:
                sleep(5)
                try:
                    title = mal.search(anime.title).title
                    found = next(
                        filter(
                            lambda x: x.title[:-2] == title[:-2], bgm_animes
                        )
                    )
                    if found is not None:
                        d['bgm'].append(found)
                        d['mal'].append(anime)
                except Exception as e:
                    d['failed'].append(anime)

            d['failed'] += set(bgm_animes) - set(d['bgm'])

            return d

        result = from_scratch()
        failed = result['failed'].copy()
        for index, bgm_anime in enumerate(result['bgm']):
            mal_anime = result['mal'][index]
            failed.append(
                AnimeItem(
                    title=f"{bgm_anime.title}({mal_anime.title})",
                    userscore=bgm_anime.userscore,
                    episode=mal_anime.episode,
                    status=bgm_anime.status,
                    score=bgm_anime.score,
                    id=bgm_anime.id
                )
            )
        return failed

    def update(self):
        pass

    def search(self, title):
        """Return an ``AnimeItem`` object representing the anime entry
        of this search result.

        :param str title: the title user wish to search
        :returns: an ``AnimeItem`` object representing the search result
        :rtype: AnimeItem

        """
        pass

    def mark_as_watched(self, anime_item):
        """Mark the given anime as watched with the given score, return true
        if this call succeeds.

        :param AnimeItem title: an AnimeItem that the user want to mark
                                as watched.
        :returns: true or false
        :rtype: bool

        """
        pass
