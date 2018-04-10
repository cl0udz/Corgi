#!/usr/bin/env python
# encoding: utf-8

from termcolor import colored

import sys, os, getopt, time
reload(sys)
sys.setdefaultencoding("utf-8")

import config
import ScriptGenerator, ScriptExecutor, JSDivider, FuncFilter, DataResolver

#
# Name: SetCurBinName
# Args: None
# Retval: None
# Action: It will simply get the binary name from given filename
# 
def SetCurBinName(cur_file_name):
    config.set('cur_file_name', cur_file_name)
    return

def main(argv):
    config._init()

    appName = unicode(argv[1], 'utf-8')

    try:
        opts, args = getopt.getopt(argv[2:], "f:j:n:a:", ["file=", "jumpto=", 'jscnt=', 'actionid='])
    except Exception as e:
        raise e

    jumpFlag = 0
    actionid = 0
    actionNum = 2
    
    for opt, arg in opts:
        if opt in ("-f", '--file'):
            SetCurBinName(arg)
        elif opt in ("-j", '--jumpto'):
            if arg == "FuncFilter":
                jumpFlag = 0
            elif arg == "ScriptGenerator":
                jumpFlag = 1
            elif arg == "JSDivider":
                jumpFlag = 2
            elif arg == "ScriptExecutor":
                jumpFlag = 3
            else:
                jumpFlag = 4
        elif opt in ("-n", '--jscnt'):
            jscnt = int(arg)
        elif opt in ("-a", '--actionid'):
            actionid = int(arg)


    print colored('[Corgi] Welcome!', 'green')

    with open('log.txt', 'w+') as f:
        pass

    if config.get('cur_os') == "MAC":
        config.set('script_path',config.get('script_path_MAC'))
        config.set('db_path', config.get('db_path_MAC'))
    else:
        config.set('script_path', config.get('script_path_WIN'))
        config.set('db_path', config.get('db_path_WIN'))

    if jumpFlag <= 0:
        print colored("[FuncFilter] Filtering irrelavant methods...", 'yellow')
        cp = os.path.join(config.get('class_filtered_dir'), config.get('cur_file_name'))

        if os.path.exists(cp + "_filtered_class.txt"):
            print colored("[FuncFilter] Already filtered before.", 'yellow')
        else:
            ff = FuncFilter.FuncFilter(cp + '_origin_class.txt')
            result = ff.FuncFilterFunc()

            with open(cp + '_filtered_class.txt', 'w+') as f:
                for i in result:
                    print >> f, i[:-1]
            print ''

    if jumpFlag <= 1:
        print colored("[ScriptGenerator] Start generating...", 'yellow')
        sp = os.path.join(config.get('class_filtered_dir'), config.get('cur_file_name')) + "_filtered_class.txt"
        script_p = os.path.join(config.get('script_path'), config.get('cur_file_name')) + ".js"
        
        if os.path.exists(script_p):
            print colored("[ScriptGenerator] Already generated before.", 'yellow')
        else:
            sg = ScriptGenerator.ScriptGenerator()
            sg.GenerateScript(sp)
            print colored("[ScriptGenerator] Generated.", 'yellow')

    if jumpFlag <= 2:
        print colored("[JSDivider] Start dividing JS...", 'yellow')
        jsd = JSDivider.JSDivider()
        jscnt = jsd.divideJS(config.get('cur_file_name'))
        print colored("[JSDivider] Divided.", 'yellow')

    if jumpFlag <= 3:
        print colored("[ScriptExecutor] How many actions will you test?", 'yellow')
        actionNum = int(raw_input())

        for j in range(actionNum):
            for i in range(jscnt+1):
                print colored("[ScriptExecutor] Please prepare to perform Action %d(js %d)." % (j, i))

                while True:
                    input = raw_input("[ScriptExecutor] When ready, please input Y to start record:")
                    if input == "Y":
                        break

                print "???" + config.get('cur_file_name') + "_" + str(i) + ".js"
                se = ScriptExecutor.ScriptExecutor()
                se.StartExecute(config.get('cur_file_name') + "_" + str(i) + ".js", appName, j+actionid, i)

                print colored("[ScriptExecutor] Hooking functions in JS by Frida...", 'yellow')
                time.sleep(5)
                print colored("[ScriptExecutor] All functions hooked.", 'yellow')
                input = raw_input("[ScriptExecutor] Recording. Input D to stop record:")
                if input == "D":
                    continue

    print colored("[Corgi] Congrats. All done.", 'green')
    print colored("[Corgi] Now, let's rock with the data!", 'green')

    print colored("[DataResolver] Start resolving these data...", 'yellow')
    dr = DataResolver.DataResolver()
    for j in range(actionNum):
        if j % 2 == 0:
            dr.GetDifferentFuncListForActionId(j + actionid, j + actionid + 1)
            print colored("[DataResolver] Result for action %d generated." % (j), 'yellow')

            dr.GetDifferentFuncListForActionId(j + actionid + 1, j + actionid)
            print colored("[DataResolver] Result for action %d generated." % (j + 1), 'yellow')


    print colored("[Corgi] Finished.", 'green')


if __name__ == '__main__':
    main(sys.argv)