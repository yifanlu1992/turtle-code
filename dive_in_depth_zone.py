# -*- coding: utf-8 -*-
"""
Created on Tue Feb  3 11:12:04 2015

@author: zhaobin
"""
'return number of obsDeepest/moddeepest>0.8 in each depth zone'
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import netCDF4
from datetime import datetime, timedelta
from turtleModule import str2ndlist
import watertempModule as wtm         
######################################################################################
obsData = pd.read_csv('ctdWithModTempByDepth.csv') 
tf_index = np.where(obsData['TF'].notnull())[0] # Get index of good data.
obsDeepest = obsData['MAX_DBAR'][tf_index] # get deepest data file depth
modNearestIndex = pd.Series(str2ndlist(obsData['modNearestIndex'][tf_index], bracket=True), index=tf_index)

starttime = datetime(2013,05,20) # starttime and endtime here is just to get 'h', the model depth
endtime = datetime(2013, 12, 13)
tempObj = wtm.waterCTD()
url = tempObj.get_url(starttime, endtime)
modData = netCDF4.Dataset(url)
h = modData.variables['h']
moddeepest=[]
for i in tf_index:
    m, n = int(modNearestIndex[i][0]), int(modNearestIndex[i][1])
    moddeepest.append(h[m][n])
   
p = obsDeepest/moddeepest
index1 = p[p>0.8].index

INDEX=[0]*9
for i in index1:
    for j in range(len(INDEX)):
        if j+1<len(INDEX):
            if 10*j<=obsDeepest[i]<10*(j+1):            #calculate number of dive in each depth zone
                INDEX[j]+=1
        else:
            INDEX[j]+1
    
fig=plt.figure()
ax=fig.add_subplot(111)
pd.Series(INDEX).plot(kind='bar')
ax.set_xticklabels(['0~10','10~20','20~30','30~40','40~50','50~60','60~70','70~80','>80'],rotation=0)
plt.xlabel('depth(m)',fontsize=15)
plt.ylabel('quantity',fontsize=15)
plt.title('maxDepth/moddepth>0.8 in each depth zone',fontsize=25)
plt.savefig('dives_in_depth_zone.png')
plt.show()