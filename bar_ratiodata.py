# -*- coding: utf-8 -*-
"""
Created on Tue Dec  9 10:08:54 2014

@author: zhaobin
"""
'calculate number of data in 0~25,25~50,50~75,75<'
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from turtleModule import str2ndlist,np_datetime
############################# main code ###############################
criteria=2                  # criteria for error
obsData=pd.read_csv('ctdWithModTempByDepth.csv')
tf_index=np.where(obsData['TF'].notnull())[0]
modTemp = pd.Series(str2ndlist(obsData['modTempByDepth'][tf_index],bracket=True), index=tf_index) # if str has '[' and ']', bracket should be True
obsTemp = pd.Series(str2ndlist(obsData['TEMP_VALS'][tf_index]), index=tf_index)
obsDepth = pd.Series(str2ndlist(obsData['TEMP_DBAR'][tf_index]), index=tf_index)
modLayer = pd.Series(str2ndlist(obsData['modDepthLayer'][tf_index], bracket=True), index=tf_index)

depth_bottom=[]
for i in tf_index:
    d_each=(obsDepth[i][-1]-obsDepth[i][0]) *1.0/((modLayer[i][0]-modLayer[i][-1])+0.00000000000000000000001)# except divded by zero 
    depth_bottom.append(36*d_each)
depth_bottom=pd.Series(depth_bottom,index=tf_index) 
zones_bottom=[0,0,0,0]
zones=[0,0,0,0]
error_zones_bottom=[0,0,0,0]
error_zones=[0,0,0,0]
for i in tf_index:                       #calculate each depth zone`s error
    if depth_bottom[i]<25:
        dif=np.array(obsTemp[i])-np.array(modTemp[i])
        indx=np.where(abs(dif)>criteria)[0]
        error_zones[0]=error_zones[0]+len(indx)
        zones[0]=zones[0]+len(modTemp[i])
        zones_bottom[0]+=1
        diff=np.array(obsTemp[i][-1])-np.array(modTemp[i][-1])
        if abs(diff)>criteria:
            error_zones_bottom[0]+=1
    if 25<depth_bottom[i]<50:
        dif=np.array(obsTemp[i])-np.array(modTemp[i])
        indx=np.where(abs(dif)>criteria)[0]
        error_zones[1]=error_zones[1]+len(indx)
        zones[1]=zones[1]+len(modTemp[i])
        zones_bottom[1]+=1
        diff=np.array(obsTemp[i][-1])-np.array(modTemp[i][-1])
        if abs(diff)>criteria:
            error_zones_bottom[1]+=1
    if 50<depth_bottom[i]<75:
        dif=np.array(obsTemp[i])-np.array(modTemp[i])
        indx=np.where(abs(dif)>criteria)[0]
        error_zones[2]=error_zones[2]+len(indx)
        zones[2]=zones[2]+len(modTemp[i])
        zones_bottom[2]+=1
        diff=np.array(obsTemp[i][-1])-np.array(modTemp[i][-1])
        if abs(diff)>criteria:
            error_zones_bottom[2]+=1
    if 75<depth_bottom[i]:
        dif=np.array(obsTemp[i])-np.array(modTemp[i])
        indx=np.where(abs(dif)>criteria)[0]
        error_zones[3]=error_zones[3]+len(indx)
        zones[3]=zones[3]+len(modTemp[i])
        zones_bottom[3]+=1
        diff=np.array(obsTemp[i][-1])-np.array(modTemp[i][-1])
        if abs(diff)>criteria:
            error_zones_bottom[3]+=1
ratio=np.array(error_zones)/(np.array(zones)*1.0)                              # ratio of all data
ratio_bottom=np.array(error_zones_bottom)/(np.array(zones_bottom)*1.0)         # ratio of bottom data
fig=plt.figure()
ax=fig.add_subplot(111)
pd.Series(ratio).plot(kind='bar')
ax.set_xticklabels(['0~25','25~50','50~75','75<'],rotation=0)
plt.ylim([0,0.6])
plt.text(0.3,0.48,str(error_zones[0])+'/'+str(zones[0]))
plt.text(1.3,0.41,str(error_zones[1])+'/'+str(zones[1]))
plt.text(2.3,0.5 ,str(error_zones[2])+'/'+str(zones[2]))
plt.text(3.4,0.37,str(error_zones[3])+'/'+str(zones[3]))
plt.xlabel('depth zones',fontsize=15)
plt.ylabel('ratio of |error|>'+str(criteria),fontsize=15)
plt.title('all data',fontsize=25)
plt.savefig('bar_alldata.png')

fig=plt.figure()
ax=fig.add_subplot(111)
pd.Series(ratio_bottom).plot(kind='bar')
ax.set_xticklabels(['0~25','25~50','50~75','75<'],rotation=0)
plt.ylim([0,0.6])
plt.text(0.4,0.54,str(error_zones_bottom[0])+'/'+str(zones_bottom[0]))
plt.text(1.3,0.32,str(error_zones_bottom[1])+'/'+str(zones_bottom[1]))
plt.text(2.3,0.3 ,str(error_zones_bottom[2])+'/'+str(zones_bottom[2]))
plt.text(3.45,0.32,str(error_zones_bottom[3])+'/'+str(zones_bottom[3]))
plt.xlabel('depth zones',fontsize=15)
plt.ylabel('ratio of |error|>'+str(criteria),fontsize=15)
plt.title('bottom only',fontsize=25)
plt.savefig('bar_bottomdata.png')
plt.show()
