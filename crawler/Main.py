import csv
import threading

import requests
import tqdm
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import pymysql
import time
import datetime
import pandas as pd
from gensim import corpora, models
from sqlalchemy import create_engine
import pymysql
from sqlalchemy import create_engine
import pandas as pd
from datetime import datetime
import os
from apscheduler.schedulers.blocking import BlockingScheduler

'''
爬取数据

global df
'''


def csdn_article_crawler(id_, urls):
    import jieba.analyse
    # 随机爬虫头
    ua = UserAgent()
    headers = {'User-Agent': ua.random}

    url = urls
    response = requests.get(url, headers=headers, timeout=30)
    data = response.content.decode('utf-8')
    soup = BeautifulSoup(data, 'lxml')
    items = soup.find_all('div', class_='list_con')
    articles = []
    for itm in tqdm.tqdm(items):
        cat_id = id_
        article_title = itm.find('a').text.strip()  # strip()去空格
        # article_content = itm.find('div', class_='summary oneline').text.strip()  # 详情
        article_author = itm.find('dd', class_='name').text.strip()
        is_open = '1'
        article_link = itm.find('a').get('href')  # url
        # ", ".join(LIST) 转化成字符串并去中括号
        keyword = itm.find('div', class_='summary oneline').text.strip()
        article_keyword= (','.join(jieba.analyse.extract_tags(keyword, topK=5, withWeight=False)))
        # topK为返回几个TF/IDF权重最大的词，默认为5个
        # withWeight为是否返回关键词权重词
        article_add_time = add_time_crawlar(article_link)
        article_content = content_crawlar(article_link)
        article_img = get_thumb(article_link)
        b = (cat_id, article_title, article_content, article_author, is_open,article_keyword,
             article_add_time, article_link,article_img)
        articles.append(b)
    global df
    df = pd.DataFrame(articles, columns=['cat_id', 'title', 'content', 'author', 'is_open','keywords',
                                         'add_time', 'link','thumb'])
    df.index = df.index + 1
    df.to_csv('Training_Data.csv', encoding='utf-8-sig')
    database_save()
    line = len(df)
    if line == 0:
        print('该分类获取失败')
    print(str(id_) + '新增加文章%d篇' % line)


# def article_crawler1(id_, urls):
#     import jieba.analyse
#     # 随机爬虫头
#     ua = UserAgent()
#     headers = {'User-Agent': ua.random}
#     url = urls
#     response = requests.get(url, headers=headers, timeout=30)
#     data = response.content.decode('utf-8')
#     soup = BeautifulSoup(data, 'lxml')
#     items = soup.find_all('li', class_='clearfix')
#     articles = []
#     for itm in items:
#         cat_id = id_
#         article_title = itm.find('h2').text.strip()  # strip()去空格
#         # article_content = itm.find('div', class_='summary oneline').text.strip()  # 详情
#         article_author = itm.find('dd', class_='name').text.strip()
#         is_open = '1'
#         article_link = itm.find('a').get('href')  # url
#         article_content = content_crawlar(article_link)
#         article_add_time = add_time_crawlar(article_link)
#         # ", ".join(LIST) 转化成字符串并去中括号
#         # keywords = (','.join(jieba.analyse.extract_tags(article_content, topK=5, withWeight=False)))
#         # topK为返回几个TF/IDF权重最大的词，默认为5个
#         # withWeight为是否返回关键词权重词
#         b = (cat_id, article_title, article_content, article_author, is_open,
#              article_add_time, article_link)
#         articles.append(b)
#     global df
#     df = pd.DataFrame(articles, columns=['cat_id', 'title', 'content', 'author', 'is_open',
#                                          'add_time', 'link'])
#     df.index = df.index + 1
#     df.to_csv('Training_Data.csv', encoding='utf-8-sig')
#     database_save()
#     line = len(df)
#     if line == 0:
#         print('该分类获取失败')
#     print(str(id_) + '新增加文章%d篇' % line)


def add_time_crawlar(urls):
    # 随机爬虫头
    ua = UserAgent()
    headers = {'User-Agent': ua.random}
    url = urls
    response = requests.get(url, headers=headers, timeout=30)
    data = response.content.decode('utf-8')
    soup = BeautifulSoup(data, 'lxml')
    times = soup.find('span', class_='time')
    try:
        add_time = times.text
        timeArray = time.strptime(add_time, '%Y-%m-%d %H:%M:%S')
        timeStamp = int(time.mktime(timeArray))
    # print(timeStamp)
    except:
        timeStamp = int(time.time())
    return timeStamp


