import re
import requests
from lxml import html
from pprint import pprint

header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'}


main_url = 'https://lenta.ru'
response = requests.get(main_url, headers=header)
dom = html.fromstring(response.text)

items = dom.xpath("//section[@class='row b-top7-for-main js-top-seven']//div[@class='span4']//div[contains(@class, 'item')]")
lenta_main_news = []


for itm in range(0, len(items) -1):
    lenta_news_data = {}

    top_news = [re.sub(r'\W', ' ', i) for i in
                dom.xpath("//section[@class='row b-top7-for-main js-top-seven']//div[@class='span4']/*/h2/a/text()")]
    news = top_news + [re.sub(r'\W', ' ', i) for i in
                       dom.xpath("//section[@class='row b-top7-for-main js-top-seven']//div[@class='item']/a/text()")]
    lenta_news_data['news'] = news[itm]

    top_link = [main_url + i for i in
                dom.xpath("//section[@class='row b-top7-for-main js-top-seven']//div[@class='span4']/*/h2/a/@href")]
    links = top_link + [main_url + i for i in
                        dom.xpath("//section[@class='row b-top7-for-main js-top-seven']//div[@class='item']/a/@href")]
    lenta_news_data['link'] = links[itm]

    dates = dom.xpath("//div[@class='item']/a/time//@title")
    lenta_news_data['date'] = dates[itm]

    lenta_news_data['url'] = main_url

    lenta_main_news.append(lenta_news_data)








from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client['news']
lenta_news = db.lenta_news
db.lenta_news.insert_many(lenta_main_news)






