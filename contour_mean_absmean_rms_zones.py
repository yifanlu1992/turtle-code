# -*- coding: utf-8 -*-
"""
Created on Tue Dec 16 10:41:29 2014

@author: zhaobin
"""
'plot mean error,absolute mean error and rms of temperature of observe and model in different depth zones'
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
r1 = range(0, 82, 1)
r2 = range(0, 130, 1)  
lon_m=[]
lat_n=[]
dataNum,sumdata,abs_sumdata,rms = [[],[],[],[]],[[],[],[],[]],[[],[],[],[]],[[],[],[],[]]
mean,abs_mean,rms,RMS=[[],[],[],[]],[[],[],[],[]],[[],[],[],[]],[[],[],[],[]]
Mean,Absmean,Rms=[[],[],[],[]],[[],[],[],[]],[[],[],[],[]]
for k in range(4):
    for i in range(82):  # just create a list with all zero to calculate error number 
        j = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        dataNum[k].append(j)                  
    for i in range(82):     # just create a list with all zero to calculate error number 
        j = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        sumdata[k].append(j)            
    for i in range(82):     # just create a list with all zero to calculate error number 
        j = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        abs_sumdata[k].append(j)                     
    for i in range(82):     # just create a list with all zero to calculate error number 
        j = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        rms[k].append(j)
    
    for i in data.index:
        m = whichArea(data['nearestIndex'][i][0], r1)
        n = whichArea(data['nearestIndex'][i][1], r2)
        for j in range(len(data['obstemp'][i])):
            if k<3:            
                if k*25<data['depth'][i][j]<(k+1)*25:
                    dataNum[k][m][n] += 1 
                
                    diff=np.array(data['obstemp'][i][j])-np.array(data['modtemp'][i][j])
                    sumdata[k][m][n] = sumdata[k][m][n]+diff
                
                    absdiff=abs(np.array(data['obstemp'][i][j])-np.array(data['modtemp'][i][j]))
                    abs_sumdata[k][m][n] = abs_sumdata[k][m][n]+absdiff
                
                    dif=np.sum(diff*diff)
                    rms[k][m][n]=rms[k][m][n]+dif 
            if k==3:
                if k*25<data['depth'][i][j]:
                    dataNum[k][m][n] += 1 
                
                    diff=np.array(data['obstemp'][i][j])-np.array(data['modtemp'][i][j])
                    sumdata[k][m][n] = sumdata[k][m][n]+diff
                
                    absdiff=abs(np.array(data['obstemp'][i][j])-np.array(data['modtemp'][i][j]))
                    abs_sumdata[k][m][n] = abs_sumdata[k][m][n]+absdiff
                
                    dif=np.sum(diff*diff)
                    rms[k][m][n]=rms[k][m][n]+dif 
    mean[k]=np.array(sumdata[k])/(np.array(dataNum[k])*1.0)            #calculate mean error
    abs_mean[k]=np.array(abs_sumdata[k])/(np.array(dataNum[k])*1.0)    #calculate absolulate mean error
    rms[k]=np.array(rms[k])/(np.array(dataNum[k])*1.0)
    RMS[k]=np.sqrt(np.array(rms[k]))                                   #calculate rms
   
    for i in range(82):
        for j in range(130):
            Mean[k].append(mean[k][i][j])
            Absmean[k].append(abs_mean[k][i][j])
            Rms[k].append(RMS[k][i][j])
modLon=[]
modLat=[]
for i in range(len(modLons)):
    for j in range(len(modLons[i])):
        modLon.append(modLons[i][j])
        modLat.append(modLats[i][j])

lonsize = [-79.5, -72.5]
latsize = [34.5, 41]
lon_i = np.linspace(lonsize[0],lonsize[1],1000)
lat_i = np.linspace(latsize[0],latsize[1],1000)
lon_is = np.linspace(lonsize[0],lonsize[1],100)
lat_is = np.linspace(latsize[0],latsize[1],100)
depth_i=griddata(np.array(obsLon),np.array(obsLat),np.array(depth_bottom),lon_is,lat_is)
title=['mean_error','abs_mean_error','rms']
depth_zones=['0~25','25~50','50~75','75~100']
mean_i,abs_mean_i,RMS_i=[[],[],[],[]],[[],[],[],[]],[[],[],[],[]]
for i in range(4):
    mean_i[i] = griddata(np.array(modLon),np.array(modLat),np.array(Mean[i]),lon_i,lat_i)
    abs_mean_i[i]=griddata(np.array(modLon),np.array(modLat),np.array(Absmean[i]),lon_i,lat_i)
    RMS_i[i]=griddata(np.array(modLon),np.array(modLat),np.array(Rms[i]),lon_i,lat_i)
    temp_i=[mean_i[i],abs_mean_i[i],RMS_i[i]]
    
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
        plt.title(title[k]+'  DEPTH:'+depth_zones[i],fontsize=30)
        plt.savefig('contourof'+title[k]+'_'+depth_zones[i]+'.png')
plt.show()