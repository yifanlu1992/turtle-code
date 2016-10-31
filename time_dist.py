# -*- coding: utf-8 -*-
"""
Created on Thu Nov 13 12:40:52 2014

@author: zhaobin
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
from datetime import datetime, timedelta
#from turtleModule import dist
def angle_conversion(a):
    a = np.array(a)
    return a/180*np.pi
def dist(lon1, lat1, lon2, lat2):
    R = 6371.004
    lon1, lat1 = angle_conversion(lon1), angle_conversion(lat1)
    lon2, lat2 = angle_conversion(lon2), angle_conversion(lat2)
    l = R*np.arccos(np.cos(lat1)*np.cos(lat2)*np.cos(lon1-lon2)+\
                        np.sin(lat1)*np.sin(lat2))
    return l
def mon_alpha2num(m):
    '''
    Return num from name of Month
    '''
    month = ['JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC']
    if m in month:
        n = month.index(m)
    else:
        raise Exception('Wrong month abbreviation')
    return n+1
def np_datetime(m):
    '''
    return np.datettime.datetime from ctd observation 'END_DATE'
    '''
    dt = []
    for i in m:
        year = int(i[5:9])
        month = mon_alpha2num(i[2:5])
        day =  int(i[0:2])
        hour = int(i[10:12])
        minute = int(i[13:15])
        second = int(i[-2:])
        temp = datetime(year,month,day,hour=hour,minute=minute,second=second)
        dt.append(temp)
    dt = np.array(dt)
    return dt

ctdData=pd.read_csv('ctdwithoutbad.csv', index_col=0)
lons=pd.Series(ctdData['LON'],index=ctdData.index)
lats=pd.Series(ctdData['LAT'],index=ctdData.index)
ctdTime=pd.Series(np_datetime(ctdData['END_DATE'].values), index=ctdData.index)
ctdturtle_id=pd.Series(ctdData['REF'],index=ctdData.index)

turtle_id='tu80-R808-13'  #which turtle you want to plot
indx=[]
diff_dist=[]
diff_time=[]
for i in ctdData.index:
    if ctdturtle_id[i] == turtle_id:
        indx.append(i)
ctd=ctdData.ix[indx]    
goodTime=pd.Series(np_datetime(ctd['END_DATE'].values), index=indx)
goodlons=pd.Series(ctd['LON'], index=indx)
goodlats=pd.Series(ctd['LAT'], index=indx)
goodturtle_id=pd.Series(ctd['REF'],index=indx)
d=pd.DataFrame({'Time':goodTime,'lon':goodlons,'lat':goodlats,'turtle':goodturtle_id},index=indx)
d=d.sort(['Time'])
d.index=range(len(d))
for i in d.index:
    if i+1 == len(d):
        break
    dis=dist(d['lon'][i],d['lat'][i],d['lon'][i+1],d['lat'][i+1])
    diff_dist.append(dis)
    t=(d['Time'][i+1]-d['Time'][i]).total_seconds()/3600
    diff_time.append(t)
time_ave=round(np.mean(diff_time),2)
dist_ave=round(np.mean(diff_dist),2)
fig=plt.figure()
plt.bar(range(len(diff_dist)),diff_dist) 
plt.ylim([0,220])
plt.xlim([0,164])
plt.xlabel('sort by time')
plt.ylabel('distance unit:km')
plt.title('dist,average='+str(dist_ave)+'km')
plt.savefig('time_dist_1.png')
 
fig=plt.figure()
plt.bar(range(len(diff_time)),diff_time) 
plt.ylim([0,150])
plt.xlim([0,164])
plt.xlabel('sort by time')
plt.ylabel('time unit:h')
plt.title('time,average='+str(time_ave)+'h')
plt.savefig('time_dist_2.png')
       
plt.show()