import os
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

IDA32_MAC_PATH = "/Applications/IDA\ Pro\ 7.0/ida.app/Contents/MacOS/ida "
IDA64_MAC_PATH = "/Applications/IDA\ Pro\ 7.0/ida64.app/Contents/MacOS/ida64 "

SCRIPTPATH = "/Users/Cloud/Documents/iOS/CryptoFuncFinder/Analyzer/main.py"

CURRENT_IDA_PATH = IDA32_MAC_PATH

tmp = "/Users/Cloud/Documents/iOS/IDA_script/idb/20171209_64828_214455645172"

cmd = CURRENT_IDA_PATH + ' -B -S"' + SCRIPTPATH + '" ' + tmp
os.system(cmd)