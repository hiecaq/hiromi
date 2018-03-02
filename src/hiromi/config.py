# -*- coding: utf-8 -*-
"""
    hiromi.config
    ~~~~~~~~~~~~~

    The config file manipulation module.

    :copyright: (c) 2018 by quinoa42.
    :license: MIT, see LICENSE for more details.
"""

import json
from os import path

from bgmal import Bangumi, MyAnimeList

from .local import Hiromi


class ConfigNotFoundException(Exception):
    pass


def to_symbol(text):
    """Return the corresponding string representing the websites.

    :param str text: TODO
    :returns: TODO

    """
    text = text.upper()
    if text in ("BGM", "BANGUMI"):
        return "bgm"
    elif text in ("MAL", "MYANIMELIST"):
        return "mal"
    else:
        return None


class ConfigManager(object):
    """Docstring for ConfigManager. """

    def __init__(self, filename):
        """TODO

        :param filename: TODO

        """
        _filename = ConfigManager.fallback_file(filename)
        with open(_filename) as f:
            self._config = json.loads(f.read())

    def load_config(self, target):
        """Return the corresponding string representing the websites.

        :param str target: TODO
        :returns: an ``AnimeWebsite`` object, depending on the input
        :rtype: AnimeWebsite

        """

        def new_bgm():
            return Bangumi(
                self._config['bgm']['account'], self._config['bgm']['password']
            )

        def new_mal():
            return MyAnimeList(
                self._config['mal']['account'], self._config['mal']['password']
            )

        target = to_symbol(target)
        if target == "bgm":
            result = new_bgm()
        elif target == "mal":
            result = new_mal()
        else:
            result = Hiromi(new_bgm, new_mal)

        return result

    @classmethod
    def fallback_file(cls, filename):
        """Return the fallback file for config. It will first try given
        file, then ~/.config/hiromi.json, then ~/.hiromi

        :param str filename: the given file
        :returns: a usable filename
        :rtype: AnimeWebsite

        """
        file_list = (
            filename,
            path.join(path.expanduser('~'), '.config', 'hiromi.json'),
            path.join(path.expanduser('~'), '.hiromi')
        )
        for a_file in file_list:
            if path.exists(a_file):
                return a_file
        print(
            "Please given a legal config file, or make a config file at"
            "~/.hiromi or ~/.config/hiromi.json"
        )
        raise ConfigNotFoundException()
