import json
import xml.etree.ElementTree as ElementTree
from urllib.request import urlopen


def get_channel():
    data = urlopen('https://lenta.ru/rss').read().decode('utf8')
    root = ElementTree.fromstring(data)
    return root[0]


def get_news(channel):
    news = []
    for item in channel.findall('item'):
        news.append({'pubDate': item.find('pubDate').text, 'title': item.find('title').text})
    return news


def get_full_news(channel):
    news = []
    tags = {}
    for item in channel.findall('item'):
        for tag in item:
            tags[tag.tag] = tag.text
        news.append(tags)
    return news


def save_json(news, filename):
    json_file = json.dumps(news, ensure_ascii=False, indent=4).encode('utf8')
    with open(filename, 'wb') as file:
        file.write(json_file)


save_json(get_news(get_channel()), 'news.json')
save_json(get_full_news(get_channel()), 'full_news.json')




