# -*- coding: utf-8 -*-
 
import hashlib
import json
import random
from urllib import request
from urllib import parse
from urllib.request import urlopen
 
class Baidu_Translation:
    def __init__(self):
        self._q = ''
        self._from = ''
        self._to = ''
        self._appid = 0
        self._key = ''
        self._salt = 0
        self._sign = ''
        self._dst = ''
        self._enable = True
        
    def GetResult(self):
        self._q.encode('utf-8')
        m = str(Trans._appid) + Trans._q + str(Trans._salt) + Trans._key
        m_MD5 = hashlib.md5(m.encode('utf-8'))
        Trans._sign = m_MD5.hexdigest()        
        Url_1 = 'http://api.fanyi.baidu.com/api/trans/vip/translate?'
        Url_2 = 'q='+self._q+'&from='+self._from+'&to='+self._to+'&appid='+str(Trans._appid)+'&salt='+str(Trans._salt)+'&sign='+self._sign
        Url = Url_1+Url_2
        PostUrl = Url.encode()
        TransRequest = request.Request(PostUrl)
        TransResponse = urlopen(TransRequest)
        TransResult = TransResponse.read()
        data = json.loads(TransResult)
        if 'error_code' in data:
            print('Crash')
            print('error:',data['error_code'])
            return data['error_msg']
        else:
            self._dst = data['trans_result'][0]['dst']
            return self._dst
 
    def ShowResult(self,result):
        print(result)
        
    def Welcome(self):
        self._q = 'Welcome to use icedaisy online translation tool'
        self._from = 'auto'
        self._to = 'zh'
        self._appid = 20181027000225987
        self._key = '4TYcP_uUit4JB7FLMdx9'
        self._salt = random.randint(10001,99999)
        welcome = self.GetResult()
        self.ShowResult(welcome)
        
    def StartTrans(self):
        while self._enable:
            self._q = raw_input()
            if cmp(self._q, '!quit') == 0:
                self._enable = False
                print('Thanks for using!')
                break
            _q_len = len(self._q)
            if _q_len < 4096:
                result = self.GetResult()
                self.ShowResult(result)
            else:
                print('Exceeds the maximum limit of 4096 characters')
 
 
#----------- 程序的入口 -----------
print (u"""  
---------------------------------------  
    程序：hws的在线翻译工具  
    版本：0.1  
    作者：hws  
    日期：2018-10-27  
    语言：Python 3.6 
    功能：输入原文后得到翻译结果
    原理：调用百度翻译API
    退出：输入!quit
---------------------------------------  
""")
Trans = Baidu_Translation()
Trans.Welcome()
Trans.StartTrans()
