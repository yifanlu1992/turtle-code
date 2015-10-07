# -*- coding: utf-8 -*-
"""
Created on Wed Mar  4 12:46:52 2015

@author: zhaobin
"""
'find out which are downcasts and upcasts'
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
from datetime import datetime,timedelta
def find_zero(a,List):
    start=len(List)-3
    if List[a]<2:
        for i in range(a,len(List)-2):
            if List[i]<List[i+1] and List[i]<2:
                if List[i+1]<List[i+2] and List[i+1]>=2 :
                    start=i
                    break                            #find farest on surface before diving
        for i in range(start,len(List)-2):
            if List[i]>=2 and List[i]>List[i+1]:
               if List[i+1]<2 and List[i+1]>List[i+2]:
                   break                             #find nearest on surface after diving
    return [start,i+1]
#####################################
data=pd.read_csv('turtle_13137_tdr.csv')  #two option:13137,12487
depth=pd.Series(data['Depth'])
time=pd.Series(data['Date'])                         
for i in range(len(data.index)-1,0,-1):
    if depth[i]==0:
        if depth[i-1]>0:
            T=i
            break                        #depth of last loaction is not zero.
print T
indx=[]
for i in range(T):
    if 1+i<T:              #get rid of the last one
        if depth[i]<2:      # use 2 beacuse some dives don`t go to air
            I=find_zero(i,depth)
            indx.append(I)
    if i%1000==0:    
        print 'I',i 
Indx = [list(x) for x in set(tuple(x) for x in indx)]  #get rid of repeated data
Indx.sort()
INDX=[]
for i in range(len(Indx)):
    Max=max(depth[Indx[i][0]:Indx[i][1]+1])
    Max_indx=[]
    for j in range(Indx[i][0],Indx[i][1]+1):
        if int(depth[j])==int(Max):
             Max_indx.append(j)    
    INDX.append(Max_indx)
    print 'i',i

downcast,upcast=[],[]
for i in range(len(Indx)):
    downcast.append([Indx[i][0],INDX[i][0]])
    upcast.append([INDX[i][-1],Indx[i][-1]])
data=pd.DataFrame(range(len(upcast)))
data['down']=pd.Series(downcast)
data['up']=pd.Series(upcast)
data.to_csv('13137up_down.csv')
