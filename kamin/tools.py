#This file is used as tools to support the Security in Clouds
#This file is used to test Accumulating Automaton
#Especially for String Matching
#Date:2014 July 21
#update on 2014.06.26. to add class for database
#Author Ximing Li
#email: liximing.cn@gmail.com, liximing@scau.edu.cn

from random import randrange, getrandbits
from math import *
import os
from AAbasictools import *

#list all the files names in the diretory
#such as d=ListFiles(".\data")
def ListFiles(sPath):
    # returns a list of names (with extension, without full path) of all files 
    # in folder sPath
    lsFiles = []
    for sName in os.listdir(sPath):
        if os.path.isfile(os.path.join(sPath, sName)):
            lsFiles.append(sName)
    return lsFiles


#Function Zeros list
def GetFilenamefromPath(path):
    str=path
    f_list=str.rsplit('/')
    str1=f_list[len(f_list)-1]
    str2=str1.split('.')
    return str2[0]

#used to store fileshares in one file for (one cloud)
class DatabaseShares:
    n_xs=0 #for the number or each cloud
    n_filelen=0 #database length.how many record rows
    n_LastEmptyKeyNumber=0
    #to give the last empty record key, with numbers
    #such as $05 means their is five empty place.
    #so search $05 can find the last empty place
    n_alphabetlistlen=len(alphabetlist)
    n_Keylen=5
    n_Indexlen=2
    n_Recordlen=12
    l_Keyshares=[]
    l_Indexshares=[]
    l_Recordshares=[]
    def __init__(self):
        self.n_xs=0 #for the number or each cloud
        self.n_filelen=0 #database length
        self.n_alphabetlistlen=len(alphabetlist)
        self.n_Keylen=5
        self.n_Indexlen=2
        self.n_Recordlen=12
        self.l_Keyshares=[]
        self.l_Indexshares=[] # it is numbers. secret shared with degeree 1
        self.l_Recordshares=[]            
    def __str__(self):
        return 'Class:DatabaseShares [] length= %d' % self.n_filelen

class FileShares:
    n_xs=0
    n_filelen=0
    l_Filshares=[]
    def __str__(self):
        return 'Class: Filshares [] length= %d' % self.n_filelen
   
  

#used to store fileshares
class AAShares:
    n_node=0
    l_NodesharesforC=[]
    l_transion=[]
    def __str__(self):
        return 'Class: AAShares length= %d' % self.n_node


#used to store database shares
class AAdatabaseShares:
    n_node=0
    l_DNodesharesforC=[]
    l_iDNodesharesforC=[] #this is for index Node shares
    l_rDNodesharesforC=[] #this is for record Node shares
    
    l_Dtransion=[]
    l_DindexTransition=[] #Transition for the extra index nodes.
    l_DrecordTransition=[] #Transition for the extra record nodes.


    def __str__(self):
        return 'Class: AAShares length= %d' % self.n_node


#input alpha,n_clouds,1,p,l_xs,Zp
#output list of the secretshared alpha in n_clouds
def secretshareAlpha(alpha,n_clouds,n_order,p,l_xs,Zp):
    vector=MapAlphabetToVector(alpha)
    #print vector
    #secret share each vector
    l_y_vectorshares=[]
    #this list should be
    #for one vector,or for one symbol
    for i_xxx in range(n_clouds):
        l_y_vectorshares.append([])
    #now it is [10]list
    #if IFtest: print 'for one symbol'; print l_y_vectorshares
    shares=[]  #for one element (0 or 1)
    for y in vector:
        #len(vector) will be 53
        #print 'y=',y
        l_shares=[] 
        l_shares=secretshare(y,n_clouds,n_order,p,l_xs,Zp);
        #it is [10]. ten element in one row
        #one degree sharing, so we need 1 here.
        #the return value is a list, which is shares for each cloud
        #of one bit (0 or 1)
        n_shares=[]
        for i_x in range(n_clouds):
            n_shares.append(l_shares[i_x].n)
        #print n_shares
        #print len(n_shares)
        for xx in range(n_clouds):
            l_y_vectorshares[xx].append(n_shares[xx])        
    return l_y_vectorshares #it is a [10][63]list

'''
#update cloud shares
#input: node shares, it is a pointer,
        file shares,
        transion
#output: nothing. actually, the data is manipulated in lists.
'''
def updateCloudshares(NodesharesforC,\
                                    Filshares,\
                                    transion):
    FileLen=len(Filshares)#
    KeyLen=len(transion)#4 =len('LOVE')
    # it is 14 for 'Alice Love Bob'
    ret=1         
    for i in range(FileLen):
    #for each symbol in file stream
        #the accumulating node is different
        #it is the last node.
        a=NodesharesforC[KeyLen]
        b=NodesharesforC[KeyLen-1]
        c=Filshares[i][transion[KeyLen-1]]
        #print c
        NodesharesforC[KeyLen]=a+ b*c
        
        for c_count in range(KeyLen-1,0,-1):
            NodesharesforC[c_count]=NodesharesforC[c_count-1]* \
                           Filshares[i][transion[c_count-1]]
            
    #return NodesharesforC
    return ret

