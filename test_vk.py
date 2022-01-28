#!/usr/bin/python3
# -*- coding: utf-8 -*

import requests

token = '72bf1ffb99b7fd6b51af68f6bff767b73c16c84c50f6d05280b6c1550fcb739ab6c9ec6712d5fb7e85b6e'
version = 5.81

data = {
    'access_token': token,
    'from_group': 1,
    'message': 'Тест',
    'attachments': 'https://www.clkon.net',
    'signed': 0,
    'close_comments': 1,
    'v':version
    }

r = requests.post('https://api.vk.com/method/wall.post', data).json()

print(r)

