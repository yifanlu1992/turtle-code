# -*- coding: utf-8 -*-
"""
Created on Mon Sep 14 13:40:26 2015
plot 4 maps in 1 figure to show which depth has the most errors. Also plot the errorbar and ratio
Plot error bar and ratio of error in 3 models.
@author: zdong
"""
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import netCDF4
import watertempModule as wtm   # A module of classes that using ROMS, FVCOM
from turtleModule import str2ndlist, np_datetime, bottom_value, dist
#####################################roms######################################
obsData = pd.read_csv('ctdWithModTempByDepth.csv') # extracted from ctdWithModTempByDepth.py
tf_index = np.where(obsData['TF'].notnull())[0]    # get the index of good data
obsTime = pd.Series(np_datetime(obsData['END_DATE'][tf_index]), index=tf_index)
obsTemp = pd.Series(str2ndlist(obsData['TEMP_VALS'][tf_index]), index=tf_index)
obsDepth = pd.Series(str2ndlist(obsData['TEMP_DBAR'][tf_index]), index=tf_index)
modTemp = pd.Series(np.array(str2ndlist(obsData['modTempByDepth'][tf_index], bracket=True)), index=tf_index)
data_roms = pd.DataFrame({'obstemp': obsTemp.values,'modtemp':modTemp,'depth': obsDepth}, index=tf_index)
TEMP_roms=[]
for i in np.arange(50):   #depth 0~50m
    TEMP_roms.append([])
    for j in data_roms.index:
        for q in range(len(data_roms['depth'][j])):
            if int(data_roms['depth'][j][q])==i:   #no depth<2m
                if data_roms['modtemp'][j][q]<100:  #some bad data>100 degC
                    TEMP_roms[i].append(data_roms['modtemp'][j][q]-data_roms['obstemp'][j][q])
######################################fvcom####################################
obsData = pd.read_csv('ctdWithdepthofbottom_fvcom.csv') 
tf_index = np.where(obsData['in FVcom range'].notnull())[0]    # get the index of good data
obsTemp = pd.Series(str2ndlist(obsData['TEMP_VALS'][tf_index]), index=tf_index)
obsDepth = pd.Series(str2ndlist(obsData['TEMP_DBAR'][tf_index]), index=tf_index)
modTemp = pd.Series(np.array(str2ndlist(obsData['modtempBYdepth'][tf_index], bracket=True)), index=tf_index)
data_fvcom = pd.DataFrame({'obstemp': obsTemp.values,'modtemp':modTemp,'depth': obsDepth}, index=tf_index)
TEMP_fvcom=[]
for i in np.arange(50):   #depth 0~50m
    TEMP_fvcom.append([])
    for j in data_fvcom.index:
        for q in range(len(data_fvcom['depth'][j])):
            if int(data_fvcom['depth'][j][q])==i:   #no depth<2m
                if data_fvcom['modtemp'][j][q]<100:  #some bad data>100 degC
                    TEMP_fvcom[i].append(data_fvcom['modtemp'][j][q]-data_fvcom['obstemp'][j][q])
######################################hycom####################################
obsData = pd.read_csv('ctd_withHYCOMtemp.csv') 
tf_index = np.where(obsData['TF'].notnull())[0]    # get the index of good data
obsTemp = pd.Series(str2ndlist(obsData['TEMP_VALS'][tf_index]), index=tf_index)
obsDepth = pd.Series(str2ndlist(obsData['TEMP_DBAR'][tf_index]), index=tf_index)
modTemp = pd.Series(np.array(str2ndlist(obsData['modtemp_HYCOM'][tf_index], bracket=True)), index=tf_index)
data_hycom = pd.DataFrame({'obstemp': obsTemp.values,'modtemp':modTemp,'depth': obsDepth}, index=tf_index)
TEMP_hycom=[]
for i in np.arange(50):   #depth 0~50m
    TEMP_hycom.append([])
    for j in data_hycom.index:
        for q in range(len(data_hycom['depth'][j])):
            if int(data_hycom['depth'][j][q])==i:   #no depth<2m
                if -10<data_hycom['modtemp'][j][q]<100:  #some bad data>100 and <-10 degC
                    TEMP_hycom[i].append(data_hycom['modtemp'][j][q]-data_hycom['obstemp'][j][q])
ave_roms,std_roms=[],[]
ave_fvcom,std_fvcom=[],[]
ave_hycom,std_hycom=[],[]
for i in range(50):  #depth 0~50m
    ave_roms.append(np.mean(TEMP_roms[i]))
    std_roms.append(np.std(TEMP_roms[i]))
    ave_fvcom.append(np.mean(TEMP_fvcom[i]))
    std_fvcom.append(np.std(TEMP_fvcom[i]))
    ave_hycom.append(np.mean(TEMP_hycom[i]))
    std_hycom.append(np.std(TEMP_hycom[i]))
fig=plt.figure()
ax=fig.add_subplot(311)
ax.errorbar(ave_roms,range(len(ave_roms)),xerr=std_roms)
plt.ylim([50,0])
plt.xlim([-8.1,11])
plt.text(-7,40,'ROMS',fontsize=20)
plt.title('Statistics between modelled and observed temperature',fontsize=30)
ax1=fig.add_subplot(312)
ax1.errorbar(ave_fvcom,range(len(ave_fvcom)),xerr=std_fvcom)
plt.ylim([50,0])
plt.xlim([-8.1,11])
plt.text(-7,40,'FVCOM',fontsize=20)
plt.ylabel('Depth(m)',fontsize=30)
ax2=fig.add_subplot(313)
ax2.errorbar(ave_hycom,range(len(ave_hycom)),xerr=std_hycom)
plt.ylim([50,0])
plt.xlim([-8.1,11])
plt.text(-7,40,'HYCOM',fontsize=20)
plt.xlabel('degC',fontsize=30)
plt.show()                