'''
#update cloud shares
#input: l_Datashares=self.l_Datashares         
        l_Dtransion= self.l_Dtransion
        l_DindexTransition=self.l_DindexTransition
        l_DNodesharesforC=self.l_DNodesharesforC
        l_iDNodesharesforC=self.l_iDNodesharesforC
#output: nothing
#metion:
        self.l_Keyshares=[]
        self.l_Indexshares=[]
        self.l_Recordshares=[] 
            n_ret=updateDataCloudshares(l_Datashares[xx],\
                          l_DNodesharesforC[xx],l_iDNodesharesforC[xx],l_rDNodesharesforC[xx],\
                          l_Dtransion,l_DindexTransition,l_DrecordTransition)  
'''
#this function update the dataseshres when searching key
#it return nothing.
#the parameters in the input para will take tha result back
def updateDataCloudshares(DatabaseShares,\
                          l_DNodesharesforC,l_iDNodesharesforC,l_rDNodesharesforC,\
                          l_Dtransion,l_DindexTransition,l_DrecordTransition):  
    # how many records are in the shares
    n_fl=DatabaseShares.n_filelen
    n_kl=DatabaseShares.n_Keylen
    n_Il=DatabaseShares.n_Indexlen
    n_Rl=DatabaseShares.n_Recordlen
    SearchKeyLen=len(l_Dtransion)#4 =len('LOVE')
    # it is 14 for 'Alice Love Bob'
    #print 'in function: updateDataCloudshares'
    #print 'n_fl,n_kl,n_Il,n_Rl,SearchKeyLen=',\
      #n_fl,n_kl,n_Il,n_Rl,SearchKeyLen
    #print 'l_DrecordTransition=',l_DrecordTransition
    ret=1
    n_indextransition=len(l_DindexTransition)
    n_recordtransition=len(l_DrecordTransition)
    
    n_ID=[]
    n_rID=[]
    for n_index in range(n_indextransition):
        n_ID.append([])
    for n_index in range(n_Rl):
        n_rID.append([])
    
    l_temp_DNodesharesforC=l_DNodesharesforC
    for i in range(n_fl*n_kl):
        #this is used to clear node values
        if i % n_kl==0:
            l_DNodesharesforC=l_temp_DNodesharesforC
        #This is used to select different Index 
        for n_index in range(n_indextransition):
            n_ID[n_index]=(i / n_kl)*n_Il+ n_index                 
        for n_index in range(n_recordtransition):
            n_rID[n_index]=(i / n_kl)*n_Rl+ n_index                 
        

        #for each symbol in key
        a=l_DNodesharesforC[SearchKeyLen]
        b=l_DNodesharesforC[SearchKeyLen-1]
        c=DatabaseShares.l_Keyshares[i][l_Dtransion[SearchKeyLen-1]]
        l_DNodesharesforC[SearchKeyLen]=a+ b*c
        #it is for record
        for n_record in range(n_recordtransition): #normally 12. for record
            #print n_record,l_rDNodesharesforC[n_record]
            temp=l_rDNodesharesforC[n_record]
            l_rDNodesharesforC[n_record]=temp+\
                    b*c*DatabaseShares.l_Recordshares[n_rID[n_record]]
        
        
        #it is for Index
        for n_index in range(n_indextransition): #normally 2. for index
            l_iDNodesharesforC[n_index]=l_iDNodesharesforC[n_index]+\
                                        b*c*DatabaseShares.l_Indexshares[n_ID[n_index]]
                                      
        #for the main search
        for c_count in range(SearchKeyLen-1,0,-1):
            l_DNodesharesforC[c_count]=l_DNodesharesforC[c_count-1]* \
                           DatabaseShares.l_Keyshares[i][l_Dtransion[c_count-1]]
            
    #return NodesharesforC
    return ret


''' This function is used to create an empty file
which will be secret shared to clouds and used to refresh the database
Add this file the objected file will not change its content'''
def createallzerodatabase(n_filelen,n_Keylen,n_Indexlen,n_Recordlen):
    l_data=[]
    for i in range(n_filelen):
        l_data.append([])
        l_data[i].append('')
        l_data[i].append('')
        l_data[i].append('')        
        for i_x in range(n_Keylen):
            l_data[i][0]=l_data[i][0]+MapIntToAlphabet(0)
        for i_y in range(n_Indexlen):
            l_data[i][1]=l_data[i][1]+MapIntToAlphabet(0)
        for i_z in range(n_Recordlen):
            l_data[i][2]=l_data[i][2]+MapIntToAlphabet(0)

    return l_data


