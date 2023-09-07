import ida_auto, idc, ida_ida
import re
import idautils, idaapi, ida_funcs, ida_bytes

import os

script_path = "Z:\projects\Corgi"
class_filtered_dir = "class_filter_result"

# 匹配pattern
pattern_list = [
	'sub_[0-f]{8,10}', # 去掉所有子函数
	'nullsub'
]

def DeMangleName(name):
	return idc.Demangle(name, idc.GetLongPrm(idc.INF_SHORT_DN))

def GetFunctionList():
	candidate = []

	ida_auto.auto_wait()

	ea = ida_ida.inf_get_min_ea()
	# ea = 0x0000000000001E80

	pattern = []
	for i in pattern_list:
		pattern.append(re.compile(i))

	for s in idautils.Segments():
		start = idc.get_segm_start(s)
		end = idc.get_segm_end(s)
		name = idc.get_segm_name(s)
		data = ida_bytes.get_bytes(start, end-start)

		for funcea in idautils.Functions(start, end):
			fn = ida_funcs.get_func_name(funcea)
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
			print(i, file=f)


def main():
	FuncList = GetFunctionList()
	path = os.path.join(script_path, class_filtered_dir)
	filename = idaapi.get_root_filename()
	WriteListToFile(os.path.join(path, filename + "_origin_class.txt"), FuncList)

if __name__ == '__main__':
	main()