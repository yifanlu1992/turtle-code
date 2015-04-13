# -*- coding: utf-8 -*-
"""
Created on Tue Feb  3 09:07:00 2015

@author: zhaobin
"""
'plot number of dive and turtle in each month'
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from turtleModule import str2ndlist,np_datetime
####################################################
obsData=pd.read_csv('ctdWithModTempByDepth.csv')
tf_index=np.where(obsData['TF'].notnull())[0]
obsTime = pd.Series(np_datetime(obsData['END_DATE'][tf_index]), index=tf_index)
turtle_ids = pd.Series(obsData['PTT'])
Num=[]
num=[[[],[],[],[],[],[],[],[],[],[],[],[]],[[],[],[],[],[],[],[],[],[],[],[],[]],[[],[],[],[],[],[],[],[],[],[],[],[]],[[],[],[],[],[],[],[],[],[],[],[],[]],[[],[],[],[],[],[],[],[],[],[],[],[]]]
for i in range(5):    # 2009~2013,5 years
    Num.append([0]*12)    #12 months
for i in tf_index:
    for j in range(5):
        if obsTime[i].year==2009+j:
            for q in range(12):
                if obsTime[i].month==q+1:
                    Num[j][q]+=1
                    num[j][q].append(i)
for i in range(len(num)):
    for j in range(len(num[i])):
        num[i][j]=len(turtle_ids[num[i][j]].unique())

width=0.15
color=['blue','black','red','green','yellow']
fig=plt.figure()
for i in range(5):
    plt.bar(np.arange(1,13)+width*(i-2),Num[i],align="center",width=width,color=color[i] ,label=str(i+2009))
plt.legend(loc='best')
plt.xlim([0,13]) 
plt.xticks(range(13),fontsize=18)
plt.yticks(fontsize=18)
plt.xlabel('Month',fontsize=20)
plt.ylabel('Quantity',fontsize=20)
plt.title('Dives per month',fontsize=20)

fig = plt.figure()
for i in range(5):
    plt.bar(np.arange(1,13)+width*(i-2),num[i],align="center",width=width,color=color[i] ,label=str(i+2009))
plt.legend(loc='best')
plt.xlim([0,13]) 
plt.xticks(range(13),fontsize=18)
plt.yticks(fontsize=18)
plt.xlabel('month',fontsize=20)
plt.ylabel('quantity',fontsize=20)
plt.title('number of turtle',fontsize=20)
plt.show()
