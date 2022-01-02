import requests
import string
import os
import re

from bs4 import BeautifulSoup


def article_scraper(pages, article_category):
    path = os.getcwd()
    regex = re.compile(".*body.*")

    for x in range(1, pages + 1):
        r = requests.get(f'https://www.nature.com/nature/articles?searchType=journalSearch&sort=PubDate&year=2020&page='
                         f'{x}')
        soup = BeautifulSoup(r.content, 'html.parser')
        article_titles = soup.find_all('article')
        article_cat = article_category.title()
        new_dir = 'Page_' + str(x)
        os.mkdir(new_dir)
        new_path = f'{path}/{new_dir}'
        os.chdir(new_path)

        for i in article_titles:
            article_type = i.find('span', class_='c-meta__type')
            if article_type.text == article_cat:
                nature_url = 'https://www.nature.com'
                article_link = i.find('a')
                response = requests.get(nature_url + article_link['href'])
                article_soup = BeautifulSoup(response.content, 'html.parser')
                article_title = article_soup.find('h1').text.strip()\
                    .translate(str.maketrans('', '', string.punctuation)).replace(" ", "_")
                article_body = article_soup.find('div', attrs={'class': regex}).text.strip().encode('utf-8')
                with open(f'{article_title}.txt', 'wb') as file:
                    file.write(article_body)
                print('\nContent saved.')
        os.chdir(path)


pages_input = int(input())
category_input = input()

article_scraper(pages_input, category_input)
