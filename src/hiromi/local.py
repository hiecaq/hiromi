from bgmal import AnimeItem, AnimeWebsite


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
        bgm = self._getBgm()
        mal = self._getMal()
        animes = bgm.watching_list()
        return [
            AnimeItem(
                anime.title + mal.search(
                    anime.title, lambda x: abs(x.episode - anime.episode) <= 3
                ).title,
                anime.score,
                anime.userscore,
                anime.episode,
                anime.status,
                anime.id,
            ) for anime in animes
        ]

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
