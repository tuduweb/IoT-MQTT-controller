import qiniu
import time
import sys

access_key = ""
secret_key = ""

q = qiniu.Auth(access_key, secret_key)

#要上传的空间
bucket_name = 'educoder-control'

#上传后保存的文件名
key = '1000kb123.jpg'
#生成上传 Token，可以指定过期时间等
token = q.upload_token(bucket_name, key, 3600)
#要上传文件的本地路径
localfile = './1000kb.jpg'

print(int(time.time()))
ret, info = qiniu.put_file(token, key, localfile, version='v2') 
print(int(time.time()))

print(info)
print(ret)
assert ret['key'] == key
assert ret['hash'] == qiniu.etag(localfile)