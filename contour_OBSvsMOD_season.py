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
latsize = [34.5, 41]                # range of basemap
obsData = pd.read_csv('ctdWithdepthofbottom_roms.csv')
modTemp = pd.Series(str2ndlist(obsData['modTempByDepth'],bracket=True), index=obsData.index) # if str has '[' and ']', bracket should be True
obsTemp = pd.Series(str2ndlist(obsData['TEMP_VALS']), index=obsData.index)
obsDepth = pd.Series(str2ndlist(obsData['TEMP_DBAR']), index=obsData.index)
obsTime = pd.Series(np_datetime(obsData['END_DATE']),index=obsData.index)
depthBottom = pd.Series(obsData['depth_bottom'],index=obsData.index)
for i in obsData.index:
    if depthBottom[i]>200:
        depthBottom[i]=200     #Just a little points are deeper than 200m.Removing them can plot depth betterex)
obsLons, obsLats = obsData['LON'], obsData['LAT']
index_inside=[]
for i in obsLons.index:
    if lonsize[0]<obsLons[i]<lonsize[1]:
        if abs(obsDepth[i][-1]-depthBottom[i])<10:     #diff<10m,wo can use the data
            index_inside.append(i)                    #Just use data in this area.
obsLon, obsLat = obsData['LON'][index_inside], obsData['LAT'][index_inside]

modtemp=[]
obstemp=[]
for i in index_inside:
    modtemp.append(modTemp[i][-1])
    obstemp.append(obsTemp[i][-1])   #just need temperature in the bottom
modtemp=pd.Series(modtemp,index=index_inside)
obstemp=pd.Series(obstemp,index=index_inside)
SPRING=[]
SUMMER=[]
FALL=[]
WINTER=[]
YEAR=[]
for i in index_inside:
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
lat_i = np.linspace(latsize[0],latsize[1],1000)                #use for mean error,absolute mean error and rms
lon_is = np.linspace(lonsize[0],lonsize[1],100)
lat_is = np.linspace(latsize[0],latsize[1],100)                #use for depth line
depth_i = griddata(np.array(obsLons),np.array(obsLats),np.array(depthBottom),lon_is,lat_is,interp='linear')   #use for plotting 100m depth line.
for i in [0,2]:        #two seasons together plot.
    modtemps=pd.Series(modtemp[SEASON[i]],index=SEASON[i])
    obstemps=pd.Series(obstemp[SEASON[i]],index=SEASON[i])
    print(str(len(modtemps)))
    obsLon, obsLat = obsData['LON'][SEASON[i]], obsData['LAT'][SEASON[i]]
    modtemp_i = griddata(np.array(obsLon),np.array(obsLat),np.array(modtemps),lon_i,lat_i,interp='linear')
    obstemp_i = griddata(np.array(obsLon),np.array(obsLat),np.array(obstemps),lon_i,lat_i,interp='linear')  
    fig = plt.figure()
    ax = fig.add_subplot(221)              #plot model temperature 
    draw_basemap(fig, ax, lonsize, latsize)
    CS = ax.contourf(lon_i, lat_i, modtemp_i, np.arange(modtemp_i.min(),modtemp_i.max(),0.1), cmap=plt.cm.rainbow,
                  vmax=modtemp_i.max(), vmin=modtemp_i.min())
    CS1=ax.contour(lon_is, lat_is,depth_i,1,colors = 'r',linestyles=':',linewidths=2)
    plt.colorbar(CS,ticks=np.arange(int(modtemp_i.min())-1,int(modtemp_i.max())+1,2))
    #plt.scatter(np.array(obsLon),np.array(obsLat), marker='o', c='b', s=5, zorder=10)
    ax.set_title('Model_'+season[i])
    ax.annotate('100m depth',xy=(-75.289,35.0395),xytext=(-75.0034,34.9842),arrowprops=dict(facecolor='black'))    
    
    ax1 = fig.add_subplot(222)             #plot model temperature
    draw_basemap(fig, ax1, lonsize, latsize)
    CS = ax1.contourf(lon_i, lat_i, obstemp_i, np.arange(obstemp_i.min(),obstemp_i.max(),0.1), cmap=plt.cm.rainbow,
                  vmax=obstemp_i.max(), vmin=obstemp_i.min())
    CS1=ax1.contour(lon_is, lat_is,depth_i,1,colors = 'r',linestyles=':',linewidths=2)
    plt.colorbar(CS,ticks=np.arange(int(obstemp_i.min())-1,int(obstemp_i.max())+1,2))
    #plt.scatter(np.array(obsLon),np.array(obsLat), marker='o', c='b', s=5, zorder=10)
    ax1.set_title('Observation_'+season[i])
    ax1.annotate('100m depth',xy=(-75.289,35.0395),xytext=(-75.0034,34.9842),arrowprops=dict(facecolor='black'))  

    
    modtemps=pd.Series(modtemp[SEASON[i+1]],index=SEASON[i+1])
    obstemps=pd.Series(obstemp[SEASON[i+1]],index=SEASON[i+1])
    obsLon, obsLat = obsData['LON'][SEASON[i+1]], obsData['LAT'][SEASON[i+1]]
    modtemp_i = griddata(np.array(obsLon),np.array(obsLat),np.array(modtemps),lon_i,lat_i,interp='linear')
    obstemp_i = griddata(np.array(obsLon),np.array(obsLat),np.array(obstemps),lon_i,lat_i,interp='linear')  
    ax2 = fig.add_subplot(223)                 #plot model temperature
    draw_basemap(fig, ax2, lonsize, latsize)
    CS = ax2.contourf(lon_i, lat_i, modtemp_i, np.arange(modtemp_i.min(),modtemp_i.max(),0.1), cmap=plt.cm.rainbow,
                  vmax=modtemp_i.max(), vmin=modtemp_i.min())
    CS1=ax2.contour(lon_is, lat_is,depth_i,1,colors = 'r',linestyles=':',linewidths=2)
    plt.colorbar(CS,ticks=np.arange(int(modtemp_i.min())-1,int(modtemp_i.max())+1,2))
    #plt.scatter(np.array(obsLon),np.array(obsLat), marker='o', c='b', s=5, zorder=10)
    ax2.set_title('Model_'+season[i+1])
    ax2.annotate('100m depth',xy=(-75.289,35.0395),xytext=(-75.0034,34.9842),arrowprops=dict(facecolor='black'))    
    
    ax3 = fig.add_subplot(224)                #plot model temperature
    draw_basemap(fig, ax3, lonsize, latsize)
    CS = ax3.contourf(lon_i, lat_i, obstemp_i, np.arange(obstemp_i.min(),obstemp_i.max(),0.1), cmap=plt.cm.rainbow,
                  vmax=obstemp_i.max(), vmin=obstemp_i.min())
    CS1=ax3.contour(lon_is, lat_is,depth_i,1,colors = 'r',linestyles=':',linewidths=2)
    plt.colorbar(CS,ticks=np.arange(int(obstemp_i.min())-1,int(obstemp_i.max())+1,2))
    #plt.scatter(np.array(obsLon),np.array(obsLat), marker='o', c='b', s=5, zorder=10)
    ax3.set_title('Observation_'+season[i+1])
    ax3.annotate('100m depth',xy=(-75.289,35.0395),xytext=(-75.0034,34.9842),arrowprops=dict(facecolor='black'))  
    plt.savefig(season[i]+season[i+1]+'contour.png')
plt.show()
