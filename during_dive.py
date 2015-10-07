# -*- coding: utf-8 -*-
"""
Created on Fri Dec  5 10:32:22 2014

@author: zhaobin
"""
'plot total time and distance of turtles during in the ocean'
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from turtleModule import dist,np_datetime
###################################main code###################################
'''
obsData=pd.read_csv('ctdwithoutbad_roms.csv', index_col=0)
obsturtle_id=pd.Series(obsData['PTT'],index=obsData.index)
obsturtle_ids=obsturtle_id.unique()
length=len(obsturtle_ids)                #length is number of turtles 
'''
obsData = pd.read_csv('ctdWithModTempByDepth.csv')
tf_index = np.where(obsData['TF'].notnull())[0]
obsturtle_id=pd.Series(obsData['REF'][tf_index],index=tf_index)
obsturtle_ids=obsturtle_id.unique()
length=len(obsturtle_ids)                #length is number of turtles 
ids=[]
for i in range(length):
    ids.append([])   
for i in range(length):
    for j in tf_index:
        if obsturtle_id[j]==obsturtle_ids[i]:
            ids[i].append(j)             #collect each turtle`s index
time_aves=[]                             
dist_aves=[]                             
for i in range(len(ids)):
    obs=obsData.ix[ids[i]]    
    goodTime=pd.Series(np_datetime(obs['END_DATE']), index=ids[i])
    goodlons=pd.Series(obs['LON'], index=ids[i])
    goodlats=pd.Series(obs['LAT'], index=ids[i])
    d=pd.DataFrame({'Time':goodTime,'lon':goodlons,'lat':goodlats},index=ids[i])
    d=d.sort(['Time'])
    d.index=range(len(d))
    diff_dist=[]
    diff_time=[]
    for j in d.index:
        if j+1 == len(d):
            diff_dist.append(0)
            diff_time.append(0)
            break
        if j>0:
            dis=dist(d['lon'][0],d['lat'][0],d['lon'][j],d['lat'][j])
            diff_dist.append(dis)
            t=(d['Time'][j]-d['Time'][0]).total_seconds()/3600/24
            diff_time.append(t)
    time_ave=int(np.max(diff_time))
    dist_ave=int(np.max(diff_dist))
    time_aves.append(time_ave)
    dist_aves.append(dist_ave)
    
time_aves.sort()
dist_aves.sort()
time_aves=pd.Series(time_aves)
dist_aves=pd.Series(dist_aves)
y1=time_aves.value_counts()
y1=y1.sort_index()
y2=dist_aves.value_counts()
y2=y2.sort_index()
x1=time_aves.unique()
x2=dist_aves.unique()   #calculate quantity of each average number and use for plotting

fig=plt.figure(figsize=[16,16])
plt.bar(x1,y1)
plt.xlabel('Time(days)',fontsize=20)
plt.ylabel('Turtle numbers',fontsize=20)
plt.title('Days reporting',fontsize=20)
plt.xlim([0,200])
plt.xticks(range(0,200,20),fontsize=20)
plt.yticks(fontsize=20)
plt.savefig('during_dive_time.png')

fig=plt.figure(figsize=[16,16])
plt.bar(x2,y2)
plt.xlabel('Linear distance traveled(km)',fontsize=20)
plt.ylabel('Turtle numbers',fontsize=20)
plt.title('Distance reporting',fontsize=30)
plt.xticks(fontsize=20)
plt.yticks([0,1,2],fontsize=20)
plt.savefig('during_dive_dist.png')
plt.show()
