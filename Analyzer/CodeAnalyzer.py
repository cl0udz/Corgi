#!/usr/bin/env python
# encoding: utf-8

from idc import *
from idautils import *
from idaapi import *

class CodeAnalyzer():
    def __init__(self):
        self.ea = BeginEA()        
        self.candidate = []
        self.funccontent = {}

    def StartCodeAnalyze(self):
        self.__CCCrryptFinder()
        for i in self.candidate:
            self.__Decompiler(i)
            self.__Tracer(i)

    def __Tracer(self, ea):
        pass

    def __Decompiler(self, ea):
        cfunc = decompile(ea);
        if cfunc is None:
            print "Failed to decompile!"
            return True

        self.funccontent[ea] = ""
        sv = cfunc.get_pseudocode();
        for sline in sv:
            self.funccontent[ea] += tag_remove(sline.line)
            self.funccontent[ea] += '\n'

        return self.funccontent
    
    def __CCCrryptFinder(self):
        for funcea in Functions(SegStart(self.ea), SegEnd(self.ea)):
            for j in list(FuncItems(funcea)):
                if "CCCrypt" in GetDisasm(j):
                    self.candidate.append(funcea) #, GetDisasm(j)