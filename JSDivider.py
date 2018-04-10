# encoding: utf-8

import os.path
import sys
import time

from termcolor import colored

import config

class JSDivider(object):
    """docstring for JSDivider"""
    def __init__(self):
        super(JSDivider, self).__init__()
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

    def divideJS(self, binname):
        self.path = config.get('script_path')
        self.f = open(os.path.join(self.path, binname) + ".js", 'r')

        cnt = 0
        filecnt = 0

        self.nf = open(os.path.join(self.path, binname) + "_0.js", 'w+')
        print >> self.nf, self.script_head
        for line in self.f:
            cnt += 1
            if cnt >= 3000:
                filecnt += 1
                cnt = 0
                self.nf.close()
                self.nf = open(os.path.join(self.path, binname) + "_"+ str(filecnt) +".js", 'w+')
                print >> self.nf, self.script_head
                self.nf.write(line)
            else:
                self.nf.write(line)

        self.nf.close()
        return filecnt

def main():
    config._init()

    if config.get('cur_os') == "MAC":
        config.set('script_path',config.get('script_path_MAC'))
        config.set('db_path', config.get('db_path_MAC'))
    else:
        config.set('script_path', config.get('script_path_WIN'))
        config.set('db_path', config.get('db_path_WIN'))

    jsd = JSDivider()
    jsd.divideJS(sys.argv[1])

if __name__ == '__main__':
    main()