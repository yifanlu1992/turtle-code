# -*- coding: utf-8 -*-
"""
Created on Mon Feb 23 11:49:45 2015

@author: zhaobin
"""
'compare 6 conditions upcasts and downcasts'
import pandas as pd
import numpy as np
from datetime import datetime,timedelta
import matplotlib.pyplot as plt
#######################################################################
'''
example_down=[[0,50],[136691,136712],[360552,360574],[586444,586469],[694150,694179],[695537,695568]]
example_up=[[382,438],[137136,137184],[360849,360883],[586742,586788],[694421,694495],[695712,695775]]   #13137
'''
example_down=[[191,212],[7800,7847],[34293,34334],[582550,582583],[987586,987648],[1032448,1032951]]
example_up=[[216,267],[8061,9800],[35674,35731],[583380,583420],[987858,988141],[1032950,1033003]]      #12487

data=pd.read_csv('turtle_12487_tdr.csv')
temp=pd.Series(data['temp'])
time=pd.Series(data['Date'])
depth=pd.Series(data['Depth'])
fig=plt.figure()
for i in range(len(example_down)):
    ax1=fig.add_subplot(2,3,i+1)
    ax1.plot(temp[example_down[i][0]:example_down[i][1]],depth[example_down[i][0]:example_down[i][1]],color='r',label=str(time[example_down[i][0]]))
    ax1.plot(temp[example_up[i][0]:example_up[i][1]],depth[example_up[i][0]:example_up[i][1]],color='b',label=str(time[example_up[i][1]]))
    ax1.set_ylim([50, 0])
    T=0
    if i==1 :
        for j in depth[example_up[i][0]:example_up[i][1]]:
            if 10<j<15:
                T=T+1
        ax1.annotate('stay '+str(int(T*4.0/60))+' minutes',xy=(12,15),xytext=(12,21),arrowprops=dict(facecolor='red',shrink=0.05),fontsize=16)
    if i==4 :
        for j in depth[example_up[i][0]:example_up[i][1]]:
            if 10<j<15:
                T=T+1   
        ax1.annotate('stay '+str(int(T*4.0/60))+' minutes',xy=(20,14),xytext=(16,19),arrowprops=dict(facecolor='red'),fontsize=16)
        plt.xlabel('Temperature(degC)', fontsize=20)
    ax1.set_ylabel('Depth(m)', fontsize=20) 
    ax1.set_xlim(int(np.amin(temp[example_down[i]]))-1,int(np.amax(temp[example_down[i]])+1))
    ax1.legend(loc='lower right')
    ax1.set_title(str(i))
    plt.xticks(fontsize=15)
    plt.yticks(fontsize=15)
plt.show()  
    