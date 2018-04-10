
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

setTimeout(function(){hookObjC("-[BDSIntent userInfo]", 0)}, 0);
