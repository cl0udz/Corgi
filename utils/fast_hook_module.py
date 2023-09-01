
# encoding: utf-8

import os.path
import sys
import frida
import time

src = '''
var argArray = new Array(11);

function strFilter(str) {
    for(var i=0; i<str.length; ++i){
        if(str.charCodeAt(i) >= 32 && str.charCodeAt(i) <= 127) { }
        else
            return str.substring(0, i);
    }
    return str;
}

function getObjCArgs(args, argNum) {
    for(var i=0; i<argNum+2; ++i) {
        try {
            tmp = new ObjC.Object(args[i]);
            argArray[i+1] = tmp.toString();
        } catch(error){
            try { 
                argArray[i+1] = strFilter(Memory.readCString(args[i], 128).toString());
            } catch(err) {
                argArray[i+1] = args[i].toString();
            }
        }
    }
}

function getCArgs(args, argNum) {
    for(var i=0; i<argNum; ++i) {
        try {
            argArray[i] = strFilter(Memory.readCString(args[i], 128).toString());
        } catch(error) {
            argArray[i] = args[i].toString();
        }
    }
}

function getRetVal(ret) {
    try {
        tmp = new ObjC.Object(ret);
        //var NSString = ObjC.classes.NSString;
        //NSString.initWithData_encoding_(tmp, NSUTF8StringEncoding);
        argArray[11] = tmp.toString();
    } catch(error) {
        try {
            argArray[11] = strFilter(Memory.readCString(ret, 128).toString());
        } catch(err) {
            argArray[11] = ret.toString();
        }
    }
}

var resolver = new ApiResolver('module');

function strFilter(str) {
    for(var i=0; i<str.length; ++i){
        if(str.charCodeAt(i) >= 32 && str.charCodeAt(i) <= 127)
            { }
        else
            return str.substring(0, i);
    }
    return str;

}

function hookObjC(funcname, argNum) {
    var name = funcname;
    resolver.enumerateMatches(name, {
        onMatch: function (match) {
                    send(match.name);
                    Interceptor.attach(match.address,{
                        onEnter: function (args) {
                                argArray[0] = match.name;
                                getObjCArgs(args, argNum);
                        },
        
                        onLeave: function(retval) { 
                            getRetVal(retval);
                            send(argArray);
                            //retval.replace(1);
                        }
                    })
        },
        onComplete: function () {}
    });
}
'''


def rewritesrc(funcname):
    ss = ""
    argNum = funcname.count(":")
    ss = src + "setTimeout(function(){{hookObjC(\"{0}\", {1})}}, 0);".format(funcname, argNum)

    return ss


def main():
    app = u"Ownbit"

    
    s = frida.get_usb_device().attach(app)
    script = s.create_script(rewritesrc(sys.argv[1]))
    script.on('message', on_msg)
    script.load()

    sys.stdin.read()


def on_msg(msg, data):
    print(msg)


if __name__ == '__main__':
        main()
