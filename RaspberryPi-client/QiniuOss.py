from tokenize import String
import qiniu
import time
import sys

from qiniu.http import ResponseInfo
from hub.utils.providers import LoggerProvider
from typing import Tuple

from AppConfig import AppConfigProvider


class QiniuOss:
    def __init__(self) -> None:

        self.q = None

        self.__config_provider = AppConfigProvider()

        self.config = self.__config_provider.qiniu_config

        self.QN_ACCESS_KEY = self.config.get("QN_ACCESS_KEY")
        self.QN_SECRET_KEY = self.config.get("QN_SECRET_KEY")
        self.BUCKET_NAME = self.config.get("BUCKET_NAME")

        # self.devicePath = 

        self.__log_provider = LoggerProvider()
        self.__logger = self.__log_provider.logger
        self.__logger.info('current qiniu bucketname {}'.format(self.BUCKET_NAME))
        pass

    def SdkInit(self) -> int:
        self.q = qiniu.Auth(self.QN_ACCESS_KEY, self.QN_SECRET_KEY)

        self.__logger.info('qiniu sdk init')

        return 0
    
    def UploadFile(self, localfile : String, key : String) -> Tuple[int, ResponseInfo]:
        token = self.q.upload_token(self.BUCKET_NAME, key, 3600)
        ret, info = qiniu.put_file(token, key, localfile, version='v2')

        self.__logger.info('\033[1;36m qiniu update file {} ; key {}\033[0m'.format(localfile, key))

        return ret, info