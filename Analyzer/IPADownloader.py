#!/usr/bin/env python
# encoding: utf-8

import sys
import shutil
import os
import multiprocessing
import time

reload(sys)
sys.setdefaultencoding("utf-8")

IPAFilePath = r"D:\iOS\IPAFiles"
#IPAFilePath = r"D:\iOS\code\IPA_Spider\extractTest"
urlPath = r"D:\iOS\code\IPA_Spider\urls1.txt"
#wget.exe 路径
wget = r"D:\iOS\code\IPA_Spider\extractTest\wget64.exe"
#7z.exe路径
_7z = r'"C:\Program Files\7-Zip\7z.exe"'
IDBStorage = r"D:\iOS\IDBS"
#IDBStorage = r"D:\iOS\code\IPA_Spider\extractTest\123"
IDA32_path = "idaq.exe -B "

existFiles = []
urls = []

def init():
    global urls,existFiles
    existFiles = os.listdir(IPAFilePath)
    url_ =sys.argv[1]
    with open(url_,"r") as f:
        urls = f.read().split("\n")

def handleUrl(url):
    if url == "":
        return
    tmp = url.split("/")[-1]
    if tmp in existFiles:
        return
    cmd = wget + " -P "+ IPAFilePath + " "+url + ' 2>NUL 1>NUL'
    result = os.system(cmd)
    
    if result == 0:
        tmp = tmp.replace(".ipa","")
        #解压的
        t_path = os.path.join(IPAFilePath,tmp)
        if os.path.exists(t_path):
            cmd = "rd /s/q " + t_path
            os.system(cmd)
        result = os.mkdir(t_path)
        cmd = _7z + ' x -y -aoa -o'+ r"%s"%t_path + " " + os.path.join(IPAFilePath,tmp+".ipa") + ' 2>NUL 1>NUL'
        
        result = os.system(cmd)
        
def main():
    init()

    for i in urls:
        handleUrl(i)

if __name__ == '__main__':
    main()