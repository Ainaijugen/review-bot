# encoding:utf-8
from aip import AipImageClassify
import base64
import urllib.request, urllib.error, urllib.parse
import sys
import ssl

# get access key
host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=6H1uMN13PEUt9w2CQFysaIfC&client_secret=11GUk7ctyI12h3QLWGZ9VjHaa8tO13ug'
request = urllib.request.Request(host)
request.add_header('Content-Type', 'application/json; charset=UTF-8')
response = urllib.request.urlopen(request)
content = response.read()
if (content):
    print(content)


request_url = "https://aip.baidubce.com/rest/2.0/image-classify/v2/advanced_general"

# 二进制方式打开图片文件
f = open('./test.jpg', 'rb')
img = base64.b64encode(f.read())

params = {"image":img}
params = urllib.parse.urlencode(params).encode(encoding='UTF8')

access_token = '24.baa1a7b8a79eeadc4f27b505a6564975.2592000.1530098008.282335-11094949'
request_url = request_url + "?access_token=" + access_token
request = urllib.request.Request(url=request_url, data=params)
request.add_header('Content-Type', 'application/x-www-form-urlencoded')
response = urllib.request.urlopen(request)
content = response.read()
print(content)
if content:
    file = open('./ans.txt','w')
    file.write(content.decode(encoding = 'UTF8'))
    file.close()
