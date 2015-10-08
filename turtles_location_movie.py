# -*- coding: utf-8 -*-
"""
Created on Wed Jan 21 09:06:05 2015

@author: zhaobin
"""
'a movie about turtle points in each month'
import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
from turtleModule import str2ndlist,np_datetime,draw_basemap
from matplotlib import animation
#################################################################
obsData = pd.read_csv('ctdWithdepthofbottom_roms.csv')
obsTime = pd.Series(np_datetime(obsData['END_DATE']),index=obsData.index)
obsLon, obsLat = obsData['LON'], obsData['LAT']  
shipData = pd.read_csv('06-08-Depth_ch.csv')
shipLat=pd.Series(shipData['LAT'],index=shipData.index)
shipLon=pd.Series(shipData['LON'],index=shipData.index)
shipTime=pd.Series(shipData['time'],index=shipData.index)
for i in range(len(shipTime)):
    shipTime[i]=datetime.strptime(shipTime[i], "%Y-%m-%d %H:%M:%S")  # change str to datatime
lonsize = [-78, -71.5]
latsize = [33.5, 41.5]                # range of basemap
obsyears=[[[],[],[],[],[],[],[],[],[],[],[],[]],[[],[],[],[],[],[],[],[],[],[],[],[]],[[],[],[],[],[],[],[],[],[],[],[],[]],[[],[],[],[],[],[],[],[],[],[],[],[]],[[],[],[],[],[],[],[],[],[],[],[],[]]]
for i in range(len(obsyears)):
    for j in obsData.index:
        if obsTime[j].year==2009+i:
            for q in range(12):
                if obsTime[j].month==q:
                    obsyears[i][q].append(j)
shipyears=[[[],[],[],[],[],[],[],[],[],[],[],[]],[[],[],[],[],[],[],[],[],[],[],[],[]],[[],[],[],[],[],[],[],[],[],[],[],[]],[[],[],[],[],[],[],[],[],[],[],[],[]],[[],[],[],[],[],[],[],[],[],[],[],[]]]
for i in range(len(shipyears)):
    for j in shipData.index:
        if shipTime[j].year==2009+i:
            for q in range(12):
                if shipTime[j].month==q+1:
                    shipyears[i][q].append(j)
obsYear=[]
for i in range(5):                     #5 is the number of obsYear
    for j in range(12):                #12 is number of month
        obsYear.append(obsyears[i][j])
shipYear=[]
for i in range(5):                     #5 is the number of obsYear
    for j in range(12):                #12 is number of month
        shipYear.append(shipyears[i][j])
k=[0]*12+[1]*12+[2]*12+[3]*12+[4]*12           #use for year
K=[1,2,3,4,5,6,7,8,9,10,11,12]*5               #use for month

fig=plt.figure()
ax=fig.add_subplot(111)
draw_basemap(fig, ax, lonsize, latsize)

def animate(i):
    del ax.collections[:] 
    plt.scatter(np.array(obsLon[obsYear[i]]),np.array(obsLat[obsYear[i]]), marker='o',edgecolors='none',c='r', s=10, zorder=15,label='turtle')
    plt.scatter(np.array(shipLon[shipYear[i]]),np.array(shipLat[shipYear[i]]), marker='>',edgecolors='none',c='green', s=10, zorder=15,label='ship')
    plt.title('year='+str(2009+k[i])+',month='+str(K[i])+'') 
    plt.legend(loc='upper left')
anim = animation.FuncAnimation(fig, animate, frames=60, interval=1000)    
anim.save('turtle.mp4', fps=2)
plt.show()
