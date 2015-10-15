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
#####################################roms######################################
obsData = pd.read_csv('ctdWithModTempByDepth.csv') # extracted from ctdWithModTempByDepth.py
tf_index = np.where(obsData['TF'].notnull())[0]    # get the index of good data
obsTemp = pd.Series(str2ndlist(obsData['TEMP_VALS'][tf_index]), index=tf_index)
obsDepth = pd.Series(str2ndlist(obsData['TEMP_DBAR'][tf_index]), index=tf_index)
modTemp = pd.Series(np.array(str2ndlist(obsData['modTempByDepth'][tf_index], bracket=True)), index=tf_index)
data_roms = pd.DataFrame({'obstemp': obsTemp.values,'modtemp':modTemp,'depth': obsDepth}, index=tf_index)
TEMP_roms_all=[]
TEMP_roms=[]
TEMP_roms_negivate=[]
for i in range(50):   #depth 0~50m
    TEMP_roms.append(0)
    TEMP_roms_negivate.append(0)
    TEMP_roms_all.append(0)
    for j in data_roms.index:
        for q in range(len(data_roms['depth'][j])):
            if int(data_roms['depth'][j][q])==i:   
                TEMP_roms_all[i]=TEMP_roms_all[i]+1
                if data_roms['modtemp'][j][q]<100:  #some bad data>100 degC
                    if data_roms['modtemp'][j][q]-data_roms['obstemp'][j][q]>10:
                        TEMP_roms[i]=TEMP_roms[i]+1
                    if data_roms['obstemp'][j][q]-data_roms['modtemp'][j][q]>10:
                        TEMP_roms_negivate[i]=TEMP_roms_negivate[i]-1
######################################fvcom####################################
obsData = pd.read_csv('ctdWithdepthofbottom_fvcom.csv') 
tf_index = np.where(obsData['in FVcom range'].notnull())[0]    # get the index of good data
obsTemp = pd.Series(str2ndlist(obsData['TEMP_VALS'][tf_index]), index=tf_index)
obsDepth = pd.Series(str2ndlist(obsData['TEMP_DBAR'][tf_index]), index=tf_index)
modTemp = pd.Series(np.array(str2ndlist(obsData['modtempBYdepth'][tf_index], bracket=True)), index=tf_index)
data_fvcom = pd.DataFrame({'obstemp': obsTemp.values,'modtemp':modTemp,'depth': obsDepth}, index=tf_index)
TEMP_fvcom_all=[]
TEMP_fvcom=[]
TEMP_fvcom_negivate=[]
for i in range(50):   #depth 0~50m
    TEMP_fvcom.append(0)
    TEMP_fvcom_negivate.append(0)
    TEMP_fvcom_all.append(0)
    for j in data_fvcom.index:
        for q in range(len(data_fvcom['depth'][j])):
            if int(data_fvcom['depth'][j][q])==i:   
                TEMP_fvcom_all[i]=TEMP_fvcom_all[i]+1
                if -10<data_fvcom['modtemp'][j][q]<100:  #some bad data>100 degC
                    if data_fvcom['modtemp'][j][q]-data_fvcom['obstemp'][j][q]>10:
                        TEMP_fvcom[i]=TEMP_fvcom[i]+1
                    if data_fvcom['obstemp'][j][q]-data_fvcom['modtemp'][j][q]>10:
                        TEMP_fvcom_negivate[i]=TEMP_fvcom_negivate[i]-1
