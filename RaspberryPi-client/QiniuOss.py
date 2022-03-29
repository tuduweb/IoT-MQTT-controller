from tokenize import String
import qiniu
import time
import sys

from qiniu.http import ResponseInfo
from hub.utils.providers import LoggerProvider
from typing import Tuple


QN_ACCESS_KEY = "MoVNHexgySseNvZuQvjR-aBPsRnOST06X1YVzXW9"
QN_SECRET_KEY = "9Ho3IMrZTF9a4c-6aX8HCdnzIiEzMtnsdrju1xAy"
BUCKET_NAME = 'educoder-control'


# q = qiniu.Auth(QN_ACCESS_KEY, QN_SECRET_KEY)

# #要上传的空间
# bucket_name = 'educoder-control'

# #上传后保存的文件名
# key = '1000kb123.jpg'
# #生成上传 Token，可以指定过期时间等
# token = q.upload_token(bucket_name, key, 3600)
# #要上传文件的本地路径
# localfile = './1000kb.jpg'

# print(int(time.time()))
# ret, info = qiniu.put_file(token, key, localfile, version='v2') 
# print(int(time.time()))

# print(info)
# print(ret)
# assert ret['key'] == key
# assert ret['hash'] == qiniu.etag(localfile)



class QiniuOss:
    def __init__(self) -> None:

        self.q = None

        self.QN_ACCESS_KEY = "MoVNHexgySseNvZuQvjR-aBPsRnOST06X1YVzXW9"
        self.QN_SECRET_KEY = "9Ho3IMrZTF9a4c-6aX8HCdnzIiEzMtnsdrju1xAy"
        self.BUCKET_NAME = 'educoder-control'

        self.__log_provider = LoggerProvider()
        self.__logger = self.__log_provider.logger
        self.__logger.info('current qiniu bucketname {}'.format(self.BUCKET_NAME))
        pass

    def SdkInit(self) -> int:
        self.q = qiniu.Auth(QN_ACCESS_KEY, QN_SECRET_KEY)

        self.__logger.info('qiniu sdk init')

        return 0
    
    def UploadFile(self, localfile : String, key : String) -> Tuple[int, ResponseInfo]:
        token = self.q.upload_token(self.BUCKET_NAME, key, 3600)
        ret, info = qiniu.put_file(token, key, localfile, version='v2')

        self.__logger.info('\033[1;34;47mqiniu update file {} ; key {}\033[0m'.format(localfile, key))
        
        return ret, info