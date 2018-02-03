# -*- coding: utf-8 -*-
"""
    hiromi.cache
    ~~~~~~~~~~~~

    A toolkit that defines some descorators in order to cache
    things.

    :copyright: (c) 2018 by quinoa42.
    :license: MIT, see LICENSE for more details.
"""

import hashlib
import json
import os
import sys
from os import path
from time import time

from bgmal import AnimeItem

CACHE_DIR = path.join(path.expanduser('~'), '.cache', 'hiromi')
if not path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)


def period_cache(name, period=600):
    def save_name():
        return path.join(
            CACHE_DIR,
            hashlib.md5(name.encode('utf-8')).hexdigest()
        )

    def period_cache_decorator(func):
        def period_cache_wrapper(*args, **kwords):
            cache = None
            try:
                last_time = path.getmtime(save_name())
            except Exception as e:
                last_time = 0
            else:
                with open(save_name()) as f:
                    raw = json.loads(f.read())
                cache = [AnimeItem(*cached) for cached in raw]
            finally:
                if time() - last_time >= period:
                    cache = func(*args, **kwords)
                    sys.setrecursionlimit(10000)
                    with open(save_name(), "w") as f:
                        f.write(json.dumps(cache))
                return cache

        return period_cache_wrapper

    return period_cache_decorator
