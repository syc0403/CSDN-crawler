import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import csv


def get_main():
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
    f = open('CSDN blog.csv', 'w', encoding='utf-8-sig', newline='')
    csv_write = csv.writer(f)
    csv_write.writerow(['标题', 'url', '详情'])
    for i in blog:
        csv_write.writerows(blog)
        break
    # with open('CSDN blog.csv','r',encoding='utf-8-sig') as fp:
    #     nums = len(fp.readlines())
    #     print('获取到%d篇新文章' % nums)


if __name__ == '__main__':
    get_main()
