import ConfigParser
import StringIO
import os

def read_prop_file(filename,keyname):   
    f=open(filename,'r')       
    config = StringIO.StringIO()   
    config.write('[{0}]\n'.format('dummy'))
    config.write(f.read())
    config.seek(0, os.SEEK_SET)

    cp = ConfigParser.SafeConfigParser()
    cp.readfp(config)
    d=dict(cp.items('dummy'))
    keywords=d.keys()
    target=''
    
    for keyword in keywords:
        if keyword.find(keyname)>0:
            target=keyword
    if len(target)>1:
        return d.get(target)
    else:
        return 'No-value'
    
def read_conf_file(filename,section,keyname,defvalue=''):
    result=''
    config = ConfigParser.SafeConfigParser()
    config.read(filename)
    try:
        result=config.get(section, keyname)
    except ConfigParser.NoSectionError:
        result=defvalue
    except ConfigParser.NoOptionError:
        result=defvalue
        
    return result
    
    
    
