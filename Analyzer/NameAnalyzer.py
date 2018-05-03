#!/usr/bin/env python
# encoding: utf-8

from idc import *
from idautils import *
from idaapi import *

from PatternFilter import *

# import sys
# reload(sys)
# sys.setdefaultencoding("utf-8")

#  This class is defined as an automatically function name analyzer
#  in an IDA context.
#
#   !!!ATTENTION!!!
#       Nothing is worth mentioning here :P
#
#   How To Use:
#       First you should new a instance for NameAnalyzer:
#           The argument(funcname) is the name of the function. IT IS NEEDED WHEN YOU NEW A INSTANCE
#       1   na = NameAnalyzer()
#
#       Then you just need to call StartNameAnalyze(), it will return a list of relevant functioname and corresponding head
#       2   for i, j in ff.StartNameAnalyze():
#       3       return True
#       4   else:
#       5       return False
#
#       Whenever you want to replace the args with a new one, just call the corresponding method
#       6   newkeywords = ['apple', 'pear']
#       7   ff.SetKeywords(newkeywords)
#
#       Besides that, the token words in pattern template and in this class should be the same word,
#       which means that your should set a new token word when you set a new pattern template
#       For example:
#       8   newtemplate = [
#       9   {
#       10      "prefix": "[0-9]{",
#       11      "template": "NEWTOKEN",
#       12      "suffix": "}"
#       13      }
#       14  ]
#       15  ff.SetPatternTemplate(newtemplate)
#       16  ff.SetTokenWord("newtoken")

class NameAnalyzer():
    def __init__(self):
        self.ea = BeginEA()
        self.output = ""
        self.candidate = {}
        self.parsedname = []
        self.relevant_list = []
        self.relevant_func_head = []

    def __log(self, data):
        f = open("/Users/Cloud/Documents/iOS/CryptoFuncFinder/Analyzer/log.txt", 'a')
        f.write(data)
        f.write('\n')
        f.close()

    # The external method to analyze the given name
    def StartNameAnalyze(self, keywords = [], special_keywords = [], pattern_template = [], tokenword = ""):
        if self.__GetFuncName():
            pf = PatternFilter()

            if keywords != []:
                pf.SetKeywords(keywords)
            if special_keywords != []:
                pf.SetSpecialKeywords(special_keywords)
            if pattern_template != []:
                pf.SetPatternTemplate(pattern_template)
                pf.SetTokenWord(tokenword)

            #for i in self.candidate:
            #    self.__log(i + "aaaaaaaa" + str(self.candidate[i]))
            for i in self.candidate:
                pn = self.__ParseName(i)
                self.__ChkRelation(self.candidate[i], i, pn, pf)
        return self.relevant_list, self.relevant_func_head

    def __GetFuncName(self):
        for funcea in Functions(SegStart(self.ea), SegEnd(self.ea)):
            self.candidate[GetFunctionName(funcea)] = funcea
            #self.__log(GetFunctionName(funcea) + "::::" + self.candidate[GetFunctionName(funcea)])
            

        return True

    def __ParseName(self, srcname):
        parsedname = ""

        lastword = 0

        i = 0
        while(i < len(srcname)):
            if(srcname[i].isupper() or srcname[i] == ':' or srcname[i] == ' '):
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

        self.parsedname.append(parsedname)

        return

    def __ChkRelation(self, head, fn, pn, ff = None):
        if ff == None:
            ff = PatternFilter()

        if ff.ChkRelation(fn):
            self.relevant_list.append(pn)
            self.relevant_func_head.append(head)
            return True
        else:
            return False

    def Output(self):
        with open('func_parsed.txt', 'a') as f:
            print >> f, self.parsedname
