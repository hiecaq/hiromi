import re
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

    @period_cache("local", period=1800)
    def _get_bgm_and_mal_watchlist(self):
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
                    filter(lambda x: x.title[:-2] == title[:-2], bgm_animes)
                )
                if found is not None:
                    d['bgm'].append(found)
                    d['mal'].append(anime)
            except Exception as e:
                d['failed'].append(anime)

        d['failed'] += set(bgm_animes) - set(d['bgm'])

        return d

    def watching_list(self):
        result = self._get_bgm_and_mal_watchlist()
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

    def increment_status(self, anime_item):
        """Mark the next episode of this given anime as watched.

        :param AnimeItem anime_item: an AnimeItem that the user want to mark
                                as watched.
        :returns: true or false
        :rtype: bool

        """

        def try_until_sucess(site, anime):
            while True:
                seceeded = site.increment_status(anime)
                if seceeded:
                    print(
                        "sucessfully update episode "
                        f"{anime.status + 1} of "
                        f"{anime.title} as watched"
                    )
                    break
                print(
                    f"failed to update {anime.title}, "
                    "wait 5 seconds to try again"
                )
                sleep(5)

        def build_new_anime_item(anime):
            unpack = anime._asdict()
            unpack['status'] = unpack['status'] + 1
            return AnimeItem(**unpack)

        watching_list = self._get_bgm_and_mal_watchlist()
        test = re.compile(anime_item.title, re.IGNORECASE)
        for index, (bgm_anime, mal_anime) in enumerate(
            zip(watching_list['bgm'], watching_list['mal'])
        ):
            if test.match(bgm_anime.title) or test.match(mal_anime.title):

                try_until_sucess(self._getBgm(), bgm_anime)
                try_until_sucess(self._getMal(), mal_anime)

                @period_cache("local", period=0)
                def new_result():
                    """ A helper method that overwrite the cache"""
                    result = watching_list.copy()
                    result['bgm'][index] = build_new_anime_item(
                        result['bgm'][index]
                    )
                    result['mal'][index] = build_new_anime_item(
                        result['mal'][index]
                    )
                    return result

                new_result()
                return True
        return False
