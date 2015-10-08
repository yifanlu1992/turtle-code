# -*- coding: utf-8 -*-
"""
Created on Mon Jan 26 09:06:18 2015

@author: zhaobin
"""
'make a movie about each turtle`s temperature'
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from datetime import datetime
from turtleModule import str2ndlist,np_datetime
#############################################################################
obsData=pd.read_csv('ctdwithoutbad.csv', index_col=0)
obsTime = pd.Series(np_datetime(obsData['END_DATE']), index=obsData.index)
#obsData=obsData.sort_index(by='END_DATE')
modTemp = pd.Series(str2ndlist(obsData['modTempByDepth'],bracket=True), index=obsData.index) # if str has '[' and ']', bracket should be True
obsTemp = pd.Series(str2ndlist(obsData['TEMP_VALS']), index=obsData.index)
obsDepth = pd.Series(str2ndlist(obsData['TEMP_DBAR']), index=obsData.index)
obsLon, obsLat = obsData['LON'], obsData['LAT']    
obsturtle_id = pd.Series(obsData['PTT'],index=obsData.index)
obsturtle_ids = obsturtle_id.unique()
length=len(obsturtle_ids)                #length is number of turtles 
ids=[]
for i in range(length):
    ids.append([])   
for i in range(length):
    for j in obsData.index:
        if obsturtle_id[j]==obsturtle_ids[i]:
            ids[i].append(j)   #collect index of each turtle 
for j in range(24,107):
    fig=plt.figure()
    ax=fig.add_subplot(111)
    plt.text(2,2,'id:'+str(obsturtle_id[ids[j][0]])+'')
    ax.set_xlim([0, 30])
    ax.set_ylim([70, 0])
    ax.set_xlabel('Temp', fontsize=20)
    ax.set_ylabel('Depth', fontsize=20)
    plt.xticks(fontsize=15)
    plt.yticks(fontsize=15)
    def animate(i):
        del ax.lines[:]
        ax.plot(modTemp[ids[j][i]],obsDepth[ids[j][i]],'bo--', label='model',linewidth=2)      
        ax.plot(obsTemp[ids[j][i]],obsDepth[ids[j][i]],'ro-', label='obs', linewidth=2)
        ax.set_title('Location:'+str(round(obsLon[ids[j][i]],2))+','
             +str(round(obsLat[ids[j][i]],2))+',Time:'+str(obsTime[ids[j][i]]),fontsize=25)
        ax.legend(loc='lower right')
    anim = animation.FuncAnimation(fig, animate, frames=len(ids[j]), interval=1000)
    anim.save('turtle'+str(obsturtle_id[ids[j][0]])+'.mp4', fps=2)
plt.show()
