# Corgi
Utility written in Python 2.7 to locate methods of specific functions on iOS.

## Dependency
Corgi is developed based on
 
* [Frida](https://frida.re)
* [MySQL](https://www.mysql.com)
* [IDA](https://www.hex-rays.com/products/ida/)

So, before you start to use Corgi, please make sure all of them work well.

Besides these softwares, Corgi uses some libraries of Python. They are as followings.

* termcolor
* MySQLdb
* sqlite3
* idc
* idautils
* idaapi

## Installation & Configuration
### Installation
Just git clone the repo to your own computer. Then, you've done the installation.

```
git clone https://github.com/cl0udz/Corgi
```

### Configuration
To use Corgi, you should first configure it to suit your environment.

1. Edit all the variables in config.py. The meaning of each variable is commented in the script.
2. Edit ScriptExecutor.py(line 15). Change the mysql address, username and password to your own.
3. Edit DataResolver.py(line 22). Change the mysql address, username and password to your own.
4. Edit IDAFuncExport.py(line 14-15). Change the script_path to the path of Corgi and change the class_filtered_dir to the name of class_filtered_directory.
4. Start your MySQL server and create a database named hook_log.
5. Done.

## Usage
### Steps
There are 5 steps that the user should do when using Corgi.

1. (Export function list) Open IDA with the target binary file. Execute IDAFuncExport.py in IDA.
2. (Start execution) `python Letrock.py [arguments]`
3. (Connect device) Connect your iOS device to your computer by USB.
4. (Perform target function) Under the guidance of Corgi, perform the function that you want to locate the methods on your iOS device.
5. (Find the key methods) When all done, you can find the outputs of Corgi in report_dir. And the key methods are expected to be included.

### Arguments
```
-f, --file                  specify the Binary file name
-j, --jumpto(optional)      jump to the specific step of Corgi if 
                            you've done the parts before that.
-n, --jscnt(optional)       if you directly jump to ScriptExecutor or 
                            parts after that, you should specify the 
                            number of js files
-a, --actionid(optional)    if the binary file has been analyzed 
                            before, you should specify an initial 
                            action ID for this execution so that 
                            your results won't be affected by former 
                            results.
```