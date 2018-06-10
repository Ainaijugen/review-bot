# encoding:utf-8
from aip import AipImageClassify
import base64
import urllib.request, urllib.error, urllib.parse
import sys
import ssl
import json
import jieba

def prepare():
    # get access key
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=6H1uMN13PEUt9w2CQFysaIfC&client_secret=11GUk7ctyI12h3QLWGZ9VjHaa8tO13ug'
    request = urllib.request.Request(host)
    request.add_header('Content-Type', 'application/json; charset=UTF-8')
    response = urllib.request.urlopen(request)
    content = response.read()
    content = str(content)
    content = content[2:-3]
    data = json.loads(content)
    return data['access_token']

def read_picture(filepath):
    request_url = "https://aip.baidubce.com/rest/2.0/image-classify/v2/advanced_general"
    f = open(filepath, 'rb')
    img = base64.b64encode(f.read())
    params = {"image":img}
    params = urllib.parse.urlencode(params).encode(encoding='UTF8')
    access_token = prepare()
    request_url = request_url + "?access_token=" + access_token
    request = urllib.request.Request(url=request_url, data=params)
    request.add_header('Content-Type', 'application/x-www-form-urlencoded')
    response = urllib.request.urlopen(request)
    content = response.read()
    # print(content.decode('utf-8'))
    # if content:
    #     file = open('./ans.txt','w')
    #     file.write(content.decode(encoding = 'UTF8'))
    #     file.close()
    data = json.loads(content)
    result = data['result']
    ans = {}
    for i in range(len(result)):
        ans[result[i]['keyword']] = result[i]['score']
    return ans


print(read_picture('./data/test.jpg'))