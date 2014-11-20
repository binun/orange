import os

def ListFiles(sPath):
    # returns a list of names (with extension, without full path) of all files 
    # in folder sPath
    lsFiles = []
    for sName in os.listdir(sPath):
        if os.path.isfile(os.path.join(sPath, sName)):
            lsFiles.append(sName)
    return lsFiles

d=ListFiles(".\data")
print d 
