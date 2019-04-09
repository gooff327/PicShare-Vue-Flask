# -*- coding=utf-8
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
from qcloud_cos import CosServiceError
from qcloud_cos import CosClientError

import sys
import logging

# 腾讯云COSV5Python SDK, 目前可以支持Python2.6与Python2.7以及Python3.x

# pip安装指南:pip install -U cos-python-sdk-v5

# cos最新可用地域,参照https://www.qcloud.com/document/product/436/6224
file_name = 'test.txt'

logging.basicConfig(level=logging.INFO, stream=sys.stdout)

# 设置用户属性, 包括secret_id, secret_key, region
# appid已在配置中移除,请在参数Bucket中带上appid。Bucket由bucketname-appid组成
appid = "1257037397"  # 替换为用户的 appid
secret_id = 'AKIDxhwweBKXMwHn5Jh3a1vgpyd4HGAqoo6e'     # 替换为用户的secret_id
secret_key = 'UklXO7FBakiSVuF9dXkmsknDR0KODm7h'     # 替换为用户的secret_key
region = 'ap-chongqing'    # 替换为用户的region
token = None               # 使用临时秘钥需要传入Token，默认为空,可不填
config = CosConfig(Appid=appid,Region=region, SecretId=secret_id, SecretKey=secret_key, Token=token)  # 获取配置对象
client = CosS3Client(config)

# response = client.head_bucket(
#     Bucket='img-bucket'
# )
# # 本地路径 简单上传
response = client.put_object_from_local_file(
    Bucket='img-bucket',
    LocalFilePath='test.txt',
    Key=file_name,
)
# print(response['ETag'])