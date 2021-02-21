import csv
import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import pymysql
import time
import datetime
import pandas as pd
from sqlalchemy import create_engine


# 爬取数据


def article_crawler(class_, urls):
    # 随机爬虫头
    ua = UserAgent()
    headers = {'User-Agent': ua.random}
    url = urls
    response = requests.get(url, headers=headers, timeout=30)
    data = response.content.decode('utf-8')
    soup = BeautifulSoup(data, 'lxml')
    items = soup.find_all('div', class_='list_con')
    articles = []
    if class_ == 'python':
        id_ = 11
    for itm in items:
        cat_id = id_
        article_title = itm.find('a').text.strip()  # strip()去空格
        article_content = itm.find('div', class_='summary oneline').text.strip()  # 详情
        article_author = itm.find('dd', class_='name').text.strip()
        is_open = '1'
        article_add_time = int(time.time())
        article_link = itm.find('a').get('href')  # url
        b = (cat_id, article_title, article_content, article_author, is_open,
             article_add_time, article_link)
        articles.append(b)
    global df
    df = pd.DataFrame(articles, columns=['cat_id', 'title', 'content', 'author', 'is_open',
                                         'add_time', 'link'])
    df.index = df.index + 1
    df.to_csv('Training_Data.csv', encoding='utf-8-sig')


def save_data():
    create_engine('mysql+pymysql://用户名:密码@主机/库名?charset=utf8')
    engine = create_engine('mysql+pymysql://root:wuzongbo751130@47.106.220.247/shop?charset=utf8')
    pd.io.sql.to_sql(df, 'article', engine, index=False, schema='shop', if_exists='append')
    # engine = create_engine('mysql+pymysql://root:333333@localhost/blog?charset=utf8')
    # print(df)
    #
    # pd.io.sql.to_sql(df, "table_name", engine, index=False, if_exists='append')


if __name__ == '__main__':
    article_crawler('python', 'https://blog.csdn.net/nav/python')
    save_data()
