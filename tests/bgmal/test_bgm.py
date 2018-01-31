# -*- coding: utf-8 -*-
"""
    bgm_mal_immigration.tests.test_bgm
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Tests for bgm.py

    :copyright: (c) 2017 by quinoa42.
    :license: MIT, see LICENSE for more details.
"""

import pytest

from bgmal.bgm import Bangumi, Bgmanime, LoginFailedException


@pytest.mark.usefixtures("mock_bgm")
class TestBangumi(object):
    def test_login_fail(self):
        with pytest.raises(LoginFailedException) as e:
            Bangumi("hello", "world")
        assert e

    def test_login_success(self):
        b = Bangumi("ACCOUNT", "PASSWORD")
        assert b._auth == "aSuperSecureAuth"
        assert b._uid == "42"

    def test_watched_list(self):
        b = Bangumi("ACCOUNT", "PASSWORD")
        watchlist = b.watched_list()
        assert len(watchlist) == 47

        entry = watchlist[1]
        assert entry.title == '機動戦士ガンダムSEED DESTINY'
        assert entry.userscore == 5

    def test_search(self):
        b = Bangumi("ACCOUNT", "PASSWORD")
        anime = b.search("gunslinger girl")
        assert anime.title == "GUNSLINGER GIRL"
        assert anime.score == 7.9


class TestBgmanime(object):
    @pytest.mark.parametrize('f', ['anime1.html'])
    def test_bgm_anime2(self, bgm_anime):
        anime = Bgmanime(bgm_anime)
        assert anime.title == "AIR"
        assert anime.userscore == 8

    @pytest.mark.parametrize('f', ['anime2.html'])
    def test_bgm_anime1(self, bgm_anime):
        anime = Bgmanime(bgm_anime)
        assert anime.title == "ピンポン THE ANIMATION"
        assert anime.userscore == 10
