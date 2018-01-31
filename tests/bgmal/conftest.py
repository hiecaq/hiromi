# -*- coding: utf-8 -*-
"""
    bgm_mal_immigration.tests.conftest
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Fixtures for test cases

    :copyright: (c) 2017 by quinoa42.
    :license: MIT, see LICENSE for more details.
"""

import json
import os.path as op
from urllib.parse import parse_qsl

import pytest
import responses
from bs4 import BeautifulSoup

DIR = op.join(op.dirname(op.abspath(__file__)), 'fixtures')


def get_content(web, name):
    path = op.join(DIR, web, name)
    with open(path) as f:
        return f.read()


@pytest.fixture
def mock_bgm():
    def request_callback(request):
        payload = dict(parse_qsl(request.body))
        if (payload['password'] == "PASSWORD"
                and payload['username'] == "ACCOUNT"
                and payload['auth'] == '0'
                and payload['sysuid'] == '0'
                and payload['sysusername'] == '0'):
            rspbody = {"username": "42", "auth": "aSuperSecureAuth"}
        else:
            rspbody = {"code": 401, "error": "Unauthorized"}
        return (200, {}, json.dumps(rspbody))

    with responses.RequestsMock(assert_all_requests_are_fired=False) as rsps:
        rsps.add_callback(
            responses.POST,
            'https://api.bgm.tv/auth?source=onAir',
            callback=request_callback,
            content_type='application/json',
        )
        rsps.add(
            responses.GET,
            'https://bgm.tv/anime/list/42/collect?page=1',
            body=get_content('bgm', 'collect1.html'),
            status=200
        )
        rsps.add(
            responses.GET,
            'https://bgm.tv/anime/list/42/collect?page=2',
            body=get_content('bgm', 'collect2.html'),
            status=200
        )
        rsps.add(
            responses.GET,
            url=(
                'https://api.bgm.tv/search/subject/{0}?{1}&{2}&{3}'.format(
                    'gunslinger%20girl', 'responseGroup=large',
                    'max_results=11', 'start=0'
                )
            ),
            body=get_content('bgm', 'search.json'),
            status=200
        )
        yield rsps


@pytest.fixture
def mock_mal():
    with responses.RequestsMock(assert_all_requests_are_fired=False) as rsps:
        rsps.add(
            responses.GET,
            'https://myanimelist.net/api/account/verify_credentials.xml',
            body=get_content('mal', 'verify.xml'),
            status=200
        )
        rsps.add(
            responses.GET,
            'https://myanimelist.net/animelist/USERNAME?status=2',
            body=get_content('mal', 'collect.html'),
            status=200
        )
        rsps.add(
            responses.GET,
            'https://myanimelist.net/search/prefix.json',
            body=get_content('mal', 'search.json'),
            #  match_querystring=True,
            status=200
        )
        rsps.add(
            responses.GET,
            'https://myanimelist.net/anime/9/xyzxyz',
            body=get_content('mal', 'search.html'),
            status=200
        )
        yield rsps


@pytest.fixture
def bgm_anime(f):
    return BeautifulSoup(get_content('bgm', f), 'lxml')
