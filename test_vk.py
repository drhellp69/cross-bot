#!/usr/bin/python3
# -*- coding: utf-8 -*

import requests

token = ''
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

