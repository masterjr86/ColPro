import re
import requests
from lxml import html
from pprint import pprint

header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'}

lenta_url = 'https://lenta.ru'
lenta_response = requests.get(lenta_url, headers=header)
lenta_dom = html.fromstring(lenta_response.text)

lenta_items = lenta_dom.xpath("//section[@class='row b-top7-for-main js-top-seven']//div[@class='span4']//div[contains(@class, 'item')]")
lenta_main_news = []

lenta_items = lenta_dom.xpath("//section[@class='row b-top7-for-main js-top-seven']//div[@class='span4']//div[contains(@class, 'item')]")
for itm in range(0, len(lenta_items) - 1):
    lenta_news_data = {}

    lenta_top_news = [re.sub(r'\W', ' ', i) for i in lenta_dom.xpath("//section[@class='row b-top7-for-main js-top-seven']//div[@class='span4']/*/h2/a/text()")]
    lenta_news = lenta_top_news + [re.sub(r'\W', ' ', i) for i in lenta_dom.xpath("//section[@class='row b-top7-for-main js-top-seven']//div[@class='item']/a/text()")]
    lenta_news_data['news'] = lenta_news[itm]

    lenta_top_link = [lenta_url + i for i in lenta_dom.xpath("//section[@class='row b-top7-for-main js-top-seven']//div[@class='span4']/*/h2/a/@href")]
    lenta_links = lenta_top_link + [lenta_url + i for i in lenta_dom.xpath("//section[@class='row b-top7-for-main js-top-seven']//div[@class='item']/a/@href")]
    lenta_news_data['link'] = lenta_links[itm]

    lenta_dates = lenta_dom.xpath("//div[@class='item']/a/time//@title")
    lenta_news_data['date'] = lenta_dates[itm]

    lenta_news_data['url'] = lenta_url

    lenta_main_news.append(lenta_news_data)


from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client['news']
lenta_news = db.lenta_news
db.lenta_news.insert_many(lenta_main_news)


mail_url = 'https://news.mail.ru'
mail_response = requests.get(mail_url, headers=header)
mailru_dom = html.fromstring(mail_response.text)

mailru_items = mailru_dom.xpath("//div[contains(@class, 'daynews__item')] | //ul[@class='list list_type_square list_half js-module']/li[@class='list__item']")


mailru_main_news = []
for itm in range(0, len(mailru_items) - 1):
    mailru_news_data = {}

    mailru_top_news = [re.sub(r'\W', ' ', i) for i in
                mailru_dom.xpath("//span[@class='photo__title photo__title_new photo__title_new_hidden js-topnews__notification']/text()")]
    mailru_news = mailru_top_news + [re.sub(r'\W', ' ', i) for i in
                       mailru_dom.xpath("//ul[@class='list list_type_square list_half js-module']/li[@class='list__item']/a/text()")]
    mailru_news_data['news'] = mailru_news[itm]

    mailru_top_link = mailru_dom.xpath("//div[contains(@class, 'daynews__item')]/a/@href")
    mailru_links = mailru_top_link + mailru_dom.xpath("//ul[@class='list list_type_square list_half js-module']/li[@class='list__item']/a/@href")
    mailru_news_data['link'] = mailru_links[itm]

    response_link = requests.get(mailru_links[itm], headers=header)
    dom_link = html.fromstring(response_link.text)
    date = re.split(r'T', dom_link.xpath("//span[@class='note__text breadcrumbs__text js-ago']/@datetime")[0])[0]
    mailru_news_data['date'] = date

    mailru_main_news.append(mailru_news_data)


mailru_news = db.mailru_news
db.mailru_news.insert_many(mailru_main_news)
