#!/usr/bin/python
#-*- coding:utf-8 -*- 
import tkinter.messagebox
from tkinter import *
from tkinter.filedialog import askdirectory
import random
import urllib.parse
import json
import http.client
import hashlib
import urllib
import os

def selectPath():
    path_ = askdirectory()
    rootdir.set(path_)
    print(rootdir.get())
    searchFiles()
    showLanguageView()
    
def searchFiles():
	list = os.listdir(rootdir.get())
	for i in range(0,len(list)):
		childpath = os.path.join(rootdir.get(),list[i])
		childpathmap[list[i]] = childpath
		
def showLanguageView():
	_column = 0
	frm = Frame(win)
	for keyName in languagemap.keys():
		checkVal = IntVar()
		Checkbutton(frm,text = languagemap[keyName],variable = checkVal,onvalue = 1,offvalue = 0).grid(row = 0,column = _column)
		checkStatus[keyName] = checkVal
		_column += 1
	frm.grid(row = 1)
	Label(win,text="Key:").grid(row = 2,column = 0)
	Entry(win,textvariable = replaceKey).grid(row = 2,column = 1)
	Label(win,text="Value:").grid(row = 2,column = 2)
	Entry(win,textvariable = replaceValue).grid(row = 2,column = 3)
	Button(win,text="查找",command = search).grid(row = 2,column = 4)
	Button(win,text="替换",command = replace).grid(row = 2,column = 5)
	Button(win,text="插入",command = inset).grid(row = 2,column = 6)
	Button(win,text="删除",command = delete).grid(row = 2,column = 7)
	Button(win,text="翻译",command = lambda : translation()).grid(row = 2,column = 8)
	
def replace():
	resultStr = ""
	replaceRet = False
	replaceCount = 0
	status = IntVar()
	for keyName in childpathmap.keys():
		if keyName in checkStatus.keys():
			status = checkStatus[keyName]
		else :
			status.set(0)
		if status.get() == 1 :
			filePath = childpathmap[keyName]
			if os.path.isfile(filePath):
				with open(filePath,'r', encoding='UTF-8') as file_r:
					lines = file_r.readlines()
					with open(filePath,'w',encoding='UTF-8') as file_w:
						for line in lines:
							if line.find(replaceKey.get()) != -1:
								resultStr = resultStr + line + "替换成" + "\n"
								line = replaceKey.get() + "=" + replaceValue.get() + "\n";
								resultStr = resultStr + line
								replaceRet = True
								replaceCount += 1
							file_w.write(line)
	if replaceRet :
		tkinter.messagebox.showinfo("有"+str(replaceCount)+"处被替换",resultStr)

def search():
	resultStr = ""
	searchCount = 0
	status = IntVar()
	for keyName in childpathmap.keys():
		if keyName in checkStatus.keys():
			status = checkStatus[keyName]
		else :
			status.set(0)
		if status.get() == 1 :
			filePath = childpathmap[keyName]
			if os.path.isfile(filePath):
				with open(filePath,'r', encoding='UTF-8') as file_r:
					lines = file_r.readlines()
					for line in lines:
						if replaceKey.get() != '' and replaceValue.get() != '':
							if line.find(replaceKey.get() + "=" + replaceValue.get()) != -1:
								searchCount += 1
								resultStr = resultStr + line + "\n"
						elif replaceKey.get() != '':
							if line.find(replaceKey.get()) != -1:
								searchCount += 1
								resultStr = resultStr + line + "\n"
								print(replaceKey.get())
						elif replaceValue.get() != '':
							if line.find(replaceValue.get()) != -1:
								searchCount += 1
								resultStr = resultStr + line + "\n"
					
	if searchCount > 0 :
		tkinter.messagebox.showinfo("查询到"+str(searchCount)+"个",resultStr)
	else :
		tkinter.messagebox.showinfo("没查询到")
	
def inset():
	resultStr = ""
	insertRet = False
	for keyName in childpathmap.keys():
		if keyName in checkStatus.keys():
			status = checkStatus[keyName]
		else :
			status = checkStatus["defualt"]
		if status.get() == 1 :
			filePath = childpathmap[keyName]
			if os.path.isfile(filePath):
				with open(filePath,'r', encoding='UTF-8') as file_r:
					lines = file_r.readlines()
					with open(filePath,'w',encoding='UTF-8') as file_w:
						for line in lines:
							file_w.write(line)
						file_w.write("\n" + replaceKey.get() + "=" + replaceValue.get() + "\n")
	tkinter.messagebox.showinfo("插入成功","插入成功")

def delete():
	resultStr = ""
	insertRet = False
	for keyName in childpathmap.keys():
		if keyName in checkStatus.keys():
			status = checkStatus[keyName]
		else :
			status = checkStatus["defualt"]
		if status.get() == 1 :
			filePath = childpathmap[keyName]
			if os.path.isfile(filePath):
				with open(filePath,'r', encoding='UTF-8') as file_r:
					lines = file_r.readlines()
					with open(filePath,'w',encoding='UTF-8') as file_w:
						for line in lines:
							if line.find(replaceKey.get() + "=" + replaceValue.get()) != -1:
								continue
							file_w.write(line)
	tkinter.messagebox.showinfo("删除成功","删除成功")
	
	
def translation():
	if checkStatus['en.txt'].get() == 1 and checkStatus['zh_CN.txt'].get() == 1:
		baidu_from = 'zh'
		baidu_to = 'en'
	elif checkStatus['zh_TW.txt'].get() == 1 and checkStatus['zh_CN.txt'].get() == 1:
		baidu_from = 'zh'
		baidu_to = 'cht'
	else :
		return
	baidu_appid = '20181027000225987'
	baidu_key = '4TYcP_uUit4JB7FLMdx9'
	baidu_q = replaceValue.get()
	baidu_salt = random.randint(32768, 65536)
	baidu_sign = baidu_appid + baidu_q + str(baidu_salt) + baidu_key
	m1 = hashlib.md5(baidu_sign.encode('utf-8'))
	baidu_sign = m1.hexdigest()
	baidu_Url = '/api/trans/vip/translate'
	baidu_Url = baidu_Url+'?appid='+baidu_appid+'&q='+urllib.parse.quote(baidu_q)+'&from='+baidu_from+'&to='+baidu_to+'&salt='+str(baidu_salt)+'&sign='+baidu_sign
	
	print(baidu_Url)
	httpClient = None
	try:
		httpClient = http.client.HTTPConnection('api.fanyi.baidu.com')
		httpClient.request('GET', baidu_Url)

		#response是HTTPResponse对象
		response = httpClient.getresponse()
		data = json.loads(response.read().decode('utf-8'))
		if 'error_code' in data:
			tkinter.messagebox.showinfo("翻译结果","翻译失败:"+data['error_code'])
		else :
			dst = data['trans_result'][0]['dst']
			replaceValue.set(dst)
		return dst
	except Exception as e:
		print(e)
	finally:
		if httpClient:
			httpClient.close()

win = Tk()
rootdir = StringVar()
checkStatus = {}
childpathmap = {}
replaceKey = StringVar()
replaceValue = StringVar()
languagemap = {"en.txt":"英文"
,"zh_CN.txt":"中文"
,"zh_TW.txt":"繁体"
,"defualt":"默认"}

Label(win,text = "翻译文件路径:").grid(row = 0,column = 0)
Entry(win,textvariable = rootdir).grid(row = 0,column = 1)
Button(win,text = "路径选择",command = selectPath).grid(row = 0,column = 2)
win.mainloop()