######################################hycom####################################  
obsData = pd.read_csv('ctd_withHYCOMtemp.csv') 
tf_index = np.where(obsData['TF'].notnull())[0]    # get the index of good data
obsTemp = pd.Series(str2ndlist(obsData['TEMP_VALS'][tf_index]), index=tf_index)
obsDepth = pd.Series(str2ndlist(obsData['TEMP_DBAR'][tf_index]), index=tf_index)
modTemp = pd.Series(np.array(str2ndlist(obsData['modtemp_HYCOM'][tf_index], bracket=True)), index=tf_index)
data_hycom = pd.DataFrame({'obstemp': obsTemp.values,'modtemp':modTemp,'depth': obsDepth}, index=tf_index)
TEMP_hycom_all=[]
TEMP_hycom=[]
TEMP_hycom_negivate=[]
for i in range(50):   #depth 0~50m
    TEMP_hycom.append(0)
    TEMP_hycom_negivate.append(0)
    TEMP_hycom_all.append(0)
    for j in data_hycom.index:
        for q in range(len(data_hycom['depth'][j])):
            if int(data_hycom['depth'][j][q])==i:   
                TEMP_hycom_all[i]=TEMP_hycom_all[i]+1
                if -10<data_hycom['modtemp'][j][q]<100:  #some bad data>100 degC
                    if data_hycom['modtemp'][j][q]-data_hycom['obstemp'][j][q]>10:
                        TEMP_hycom[i]=TEMP_hycom[i]+1
                    if data_hycom['obstemp'][j][q]-data_hycom['modtemp'][j][q]>10:
                        TEMP_hycom_negivate[i]=TEMP_hycom_negivate[i]-1 
fig=plt.figure()
ax=fig.add_subplot(311)
ax.barh(range(50),TEMP_roms,color='r',label='model warmer')
ax.barh(range(50),TEMP_roms_negivate,color='b',label='model colder')
plt.legend(loc='best')
plt.ylim([50,0])
plt.xlim([-500,600])
plt.text(-200,40,'ROMS',fontsize=20)
plt.title('Quantity |modeled-observed| Temperature>10 $^\circ$C',fontsize=30)
ax1=fig.add_subplot(312)
ax1.barh(range(50),TEMP_fvcom,color='r',label='model warmer')
ax1.barh(range(50),TEMP_fvcom_negivate,color='b',label='model colder')
plt.legend(loc='best')
plt.ylim([50,0])
plt.xlim([-500,600])
plt.text(-200,40,'FVCOM',fontsize=20)
plt.ylabel('Depth(m)',fontsize=30)
ax2=fig.add_subplot(313)
ax2.barh(range(50),TEMP_hycom,color='r',label='model warmer')
ax2.barh(range(50),TEMP_hycom_negivate,color='b',label='model colder')
plt.legend(loc='best')
plt.ylim([50,0])
plt.xlim([-500,600])
plt.text(-200,40,'HYCOM',fontsize=20)
plt.xlabel('Quantity',fontsize=30)

fig=plt.figure()
ax=fig.add_subplot(311)
ax.barh(range(50),np.round(np.array(TEMP_roms)/np.array(TEMP_roms_all)*100,3),color='r',label='model warmer')
ax.barh(range(50),np.round(np.array(TEMP_roms_negivate)/np.array(TEMP_roms_all)*100,3),color='b',label='model colder')
plt.legend(loc='best')
plt.ylim([50,0])
plt.xlim([-20,25])
plt.text(-200,40,'ROMS',fontsize=20)
plt.title('Percent time |modeled-observed| Temperature>10 $^\circ$C',fontsize=30)
ax1=fig.add_subplot(312)
ax1.barh(range(50),np.round(np.array(TEMP_fvcom)/np.array(TEMP_fvcom_all)*100,3),color='r',label='model warmer')
ax1.barh(range(50),np.round(np.array(TEMP_fvcom_negivate)/np.array(TEMP_fvcom_all)*100,3),color='b',label='model colder')
plt.legend(loc='best')
plt.ylim([50,0])
plt.xlim([-20,25])
plt.text(-200,40,'FVCOM',fontsize=20)
plt.ylabel('Depth(m)',fontsize=30)
ax2=fig.add_subplot(313)
ax2.barh(range(50),np.round(np.array(TEMP_hycom)/np.array(TEMP_hycom_all)*100,3),color='r',label='model warmer')
ax2.barh(range(50),np.round(np.array(TEMP_hycom_negivate)/np.array(TEMP_hycom_all)*100,3),color='b',label='model colder')
plt.legend(loc='best')
plt.ylim([50,0])
plt.xlim([-20,25])
plt.text(-200,40,'HYCOM',fontsize=20)
plt.xlabel('Percent Time',fontsize=30)
plt.show()                                                                 
