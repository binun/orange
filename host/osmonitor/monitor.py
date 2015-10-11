import datetime
import time
import site
import sys
import os
import threading
import socket
import atexit
from conf import read_conf_file
from tracers import trace_calls

recent_imports={}
interval=5
sock=None
conf_file='amm.conf'
host=''
port=6666

def cleanup():
    global sock
    sock.close()

def log_message(tag,message):   
    global sock
    global host
    global port
    
    os_cmdline='ps -p {0} -o cmd'.format(os.getpid())
    cmdline=os.popen(os_cmdline).read()
    agent=cmdline.split('\n')[1]
    timestamp=datetime.datetime.strftime(datetime.datetime.now(), '%H-%M-%S') 
    full_msg='{0}: {1} by {2} at {3} MSGEND)'.format(tag,message,agent,timestamp)
    try:
        sock.sendto(full_msg,(host,port))
    except:
        pass
    
def my_daemon():
    global interval
    global recent_imports
    global sock
    global host
    global port
    
    #Retrieving AMM settings
    
    host=read_conf_file('amm.conf','coordinator','host','localhost')
    port=int(read_conf_file('amm.conf','coordinator','port','6666'))
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
       
    #Now we have the connected socket...
    log_message('Startup', 'Launch monitoring')
    
    while True:
        #current_modules=sys.modules.keys()
        #process=os.getpid()
        #recent_imports[process]=current_modules
        log_message('Timer','Modules')
        time.sleep(interval)

def in_context():
    context_template=read_conf_file('amm.conf','agent','context','nova')
    #print(context_template)
    os_cmdline='ps -p {0} -o cmd'.format(os.getpid())
    cmdline=os.popen(os_cmdline).read()
    agent_name=cmdline.split('\n')[1]
    #print(agent_name)
    if agent_name.count(context_template)>1:
        return True
    else:
        return False

def init():  
    atexit.register(cleanup)
    is_in_context=in_context()
    if is_in_context:
		sys.settrace(trace_calls)
        #print('Monitoring on')
        th = threading.Thread(target=my_daemon)
        th.daemon = True
        th.start()

'''
print(sys.modules.keys())
p='neutron.plugins.ml2.plugin.Ml2Plugin'
r=lazy_load(p)
print(r)
r1=locate(p)
print(sys.modules.keys())
r=lazy_load(p)
print(r)     
'''                                       

'''
sitedir_suffix='osmonitor'
output_file='output.txt'
def getsitedir():
    dirs=site.getsitepackages()
    target_dir=''
    python_name='python{0}.{1}'.format(sys.version_info.major,sys.version_info.minor)
    
    for dir_ent in dirs:
        if python_name in dir_ent and site.PREFIXES[0] in dir_ent:
            target_dir=dir_ent
            break
    
    return target_dir
    
    sitedir=getsitedir()
    logdir=sitedir + '/'+sitedir_suffix
    log=sitedir + '/'+sitedir_suffix+'/'+output_file
'''

'''
    config = ConfigParser.SafeConfigParser()
    config.read('amm.conf')

    try:
        host_str=config.get(section, keyh)
    except ConfigParser.NoSectionError:
        host_str=''
    except ConfigParser.NoOptionError:
        host_str=''
    if len(host_str)>0:
        host=host_str

    try:
        port_str=config.get(section, keyp)
    except ConfigParser.NoSectionError:
        port_str=''
    except ConfigParser.NoOptionError:
        port_str=''
    if len(port_str)>0:
        port=int(port_str)
    '''
    
'''
def filter_modules(seq):
    keyname='neutron'
    res=filter(lambda element: keyname in element,seq)
    return res
'''

 #filtered=filter_modules(recent_imports[process]) 
