# -*- coding: utf-8 -*-
"""
Created on Fri Dec 12 09:21:16 2014

@author: zhaobin
"""
'draw temp change of all turtle data and model data and calculate ‘bad’ turtles.'
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
from math import sqrt
from datetime import datetime, timedelta
from turtleModule import str2ndlist, np_datetime
###################################main code###################################
criteria=3                   # criteria for rms
obsData=pd.read_csv('ctdWithdepthofbottom_roms.csv')
obsDepth=pd.Series(str2ndlist(obsData['TEMP_DBAR']),index=obsData.index)
modDepth=pd.Series(obsData['depth_bottom'],index=obsData.index)
indx=[]
for i in obsData.index:
    if abs(obsDepth[i][-1]-modDepth[i])<10:     #diff<10m,we can use the data
        indx.append(i)                                
obsturtle_id=pd.Series(obsData['PTT'][indx],index=indx)        
obsTemp=pd.Series(str2ndlist(obsData['TEMP_VALS'][indx]),index=indx)
modTemp=pd.Series(str2ndlist(obsData['modTempByDepth'][indx],bracket=True),index=indx)
obsTime=pd.Series(np_datetime(obsData['END_DATE'][indx]),index=indx)
obsturtle_ids=obsturtle_id.unique()
ids=[]
for i in range(len(obsturtle_ids)):
    ids.append([])   
for i in range(len(obsturtle_ids)):
    for j in indx:
       if obsturtle_id[j]==obsturtle_ids[i]:
            ids[i].append(j)   #collect index of each turtle 
bad_ids=[]
for j in range(len(ids)):
    obsMaxTemp=[]
    obsMinTemp=[]
    modMaxTemp=[]
    modMinTemp=[]
    time=[]
    for k in ids[j]:
        obsMaxTemp.append(max(obsTemp[k]))
        obsMinTemp.append(min(obsTemp[k]))
        modMaxTemp.append(max(modTemp[k]))
        modMinTemp.append(min(modTemp[k]))
        time.append(obsTime[k])
    data=pd.DataFrame({'time':time,'obsMaxTemp':obsMaxTemp,'obsMinTemp':obsMinTemp,
                       'modMaxTemp':modMaxTemp,'modMinTemp':modMinTemp},index=range(len(time)))
    data = data.sort_index(by='time')                       #calculate each turtle`s min,max temperature of observe and modle. 
    time.sort()    
    fig = plt.figure(figsize=(12,12))
    ax = fig.add_subplot(111)
    ax.plot(time, data['obsMaxTemp'], color='b', linewidth=2)
    ax.plot(time, data['obsMinTemp'], color='b', linewidth=2, label='obs')
    ax.plot(time, data['modMaxTemp'], color='r', linewidth=2)
    ax.plot(time, data['modMinTemp'], color='r', linewidth=2, label='mod')
    plt.legend()
    ax.set_xlabel('time', fontsize=20)
    ax.set_ylabel('temperature', fontsize=20)
    dates = mpl.dates.drange(np.amin(time), np.max(time), timedelta(days=30))
    dateFmt = mpl.dates.DateFormatter('%b,%Y')
    ax.set_xticks(dates)
    ax.xaxis.set_major_formatter(dateFmt)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    plt.title('time series of temp for turtle:{0}'.format(obsturtle_ids[j]), fontsize=25)
    plt.savefig('timeSeries_'+str(obsturtle_ids[j])+'.png')
    dif=np.array((data['obsMinTemp'])-np.array(data['modMinTemp']))
    rms=sqrt(np.sum(dif*dif)/len(data))
    if abs(rms)>criteria:
        bad_ids.append(obsturtle_ids[j])            #calculate 'bad' ids
print('"bad" ids are:',bad_ids)
plt.show()
