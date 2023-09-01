# encoding: utf-8

import os.path

import config
from termcolor import colored


class ScriptGenerator(object):
    """docstring for ScriptGenerator"""
    def __init__(self):
        super(ScriptGenerator, self).__init__()

        self.script_head = '''
var resolver = new ApiResolver('objc');

function onEnterFunc(args, argNum, infoArray){
    // infoArray = [ argNum, args[1], args[2], ... , args[argNum + 1], args[0], retval, funcname ]
    infoArray[0] = argNum;

    /*try {
        tmp = new ObjC.Object(args[0]);
        infoArray[argNum + 2] = tmp.toString();
    } catch(error){
        try { 
            infoArray[argNum + 2] = strFilter(Memory.readCString(args[0], 128).toString());
        } catch(err) {
            infoArray[argNum + 2] = args[0].toString();
        }
    }*/

    for(var i=1; i<argNum+2; ++i) {
        infoArray[i] = 'arg';
        /*try {
            tmp = new ObjC.Object(args[i]);
            infoArray[i] = tmp.toString();
        } catch(error){
            try { 
                infoArray[i] = strFilter(Memory.readCString(args[i], 128).toString());
            } catch(err) {
                infoArray[i] = args[i].toString();
            }
        }*/
    }

    return;
}

function onLeaveFunc(retval, argNum, infoArray){

    infoArray[argNum + 3] = 'retval';
    /*try {
        tmp = new ObjC.Object(retval);
        infoArray[argNum + 3] = tmp.toString();
    } catch(error){
        try { 
            infoArray[argNum + 3] = strFilter(Memory.readCString(retval, 128).toString());
        } catch(err) {
            infoArray[argNum + 3] = retval.toString();
        }
    }*/

    return;
}

function strFilter(str) {
    for(var i=0; i<str.length; ++i){
        if(str.charCodeAt(i) >= 32 && str.charCodeAt(i) <= 127)
            { }
        else
            return str.substring(0, i);
    }
    return str;
}

function hookObjC(FuncName, ArgNum){
    resolver.enumerateMatches(FuncName, {
        onMatch: function (match) {
                    // infoArray = [ argNum, args[1], args[2], ... , args[argNum + 1], args[0], retval, funcname ]
                    var infoArray = new Array(ArgNum + 4);
                    infoArray[ArgNum + 4] = match.name;
                    //send(match.name);

                    Interceptor.attach(match.address, {
                    onEnter: function(args){
                        //send(match.name);
                        onEnterFunc(args, ArgNum, infoArray);
                    },
                    onLeave: function(retval){
                        onLeaveFunc(retval, ArgNum, infoArray);
                        send(infoArray);
                    }
                    })
                },
        onComplete: function () {
                }
    }); 
}
'''

    def __generate_script(self, funcname):
        isObjc = True
        resolver = 'objc'

        if funcname.__contains__("["):
            # an objective C function
            argNum = funcname.count(":")
            func = funcname
        else:
            # a C function
            argNum = 0
            isObjc = False
            resolver = 'module'
            func = "exports:*!" + funcname.replace("_", "")

        if isObjc:
            # objc function
            scr = 'setTimeout(function(){hookObjC("%s", %d)}, 0);' % (func, argNum)
        else:
            # C function
            scr = '''
            '''
        return scr

    def GenerateScript(self, funclist):
        sp = os.path.join(config.get('script_path'), config.get('cur_file_name')) + ".js"

        g = open(sp, 'w+')
        print(self.script_head, file = g)


        flp = os.path.join(config.get('class_filtered_dir'), funclist)
        with open(flp, 'r') as f:
            for line in f:
                script = self.__generate_script(line[:-1])

                print(script, file = g)

        g.close()

def main():
    print(colored("[ScriptGenerator] Start generating...", 'yellow'))
    config._init()

    with open('log.txt', 'w+') as f:
        pass

    if config.get('cur_os') == "MAC":
        config.set('script_path',config.get('script_path_MAC'))
        config.set('db_path', config.get('db_path_MAC'))
    else:
        config.set('script_path', config.get('script_path_WIN'))
        config.set('db_path', config.get('db_path_WIN'))

    sg = ScriptGenerator()
    sg.GenerateScript("BWA_filtered_class.txt")
    print(colored("[ScriptGenerator] Generating finished...", 'yellow'))

if __name__ == '__main__':
    main()
