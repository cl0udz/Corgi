#!/usr/bin/env python
# encoding: utf-8

import sqlite3
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

DB_PATH = "info.db"


keywords = [
    "中国银行",
    "农业银行",
    "工商银行",
    "华夏银行",
    "汇丰银行",
    "邮政储蓄",
    "支付宝",
    "光大银行",
    "民生银行",
    "招商银行",
    "浦发银行",
    "广发银行",
    "兴业银行",
    "中信银行",
    "北京银行",
    "重庆银行",
    "信用社",
    "农村商业银行",
    "农商银行",
    "微众银行",
    "微信钱包",
    "百度钱包",
    "银联",
    "京东",
    "壹钱包",
    "翼支付",
    "美团",
    "苏宁",
    "和包"
    "沃支付",
    "财付通",
    "云闪付",
    "工银",
    "交通银行",
    "平安信用卡",
    "小米金融"
]

def main():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    commmand = "select title, down_u from ipa_info where title LIKE \"%"

    with open("RelatedAPP.txt", 'w') as f:
        for i in keywords:
            r_command = commmand + i + "%\""
            result = c.execute(r_command)
            for j in result:
                print >> f, j[0], "\t",
                print >> f, j[1]



if __name__ == '__main__':
    main()