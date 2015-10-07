# -*- coding: utf-8 -*-
"""
Created on Thu Nov 13 12:40:52 2014
plot one turtle`s time and distance of sending message.
@author: zhaobin
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from turtleModule import dist,np_datetime
#############################main code##################################################
obsData = pd.read_csv('ctdWithModTempByDepth.csv')
tf_index = np.where(obsData['TF'].notnull())[0]
obsturtle_id=pd.Series(obsData['PTT'][tf_index],index=tf_index)
obsturtle_ids=obsturtle_id.unique()

turtle_id=obsturtle_ids[0]        #which turtle you want to plot.such as 0~106
indx=[]                           #collect index of the turtle which you want to plot
for i in tf_index:
    if obsturtle_id[i] == turtle_id:
        indx.append(i)

obs=obsData.ix[indx]    
goodTime=pd.Series(np_datetime(obs['END_DATE']), index=indx)
goodlons=pd.Series(obs['LON'], index=indx)
goodlats=pd.Series(obs['LAT'], index=indx)
d=pd.DataFrame({'Time':goodTime,'lon':goodlons,'lat':goodlats},index=indx)
d=d.sort(['Time'])
d.index=range(len(d))
diff_dist=[]                      #collect distance
diff_time=[]                      #collect time
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
plt.xlabel('Sort by time')
plt.ylabel('Distance unit:km')
plt.title('Dist,average='+str(dist_ave)+'(km). turtle:'+str(turtle_id))
plt.savefig('between_dive_dist.png')
 
fig=plt.figure()
plt.bar(range(len(diff_time)),diff_time) 
plt.ylim([0,150])
plt.xlim([0,164])
plt.xlabel('Sort by time')
plt.ylabel('Time unit:h')
plt.title('Time,average='+str(time_ave)+'(h). turtle:'+str(turtle_id))
plt.savefig('between_dive_time.png')
       
plt.show()
