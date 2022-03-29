from hub.utils.providers import LoggerProvider
import json


class ConfigProvider(object):
    def __init__(self, file_path) -> None:

        self.__file_path = file_path

        self.__log_provider = LoggerProvider()
        self.__logger = self.__log_provider.logger
        self.__logger.info('app_settings file {}'.format(file_path))

        self.__qiniu_config = {
            "QN_ACCESS_KEY" : "",
            "QN_SECRET_KEY" : "",
            "BUCKET_NAME"   : ""
        }

        with open(file_path, 'r', encoding='utf-8') as f:
            self.__json_data = json.loads(f.read())
            self.__qiniu_config = json.loads(self.__json_data['qiniu'])
            # self.__device_name = self.__json_data['deviceName']
            # self.__product_id = self.__json_data['productId']
            # self.__product_secret = self.__json_data['productSecret']
            # self.__device_secret = self.__json_data['key_deviceinfo']['deviceSecret']
            # self.__ca_file = self.__json_data['cert_deviceinfo']['devCaFile']
            # self.__cert_file = self.__json_data['cert_deviceinfo']['devCertFile']
            # self.__private_key_file = self.__json_data['cert_deviceinfo']['devPrivateKeyFile']
            # self.__region = self.__json_data["region"]
        
        
        pass

    @property
    def qiniu_config(self):
        return self.__qiniu_config