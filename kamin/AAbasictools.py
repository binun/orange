#This file is used as tools to support the Security in Clouds
#This file is used to test Accumulating Automaton
#Especially for String Matching
#Date:2014 July 17
#Updated on 2014 July 19
#Updated on 2014 July 22. small change

#Author Ximing Li
#email: liximing.cn@gmail.com, liximing@scau.edu.cn

from random import randrange, getrandbits
from finitefield import *
from math import *
from getPrime import *

p=getPrime(50)
p=97
Zp = IntegersModP(p)
alphabetlist='^ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789 ,.+'
malphabetlist=len(alphabetlist)
nalphabetlist=malphabetlist
vectorlist=[[0 for j in range(malphabetlist)] for i in range(nalphabetlist)]
for i in range(nalphabetlist):
    vectorlist[i][i]=1

#it will be used for refreshing file in the clouds    
vectorlist[0][0]=0

#this array is used to create minus vector
Minusvectorlist=[[0 for j in range(malphabetlist)] for i in range(nalphabetlist)]
for i in range(nalphabetlist):
    Minusvectorlist[i][i]=-1

#find a number in a list
#not find, return -1
def FindinList(tem,lxs):
    lenlist=len(lxs)
    ret=-1
    for x in range(lenlist):
        if lxs[x]==tem:
           ret=x
           break
    return ret


#generate n randome numbers,
#not repeated
def GenR(n,Zp):
    l_xs=[]
    tem=Zp(getrandbits(n))
    while tem == 0:
          tem = Zp(getrandbits(n))
    l_xs.append(tem)
    while len(l_xs) < n:
        tem=Zp(getrandbits(n))
        while tem==0:
              tem=Zp(getrandbits(n))
        if FindinList(tem,l_xs)<0:
            l_xs.append(tem)
    return l_xs

#input:prime number, order
#output: a efficiency list of a polynomial
def GenPolynomial(p,n_Polynomialorder):
    Zp = IntegersModP(p)
    n_efficiency=[]
    for i in range(n_Polynomialorder+1):
        n_efficiency.append(Zp(getrandbits(p)))  
    return n_efficiency

#input: order, efficiency, xvlaues,finite filed
#output: Result
def EvalPolynomial(n_Polynomialorder,n_efficiency,n_Values,Zp):
    result=Zp(0)
    for i in range(n_Polynomialorder+1):
        result=result+n_efficiency[i]*n_Values**i
    #print 'n_values=',n_Values,'r=',result  
    return result

#input: order, efficiency, xvlaues
#output: Result
def EvalPolynomialNormal(n_Polynomialorder,n_efficiency,n_Values):
    result=0
    for i in range(n_Polynomialorder+1):
        result=result+n_efficiency[i]*n_Values**i
    #print 'n_values=',n_Values,'r=',result  
    return result

#Function Zeros list
def zerosZp(x,y,Zp):
    result=[]
    #it is diiferent from matlab,
    #the list begin from 0, not 1 ...!!
    for i in range(0,x):
        result.append([])
        for j in range(0,y):
            result[i].append(Zp(0))
    return result

#Function Zeros list
#to check whether the function in Zp is correct or not
#updated on 18 June 2014,By ximin li
def zerosZ(x,y):
    result=[]
    #it is diiferent from matlab,
    #the list begin from 0 not 1 ...!!
    for i in range(0,x):
        result.append([])
        for j in range(0,y):
            result[i].append(0)
    return result

#Function  Conv function. this my conv function
#input: two vectors
#output: the conv of the two vectors
#you can see this function in MATLAB
#it is for not Zp.
#updated on 18 June 2014,By ximin li
def convmy(V,polyva1):
        #c=conv(V,polyva1);
        #c=[polyva1[1]*V,polyva1[2]*V];
    len1=len(V)
    len2=len(polyva1)
    result=zerosZ(len1+1,len2)
    result2=zerosZ(1,len1+1)
    for i in range(0,len1): 
        for j in range(0,len2): 
            result[i][j]=V[i]*polyva1[j]

    for i in range(1,len1+1): 
        result[i][0]=result[i][0]+result[i-1][1]
        

    for i in range(0,len1+1):
        result2[0][i]=result[i][0]  

    c=result2
    return c 


#Function  Conv function. this my conv function
#input: two vectors
#output: the conv of the two vectors
#you can see this function in MATLAB
#updated on 18 June 2014, By ximin li
def convmyZp(V,polyva1,Zp):
    #c=conv(V,polyva1);
    #c=[polyva1[1]*V,polyva1[2]*V];
    len1=len(V)
    len2=len(polyva1)
    result=zerosZp(len1+1,len2,Zp)
    result2=zerosZp(1,len1+1,Zp)
    for i in range(0,len1): 
        for j in range(0,len2): 
            result[i][j]=V[i]*polyva1[j]

    for i in range(1,len1+1): 
        result[i][0]=result[i][0]+result[i-1][1]
        

    for i in range(0,len1+1):
        result2[0][i]=result[i][0]  

    c=result2
    return c 



