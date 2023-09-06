# encoding: utf-8

import os.path
import sys
import time

from termcolor import colored

import config
import pymysql


class DataResolver(object):
    """
    This class is defined as the resolver of collected data to generate the report.
    """
    def __init__(self):
        super(DataResolver, self).__init__()
        

    #
    # Name: GetDifferentFuncListForActionId
    # Args: action_id           ID of the performed action
    #       compare_id          ID of the action to be compared with
    # Retval: No return value
    # Action: It will find the difference in called methods between the two actions.
    # 
    def GetDifferentFuncListForActionId(self, action_id, compare_id):
        rp = os.path.join(config.get("report_dir"), config.get("cur_file_name")) + "_ActionID_%d.txt" % action_id

        f = open(rp, 'w+')
        db = pymysql.connect(host = "localhost", user = "root", password = "", database = "hook_log")
        cur = db.cursor()

        cur.execute("CREATE TABLE tmp_%d_%d SELECT DISTINCT ActionId, Function_Name, JSid FROM (SELECT * FROM frida_log_%s WHERE ActionID = %d or ActionID = %d) as PI" % (action_id, compare_id, (config.get('cur_file_name').replace('-', '')), action_id, compare_id))
        
        db.commit()

        cur.execute("SELECT DISTINCT ActionId, Function_Name FROM tmp_%d_%d WHERE ActionID = %d and Function_Name NOT IN \
            (SELECT DISTINCT Function_Name FROM tmp_%d_%d where ActionId = %d);" % (action_id, compare_id, action_id, action_id, compare_id, compare_id))

        pi = cur.fetchone()
        while pi != None:
            print(pi, file = f)
            pi = cur.fetchone()

        cur.execute("DROP TABLE tmp_%d_%d" % (action_id, compare_id))

        db.commit()
