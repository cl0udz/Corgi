#!/usr/bin/env python
# coding=utf-8

def _init():
	"""docstring for global_var"""
	global _global_dict

	_global_dict = {
		# current OS
		"cur_os": "MAC",

		# location of frida scripts（MAC）
		"script_path_MAC": "/Volumes/Work/loccs/code/Corgi/frida_script",

		# location of 3rd-party lib database file（MAC）
		"db_path_MAC": "/Volumes/Work/loccs/what/cocoapods.db",

		# location of python scripts（WIN）
		"script_path_WIN": "F:\\loccs\\code\\Corgi\\",

		# location of 3rd-party lib database file（WIN）
		"db_path_WIN": "F:\\loccs\\what\\cocoapods.db",

		# directory to save filtered methods
		"class_filtered_dir": "/Volumes/Work/loccs/code/Corgi/class_filter_result",

		# directory to save frida scripts
		"frida_script_dir": "/Volumes/Work/loccs/code/Corgi/frida_script",

		# directory of logs
		"frida_log_dir": "/Volumes/Work/loccs/code/Corgi/frida_log",

		# (not needed to be configured in most cases) filename that is being analyzed
		"cur_file_name": "",

		# directory to save reports
		"report_dir": "/Volumes/Work/loccs/code/Corgi/report"
	}


def set(key, value):
	global _global_dict
	_global_dict[key] = value

def get(key):
	try:
		return _global_dict[key]
	except KeyError:
		return None
