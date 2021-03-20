# -*- coding=utf-8
# appid 已在配置中移除,请在参数 Bucket 中带上 appid。Bucket 由 BucketName-APPID 组成
# 1. 设置用户配置, 包括 secretId，secretKey 以及 Region
import re

import requests
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
import sys
import logging
import time
import datetime

logging.basicConfig(level=logging.INFO, stream=sys.stdout)
secret_id = 'AKIDjHXYGCOSllVx81v7Rmpc6JM7cqnT22i6'  # 替换为用户的 secretId
secret_key = 'C5iAJDrVv0qNdcMpHSMz1nHWUUCf5E7j'  # 替换为用户的 secretKey
region = 'ap-shanghai'  # 替换为用户的 Region
token = None  # 使用临时密钥需要传入 Token，默认为空，可不填
scheme = 'https'  # 指定使用 http/https 协议来访问 COS，默认为 https，可不填
config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key, Token=token, Scheme=scheme)
# 2. 获取客户端对象
client = CosS3Client(config)


def upload(filename):
    stream = requests.get(filename)
    times = datetime.datetime.now().timetuple()
    keys = str(times.tm_year) + "-" + str(times.tm_mon) + "-" + str(times.tm_mday) + str(int(time.time())) + '.png'
    response = client.put_object(
        Bucket='example-1251531734',
        Body=stream,
        Key=keys
    )
    # img = str(response['ETag'])
    # print(re.findall(r'url=:([^"]+) ,', img))
    return 'https://example-1251531734.cos.ap-shanghai.myqcloud.com/' + keys


def upload_pic():
    #### 文件流简单上传（不支持超过5G的文件，推荐使用下方高级上传接口）
    # 强烈建议您以二进制模式(binary mode)打开文件,否则可能会导致错误
    times = datetime.datetime.now().timetuple()
    keys = str(times.tm_year) + "-" + str(times.tm_mon) + "-" + str(times.tm_mday) + str(int(time.time())) + '.png'
    with open('D:\Desktop/16.jpg', 'rb') as fp:
        response = client.put_object(
            Bucket='example-1251531734',
            Body=fp,
            Key=keys,
            StorageClass='STANDARD',
            EnableMD5=False
        )
    print(response['ETag'])
