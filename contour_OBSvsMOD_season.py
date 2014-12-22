# -*- coding: utf-8 -*-
"""
Created on Thu Nov 20 10:57:43 2014

@author: zhaobin
"""
'plot contour of observe and model temperature in four seasons'
from matplotlib.mlab import griddata
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import netCDF4
from turtleModule import str2ndlist,draw_basemap,np_datetime
##############################main code########################################
lonsize = [-79.5, -72.5]
latsize = [34.5, 41]

obsData = pd.read_csv('ctdWithModTempByDepth.csv')
tf_index = np.where(obsData['TF'].notnull())[0]
modTemp = pd.Series(str2ndlist(obsData['modTempByDepth'][tf_index],bracket=True), index=tf_index) # if str has '[' and ']', bracket should be True
obsTemp = pd.Series(str2ndlist(obsData['TEMP_VALS'][tf_index]), index=tf_index)
obsDepth = pd.Series(str2ndlist(obsData['TEMP_DBAR'][tf_index]), index=tf_index)
modLayer = pd.Series(str2ndlist(obsData['modDepthLayer'][tf_index], bracket=True), index=tf_index)
data = pd.DataFrame({'depth':obsDepth,'layer':modLayer},index=tf_index)

depth_bottom=[]

indx=[]
modtemp=[]
obstemp=[]
for i in tf_index:
    d_each=(data['depth'][i][-1]-data['depth'][i][0]) *1.0/((data['layer'][i][0]-data['layer'][i][-1])+0.00000000000000000000001)# except divded by zero 
    if  36*d_each<200:   
        depth_bottom.append(36*d_each)
    else:
        depth_bottom.append(200)                # Just one point is deeper than 200m.
    if 36*d_each-data['depth'][i][-1]<10:
        if modTemp[i][-1]<100:
            indx.append(i)
            modtemp.append(modTemp[i][-1])
            obstemp.append(obsTemp[i][-1])      #Some datas` temperatures are wrong.Get rid of them.                  
depth_bottom=pd.Series(depth_bottom,index=tf_index) 
obsLons, obsLats = obsData['LON'][tf_index], obsData['LAT'][tf_index] 
modtemp=pd.Series(modtemp,index=indx)
obstemp=pd.Series(obstemp,index=indx)
obsLon, obsLat = obsData['LON'][indx], obsData['LAT'][indx]

index_inside=[]
for i in obsLon.index:
    if lonsize[0]<obsLon[i]<lonsize[1]:
        index_inside.append(i)                           #Just use data in this area.
obsTime = pd.Series(np_datetime(obsData['END_DATE'][index_inside]), index=index_inside)
SPRING=[]
SUMMER=[]
FALL=[]
WINTER=[]
YEAR=[]
for i in obsTime.index:
    if 2<obsTime[i].month<6:
        SPRING.append(i)
    if 5<obsTime[i].month<9:
        SUMMER.append(i)
    if 8<obsTime[i].month<12:
        FALL.append(i)
    if 11<obsTime[i].month or obsTime[i].month<3:
        WINTER.append(i)                                      #Collect each season`s index.
