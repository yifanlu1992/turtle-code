# -*- coding: utf-8 -*-
"""
Created on Thu Feb 26 09:49:21 2015

@author: jmanning
"""
import pandas as pd
import numpy as np
from datetime import datetime,timedelta
import matplotlib.pyplot as plt
from turtleModule import str2ndlist,np_datetime,str2list
###########################################################################
obsData = pd.read_csv('ctdWithModTempByDepth.csv') 
tf_index = np.where(obsData['TF'].notnull())[0]    # get the index of good data
obsturtle_id=pd.Series(obsData['PTT'][tf_index],index=tf_index)

secondData=pd.read_csv('12487_location.csv')
tf_index1 = np.where(secondData['index'].notnull())[0]
time=pd.Series(secondData['time'],index=tf_index1)
depth=pd.Series(secondData['depth'],index=tf_index1)
temp=pd.Series(secondData['temp'],index=tf_index1)
lon=pd.Series(secondData['lon'],index=tf_index1)
lat=pd.Series(secondData['lat'],index=tf_index1)
inde=pd.Series(secondData['index'],index=tf_index1)
indx=[]
for i in tf_index:
    if obsturtle_id[i]==118905:
        indx.append(i)
obsLon, obsLat = obsData['LON'][indx], obsData['LAT'][indx]
obsTime = pd.Series(np_datetime(obsData['END_DATE'][indx]), index=indx)
obsTemp = pd.Series(str2ndlist(obsData['TEMP_VALS'][indx]), index=indx)
obsDepth = pd.Series(str2ndlist(obsData['TEMP_DBAR'][indx]), index=indx)
modTemp = pd.Series(obsData['modTempByDepth'],index=indx)
for i in indx:
    modTemp[i]=str2list(modTemp[i],bracket=True)
    INDX=[]
    for j in tf_index1:
        if i==inde[j]:
            INDX.append(j)
    print i    
    fig=plt.figure()
    ax=fig.add_subplot(111)
    ax.plot(temp[INDX],depth[INDX],'ro-', label='raw',linewidth=1)
    ax.plot(modTemp[i],obsDepth[i],'go--' ,label='roms',linewidth=3)
    ax.plot(obsTemp[i],obsDepth[i],'bo--', label='telemetered',linewidth=3)
    ax.set_xlim([0, 30])
    ax.set_ylim([max(obsDepth[i])+3, -1])
    ax.set_xlabel('Temp', fontsize=10)
    ax.set_ylabel('Depth', fontsize=10)
    plt.xticks(fontsize=10)
    plt.yticks(fontsize=10)
    ax.legend(loc='lower right')
    plt.title('profile',fontsize=25)
    plt.text(1,0,'time:'+str(obsTime[i])+'')
    plt.text(1,2,'location:'+str(round(obsLon[i],2))+', '+str(round(obsLat[i],2))+'')
plt.show()