import csv
import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import pymysql

# 随机爬虫头
ua = UserAgent()
headers = {'User-Agent': ua.random}
# csv存入数据库不会清除原先的数据，于是就不采用追加的方式保存csv文件
with open('Training data.csv', 'w', encoding='utf-8', newline='') as csvfile:
    writer = csv.writer(csvfile)
    # 以只读的方式打开csv，用csv.reader方式判断是否存在标题.
    with open('Training data.csv', 'r', encoding='utf-8', newline='') as fe:
        reader = csv.reader(fe)
        if not [row for row in reader]:
            writer.writerow(['类别', '标题','内容'])


def get_python():
    url = 'https://blog.csdn.net/nav/python'
    response = requests.get(url, headers=headers, timeout= 30)
    data = response.content.decode('utf-8')
    soup = BeautifulSoup(data, 'lxml')
    items = soup.find_all('div', class_='list_con')
    python_blog = []
    for itm in items:
        python_class = 'python'
        python_title = itm.find('a').text.strip()  # strip()去空格
        text_ = itm.find('div', class_='summary oneline').text  # 详情
        text = text_.strip()
        b = (python_class, python_title,text)
        python_blog.append(b)
    # a+ 将爬取到的数据追加写入csv文件中
    f = open('Training data.csv', 'a+', encoding='utf-8', newline='')
    write = csv.writer(f)
    for i in python_blog:
        write.writerows(python_blog)
        break
    # 统计保存文章的数量
    nums = len(python_blog)
    print('新保存python类文章%d篇' % nums)


def get_java():
    url = 'https://blog.csdn.net/nav/java'
    response = requests.get(url, headers=headers, timeout=30)
    data = response.content.decode('utf-8')
    soup = BeautifulSoup(data, 'lxml')
    items = soup.find_all('div', class_='list_con')
    java_blog = []
    for itm in items:
        java_class = 'java'
        java_title = itm.find('a').text.strip()  # strip()去空格
        text_ = itm.find('div', class_='summary oneline').text  # 详情
        text = text_.strip()
        b = (java_class, java_title,text)
        java_blog.append(b)
    # a+ 将爬取到的数据追加写入csv文件中
    f = open('Training data.csv', 'a+', encoding='utf-8', newline='')
    write = csv.writer(f)
    for i in java_blog:
        write.writerows(java_blog)
        break
    # 统计保存文章的数量
    nums = len(java_blog)
    print('新保存java类文章%d篇' % nums)


def get_web():
    url = 'https://blog.csdn.net/nav/web'
    response = requests.get(url, headers=headers, timeout=30)
    data = response.content.decode('utf-8')
    soup = BeautifulSoup(data, 'lxml')
    items = soup.find_all('div', class_='list_con')
    web_blog = []
    for itm in items:
        web_class = '前端'
        web_title = itm.find('a').text.strip()  # strip()去空格
        text_ = itm.find('div', class_='summary oneline').text  # 详情
        text = text_.strip()
        b = (web_class, web_title,text)
        web_blog.append(b)
    # a+ 将爬取到的数据追加写入csv文件中
    f = open('Training data.csv', 'a+', encoding='utf-8', newline='')
    write = csv.writer(f)
    for i in web_blog:
        write.writerows(web_blog)
        break
    # 统计保存文章的数量
    nums = len(web_blog)
    print('新保存前端类文章%d篇' % nums)


def get_ai():
    url = 'https://ai.csdn.net/'
    response = requests.get(url, headers=headers, timeout=30)
    data = response.content.decode('utf-8')
    soup = BeautifulSoup(data, 'lxml')
    items = soup.find_all('div', class_='list_con')
    ai_blog = []
    for itm in items:
        ai_class = 'AI'
        ai_title = itm.find('a').text.strip()  # strip()去空格
        text_ = itm.find('div', class_='summary oneline').text  # 详情
        text = text_.strip()
        b = (ai_class, ai_title,text)
        ai_blog.append(b)
    # a+ 将爬取到的数据追加写入csv文件中
    f = open('Training data.csv', 'a+', encoding='utf-8', newline='')
    write = csv.writer(f)
    for i in ai_blog:
        write.writerows(ai_blog)
        break
    # 统计保存文章的数量
    nums = len(ai_blog)
    print('新保存AI类文章%d篇' % nums)


def get_arch():
    url = 'https://blog.csdn.net/nav/arch'
    response = requests.get(url, headers=headers, timeout=30)
    data = response.content.decode('utf-8')
    soup = BeautifulSoup(data, 'lxml')
    items = soup.find_all('div', class_='list_con')
    arch_blog = []
    for itm in items:
        arch_class = '架构'
        arch_title = itm.find('a').text.strip()  # strip()去空格
        text_ = itm.find('div', class_='summary oneline').text  # 详情
        text = text_.strip()
        b = (arch_class, arch_title,text)
        arch_blog.append(b)
    # a+ 将爬取到的数据追加写入csv文件中
    f = open('Training data.csv', 'a+', encoding='utf-8', newline='')
    write = csv.writer(f)
    for i in arch_blog:
        write.writerows(arch_blog)
        break
    # 统计保存文章的数量
    nums = len(arch_blog)
    print('新保存架构类文章%d篇' % nums)