'''this function will be used to delte key
it will generate the vector shares from lpha to beta '''
#input alpha,beta,n_clouds,1,p,l_xs,Zp
#output list of the secretshared (-alpha+beta) in n_clouds
def secretshareAlphaToBeta(letterDe,letterNk,n_clouds,n_order,p,l_xs,Zp):
    vectorA=[0 for j in range(malphabetlist)]
    vectorB=[0 for j in range(malphabetlist)]
    vectorA=MapAlphabetToVector(letterNk)
    #print vectorA
    vectorB=minusMapAlphabetToVector(letterDe)
    #print vectorB
    for n_x in range(len(vectorA)):
        vectorA[n_x]=vectorA[n_x]+vectorB[n_x]
    #print vectorA
    #secret share each vector
    l_y_vectorshares=[]
    #this list should be
    #for one vector,or for one symbol
    for i_xxx in range(n_clouds):
        l_y_vectorshares.append([])
    #now it is [10]list
    #if IFtest: print 'for one symbol'; print l_y_vectorshares
    shares=[]  #for one element (0 or 1)
    for y in vectorA:
        #len(vector) will be 53
        #print 'y=',y
        l_shares=[] 
        l_shares=secretshare(y,n_clouds,n_order,p,l_xs,Zp);
        #it is [10]. ten element in one row
        #one degree sharing, so we need 1 here.
        #the return value is a list, which is shares for each cloud
        #of one bit (0 or 1)
        n_shares=[]
        for i_x in range(n_clouds):
            n_shares.append(l_shares[i_x].n)
        #print n_shares
        #print len(n_shares)
        for xx in range(n_clouds):
            l_y_vectorshares[xx].append(n_shares[xx])        
    return l_y_vectorshares #it is a [10][63]list


#refresh database shares in each cloud
#input: datbase shares, refresh database shares
#the parameter are objects
#output nothing
#add on 2 July 2014
def  refreshDataCloudshares(o_DataShares,o_reDataShares):
    n_fl=o_DataShares.n_filelen
    n_kl=o_DataShares.n_Keylen
    n_Il=o_DataShares.n_Indexlen
    n_Rl=o_DataShares.n_Recordlen
    #define the datashares need to return
    retDataShares=DatabaseShares()
    retDataShares.n_LastEmptyKeyNumber=o_DataShares.n_LastEmptyKeyNumber 
    retDataShares.n_xs=o_DataShares.n_xs 
    retDataShares.n_alphabetlistlen=o_DataShares.n_alphabetlistlen
    retDataShares.n_filelen=o_DataShares.n_filelen
    retDataShares.n_Keylen=n_kl
    retDataShares.n_Indexlen=n_Il
    retDataShares.n_Recordlen=n_Rl
    retDataShares.l_Keyshares=o_DataShares.l_Keyshares
    retDataShares.l_Indexshares=o_DataShares.l_Indexshares
    retDataShares.l_Recordshares=o_DataShares.l_Recordshares
    n_alphabetlistlen=o_DataShares.n_alphabetlistlen
    ret=1
    for i in range(n_fl):
        for i_x in range(n_kl): #it is also a list
            for i_kx in range(n_alphabetlistlen):
            #to add number by number
                n_num=i*n_kl+i_x
                retDataShares.l_Keyshares[n_num][i_kx]=\
                            o_DataShares.l_Keyshares[n_num][i_kx]+\
                          o_reDataShares.l_Keyshares[n_num][i_kx]
        for i_y in range(n_Rl): #it is also a list
            #to add number by number
            n_num=i*n_Rl+i_y
            retDataShares.l_Recordshares[n_num]=o_DataShares.l_Recordshares[n_num]+\
                                             o_reDataShares.l_Recordshares[n_num]

    return retDataShares


#used to convert vetctor to alphabet
def mapvectorToAlphabet(Vector):
    ret='a'
    return ret


'''
2014.7.10
#update cloud shares.
the pattern is hiden by secret sharing
#input: node shares, it is a pointer,
        file shares,
        transion shares.
#output: nothing. actually, the data is manipulated in lists.

'''
def updateCloudsharesHPWE(NodesharesforC,\
                                    Filshares,\
                                    transionforC):
    FileLen=len(Filshares)#
    KeyLen=len(transionforC)#4 =len('LOVE')
    n_alphabetlistlen=len(alphabetlist)
    # it is 14 for 'Alice Love Bob'
    ret=1         
    for i in range(FileLen):
    #for each symbol in file stream
        #the accumulating node is different
        #it is the last node.
        a=NodesharesforC[KeyLen]
        b=NodesharesforC[KeyLen-1]
        c=0
        for i_x in range(n_alphabetlistlen):
            c=c+Filshares[i][i_x]*transionforC[KeyLen-1][i_x]
            
            #c=c+Filshares[i][transion[KeyLen-1]]
        #print c
        NodesharesforC[KeyLen]=a+ b*c
        
        for c_count in range(KeyLen-1,0,-1):
            c=0
            for i_x in range(n_alphabetlistlen):
                c=c+Filshares[i][i_x]*transionforC[c_count-1][i_x]
            NodesharesforC[c_count]=NodesharesforC[c_count-1]*c
            
            #NodesharesforC[c_count]=NodesharesforC[c_count-1]* \
                           #Filshares[i][transion[c_count-1]]
            
    #return NodesharesforC
    return ret
    
