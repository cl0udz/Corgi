#!/usr/bin/env python
# encoding: utf-8

from idc import *
from idautils import *
from idaapi import *

import re

import sys, os
reload(sys)
sys.setdefaultencoding("utf-8")

script_path = "/Volumes/Work/loccs/code/Corgi/"
class_filtered_dir = "class_filter_result"

# 匹配pattern之王
pattern_list = [
	'sub_[0-f]{8,10}', # 去掉所有子函数
	'nullsub'
]

def GetFunctionList():
	candidate = []

	Wait()

	ea = BeginEA()
	# ea = 0x0000000000001E80

	pattern = []
	for i in pattern_list:
		pattern.append(re.compile(i))

	for funcea in Functions(SegStart(ea), SegEnd(ea)):
		fn = GetFunctionName(funcea)
		match_flag = False
		for i in pattern:
			if i.match(fn) != None:
				match_flag = True
				break

		if not match_flag and fn.find('[') != -1 and fn.find(']') != -1:
			candidate.append(fn)

	return candidate

def WriteListToFile(filepath, data):
	with open(filepath, 'w+') as f:
		for i in data:
			print >> f, i


def main():
	FuncList = GetFunctionList()
	path = os.path.join(script_path, class_filtered_dir)
	filename = get_root_filename()
	WriteListToFile(os.path.join(path, filename + "_origin_class.txt"), FuncList)

if __name__ == '__main__':
	main()