import paho.mqtt.client as mqtt
import json

import qiniu
import time

access_key = "MoVNHexgySseNvZuQvjR-aBPsRnOST06X1YVzXW9"
secret_key = "9Ho3IMrZTF9a4c-6aX8HCdnzIiEzMtnsdrju1xAy"
#要上传的空间
bucket_name = 'educoder-control'

## configs

"""
QCloud Device Info
"""
PRODUCT_ID = "OLER6OOJDJ"
DEVICE_NAME = "test2"
DEVICE_KEY = "lyHtcytkme4rXidAwYoqkw=="
"""
MQTT topic
"""
MQTT_DEVICE_CONTROL_TOPIC = "$thing/down/property/"+PRODUCT_ID+"/"+DEVICE_NAME
MQTT_DEVICE_STATUS_TOPIC = "$$thing/up/property/"+PRODUCT_ID+"/"+DEVICE_NAME
MQTT_SERVER = PRODUCT_ID + ".iotcloud.tencentdevices.com"
MQTT_PORT = 1883
MQTT_CLIENT_ID = PRODUCT_ID+DEVICE_NAME
MQTT_USERNAME = "OLER6OOJDJpaho-test1;12010126;6TLNG;1648534244"
MQTT_PASSWORD = "7f42a1d36e85c126a6fff618c220158b8060ae20e9de9bf2eb800b3d901fb90a;hmacsha256"


################################################ IoTHmac ################################################
import base64
import hashlib
import hmac
import random
import string
import time
import sys

# 生成指定长度的随机字符串
def RandomConnid(length):
    return  ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(length))

# 生成接入物联网通信平台需要的各参数
def IotHmac(productID, devicename, devicePsk):
     # 1. 生成 connid 为一个随机字符串，方便后台定位问题
     connid   = RandomConnid(5)
     # 2. 生成过期时间，表示签名的过期时间,从纪元1970年1月1日 00:00:00 UTC 时间至今秒数的 UTF8 字符串
     expiry   = int(time.time()) + 60 * 60
     # 3. 生成 MQTT 的 clientid 部分, 格式为 ${productid}${devicename}
     clientid = "{}{}".format(productID, devicename)
     # 4. 生成 MQTT 的 username 部分, 格式为 ${clientid};${sdkappid};${connid};${expiry}
     username = "{};12010126;{};{}".format(clientid, connid, expiry)
     # 5. 对 username 进行签名，生成token
     secret_key = devicePsk.encode('utf-8')  # convert to bytes
     data_to_sign = username.encode('utf-8')  # convert to bytes
     secret_key = base64.b64decode(secret_key)  # this is still bytes
     token = hmac.new(secret_key, data_to_sign, digestmod=hashlib.sha256).hexdigest()
     # 6. 根据物联网通信平台规则生成 password 字段
     password = "{};{}".format(token, "hmacsha256")
     return {
        "clientid" : clientid,
        "username" : username,
        "password" : password
     }
#########################################################################################################

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("$SYS/#")
    client.subscribe(MQTT_DEVICE_CONTROL_TOPIC)
    client.subscribe("$thing/down/action/OLER6OOJDJ/"+DEVICE_NAME)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload) + " " + str(userdata), client)

    data = json.loads(msg.payload)

    print(data)


    # json_out = {
    #         "method": "action_reply",
    #         "code": replyPara.code,
    #         "clientToken": clientToken,
    #         "status": replyPara.status_msg,
    #         "response": response
    #     }

    # clientToken = payload["clientToken"]
    # reply_param = qcloud.ReplyPara()
    # reply_param.code = 0
    # reply_param.timeout_ms = 5 * 1000
    # reply_param.status_msg = "action execute success!"
    # reply_param
    filekey = 'pic-%s.jpg' % int(time.time())
    token = q.upload_token(bucket_name, filekey, 3600)
    ret, info = qiniu.put_file(token, filekey, './100kb.jpg', version='v2') 

    print(info)
    print(ret)

    reply = {
        "method": "action_reply",
        'code' : 0,
        'clientToken': data.get('clientToken'),
        'status': "action execute success!",
        'response':   {
            "imageKey": filekey
        }
    }

    if data.get('method') == 'action':
        print("action action")
        res = client.publish('$thing/up/action/OLER6OOJDJ/'+DEVICE_NAME, json.dumps(reply))
        print(res)


def on_publish(client, userdata, mid):
    print(userdata)
    print(mid)

client = mqtt.Client(MQTT_CLIENT_ID)
client.on_connect = on_connect
client.on_message = on_message
client.on_publish = on_publish

#generate hmac
hmac = IotHmac(PRODUCT_ID, DEVICE_NAME, DEVICE_KEY)

client.username_pw_set(hmac['username'], hmac['password'])
client.connect(MQTT_SERVER, MQTT_PORT, 60)

q = qiniu.Auth(access_key, secret_key)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()