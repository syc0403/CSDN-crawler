import csv
import threading
import requests
from tqdm import tqdm
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
import re
from apscheduler.schedulers.blocking import BlockingScheduler
import upload
import urllib.request
from pyquery import PyQuery


def csdn_article_crawler(id_, urls):
    """
    爬虫函数
    :param id_:文章的类型
    :param urls:博客获取的url
    """
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
    for itm in tqdm(items):
        cat_id = id_
        article_title = itm.find('a').text.strip()  # strip()去空格
        # article_content = itm.find('div', class_='summary oneline').text.strip()  # 详情
        article_author = itm.find('dd', class_='name').text.strip()
        is_open = '1'
        article_link = itm.find('a').get('href')  # url
        # ", ".join(LIST) 转化成字符串并去中括号
        keyword = itm.find('div', class_='summary oneline').text.strip()
        article_keyword = (','.join(jieba.analyse.extract_tags(keyword, topK=5, withWeight=False)))
        # topK为返回几个TF/IDF权重最大的词，默认为5个
        # withWeight为是否返回关键词权重词
        article_add_time = add_time_crawlar(article_link)
        article_content = content_crawlar(article_link)
        article_img = get_thumb(article_link)
        b = (cat_id, article_title, article_content, article_author, is_open, article_keyword,
             article_add_time, article_link, article_img)
        articles.append(b)
    global df
    df = pd.DataFrame(articles, columns=['cat_id', 'title', 'content', 'author', 'is_open', 'keywords',
                                         'add_time', 'link', 'thumb'])
    df.index = df.index + 1
    # df.to_csv('Training_Data.csv', encoding='utf-8-sig')
    database_save()
    line = len(df)
    if line == 0:
        print('该分类获取失败')
    print(str(id_) + '新增加文章%d篇' % line)


def add_time_crawlar(urls):
    """
    获取文章发布时间
    :param urls:
    """
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


def content_crawlar(urls):
    """
    获取文章正文的函数
    :param urls:
    """
    # 随机爬虫头
    ua = UserAgent()
    headers = {'User-Agent': ua.random}
    url = urls
    response = requests.get(url, headers=headers, timeout=30)
    data = response.content.decode('utf-8')
    soup = BeautifulSoup(data, 'lxml')
    items = str(soup.find_all("div", {"id": "content_views"}))
    # pattern = re.compile(r'https:\/\/[\w\-_]+(\.[\w\-_]+)+([\w\-\.,@?^=%&:/~\+#]*[\w\-\@?^=%&/~\+#])?')
    # a = items
    # print(str(pattern.match(a)))
    # content_url = upload.upload(pattern)
    # print(content_url)
    # content = re.sub(r'https:+/+/([-\w]+\.)+[\w+]+(/[-\w./?%&=]*)?', content_url, items)

    return items


def get_thumb(urls):
    """
    获取文章中第一张图片链接的函数，如果没有返回空
    :param urls:
    """
    global img_path
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
            # 防止图片链接过长
            if len(img) > 255:
                pass
            else:
                img_path = upload.upload(img)
    except:
        img_path = ''

    return img_path


def csdn_get():
    csdn_article_crawler(10, 'https://blog.csdn.net/nav/career')  # 程序人生
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


def database_save():
    """
    将存放在df中的内容存入数据库
    """
    # create_engine('mysql+pymysql://用户名:密码@主机/库名?charset=utf8')
    engine = create_engine('')
    pd.io.sql.to_sql(df, 'article', engine, index=False, schema='shop', if_exists='append')
    engine = create_engine('mysql+pymysql://root:333333@localhost/blog?charset=utf8mb4')
    pd.io.sql.to_sql(df, 'article', engine, index=False, schema='blog', if_exists='append')


def database_read():
    """
    读取数据库中文章的总函数
    """
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
    """
    要运行的全部函数
    """
    csdn_get()


def run(hour, minute):
    """
    定时函数
    :param hour:小时
    :param minute: 分钟
    """
    scheduler = BlockingScheduler()
    scheduler.add_job(main, 'cron', hour=hour, minute=minute)
    scheduler.start()


if __name__ == '__main__':
    df = []
    img_path = ''
    main()
