#!/usr/bin/python

import site
import sys
import os

sitedir_suffix='osmonitor'
filter_str='64'
services=['neutron-server','neutron-openvswitch-agent','neutron-dhcp-agent','neutron-l3-agent']
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

def check_service_status(servname):
    #curdir=getsitedir() + '/'+sitedir_suffix
    #print(curdir)
    cmd='service {0} status'.format(servname)
    outp=os.popen(cmd).read()
    loaded_offset=outp.find('Loaded:')
    splitted=outp[loaded_offset:].split()
    return splitted[1]=='loaded'

def restart_service(servname):
    cmd='service {0} restart'.format(servname)
    os.system(cmd)

def restartAll():
    global services
    for service in services:
        if check_service_status(service):
            restart_service(service)

def updateCode(sourcedir):
    targetdir=getsitedir() + '/'+sitedir_suffix
    cmd='cp -f {0}/* {1}'.format(sourcedir,targetdir)
    os.system(cmd)
    
if len(sys.argv)<2:
    cleancode=default_cleandir
else:
    cleancode=sys.argv[1]

updateCode(cleancode)
restartAll()
