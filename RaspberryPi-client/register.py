from explorer.explorer import QcloudExplorer
import os

_currentFilePath = os.path.split(os.path.realpath(__file__))[0]

# import uuid
# mac = uuid.UUID(int=uuid.getnode()).hex[-12:]

# 构造device_info.json


## 主程序
_deviceFile = os.path.join(_currentFilePath, "./device_info.json")
qcloud = QcloudExplorer(device_file= _deviceFile, tls=True)
# 初始化日志
_logFile = os.path.join(_currentFilePath, "logs/reg.log")
logger = qcloud.logInit(qcloud.LoggerLevel.DEBUG, _logFile, 1024 * 1024 * 10, 5, enable=True)

ret, msg = qcloud.dynregDevice()
if ret == 0:
    logger.debug('dynamic register success, psk: {}'.format(msg))
else:
    logger.error('dynamic register fail, msg: {}'.format(msg))