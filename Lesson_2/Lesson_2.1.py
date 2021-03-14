from bs4 import BeautifulSoup as bs
import requests
from pprint import pprint
import re
import pandas as pd

# https://hh.ru/search/vacancy?area=&fromSearchLine=true&st=searchVacancy&text=django
link = 'https://hh.ru'

params = {
    'area': 'true',
    'fromSearchLine': 'true',
    'st': 'sarchVacancy',
    'text': 'django',
    'page': 0
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'
}
vacancys = []
while True:
    response = requests.get(link + '/search/vacancy/', params=params, headers=headers)
    if response.ok:
        soup = bs(response.text, 'html.parser')
        vacancy_list = soup.findAll('div', {'class': 'vacancy-serp-item'})


        for vacancy in vacancy_list:
            vacancy_data = {}
            vacancy_name = vacancy.find('a').getText()

            vacancy_salary = vacancy.find('div', {'class': 'vacancy-serp-item__sidebar'}).getText()
            if re.search('USD', vacancy_salary):
                vacancy_currency = 'доллар США'
            elif re.search('руб', vacancy_salary):
                vacancy_currency = 'рубль'
            else:
                vacancy_currency = None

            if re.match(r'от', vacancy_salary):
                salary_min = int(re.sub('\D', '', vacancy_salary))
                salary_max = None
            elif re.match(r'до', vacancy_salary):
                salary_max = int(re.sub('\D', '', vacancy_salary))
                salary_min = None
            elif vacancy_salary == '':
                salary_min = None
                salary_max = None
            else:
                salary_min = int(re.sub(r'\D', '',re.split(r'-', vacancy_salary)[0]))
                salary_max = int(re.sub(r'\D', '', re.split(r'-', vacancy_salary)[1]))

            vacancy_link = re.sub(r'https://sergievposad.hh.ru', link, vacancy.find('a', href=True)['href'])

            vacancy_data['name'] = vacancy_name
            vacancy_data['salary_min'] = salary_min
            vacancy_data['salary_max'] = salary_max
            vacancy_data['salary_currency'] = vacancy_currency
            vacancy_data['link'] = vacancy_link
            vacancy_data['source'] = link
            vacancys.append(vacancy_data)

    params['page'] += 1



    if soup.find('a', {'class': 'HH-Pager-Controls-Next'})== None:
        break


print(len(vacancys))
vacansys_df = pd.DataFrame(vacancys)

print(vacansys_df.shape)