'''
根据得到的文章链接来获取文章内容
'''


def content_crawlar(urls):
    # 随机爬虫头
    ua = UserAgent()
    headers = {'User-Agent': ua.random}
    url = urls
    response = requests.get(url, headers=headers, timeout=30)
    data = response.content.decode('utf-8')
    soup = BeautifulSoup(data, 'lxml')
    items = soup.find_all('div', class_='article_content clearfix')
    return items


def get_thumb(urls):
    ua = UserAgent()
    headers = {'User-Agent': ua.random}
    url = urls
    response = requests.get(url, headers=headers, timeout=30)
    data = response.content.decode('utf-8')
    soup = BeautifulSoup(data, 'lxml')
    items = soup.find_all(id='content_views')
    try:
        for i in items:
            img = i.find('img').get('src')
    except:
        img = ''    
    return img


'''
各个分类文章的爬取
'''


def csdn_get():
    # article_crawler1(9, 'https://blog.csdn.net/nav/watchers')  # 动态
    # csdn_article_crawler(10, 'https://blog.csdn.net/nav/career')  # 程序人生
    csdn_article_crawler(11, 'https://blog.csdn.net/nav/python')  # python
    csdn_article_crawler(12, 'https://blog.csdn.net/nav/java')  # Java
    csdn_article_crawler(13, 'https://blog.csdn.net/nav/web')  # 大前端
    csdn_article_crawler(14, 'https://blog.csdn.net/nav/arch')  # 架构
    csdn_article_crawler(15, 'https://blockchain.csdn.net/')  # 区块链
    csdn_article_crawler(16, 'https://blog.csdn.net/nav/db')  # 数据库
    csdn_article_crawler(17, 'https://blog.csdn.net/nav/5g')  # 5G技术
    csdn_article_crawler(18, 'https://blog.csdn.net/nav/game')  # 游戏开发
    csdn_article_crawler(19, 'https://blog.csdn.net/nav/mobile')  # 移动开发
    csdn_article_crawler(20, 'https://blog.csdn.net/nav/ops')  # 运维
    csdn_article_crawler(21, 'https://blog.csdn.net/nav/sec')  # 安全
    csdn_article_crawler(22, 'https://cloud.csdn.net/')  # 云计算/大数据
    csdn_article_crawler(24, 'https://blog.csdn.net/nav/engineering')  # 研发管理
    csdn_article_crawler(25, 'https://blog.csdn.net/nav/iot')  # 物联网
    csdn_article_crawler(26, 'https://blog.csdn.net/nav/avi')  # 音视频


'''
保存数据至数据库
将爬取到的文章保存至数据库

'''


def database_save():
    # create_engine('mysql+pymysql://用户名:密码@主机/库名?charset=utf8')
    # engine = create_engine('mysql+pymysql://root:wuzongbo751130@47.106.220.247/shop?charset=utf8mb4')
    # pd.io.sql.to_sql(df, 'article', engine, index=False, schema='shop', if_exists='append')
    engine = create_engine('mysql+pymysql://root:333333@localhost/blog?charset=utf8mb4')
    pd.io.sql.to_sql(df, 'article', engine, index=False, schema='blog', if_exists='append')


'''
读取数据库的信息
读取了数据库中article表中文章的行数
'''


def database_read():
    # 读取数据库
    con = pymysql.connect(host="47.106.220.247", user="root", password="wuzongbo751130", db="shop")
    # 读取sql
    # data_sql = pd.read_sql("SELECT * FROM article", con)
    # 查询表的行数
    cursor = con.cursor()
    query = " select count(*) from article"
    cursor.execute(query)
    con.commit()
    count = cursor.fetchall()
    print('当前数据库共有', count[0][0], '篇文章')


def main():
    csdn_get()


'''
定时
'''


def run(hour, minute):
    scheduler = BlockingScheduler()
    scheduler.add_job(main, 'cron', hour=hour, minute=minute)
    scheduler.start()


if __name__ == '__main__':
    main()
