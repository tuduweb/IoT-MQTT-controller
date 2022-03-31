import sys
import time
from explorer.explorer import QcloudExplorer

from QiniuOss import *

import os

_currentFilePath = os.path.split(os.path.realpath(__file__))[0]

## init
logger = None


## function def
def on_connect(flags, rc, userdata):
    global product_id, device_name
    logger.debug("%s:flags:%d,rc:%d,userdata:%s" % (sys._getframe().f_code.co_name, flags, rc, userdata))

    # 数据模板初始化,自动订阅相关Topic
    qcloud.templateInit(product_id, device_name, on_template_property,
                            on_template_action, on_template_event, on_template_service)

    _templateConfigFile = os.path.join(_currentFilePath, "./device_info.json")
    qcloud.templateSetup(product_id, device_name, _templateConfigFile)

    pass

def on_disconnect(rc, userdata):
    logger.debug("%s:rc:%d,userdata:%s" % (sys._getframe().f_code.co_name, rc, userdata))
    pass


def on_message(topic, payload, qos, userdata):
    logger.debug("%s:topic:%s,payload:%s,qos:%s,userdata:%s" % (sys._getframe().f_code.co_name, topic, payload, qos, userdata))
    pass


def on_publish(mid, userdata):
    logger.debug("%s:mid:%d,userdata:%s" % (sys._getframe().f_code.co_name, mid, userdata))
    pass


def on_subscribe(mid, granted_qos, userdata):
    logger.debug("%s:mid:%d,granted_qos:%s,userdata:%s" % (sys._getframe().f_code.co_name, mid, granted_qos, userdata))
    pass


def on_unsubscribe(mid, userdata):
    logger.debug("%s:mid:%d,userdata:%s" % (sys._getframe().f_code.co_name, mid, userdata))
    pass


def on_template_property(topic, qos, payload, userdata):
    """属性回调
    接受$thing/down/property/{ProductID}/{DeviceName}的下行消息
    Args:
        topic: 下行主题
        qos: qos
        payload: 下行消息内容
        userdata: 用户注册的任意结构
    """
    pass

def on_template_service(topic, qos, payload, userdata):
    """服务回调
    接受$thing/down/service/{ProductID}/{DeviceName}的下行消息
    Args:
        topic: 下行主题
        qos: qos
        payload: 下行消息内容
        userdata: 用户注册的任意结构
    """
    pass

def on_template_event(topic, qos, payload, userdata):
    """事件回调
    接受$thing/down/event/{ProductID}/{DeviceName}的下行消息
    Args:
        topic: 下行主题
        qos: qos
        payload: 下行消息内容
        userdata: 用户注册的任意结构
    """
    pass

def on_template_action(topic, qos, payload, userdata):
    """行为回调
    接受$thing/down/action/{ProductID}/{DeviceName}的下行消息
    Args:
        topic: 下行主题
        qos: qos
        payload: 下行消息内容
        userdata: 用户注册的任意结构
    """
    logger.debug("%s:mid:%s,userdata:%s" % (sys._getframe().f_code.co_name, topic, userdata))
    print(payload)
    #qcloud.templateActionReply(qcloud.getProductID(), qcloud.getDeviceName(), qcloud.)

    # {'method': 'action', 'clientToken': '146761673::67c3c1c4-2116-45b3-baef-dc902b6d8e42', 'actionId': 'grapCamera', 'timestamp': 1648558746, 'params': {'camera_id': 0}}
    # {'hash': 'Ft79kB3W4rUWVmBlD4aeTBH-eTij', 'key': 'pic-1648558746.jpg'} _ResponseInfo__response:<Response [200]>, exception:None, status_code:200, text_body:{"hash":"Ft79kB3W4rUWVmBlD4aeTBH-eTij","key":"pic-1648558746.jpg"},

    if payload.get('actionId') == 'grapCamera':
        global q
        global qcloud

        # 文件名更改成时间+uuid的形式, 或者用clientToken
        filekey = 'pic-%s.jpg' % int(time.time())

        # concat file path
        _updateFile = os.path.join(_currentFilePath, "./100kb.jpg")
        ret, info = q.UploadFile(_updateFile, qcloud.getDeviceName() + "/" + filekey)

        print(ret, info)

        clientToken = payload["clientToken"]
        reply_param = qcloud.ReplyPara()
        reply_param.code = 0
        reply_param.timeout_ms = 5 * 1000
        reply_param.status_msg = "GrapCameraSuccess"
        res = {
            "imageKey": filekey
        }

        qcloud.templateActionReply(product_id, device_name, clientToken, res, reply_param)

    pass


## 主程序
_deviceFile = os.path.join(_currentFilePath, "./device_info.json")
qcloud = QcloudExplorer(device_file= _deviceFile, tls=True)
# 初始化日志

_logFile = os.path.join(_currentFilePath, "logs/log")
logger = qcloud.logInit(qcloud.LoggerLevel.DEBUG, _logFile, 1024 * 1024 * 10, 5, enable=True)

# 获取设备product id和device name
product_id = qcloud.getProductID()
device_name = qcloud.getDeviceName()

q = QiniuOss()
q.SdkInit()

# 注册mqtt回调
qcloud.registerMqttCallback(on_connect, on_disconnect,
                            on_message, on_publish,
                            on_subscribe, on_unsubscribe)

# mqtt连接, 并且进入Loop
qcloud.connect()

while(True):
    time.sleep(0.1)