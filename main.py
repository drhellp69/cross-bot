#!/usr/bin/python3
# -*- coding: utf-8 -*

import sys
import subprocess
import configparser
import feedparser
import re
import datetime
import tweepy
import telebot
import facebook
import requests
import hashlib

# Очистка текста от html тэгов
def remove_html_tags(text):
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

# Проверка доступа в интернет
def online(server):
    print ("Проверка соединения...")
    response = subprocess.call(["/usr/bin/ping", "-c", "3", server], stdout=subprocess.DEVNULL)
    if response != 0:
        print ("Нет доступа в интернет. Бот завершает работу.")
        sys.exit(1)
    print ("OK Google!")
    return

# Публикуем анонс в Twitter
def public_twitter(title, link):
    # Авторизуемся в твитере и отправляем сообщение
    auth = tweepy.OAuthHandler(
        CONSUMER_KEY,
        CONSUMER_SECRET
    )
    auth.set_access_token(
        ACCESS_TOKEN,
        ACCESS_TOKEN_SECRET
    )
    api = tweepy.API(auth)
    # Формируем сообщение twitter
    tweet = title + '\n' + link
    status = api.update_status(status=tweet)
    return

# Публикуем анонс во Вконтакт
def public_vk(title, link):
    # Формируем массив данных
    data = {
        'access_token': VK_TOKEN,
        'from_group': 1,
        'message': title,
        'attachments': link,
        'signed': 0,
        'close_comments': 1,
        'v': VK_VERSION
    }
    # Отправляем запрос
    requests.post('https://api.vk.com/method/wall.post', data).json()
    return

# Публикуем анонс в Telegram
def public_telegram(title, text, link):
    # Инициализируем телеграм бота
    bot = telebot.TeleBot(BOT_TOKEN)
    # Формируем сообщение в канал
    message = '<a href="' + link + '">' + title + '</a>' + "\n" + text
    # Отправляем сообщение в Telegram
    bot.send_message(CHANNEL, message, parse_mode='HTML', disable_web_page_preview=False)
    return

# Публикуем анонс в Facebook
def public_fb(link):
    # ID страницы для которой нужно получить токен
    page_id = FB_PAGE_ID
    # Используем для запроса токен пользователя
    graph = facebook.GraphAPI(FB_TOKEN)
    # Отправляем запрос
    resp = graph.get_object('me/accounts')
    page_access_token = None
    # Поиск токена для страницы
    for page in resp['data']:
        if page['id'] == page_id:
            page_access_token = page['access_token']
    # Запрос с токеном страницы
    graph = facebook.GraphAPI(page_access_token)
    # Публикуем анонс
    graph.put_object('me', 'feed', link=link)
    return

# Публикуем анонс в RocketChat
def public_rc(title, text, link):
    # Отправляем пост в корпоративный чат
    payload = {"username":USERNAME,"emoji":ICON_EMOJI,"attachments":[{"color":COLOR,"title":title,"title_link":link,"text":text}]}
    r = requests.post(URL, json=payload)
    return

# Публикуем анонс в Одноклассники
def public_ok(link):
    # Формируем массив параметров
    params = {
        "application_key": OK_PUBLIC_KEY,
        "attachment": '{"media": [{"type": "link", "url": "' + link + '"}]}',
        "format": "json",
        "gid": OK_GID,
        "method": "mediatopic.post",
        "type": "GROUP_THEME"
    }

    # Формируем строку параметров из массива
    string_params = ''
    for key in params:
        string_params = string_params + key + '=' + params[key]

    # Высчитываем хеш для строки параметров
    string_params = string_params + OK_SESSION_KEY
    hash_string = hashlib.md5(string_params.encode())
    # Добавляем наш токен
    params["access_token"] = OK_ACCESS_TOKEN
    # Добавляем полученный хеш
    params["sig"] = hash_string.hexdigest()

    # Отправляем пост
    r =  requests.post('https://api.ok.ru/fb.do', data=params)
    return

# Проверка доступа в интернет
server = "8.8.8.8"
online(server)

# Чтение параметров
ini = 'settings.ini'
config = configparser.ConfigParser()
config.read(ini)

# Параметры rss
FEED = config.get('RSS', 'feed')
DATETIME = config.get('RSS', 'datetime')

# Параметры Twitter
CONSUMER_KEY = config.get('Twitter', 'consumer_key')
CONSUMER_SECRET = config.get('Twitter', 'consumer_secret')
ACCESS_TOKEN = config.get('Twitter', 'access_token')
ACCESS_TOKEN_SECRET = config.get('Twitter', 'access_token_secret')

# Параметры бота Telegram
BOT_TOKEN = config.get('Telegram', 'bot_token')
CHANNEL = config.get('Telegram', 'channel')

# Параметры Вконтакт
VK_TOKEN = config.get('VK', 'access_token')
VK_VERSION = config.get('VK', 'version')

# Параметры Facebook
FB_TOKEN = config.get('Facebook', 'access_token')
FB_PAGE_ID = config.get('Facebook', 'page_id')

# Параметры RocketChat
URL = config.get('RocketChat', 'url')
USERNAME = config.get('RocketChat', 'username')
ICON_EMOJI = config.get('RocketChat', 'icon_emoji')
COLOR = config.get('RocketChat', 'color')

# Параметры в Одноклассниках
OK_ACCESS_TOKEN = config.get('OK', 'ok_access_token')
OK_PRIVATE_KEY = config.get('OK', 'ok_private_key')
OK_PUBLIC_KEY = config.get('OK', 'ok_public_key')
OK_SESSION_KEY = config.get('OK', 'ok_session_key')
OK_GID = config.get('OK', 'ok_gid')

# Получаем содержимое RSS ленты
rss = feedparser.parse(FEED)

# В цикле проходим все публикации
for post in reversed(rss.entries):
    # Время публикации
    data = post.published
    time = datetime.datetime.strptime(data, '%a, %d %b %Y %H:%M:%S %z')
    time_old = config.get('RSS', 'DATETIME')
    time_old = datetime.datetime.strptime(time_old, '%Y-%m-%d  %H:%M:%S%z')

    # Пропускаем уже опубликованные посты
    if time <= time_old:
        continue
    else:
        # Записываем время и дату нового поста в файл
        config.set('RSS', 'DATETIME', str(time))
        with open(ini, "w") as config_file:
            config.write(config_file)

        print('---------------------------------')
        # Получаем заголовок поста
        title = post.title
        print(title)

        # Получаем ссылку на пост
        link = post.links[0].href
        print(link)

        # Скачиваем текст
        text = post.description
        text = remove_html_tags(text)
        print(text)

        # -------------------------
        # Публикуем анонс в Twitter
        #public_twitter(title, link)

        # -------------------------
        # Публикуем анонс во Вконтакт
        #public_vk(title, link)

        # -------------------------
        # Публикуем анонс в Telegram
        #public_telegram(title, text, link)

        # -------------------------
        # Публикуем анонс в Facebook
        #public_fb(link)

        # -------------------------
        # Публикуем анонс в RocketChat
        #public_rc(title, text, link)

        # -------------------------
        # Публикуем анонс в Одноклассники
        #public_ok(link)
