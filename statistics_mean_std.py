# -*- coding: utf-8 -*-
"""
Created on Mon Sep 14 13:40:26 2015

@author: zdong
"""

'''
plot 4 maps in 1 figure to show which depth has the most errors. Also plot the errorbar and ratio
Plot error bar and ratio of error.
'''
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import netCDF4
import watertempModule as wtm   # A module of classes that using ROMS, FVCOM
from turtleModule import str2ndlist, np_datetime, bottom_value, dist
FONTSIZE = 25

obsData = pd.read_csv('ctdWithModTempByDepth.csv') # extracted from ctdWithModTempByDepth.py
tf_index = np.where(obsData['TF'].notnull())[0]    # get the index of good data
obsLon, obsLat = obsData['LON'][tf_index], obsData['LAT'][tf_index]
obsTime = pd.Series(np_datetime(obsData['END_DATE'][tf_index]), index=tf_index)
obsTemp = pd.Series(str2ndlist(obsData['TEMP_VALS'][tf_index]), index=tf_index)
obsDepth = pd.Series(str2ndlist(obsData['TEMP_DBAR'][tf_index]), index=tf_index)
modLayer = pd.Series(np.array(str2ndlist(obsData['modDepthLayer'][tf_index],bracket=True)), index=tf_index) # bracket is to get rid of symbol "[" and "]" in string
modNearestIndex = pd.Series(str2ndlist(obsData['modNearestIndex'][tf_index], bracket=True), index=tf_index)
modTemp = pd.Series(np.array(str2ndlist(obsData['modTempByDepth'][tf_index], bracket=True)), index=tf_index)
data = pd.DataFrame({'lon': obsLon, 'lat': obsLat,
                     'obstemp': obsTemp.values,'modtemp':modTemp,
                     'depth': obsDepth, 'time': obsTime.values,
                     'layer': modLayer}, index=tf_index)
TEMP=[]
for i in range(50):   #depth 0~50m
    TEMP.append([])
    print(i)
    for j in data.index:
        for q in range(len(data['depth'][j])):
            if int(data['depth'][j][q])==i+2:   #no depth<2m
                if data['modtemp'][j][q]<100:  #some bad data>100 degC
                    TEMP[i].append(data['modtemp'][j][q]-data['obstemp'][j][q])
ave=[]
std=[]
for i in range(50):  #depth 0~50m
    ave.append(np.mean(TEMP[i]))
    std.append(np.std(TEMP[i]))
fig=plt.figure()
ax=fig.add_subplot(111)
ax.errorbar(ave,range(len(ave)),xerr=std)
plt.ylim([50,0])
plt.axvline(0,color='black', lw=2)
plt.ylabel('Depth(m)',fontsize=20)
plt.xlabel('degC',fontsize=20)
plt.title('Statistics between modelled and observed temperature',fontsize=30)
plt.show() 