#input: xlabel, ylabel, order of the polynomial
#output a polynomial with n_Polynomialorder degree.     
def  interpolation(xs,ys,n_order):
     #pi(x) = prod(x-i for i in xs) 
     #print pi(x)
     #pid(x) = diff(pi(x),x)
     #print pid(x)
     #P(x) = sum(pi(x)/(x-i)/pid(i)*j for (i,j) in zip(xs,ys))
     #f=P(x).collect(x)
     return f


#LAGRANGE   approx a point-defined function using the Lagrange polynomial interpolation
#Input  - X is a vector that contains a list of abscissas
#      - Y is a vector that contains a list of ordinates
#Output - C is a matrix that contains the coefficents of 
#         the Lagrange interpolatory polynomial
#       x^2+2x+3 will be the list [0,3,2,1]
#It is amazing. It works well on Z and Zp!
#updated on 18 June 2014, By ximin li
def lagran(X,Y):
    w=len(X);
    n=w-1;
    L=zerosZ(w+1,w+1);
    #print 'X=',X
    #print 'Y=',Y
    #Form the Lagrange coefficient polynomials
    for k in range(0,n):
       #V=1
       V=[]
       V.append(1)
       for j in range(n):
          if k != j:
             #V=conv(V,poly(X(j)))/(X(k)-X(j));
             polyva1=[1,-1*X[j]]
             #print 'polyva1=',polyva1,'V=',V
             polyva2=convmy(V,polyva1)
             #print 'polyva2=',polyva2
             
             #polyva2=[polyva1(1)*V,polyva1(2)*V];
             #V=polyva2/(X[k]-X[j])
             #substituted by code below
             lenpolyva2=len(polyva2[0])
             V=[]
             for  jj in range(lenpolyva2):
                 V.append(polyva2[0][jj]/(X[k]-X[j]))
             #print 'j=',j,'lenpolyva2=',lenpolyva2,'V===for j end===\n',V        
       #here is to give V to be one row of the matrix.
       #  L[k,:]=V it is substitutied by the code below
       lenv=len(V)
       for  jx in range(lenv):
           #print 'L[k]=',L[k]
           L[k][jx]=V[jx]
       #print 'k=',k,'V----for k end ----',V
       #print 'L[k]=',L[k]
       
    #To subsitibute the code below..
    #It is From matlab.
    #C=Y*L
    C=[]
    lenY=len(Y)
    ColOfL=len(X)
    temp=0
    for j in range(ColOfL):
        #print L[j]
        temp=0
        for i in range(lenY):
            temp=temp+Y[i]*L[i][j]
        #record it in C
        C.append(temp)    
    #print Y
    return C

#input: alphabet
#ouput: vector
#53 symbols to vectors. a-z,A-Z,and blank.
#updated on 18 June 2014, By ximin li
#update on 2 July 2014
def MapAlphabetToVector(x):
    i=alphabetlist.find(x)
    ret=[]
    for x in alphabetlist:
        ret.append([])
    if i != -1:
        for x in range(len(alphabetlist)):
          ret[x]=vectorlist[i][x]
    else:
        for x in range(len(alphabetlist)):
          ret[x]=vectorlist[0][x]
    return ret

#input: alphabet
#ouput: vector
#used for delting keys
#53 or 63 or other symbols to vectors. a-z,A-Z,and blank.
#updated on 1 July 2014, By ximin li
def minusMapAlphabetToVector(beta):
    i=alphabetlist.find(beta)
    ret=[]
    for x in alphabetlist:
        ret.append([])
        
    if i != -1:
       for x in range(len(alphabetlist)):
          ret[x]=Minusvectorlist[i][x]
    else:
       for x in range(len(alphabetlist)):
          ret[x]=Minusvectorlist[0][x]
    return ret



#input: letter
#ouput: Reutn the index of the letter in the alphabetlist

def MapAlphabetToInt(x):
    i=alphabetlist.find(x)
    if i != -1:
        return i
    else:
        return 0

#input: number
#ouput: Reutn the index of the letter in the alphabetlist

def MapIntToAlphabet(i):
   num=Zp(i).n
   if num >=len(alphabetlist):
      return '@'  
   else:
      return alphabetlist[num]

    
#input: number in Zp,
#    number of clouds,
#    order of the polynomial
#    the prime number
#    list of each random x for each cloud
#ouput: vector
#function 
def secretshare(y,n_clouds,n_order,p,l_xs,Zp):
    shares=[]
    f_poly=GenPolynomial(p,n_order)
    f_poly[0]=y  
    #print f_poly 
    for x in range(n_clouds):
        resultValue=EvalPolynomial(n_order,f_poly,l_xs[x],Zp)
        shares.append(resultValue)
    #print "def secretshare(y,n_clouds,n_order):",shares
    return shares

#input: number in Zp,
#    number of clouds,
#    order of the polynomial
#    the prime number
#    list of each random x for each cloud
#ouput: vector,poly
#function 
def secretshareRetPoly(y,n_clouds,n_order,p,l_xs,Zp):
    shares=[]
    f_poly=GenPolynomial(p,n_order)
    f_poly[0]=y  
    #print f_poly 
    for x in range(n_clouds):
        resultValue=EvalPolynomial(n_order,f_poly,l_xs[x],Zp)
        shares.append(resultValue)
    #print "def secretshare(y,n_clouds,n_order):",shares
    return (shares,f_poly)
