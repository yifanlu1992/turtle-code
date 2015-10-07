# -*- coding: utf-8 -*-
"""
Created on Tue Nov 18 09:26:46 2014

@author: zhaobin
"""
'plot average of all turtles` time and distance of sending message'
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from turtleModule import dist,np_datetime
##################################main code####################################
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
            ids[i].append(j)   #collect index of each turtle 
time_aves=[]
dist_aves=[]        #collect all average
for i in range(len(ids)):
    obs=obsData.ix[ids[i]]    
    goodTime=pd.Series(np_datetime(obs['END_DATE']), index=ids[i])
    goodlons=pd.Series(obs['LON'], index=ids[i])
    goodlats=pd.Series(obs['LAT'], index=ids[i])
    d=pd.DataFrame({'Time':goodTime,'lon':goodlons,'lat':goodlats},index=ids[i])   #each turtle`s modtemp and obstemp
    d=d.sort(['Time'])
    d.index=range(len(d))
    diff_dist=[]
    diff_time=[]
    for j in d.index:
        if j+1 == len(d):
            break
        dis=dist(d['lon'][j],d['lat'][j],d['lon'][j+1],d['lat'][j+1])
        diff_dist.append(dis)
        t=(d['Time'][j+1]-d['Time'][j]).total_seconds()/3600
        diff_time.append(t)
    time_ave=round(np.mean(diff_time))
    dist_ave=round(np.mean(diff_dist))    #each turtle`s average
    time_aves.append(time_ave)
    dist_aves.append(dist_ave)
ave_time=round(np.mean(np.array(time_aves)),2)
ave_dist=round(np.mean(np.array(dist_aves)),2)
std_time=round(np.std(np.array(time_aves)),2)
std_dist=round(np.std(np.array(dist_aves)),2)

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

fig=plt.figure()
plt.bar(x1,y1)
plt.title('Average times:'+str(ave_time)+' standard deviation:'+str(std_time))
plt.xlabel('Average times /h')
plt.ylabel('Turtle numbers')
plt.ylim([0,10])
plt.xlim([0,75])
plt.savefig('average1.png')
fig=plt.figure()
plt.bar(x2,y2)
plt.title('Average distance:'+str(ave_dist)+' standard deviation:'+str(std_dist))
plt.xlabel('Average distance /km')
plt.ylabel('Turtle numbers')
plt.savefig('average2.png')
plt.show()
