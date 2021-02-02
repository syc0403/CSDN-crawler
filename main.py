import datetime
import time

import pymysql
import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import csv


def csvfile():
    with open('CSDN blog.csv', 'w', encoding='utf-8', newline='') as csvfile:
        writer = csv.writer(csvfile)
        # 以只读的方式打开csv，用csv.reader方式判断是否存在标题.
        with open('CSDN blog.csv', 'r', encoding='utf-8', newline='') as fe:
            reader = csv.reader(fe)
            if not [row for row in reader]:
                writer.writerow(['标题', 'url', '内容'])


def get_main(t):
    url_ = 'https://blog.csdn.net/'
    ua = UserAgent()
    headers = {'User-Agent': ua.random}
    response = requests.get(url_, headers=headers, timeout=30)
    data = response.content.decode('utf-8')
    soup = BeautifulSoup(data, 'lxml')
    # with open('CSDN blog.html', 'w', encoding='utf-8') as f:
    #     f.write(str(soup))
    items = soup.find_all('div', class_='list_con')
    # with open('CSDN blog.html', 'w', encoding='utf-8') as f:
    #     f.write(str(items))
    blog = []
    for itm in items:
        title__ = itm.find('a').text  # 标题
        title_ = title__[57:]  # 前面的57个字符是固定的推荐格式跟空格，部分有部分没有所以要删去
        title = title_.strip()  # strip() 去空格
        url = itm.find('a').get('href')  # url
        text_ = itm.find('div', class_='summary oneline').text  # 详情
        text = text_.strip()
        b = (title, url, text)
        blog.append(b)
    f = open('CSDN blog.csv', 'a+', encoding='utf-8-sig', newline='')
    csv_write = csv.writer(f)
    for i in blog:
        csv_write.writerows(blog)
        break
    with open('CSDN blog.csv', 'r', encoding='utf-8-sig') as fp:
        nums = len(fp.readlines())
        print('获取到%d篇新文章' % nums)
    # 定时任务
    # 设定一个标签 确保是运行完定时任务后 再修改时间
    flag = 0
    # 获取当前时间
    now = datetime.datetime.now()
    # 启动时间
    # 启动时间为当前时间 加5秒
    sched_timer = datetime.datetime(now.year, now.month, now.day, now.hour, now.minute,
                                    now.second) + datetime.timedelta(seconds=t)
    # 启动时间也可自行手动设置
    # sched_timer = datetime.datetime(2021,1,29,9,30,10)
    while True:
        # 当前时间
        now = datetime.datetime.now()
        # print(type(now))
        # 本想用当前时间 == 启动时间作为判断标准，但是测试的时候 毫秒级的时间相等成功率很低 而且存在启动时间秒级与当前时间毫秒级比较的问题
        # 后来换成了以下方式，允许1秒之差
        if sched_timer < now < sched_timer + datetime.timedelta(seconds=t):
            time.sleep(1)
            # 建立链接
            conn = pymysql.connect(host='localhost',
                                   user='root',
                                   password='333333',
                                   database='blog',
                                   charset='utf8')
            # 拿到游标
            cursor = conn.cursor()
            # 读取csv文件
            with open('CSDN blog.csv', 'r', encoding='utf-8') as f:
                read = csv.reader(f)
                # 统计csv文件中文章的数量
                # 一行一行的存，除去第一行
                for each in list(read)[1:]:
                    i = tuple(each)
                    # 使用sql语句添加数据
                    sql = "INSERT INTO blog VALUES " + str(i)
                    cursor.execute(sql)  # 执行sql语句
                conn.commit()
                cursor.close()
                conn.close()
                print('保存至数据库成功')
            print('当前时间', now)
            get_main(t)
            flag = 1
        else:
            # 标签控制 表示主程序已运行，才修改定时任务时间
            if flag == 1:
                # 修改定时任务时间 时间间隔为2分钟
                sched_timer = sched_timer + datetime.timedelta(seconds=t)
                flag = 0


if __name__ == '__main__':
    csvfile()
    get_main(1)
