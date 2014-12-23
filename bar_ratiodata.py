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
obsData = pd.read_csv('ctdWithdepthofbottom.csv')
modTemp = pd.Series(str2ndlist(obsData['modTempByDepth'],bracket=True), index=obsData.index) # if str has '[' and ']', bracket should be True
obsTemp = pd.Series(str2ndlist(obsData['TEMP_VALS']), index=obsData.index)
obsDepth = pd.Series(str2ndlist(obsData['TEMP_DBAR']), index=obsData.index)
depthBottom = pd.Series(obsData['depth_bottom'],index=obsData.index)

zones_bottom=[0,0,0,0]
zones=[0,0,0,0]
error_zones_bottom=[0,0,0,0]
error_zones=[0,0,0,0]
for i in obsData.index:                       #calculate each depth zone`s error
    for j in range(4):
        if j<3:
            if j*25<depthBottom[i]<25*(1+j):
                dif=np.array(obsTemp[i])-np.array(modTemp[i])  
                indx=np.where(abs(dif)>criteria)[0]
                error_zones[j]=error_zones[j]+len(indx)   #calculate all error data in each zone
                zones[j]=zones[j]+len(modTemp[i])         #calculate all data in each zone
                zones_bottom[j]+=1                        #calculate data in bottom in each zone
                diff=np.array(obsTemp[i][-1])-np.array(modTemp[i][-1])
                if abs(diff)>criteria:
                    error_zones_bottom[j]+=1              #calculate error data in bottom in each zone
        if j==3:
            if 75<depthBottom[i]:
                dif=np.array(obsTemp[i])-np.array(modTemp[i])
                indx=np.where(abs(dif)>criteria)[0]
                error_zones[3]=error_zones[3]+len(indx)   #calculate all error data in each zone
                zones[3]=zones[3]+len(modTemp[i])         #calculate all data in each zone
                zones_bottom[3]+=1                        #calculate data in bottom in each zone
                diff=np.array(obsTemp[i][-1])-np.array(modTemp[i][-1])
                if abs(diff)>criteria:
                    error_zones_bottom[3]+=1              #calculate error data in bottom in each zone
ratio=np.array(error_zones)/(np.array(zones)*1.0)                              # ratio of all data
ratio_bottom=np.array(error_zones_bottom)/(np.array(zones_bottom)*1.0)         # ratio of bottom data
fig=plt.figure()
ax=fig.add_subplot(111)
pd.Series(ratio).plot(kind='bar')
ax.set_xticklabels(['0~25','25~50','50~75','75<'],rotation=0)
plt.ylim([0,0.6])
plt.text(0.3,0.4 ,str(error_zones[0])+'/'+str(zones[0]))
plt.text(1.3,0.43,str(error_zones[1])+'/'+str(zones[1]))
plt.text(2.3,0.47,str(error_zones[2])+'/'+str(zones[2]))
plt.text(3.4,0.41,str(error_zones[3])+'/'+str(zones[3]))
plt.xlabel('depth zones',fontsize=15)
plt.ylabel('ratio of |error|>'+str(criteria),fontsize=15)
plt.title('all data',fontsize=25)
plt.savefig('bar_alldata.png')

fig=plt.figure()
ax=fig.add_subplot(111)
pd.Series(ratio_bottom).plot(kind='bar')
ax.set_xticklabels(['0~25','25~50','50~75','75<'],rotation=0)
plt.ylim([0,0.6])
plt.text(0.4 ,0.44,str(error_zones_bottom[0])+'/'+str(zones_bottom[0]))
plt.text(1.3 ,0.31,str(error_zones_bottom[1])+'/'+str(zones_bottom[1]))
plt.text(2.4 ,0.3 ,str(error_zones_bottom[2])+'/'+str(zones_bottom[2]))
plt.text(3.45,0.41,str(error_zones_bottom[3])+'/'+str(zones_bottom[3]))
plt.xlabel('depth zones',fontsize=15)
plt.ylabel('ratio of |error|>'+str(criteria),fontsize=15)
plt.title('bottom only',fontsize=25)
plt.savefig('bar_bottomdata.png')
plt.show()
