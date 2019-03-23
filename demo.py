#/usr/bin/env python
# -*- coding: utf-8 -*-

import http.client
import hashlib
import urllib
import random
import urllib.parse
import json

appid = '20181027000225987' #你的appid
secretKey = '4TYcP_uUit4JB7FLMdx9' #你的密钥


httpClient = None
myurl = '/api/trans/vip/translate'
q = '我要吃苹果'
fromLang = 'zh'
toLang = 'en'
salt = random.randint(32768, 65536)

sign = appid+q+str(salt)+secretKey
m1 = hashlib.md5(sign.encode('utf-8'))
sign = m1.hexdigest()
myurl = myurl+'?appid='+appid+'&q='+urllib.parse.quote(q)+'&from='+fromLang+'&to='+toLang+'&salt='+str(salt)+'&sign='+sign

try:
    httpClient = http.client.HTTPConnection('api.fanyi.baidu.com')
    httpClient.request('GET', myurl)

    #response是HTTPResponse对象
    response = httpClient.getresponse()
    data = json.loads(response.read().decode('utf-8'))
    if 'error_code' in data:
       print('carsh')
       print('error:',data['error_code'])
    else :
       dst = data['trans_result'][0]['dst']
       print(dst)
    #dst = data['trans_result'][0]['dst']
except Exception as e:
    print(e)
finally:
    if httpClient:
        httpClient.close()
