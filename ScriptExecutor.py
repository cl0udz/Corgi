# encoding: utf-8

import os.path
import sys
import frida
import time

import pymysql

import config

from threading import Timer
from termcolor import colored

db = pymysql.connect(host = "localhost", user = "root", password = "", database = "hook_log")
jsno = 0

actionId = 0

def SetJsNo(new_no):
    global jsno
    jsno = new_no

def SetActionID(new_id):
    global actionId
    actionId = new_id

def on_msg(msg, data):
    global db
    global actionId
    global jsno
    cur = db.cursor()

#
# +---------------+---------+------+-----+---------+-------+
# | Field         | Type    | Null | Key | Default | Extra |
# +---------------+---------+------+-----+---------+-------+
# | ActionId      | int(11) | YES  |     | NULL    |       |
# | Function_Name | text    | NO   |     | NULL    |       |
# | ARG0          | text    | NO   |     | NULL    |       |
# | ARG1          | text    | NO   |     | NULL    |       |
# | ARG2          | text    | YES  |     | NULL    |       |
# | ARG3          | text    | YES  |     | NULL    |       |
# | ARG4          | text    | YES  |     | NULL    |       |
# | ARG5          | text    | YES  |     | NULL    |       |
# | ARG6          | text    | YES  |     | NULL    |       |
# | ARG7          | text    | YES  |     | NULL    |       |
# | ARG8          | text    | YES  |     | NULL    |       |
# | ARG9          | text    | YES  |     | NULL    |       |
# | ARG10         | text    | YES  |     | NULL    |       |
# | Return_Value  | text    | YES  |     | NULL    |       |
# +---------------+---------+------+-----+---------+-------+
#
# infoArray = [ argNum, args[1], args[2], ... , args[argNum + 1], args[0], retval, funcname ]

    if msg['type'] == 'send':
        infoArray = msg['payload']
        if infoArray[0] == None:
            print(colored("[ScriptExecutor] [Dust 1]" + str(msg), "grey"))
            return

        argNum = int(infoArray[0])

        #print argNum + 5
        #print msg['payload'].__len__
        if msg['payload'].__len__() != argNum + 5:
            print(colored("[ScriptExecutor] [Dust 2]" + str(msg), "grey"))
        else:
            args = []
            args.append(infoArray[argNum+2])
            args.append(infoArray[1])
            args.append(infoArray[2])
            args.append(infoArray[3] if argNum>0 else "null")
            args.append(infoArray[4] if argNum>1 else "null")
            args.append(infoArray[5] if argNum>2 else "null")
            args.append(infoArray[6] if argNum>3 else "null")
            args.append(infoArray[7] if argNum>4 else "null")
            args.append(infoArray[8] if argNum>5 else "null")
            args.append(infoArray[9] if argNum>6 else "null")
            args.append(infoArray[10] if argNum>7 else "null")

            normalied_name = config.get('cur_file_name').replace('-', '')
            
            try:
                cur.execute("INSERT INTO frida_log_%s VALUES(%d, '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', default, %d)"
                                                   % (normalied_name, actionId, infoArray[argNum+4], args[0], args[1], args[2], args[3], args[4], args[5], args[6],
                                                    args[7], args[8], args[9], args[10],
                                                    infoArray[argNum+3], jsno))
                db.commit()
            except Exception as e:
                print(colored("[ScriptExecutor] [ERROR] INSERT INTO frida_log_%s VALUES(%d, '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', default, %d)"
                                                   % (normalied_name, actionId, infoArray[argNum+4], args[0], args[1], args[2], args[3], args[4], args[5], args[6],
                                                    args[7], args[8], args[9], args[10],
                                                    infoArray[argNum+3], jsno), 'red'))



class ScriptExecutor(object):
    """docstring for ScriptExecutor"""
    
    def __init__(self):
        super(ScriptExecutor, self).__init__()
        self.timer_interval = 5

    def StartExecute(self, filename, app, action_id, new_no):
        #app = u"百度钱包"
        SetJsNo(new_no)
        SetActionID(action_id)

        query_str = "create table if not exists frida_log_%s(ActionId int null,Function_Name text not null,ARG0 text not null,ARG1 text not null,\
            ARG2 text null,ARG3 text null,ARG4 text null,ARG5 text null,ARG6 text null,ARG7 text null,ARG8 text null,ARG9 text null,\
            ARG10 text null,Return_Value text null,CreateTime timestamp default CURRENT_TIMESTAMP null comment '创建时间',JSid int null)" % (config.get('cur_file_name').replace('-', ''))
        db.cursor().execute(query_str)

        db.commit()

        sp = config.get('script_path')

        f = open(os.path.join(sp, filename), 'r')

        st = f.read()
        s = frida.get_usb_device().attach(app)
        script = s.create_script(st)
        script.on('message', on_msg)
        script.load()

        #t = Timer(timer_interval, DBCommit)
        #t.start()



def main():
    config._init()

    if config.get('cur_os') == "MAC":
        config.set('script_path',config.get('script_path_MAC'))
        config.set('db_path', config.get('db_path_MAC'))
    else:
        config.set('script_path', config.get('script_path_WIN'))
        config.set('db_path', config.get('db_path_WIN'))

    se = ScriptExecutor()
    se.StartExecute(sys.argv[1], u'百度钱包', 2, 7)


if __name__ == '__main__':
    main()