def get_block():
    url = 'https://blockchain.csdn.net/'
    response = requests.get(url, headers=headers, timeout=30)
    data = response.content.decode('utf-8')
    soup = BeautifulSoup(data, 'lxml')
    items = soup.find_all('div', class_='list_con')
    block_blog = []
    for itm in items:
        block_class = '区块链'
        block_title = itm.find('a').text.strip()  # strip()去空格
        text_ = itm.find('div', class_='summary oneline').text  # 详情
        text = text_.strip()
        b = (block_class, block_title,text)
        block_blog.append(b)
    # a+ 将爬取到的数据追加写入csv文件中
    f = open('Training data.csv', 'a+', encoding='utf-8', newline='')
    write = csv.writer(f)
    for i in block_blog:
        write.writerows(block_blog)
        break
    # 统计保存文章的数量
    nums = len(block_blog)
    print('新保存区块链类文章%d篇' % nums)


def get_db():
    url = 'https://blog.csdn.net/nav/db'
    response = requests.get(url, headers=headers, timeout=30)
    data = response.content.decode('utf-8')
    soup = BeautifulSoup(data, 'lxml')
    items = soup.find_all('div', class_='list_con')
    db_blog = []
    for itm in items:
        db_class = '数据库'
        db_title = itm.find('a').text.strip()  # strip()去空格
        text_ = itm.find('div', class_='summary oneline').text  # 详情
        text = text_.strip()
        b = (db_class, db_title,text)
        db_blog.append(b)
    # a+ 将爬取到的数据追加写入csv文件中
    f = open('Training data.csv', 'a+', encoding='utf-8', newline='')
    write = csv.writer(f)
    for i in db_blog:
        write.writerows(db_blog)
        break
    # 统计保存文章的数量
    nums = len(db_blog)
    print('新保存数据库类文章%d篇' % nums)


def get_G5():
    url = 'https://blog.csdn.net/nav/5g'
    response = requests.get(url, headers=headers, timeout=30)
    data = response.content.decode('utf-8')
    soup = BeautifulSoup(data, 'lxml')
    items = soup.find_all('div', class_='list_con')
    G5_blog = []
    for itm in items:
        G5_class = '5G'
        G5_title = itm.find('a').text.strip()  # strip()去空格
        text_ = itm.find('div', class_='summary oneline').text  # 详情
        text = text_.strip()
        b = (G5_class, G5_title,text)
        G5_blog.append(b)
    # a+ 将爬取到的数据追加写入csv文件中
    f = open('Training data.csv', 'a+', encoding='utf-8', newline='')
    write = csv.writer(f)
    for i in G5_blog:
        write.writerows(G5_blog)
        break
    # 统计保存文章的数量
    nums = len(G5_blog)
    print('新保存5G类文章%d篇' % nums)


def get_game():
    url = 'https://blog.csdn.net/nav/game'
    response = requests.get(url, headers=headers, timeout=30)
    data = response.content.decode('utf-8')
    soup = BeautifulSoup(data, 'lxml')
    items = soup.find_all('div', class_='list_con')
    game_blog = []
    for itm in items:
        game_class = '游戏开发'
        game_title = itm.find('a').text.strip()  # strip()去空格
        text_ = itm.find('div', class_='summary oneline').text  # 详情
        text = text_.strip()
        b = (game_class, game_title,text)
        game_blog.append(b)
    # a+ 将爬取到的数据追加写入csv文件中
    f = open('Training data.csv', 'a+', encoding='utf-8', newline='')
    write = csv.writer(f)
    for i in game_blog:
        write.writerows(game_blog)
        break
    # 统计保存文章的数量
    nums = len(game_blog)
    print('新保存游戏开发类文章%d篇' % nums)


def get_mobile():
    url = 'https://blog.csdn.net/nav/mobile'
    response = requests.get(url, headers=headers, timeout=30)
    data = response.content.decode('utf-8')
    soup = BeautifulSoup(data, 'lxml')
    items = soup.find_all('div', class_='list_con')
    mobile_blog = []
    for itm in items:
        mobile_class = '移动开发'
        mobile_title = itm.find('a').text.strip()  # strip()去空格
        text_ = itm.find('div', class_='summary oneline').text  # 详情
        text = text_.strip()
        b = (mobile_class, mobile_title,text)
        mobile_blog.append(b)
    # a+ 将爬取到的数据追加写入csv文件中
    f = open('Training data.csv', 'a+', encoding='utf-8', newline='')
    write = csv.writer(f)
    for i in mobile_blog:
        write.writerows(mobile_blog)
        break
    # 统计保存文章的数量
    nums = len(mobile_blog)
    print('新保存移动开发类文章%d篇' % nums)


def save_data():
    # 建立链接
    conn = pymysql.connect(host='localhost',
                           user='root',
                           password='333333',
                           database='blog',
                           charset='utf8')
    # 拿到游标
    cursor = conn.cursor()
    # 读取csv文件
    with open('Training data.csv', 'r', encoding='utf-8') as f:
        read = csv.reader(f)
        # 统计csv文件中文章的数量
        # 一行一行的存，除去第一行
        for each in list(read)[1:]:
            i = tuple(each)
            # 使用sql语句添加数据
            sql = "INSERT INTO train_data VALUES " + str(i)
            cursor.execute(sql)  # 执行sql语句
        conn.commit()
        cursor.close()
        conn.close()
    print('训练数据保存成功')


def main():
    get_python()
    get_java()
    # get_web()
    # get_ai()
    # get_arch()
    # get_block()
    # get_db()
    # get_G5()
    # get_game()
    # get_mobile()
    save_data()


if __name__ == '__main__':
    main()
