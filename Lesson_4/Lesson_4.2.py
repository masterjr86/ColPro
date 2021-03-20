import re
import requests
from lxml import html
from pprint import pprint

header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'}

main_url = 'https://news.mail.ru'
response = requests.get(main_url, headers=header)

dom = html.fromstring(response.text)

items = dom.xpath("//div[contains(@class, 'daynews__item')] | //ul[@class='list list_type_square list_half js-module']/li[@class='list__item']")

print(len(items))

top_link = dom.xpath("//div[contains(@class, 'daynews__item')]/a/@href")
links = top_link + dom.xpath("//ul[@class='list list_type_square list_half js-module']/li[@class='list__item']/a/@href")




mailru_main_news = []

for itm in range(0, len(items) - 1):
    mailru__news_data = {}

    top_news = [re.sub(r'\W', ' ', i) for i in
                dom.xpath("//span[@class='photo__title photo__title_new photo__title_new_hidden js-topnews__notification']/text()")]
    news = top_news + [re.sub(r'\W', ' ', i) for i in
                       dom.xpath("//ul[@class='list list_type_square list_half js-module']/li[@class='list__item']/a/text()")]
    mailru__news_data['news'] = news[itm]


    top_link = dom.xpath("//div[contains(@class, 'daynews__item')]/a/@href")
    links = top_link + dom.xpath("//ul[@class='list list_type_square list_half js-module']/li[@class='list__item']/a/@href")
    mailru__news_data['link'] = links[itm]



    response_link = requests.get(links[itm], headers=header)
    dom_link = html.fromstring(response_link.text)
    date = re.split(r'T', dom_link.xpath("//span[@class='note__text breadcrumbs__text js-ago']/@datetime")[0])[0]
    mailru__news_data['date'] = date

    mailru_main_news.append(mailru__news_data)


from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client['news']
mailru_news = db.mailru_news
db.mailru_news.insert_many(mailru_main_news)














#from pymongo import MongoClient
#client = MongoClient('localhost', 27017)
#db = client['news']
#lenta_news = db.lenta_news
#db.lenta_news.insert_many(lenta_main_news)