season=['summer','fall','spring','winter']
SEASON=[SUMMER,FALL,SPRING,WINTER]
lon_i = np.linspace(lonsize[0],lonsize[1],1000)
lat_i = np.linspace(latsize[0],latsize[1],1000)
lon_is = np.linspace(lonsize[0],lonsize[1],100)
lat_is = np.linspace(latsize[0],latsize[1],100)
depth_i = griddata(np.array(obsLons),np.array(obsLats),np.array(depth_bottom),lon_is,lat_is)   #use for plotting 100m depth line.
for i in [0,2]:        #two seasons together plot.
    modtemps=pd.Series(modtemp[SEASON[i]],index=SEASON[i])
    obstemps=pd.Series(obstemp[SEASON[i]],index=SEASON[i])
    obsLon, obsLat = obsData['LON'][SEASON[i]], obsData['LAT'][SEASON[i]]
    modtemp_i = griddata(np.array(obsLon),np.array(obsLat),np.array(modtemps),lon_i,lat_i)
    obstemp_i = griddata(np.array(obsLon),np.array(obsLat),np.array(obstemps),lon_i,lat_i)  
    fig = plt.figure()
    ax = fig.add_subplot(221)
    draw_basemap(fig, ax, lonsize, latsize)
    CS = ax.contourf(lon_i, lat_i, modtemp_i, np.arange(0,30,1), cmap=plt.cm.rainbow,
                  vmax=abs(modtemp_i).max(), vmin=-abs(modtemp_i).max())
    CS1=ax.contour(lon_is, lat_is,depth_i,1,colors = 'r',linestyles=':',linewidths=2)
    plt.colorbar(CS)
    #plt.scatter(np.array(obsLon),np.array(obsLat), marker='o', c='b', s=5, zorder=10)
    ax.set_title('mod_'+season[i])
    ax.annotate('100m depth',xy=(-75.289,35.0395),xytext=(-75.0034,34.9842),arrowprops=dict(facecolor='black'))    
    
    ax1 = fig.add_subplot(222)
    draw_basemap(fig, ax1, lonsize, latsize)
    CS = ax1.contourf(lon_i, lat_i, obstemp_i, np.arange(0,30,1), cmap=plt.cm.rainbow,
                  vmax=abs(obstemp_i).max(), vmin=-abs(obstemp_i).max())
    CS1=ax1.contour(lon_is, lat_is,depth_i,1,colors = 'r',linestyles=':',linewidths=2)
    plt.colorbar(CS)
    #plt.scatter(np.array(obsLon),np.array(obsLat), marker='o', c='b', s=5, zorder=10)
    ax1.set_title('obs_'+season[i])
    ax1.annotate('100m depth',xy=(-75.289,35.0395),xytext=(-75.0034,34.9842),arrowprops=dict(facecolor='black'))  

    
    modtemps=pd.Series(modtemp[SEASON[i+1]],index=SEASON[i+1])
    obstemps=pd.Series(obstemp[SEASON[i+1]],index=SEASON[i+1])
    obsLon, obsLat = obsData['LON'][SEASON[i+1]], obsData['LAT'][SEASON[i+1]]
    modtemp_i = griddata(np.array(obsLon),np.array(obsLat),np.array(modtemps),lon_i,lat_i)
    obstemp_i = griddata(np.array(obsLon),np.array(obsLat),np.array(obstemps),lon_i,lat_i)  
    ax2 = fig.add_subplot(223)
    draw_basemap(fig, ax2, lonsize, latsize)
    CS = ax2.contourf(lon_i, lat_i, modtemp_i, np.arange(0,30,1), cmap=plt.cm.rainbow,
                  vmax=abs(modtemp_i).max(), vmin=-abs(modtemp_i).max())
    CS1=ax2.contour(lon_is, lat_is,depth_i,1,colors = 'r',linestyles=':',linewidths=2)
    plt.colorbar(CS)
    #plt.scatter(np.array(obsLon),np.array(obsLat), marker='o', c='b', s=5, zorder=10)
    ax2.set_title('mod_'+season[i+1])
    ax2.annotate('100m depth',xy=(-75.289,35.0395),xytext=(-75.0034,34.9842),arrowprops=dict(facecolor='black'))    
    
    ax3 = fig.add_subplot(224)
    draw_basemap(fig, ax3, lonsize, latsize)
    CS = ax3.contourf(lon_i, lat_i, obstemp_i, np.arange(0,30,1), cmap=plt.cm.rainbow,
                  vmax=abs(obstemp_i).max(), vmin=-abs(obstemp_i).max())
    CS1=ax3.contour(lon_is, lat_is,depth_i,1,colors = 'r',linestyles=':',linewidths=2)
    plt.colorbar(CS)
    #plt.scatter(np.array(obsLon),np.array(obsLat), marker='o', c='b', s=5, zorder=10)
    ax3.set_title('obs_'+season[i+1])
    ax3.annotate('100m depth',xy=(-75.289,35.0395),xytext=(-75.0034,34.9842),arrowprops=dict(facecolor='black'))  
    plt.savefig(season[i]+season[i+1]+'contour.png')
plt.show()