#!/usr/bin/python

import site
import sys
import os

sitedir_suffix='osmonitor'
filter_str='64'
default_cleandir='/home/orange/Downloads/osmonitor'

def getsitedir():
    
    dirs=site.getsitepackages()
    target_dir=''
    python_name='python{0}.{1}'.format(sys.version_info.major,sys.version_info.minor)
    
    for dir_ent in dirs:
        if python_name in dir_ent and site.PREFIXES[0] in dir_ent and filter_str in dir_ent:
            target_dir=dir_ent
            break  
    return target_dir

def updateCode(sourcedir):
    targetdir=getsitedir() + '/'+sitedir_suffix
    
    cmd_rm='rm -rf {0}'.format(targetdir)
    os.system(cmd_rm)
    
    cmd_cp='cp -rf {0} {1}'.format(sourcedir,targetdir)
    os.system(cmd_cp)
    
    cmd_pth=' cp -f {0}/*.pth {1}'.format(sourcedir,getsitedir())
    os.system(cmd_pth)
    
if len(sys.argv)<2:
    cleancode=default_cleandir
else:
    cleancode=sys.argv[1]

updateCode(cleancode)

