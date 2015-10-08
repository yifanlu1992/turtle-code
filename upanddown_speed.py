# -*- coding: utf-8 -*-
"""
Created on Fri Mar 13 09:19:10 2015

@author: zhaobin
"""
'1)plot speed of upcasts and downcasts'
'2)plot change of temperature vs speed'
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from turtleModule import str2ndlist
############################################################
second_data=pd.read_csv('turtle_12487_tdr.csv')
depth=pd.Series(second_data['Depth'])
temp=pd.Series(second_data['temp'])
time=pd.Series(second_data['Date'])

for i in second_data.index:
    time[i]=datetime.strptime(time[i],'%Y/%m/%d %H:%M:%S')

data=pd.read_csv('12487up_down.csv')
up=pd.Series(str2ndlist(data['up'],bracket=True))
down=pd.Series(str2ndlist(data['down'],bracket=True))
indx=[]
for i in data.index:
    if depth[down[i][-1]]>20:       #depth>20m
        if depth[up[i][0]]>20:
            indx.append(i)
Down_mean_temp,Up_mean_temp,Down_min_temp,Up_min_temp,Down_max_temp,Up_max_temp=[],[],[],[],[],[]
diff_temp_up,diff_temp_down=[],[]
Down_speed,Up_speed=[],[]
for i in indx[1:len(indx)]:
    if down[i][-1]-down[i][0]>0:
        a=temp[int(down[i][0]):int(down[i][-1])]
        b=temp[int(up[i][0]):int(up[i][-1])]
        Down_mean_temp.append(np.mean(a))
        Up_mean_temp.append(np.mean(b))
        Down_min_temp.append(min(a))
        Up_min_temp.append(min(b))
        Down_max_temp.append(max(a))
        Up_max_temp.append(max(b))
        aa=temp[down[i][0]]-temp[down[i][-1]]
        bb=temp[up[i][-1]]-temp[up[i][0]]    
        diff_temp_down.append(aa)
        diff_temp_up.append(bb)
    
        down_speed,up_speed=[],[]
        a=(depth[down[i][-1]]-depth[down[i][0]])/(time[down[i][-1]]-time[down[i][0]]).total_seconds()
        b=(depth[up[i][0]]-depth[up[i][-1]])/(time[up[i][-1]]-time[up[i][0]]).total_seconds()
        down_speed.append(a)
        up_speed.append(b)
        Down_speed.append(down_speed)
        Up_speed.append(up_speed)
for i in range(len(Down_speed)):
    Down_speed[i]=round(Down_speed[i][0],3)  
    Up_speed[i]=round(Up_speed[i][0],3)
slow_up_speed,slow_down_speed=[],[]
for i in range(len(Up_speed)):        #calculate slow speed
    if Up_speed[i]<=0.1:
        slow_up_speed.append(Up_speed[i])
    if Down_speed[i]<=0.1:
        slow_down_speed.append(Down_speed[i])
fig=plt.figure()
ax=fig.add_subplot(121)
ax.hist(Down_speed)
ax.set_ylabel('number of dives',fontsize=20)
ax.set_xlabel('average speed(m/s)',fontsize=20)
ax.set_title('downcasts',fontsize=25)
ax1=fig.add_subplot(122)
ax1.hist(Up_speed)
ax1.set_xlabel('average speed(m/s)',fontsize=20)
ax1.set_ylabel('number of dives',fontsize=20)
ax1.set_title('upcasts',fontsize=25)
fig1=plt.figure()
ax=fig1.add_subplot(121)
ax.scatter(diff_temp_down,Down_speed)
ax.set_xlabel('change in temperature',fontsize=20)
ax.set_ylabel('average speed(m/s)',fontsize=20)
ax.set_title('downcasts',fontsize=25)
ax1=fig1.add_subplot(122)
ax1.scatter(diff_temp_up,Up_speed)
ax1.set_xlabel('change in temperature',fontsize=20)
ax1.set_title('upcasts',fontsize=25)
plt.show()
print 'mean(mean temperature in downcasts)',round(np.mean(Down_mean_temp),3)
print 'mean(min temperature in downcasts)',round(np.mean(Down_min_temp),3)
print 'mean(max temperature in downcasts)',round(np.mean(Down_max_temp),3)
print 'mean(mean temperature in upcasts)',round(np.mean(Up_mean_temp),3)
print 'mean(min temperature in upcasts)',round(np.mean(Up_min_temp),3)
print 'mean(max temperature in upcasts)',round(np.mean(Up_max_temp),3)
print "'slow' speed in upcasts is",round(float(len(slow_up_speed))/len(Up_speed)*100,2),'%'
print "'slow' speed in downcasts is",round(float(len(slow_down_speed))/len(Down_speed)*100,2),'%'
print "mean speed of upcasts:"+str(round(np.mean(Up_speed),3))+"m/s"
print "mean speed of downcasts:"+str(round(np.mean(Down_speed),3))+"m/s"
