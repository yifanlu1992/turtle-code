# -*- coding: utf-8 -*-
"""
Created on Tue Dec 16 09:44:44 2014

@author: jmanning
"""
'plot mean error,absolute mean error and rms of temperature of observe and model'
from matplotlib.mlab import griddata
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import netCDF4
from datetime import datetime, timedelta
import math
from turtleModule import str2ndlist,draw_basemap,whichArea
import watertempModule as wtm  
###############################################################################
starttime = datetime(2013,07,10) # starttime and endtime can be any time that included by model, we just want a url to get "lon_rho", "lat_rho" in model.
endtime = starttime + timedelta(hours=1)
tempObj = wtm.water_roms()
url = tempObj.get_url(starttime, endtime)
modData = netCDF4.Dataset(url)
modLons = modData.variables['lon_rho'][:]
modLats = modData.variables['lat_rho'][:]

obsData = pd.read_csv('ctdWithModTempByDepth.csv')
tf_index = np.where(obsData['TF'].notnull())[0]
modTemp = pd.Series(str2ndlist(obsData['modTempByDepth'][tf_index],bracket=True), index=tf_index) # if str has '[' and ']', bracket should be True
obsTemp = pd.Series(str2ndlist(obsData['TEMP_VALS'][tf_index]), index=tf_index)
obsDepth = pd.Series(str2ndlist(obsData['TEMP_DBAR'][tf_index]), index=tf_index)
modLayer = pd.Series(str2ndlist(obsData['modDepthLayer'][tf_index], bracket=True), index=tf_index)
depth_bottom=[]
for i in tf_index:
    d_each=(obsDepth[i][-1]-obsDepth[i][0]) *1.0/((modLayer[i][0]-modLayer[i][-1])+0.00000000000000000000001)# except divded by zero 
    if  36*d_each<200:   
        depth_bottom.append(36*d_each)
    else:
        depth_bottom.append(200)
depth_bottom=pd.Series(depth_bottom,index=tf_index)  
indx=[]
modtemp=[]
obstemp=[]
for i in modTemp.index:
    if modTemp[i][-1]<100:
        indx.append(i)
        modtemp.append(modTemp[i][-1])
        obstemp.append(obsTemp[i][-1])
modtemp=pd.Series(modtemp,index=indx)
obstemp=pd.Series(obstemp,index=indx)
depth_bottom=pd.Series(depth_bottom[indx],index=indx)
obsLon, obsLat = obsData['LON'][indx], obsData['LAT'][indx]      #use for plotting depth line
modNearestIndex = pd.Series(str2ndlist(obsData['modNearestIndex'][indx], bracket=True), index=indx)
data = pd.DataFrame({'obstemp': obsTemp,'modtemp':modTemp, 
                     'nearestIndex': modNearestIndex,
                     'depth':obsDepth,'layer':modLayer},index=indx)
  
lon_m=[]
lat_n=[]
dataNum = []
for i in range(82):  # just create a list with all zero to calculate error number 
    j = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    dataNum.append(j)
sumdata = []                   #use for calculating mean error
for i in range(82):     # just create a list with all zero to calculate error number 
    j = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    sumdata.append(j)
abs_sumdata = []               #use for calculating absolulate mean error
for i in range(82):     # just create a list with all zero to calculate error number 
    j = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    abs_sumdata.append(j)
rms=[]                         #use for calculating RMS
for i in range(82):     # just create a list with all zero to calculate error number 
    j = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    rms.append(j)
r1 = range(0, 82, 1)
r2 = range(0, 130, 1)
for i in data.index:
    m = whichArea(data['nearestIndex'][i][0], r1)
    n = whichArea(data['nearestIndex'][i][1], r2)
    if data['layer'][i][0]-data['layer'][i][-1]<>0:
        d_each=(data['depth'][i][-1]-data['depth'][i][0]) *1.0/(data['layer'][i][0]-data['layer'][i][-1])   
        if 36*d_each-data['depth'][i][-1]<10:
            if data['modtemp'][i][-1]<100:    
                dataNum[m][n] += 1 
                
                diff=np.array(data['obstemp'][i][-1])-np.array(data['modtemp'][i][-1])
                sumdata[m][n] = sumdata[m][n]+diff
                
                absdiff=abs(np.array(data['obstemp'][i][-1])-np.array(data['modtemp'][i][-1]))
                abs_sumdata[m][n] = abs_sumdata[m][n]+absdiff
                
                dif=np.sum(diff*diff)
                rms[m][n]=rms[m][n]+dif 
mean=np.array(sumdata)/np.array(dataNum)            #calculate mean error
abs_mean=np.array(abs_sumdata)/np.array(dataNum)    #calculate absolulate mean error
rms=np.array(rms)/np.array(dataNum)
RMS=np.sqrt(np.array(rms))
Mean=[]
Absmean=[]
Rms=[]
for i in range(82):
    for j in range(130):
        Mean.append(mean[i][j])
        Absmean.append(abs_mean[i][j])
        Rms.append(RMS[i][j])
modLon=[]
modLat=[]
for i in range(len(modLons)):
    for j in range(len(modLons[i])):
        modLon.append(modLons[i][j])
        modLat.append(modLats[i][j])
mean=np.array(sumdata)/np.array(dataNum)            #calculate mean error
abs_mean=np.array(abs_sumdata)/np.array(dataNum)    #calculate absolulate mean error
rms=np.array(rms)/np.array(dataNum)
RMS=np.sqrt(np.array(rms))
lonsize = [-79.5, -72.5]
latsize = [34.5, 41]
lon_i = np.linspace(lonsize[0],lonsize[1],1000)
lat_i = np.linspace(latsize[0],latsize[1],1000)
lon_is = np.linspace(lonsize[0],lonsize[1],100)
lat_is = np.linspace(latsize[0],latsize[1],100)
mean_i = griddata(np.array(modLon),np.array(modLat),np.array(Mean),lon_i,lat_i)
abs_mean_i=griddata(np.array(modLon),np.array(modLat),np.array(Absmean),lon_i,lat_i)
RMS_i=griddata(np.array(modLon),np.array(modLat),np.array(Rms),lon_i,lat_i)
depth_i=griddata(np.array(obsLon),np.array(obsLat),np.array(depth_bottom),lon_is,lat_is)
temp_i=[mean_i,abs_mean_i,RMS_i]
title=['mean_error','abs_mean_error','rms']
for k in range(len(title)):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    draw_basemap(fig, ax, lonsize, latsize)
    CS = plt.contourf(lon_i, lat_i, temp_i[k], 15, cmap=plt.cm.rainbow,
                  vmax=abs(temp_i[k]).max(), vmin=-abs(temp_i[k]).max())
    CS1=plt.contour(lon_is, lat_is,depth_i,1,colors = 'r',linestyles=':')
    ax.annotate('100m depth',xy=(-75.289,35.0395),xytext=(-75.0034,34.9842),arrowprops=dict(facecolor='black'))
    cbar=plt.colorbar(CS)
    cbar.ax.tick_params(labelsize=20) 
    #plt.scatter(np.array(obsLon),np.array(obsLat), marker='o', c='b', s=1, zorder=1)
    plt.title('only bottom:'+title[k],fontsize=30)
    plt.savefig('bottom_contourof'+title[k]+'.png')
plt.show()