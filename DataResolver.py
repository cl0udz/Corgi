# encoding: utf-8

import os.path
import sys
import time

from termcolor import colored

import config
import MySQLdb


class DataResolver(object):
    """docstring for DataResolver"""
    def __init__(self):
        super(DataResolver, self).__init__()
        
    def GetDifferentFuncListForActionId(self, action_id, compare_id):
        rp = os.path.join(config.get("report_dir"), config.get("cur_file_name")) + "_ActionID_%d.txt" % action_id

        f = open(rp, 'w+')
        db = MySQLdb.connect("localhost", "root", "your_pass", "hook_log")
        cur = db.cursor()

        cur.execute("CREATE TABLE tmp_%d_%d SELECT DISTINCT ActionId, Function_Name, JSid FROM (SELECT * FROM frida_log_%s WHERE ActionID = %d or ActionID = %d) as PI" % (action_id, compare_id, config.get('cur_file_name'), action_id, compare_id))
        
        db.commit()

        cur.execute("SELECT DISTINCT ActionId, Function_Name FROM tmp_%d_%d WHERE ActionID = %d and Function_Name NOT IN \
            (SELECT DISTINCT Function_Name FROM tmp_%d_%d where ActionId = %d);" % (action_id, compare_id, action_id, action_id, compare_id, compare_id))

        pi = cur.fetchone()
        while pi != None:
            print >> f, pi
            pi = cur.fetchone()

        cur.execute("DROP TABLE tmp_%d_%d" % (action_id, compare_id))

        db.commit()
