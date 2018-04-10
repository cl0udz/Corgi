#!/usr/bin/env python
# encoding: utf-8

import sqlite3
from termcolor import colored


import sys, os
reload(sys)
sys.setdefaultencoding("utf-8")

import config

class FuncFilter(object):
    """docstring for FuncLister"""
    #
    # Init the instance with a filename and a filter_list(optional)
    # 
    #     The filename should be like xxxx_origin_classyyyy and xxxx is 
    # the Binary's filename.
    #     The filter_list contains all the words that should be strictly
    # filetered later.(When start filtering, the instance will automatically
    # parse the name and find these words)
    # 
    def __init__(self, filename, class_keyword_filter_list = None, class_head_filter_list = None, class_tail_filter_list = None, method_keyword_filter_list = None, method_head_filter_list = None):
        super(FuncFilter, self).__init__()
        self.filename = filename

        if class_keyword_filter_list != None:
            self.class_keyword_filter_list = class_keyword_filter_list
        else:
            self.class_keyword_filter_list = [
                                    'UI', 'Button', 'TextView', 'AlertView', 'NS', 'Model', 'Layout', 'SDK', 'Toast', 'Delegate',
                                    'Parse', 'Parser', 'Brightness', 'App', 'APP', 'Copy', 'Controller'
                                ]

        if class_head_filter_list != None:
            self.class_head_filter_list = class_head_filter_list
        else:
            self.class_head_filter_list = [
                                "XY", "SD", "Tencent", "QQ", 'ZX', 'TB', 'GP', 'QJ', 'Gexin', 'JX', "YL", "TalkingData",
                                "_Ttc", "RRD", "WE", "Join", 'RAC', 'SBJson', 'NS', 'WX', 'UI', 'GTX', 'UP', 'POP', 'ASI',
                                'MZT', 'Mob', 'AF', 'SDK', 'RN', 'AX', 'DD', 'CM', 'RSA', 'SR', 'Ad', 'UPMP', 'TD', 'UM',
                                'TDB', 'GX', 'MK', 'TP', 'GeTui', 'TDA', 'AK', 'RT', 'CMBC', 'CardIO', 'ML', 'XH', 'LD',
                                'HV', 'Open', 'Dejal', 'TP', 'MBP', 'WK', 'SFHF', 'MAS', 'XH', 'MS', 'MB', 'Growing', 'FMG3',
                                'GTM', 'Animation', "PD", "MW", "MJ", 'LFCG', 'LD', 'JP', 'JK', 'IVY', 'IS', 'Iphone', 'IFly',
                                "DW", "BB", 'GPB', 'CV', 'CipherDB', 'BM', 'API', 'All', 'Ali', 'AF', 'Acc', 'Jeky', "YFB",
                                'TC', 'WeChat', 'WK', 'Xiami', 'WX', 'TTS', 'UT', "Wap", "WB", "SSAIO", "TB", "UIC", 'UP',
                                 'UTD', 'WV', '_', 'JSON', 'BDN', 'Bainuo'
                                 ]

        if class_tail_filter_list != None:
            self.class_tail_filter_list = class_tail_filter_list
        else:
            self.class_tail_filter_list = [
                                "View", "view", "Item", "item", "btn", "Label", "Cell", "ActionSheet", "Button", "Layout", 'Bar',
                                'Agent', "Delegate", 'Alert', 'Controller'
                                ]

        if method_keyword_filter_list != None:
            self.method_keyword_filter_list = method_keyword_filter_list
        else:
            self.method_keyword_filter_list = [
                                    'UI', 'Button', 'TextView', 'AlertView', 'NS', 'Size', 'size', 'Animated', 
                                    'hide', 'Animation', 'Format', 'Java', 'java', 'Script', 'action', 'Toast',
                                    'Font', 'JSON', 'view', 'View', 'Input', 'Btn', '_', 'Delegate', 'Input', 'Button',
                                    'show', 'btn', 'click', 'Click', 'Convert', 'convert', 'Height', 'Width', 'left',
                                    'Left', 'right', 'Right', 'down', 'Down', 'up', 'Up', 'top', 'Top', 'Parse',
                                    'Parser', 'parse', 'color', 'Color', 'Cell', 'Json', 'json', 'navigation',
                                    'Navigation', 'Label', 'timestamp', 'Stamp', 'time', 'Time', 'test', 'Test','min',
                                    'Min', 'max', 'Max', 'draw', 'Display', 'Brightness', 'Tag', 'copy', 'Copy', 'Table',
                                    'table'
                                ]

        if method_head_filter_list != None:
            self.method_head_filter_list = method_head_filter_list
        else:
            self.method_head_filter_list = [
                                    "set", "get", "dealloc", "delegate", "setDelegate", ".", "is", "init", 'size', 'draw'
                                ]

    #
    # Name: __LoadOriginClass
    # Args: None
    # Retval: None
    # Action: It will simply get the binary name from given filename
    # 
    def __LoadOriginClass(self, filename):
         self.candidate = []
         with open(filename, 'r') as f:
             count = -1
             for i in f:
                 count += 1
                 self.candidate.append(i)

             self.file_length = count

    #
    # Name: __GetClassName
    # Args: name        given whole name
    # Retval: class name(string)
    # Action: It will pick up the class name from given name
    # 
    def __GetClassName(self, name):
        if ('[' in name) and (']' in name):
            return name.split(' ')[0][2:]

    #
    # Name: __GetMethodName
    # Args: name        given whole name
    # Retval: method name(string)
    # Action: It will pick up the method name from given name
    # 
    def __GetMethodName(self, name):
        if ('[' in name) and (']' in name):
            return name.split(' ')[1][:-1]

    #
    # Name: __FuncFilter
    # Args: cand_class_name
    # Retval: if passed all rule(False),
    #          if not(True)
    # Action: It will check if the class name should be filter
    # 
    def __FilterByClassName(self, cand_class_name):

        conn = sqlite3.connect(config.get('db_path'))
        c = conn.cursor()

        ## rule 0: if the class name passed before, just go
        if cand_class_name in self.passed_class:
            return False

        ## rule 1: if the class name has been filtered before
        if cand_class_name in self.filtered_class:
            return True


        ## rule 2: if the class name belong to some third party lib
        c.execute('SELECT classname FROM classmap WHERE classname == ?', [cand_class_name])

        if c.fetchone() != None:
            self.filtered_class.append(cand_class_name)
            return True

        ## rule 3: if the class name startwith one keyword given in class_head_filter_list
        for j in self.class_head_filter_list:
            if cand_class_name.startswith(j):
                self.filtered_class.append(cand_class_name)
                return True

        ## rule 4: if the class name endwith one keyword given in class_tail_filter_list
        for j in self.class_tail_filter_list:
            if cand_class_name.endswith(j):
                self.filtered_class.append(cand_class_name)
                return True

        ## rule 5: if the class name includes keyword(s) given in class_filter_list
        pn = self.__ParseName(cand_class_name)
        for j in pn:
            if j in self.class_keyword_filter_list:
                self.filtered_class.append(cand_class_name)
                return True

        self.passed_class.append(cand_class_name)
        return False

    #
    # Name: __FilterByMethodName
    # Args: cand_method_name
    # Retval: if passed all rule(False),
    #          if not(True)
    # Action: It will check if the method name should be filter
    # 
    def __FilterByMethodName(self, cand_method_name):

        ## rule 0: if the method name passed before, just go
        if cand_method_name in self.passed_class:
            return False

        ## rule 1: if the method name has been filtered before
        if cand_method_name in self.filtered_method:
            return True

        ## rule 2: if the method name startswith one keyword given in method_head_filter_list
        for j in self.method_head_filter_list:
            if cand_method_name.startswith(j):
                self.filtered_method.append(cand_method_name)
                return True

        pn = self.__ParseName(cand_method_name)

        ## rule 3: if the method name only includes one word
        if len(pn) == 1:
            return True

        ## rule 4: if the method name includes keyword(s) given in method_filter_list
        for j in pn:
            if j in self.method_keyword_filter_list:
                self.filtered_method.append(cand_method_name)
                return True
        
        self.passed_method.append(cand_method_name)
        return False

    #
    # Name: FuncFilter
    # Args: None
    # Action: It will simply get the binary name from given filename
    # 
    def FuncFilterFunc(self):
        self.__LoadOriginClass(self.filename)
        result = []

        self.filtered_class = []
        self.passed_class = []
        self.filtered_method = []
        self.passed_method = []

        maxcol = 150

        count = -1
        try:
            for i in self.candidate:
                # filter by class Name
                count += 1
                cand_class_name = self.__GetClassName(i)

                print colored("\r[FuncFilter] [%02.2f%%]" % (float(count)/self.file_length * 100), 'yellow'),# Dealing with class name : %s" % (float(count)/self.file_length * 100, cand_class_name[:maxcol-50]), 'yellow'),

                ## if not passed, continue
                if self.__FilterByClassName(cand_class_name):
                    continue

                # filter by method name
                cand_method_name = self.__GetMethodName(i)

                print colored("\r[FuncFilter] [%02.2f%%]" % (float(count)/self.file_length * 100), 'yellow'),# Dealing with method name : %s" % (float(count)/self.file_length * 100, cand_class_name[:maxcol-50]), 'yellow'),

                ## if not passed, continue
                if self.__FilterByMethodName(cand_method_name):
                    continue

                ## if all passed, add the name into result list
                result.append(i)
        except Exception as e:
            print colored(cand_class_name, 'red')
            raise e


        return result

    #
    # Name: __ParseName
    # Args: filename       The filename of the original class list
    # Action: It will simply get the binary name from given filename
    # 
    def __ParseName(self, srcname):
        parsedname = ""

        lastword = 0

        srcname = srcname.replace('[', '')
        srcname = srcname.replace(']', '')
        srcname = srcname.replace(':', ' ')
        srcname = srcname.replace('_', ' ')


        i = 0
        while(i < len(srcname)):
            if(srcname[i].isupper() or srcname[i] == ':' or srcname[i] == ' ' or srcname[i] == '_'):
                parsedname = parsedname + srcname[lastword:i] + " "

                lastword = i

                while(i + 1 < len(srcname) and (srcname[i+1].isupper() or srcname[i+1] == ':' or srcname[i+1] == ' ')):
                    i = i + 1

                if(lastword != i):
                    i = i
                else:
                    i = i + 1
            else:
                i = i + 1

        parsedname = parsedname + srcname[lastword:]

        with open('log.txt', 'a+') as f:
            print >> f, parsedname

        return parsedname.split(' ')

def main():
    config._init()

    with open('log.txt', 'w+') as f:
        pass

    if config.get('cur_os') == "MAC":
        config.set('script_path',config.get('script_path_MAC'))
        config.set('db_path', config.get('db_path_MAC'))
    else:
        config.set('script_path', config.get('script_path_WIN'))
        config.set('db_path', config.get('db_path_WIN'))

    cp = os.path.join(config.get('class_filtered_dir'), sys.argv[1])

    ff = FuncFilter(cp + '_origin_class.txt')
    result = ff.FuncFilterFunc()

    with open(cp + '_filtered_class.txt', 'w+') as f:
        for i in result:
            print >> f, i[:-1]

if __name__ == '__main__':
    main()