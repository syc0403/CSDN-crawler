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
 # 替换为用户的 Region
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
