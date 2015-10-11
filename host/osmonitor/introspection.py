import sys
from string import join

def lazy_load(path):
    parts = [part for part in path.split('.') if part]
    n = 0
    last_module=None
    last_module_path=''
    is_loaded=True
    obj=None
    path=parts[0]
    while n < len(parts)-1: #iterate until the object name is reached
        
        if not path in sys.modules:
            is_loaded=False
            #print('Module '+path+' is NOT loaded')
        else:
            #print('Module '+path+' is loaded')
            last_module_path=path
        path=join([path,parts[n+1]], '.')
        n=n+1
        
    #print('Last module  ' + last_module_path)
    #print('Object name ' + parts[n])    
    
    if last_module_path in sys.modules:
        last_module=sys.modules[last_module_path]
        #print(last_module)
    
    if not is_loaded or last_module==None:
        #print('Invalid context')
        return None
    
    try:
        obj=getattr(last_module, parts[n])
    except AttributeError:
        #print('Object is not retrieved')
        return None
    
    #print('Success')
    return obj
