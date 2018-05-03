#!/usr/bin/env python
# encoding: utf-8

from idc import *
from idautils import *
from idaapi import *

from NameAnalyzer import *
from CodeAnalyzer import *

import sys, os
reload(sys)
sys.setdefaultencoding("utf-8")

def main():
    paths = "/Users/Cloud/Documents/iOS/CryptoFuncFinder/Analyzer/result/"
    Wait()
    filename = get_root_filename()

    na = NameAnalyzer()
    func_list, func_list_head = na.StartNameAnalyze()

    with open(os.path.join(paths, "pipi.txt", 'w')) as f:
        for i in func_list:
            f.write(i)
            f.write('\n')

    # f = open(os.path.join(paths + filename) + "_result.txt", 'w')
    # for i in func_list_head:
    #ca = CodeAnalyzer()
    #ca.StartCodeAnalyze()
    #for i in ca.funccontent:
    #    f.write(ca.funccontent[i])
    #    f.write('\n')

    #f.close()


if __name__ == '__main__':
    main()