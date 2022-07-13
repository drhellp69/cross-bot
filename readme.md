# Cross-Bot

Бот для публикаций новостей из RSS а канал Telegram, в Twitter, на страницу В Контакте
Запуск по крону

```
sudo apt-get install python3-pip
sudo pip3 install feedparser
sudo pip3 install pyTelegramBotAPI
sudo apt-get install python3-tweepy
```

```
sudo nano /etc/crontab
*/5 * * * * root /usr/bin/python3 /var/cross-bot/main.py > /dev/null 2
```
Полное описание доступно на странице http://drhellp.loc.ru/news/10-09-2021/krossposting
