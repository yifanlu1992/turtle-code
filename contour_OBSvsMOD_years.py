# -*- coding: utf-8 -*-
"""
Created on Fri Dec 19 13:29:10 2014

@author: zhaobin
"""
'plot observe temperature of different years` summer and fall'
from matplotlib.mlab import griddata
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from turtleModule import np_datetime,str2ndlist,draw_basemap
###########################################################
lonsize = [-79.5, -72.5]
latsize = [34.5, 41]                # range of basemap

obsData = pd.read_csv('ctdWithdepthofbottom_roms.csv')
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

obstemp=[]
for i in index_inside:    
    obstemp.append(obsTemp[i][-1])          #just need temperature in the bottom
obstemp=pd.Series(obstemp,index=index_inside)
data = pd.DataFrame({'lon':obsLon,'lat':obsLat,'time':obsTime,'obstemp':obstemp},index=index_inside)
summer = [[],[],[],[],[]]
fall = [[],[],[],[],[]]
for i in index_inside:
    if data['time'][i].year==2009:
        if 5<data['time'][i].month<9:
            summer[0].append(i)
        if 8<data['time'][i].month<12:
            fall[0].append(i)
    if data['time'][i].year==2010:
        if 5<data['time'][i].month<9:
            summer[1].append(i)
        if 8<data['time'][i].month<12:
            fall[1].append(i)
    if data['time'][i].year==2011:
        if 5<data['time'][i].month<9:
            summer[2].append(i)
        if 8<data['time'][i].month<12:
            fall[2].append(i)
    if data['time'][i].year==2012:
        if 5<data['time'][i].month<9:
            summer[3].append(i)
        if 8<data['time'][i].month<12:
            fall[3].append(i)
    if data['time'][i].year==2013:
        if 5<data['time'][i].month<9:
            summer[4].append(i)
        if 8<data['time'][i].month<12:
            fall[4].append(i)
lon_i = np.linspace(lonsize[0],lonsize[1],1000)
lat_i = np.linspace(latsize[0],latsize[1],1000)                #use for mean error,absolute mean error and rms
lon_is = np.linspace(lonsize[0],lonsize[1],100)
lat_is = np.linspace(latsize[0],latsize[1],100)                #use for depth line
depth_i = griddata(np.array(obsLons),np.array(obsLats),np.array(depthBottom),lon_is,lat_is,interp='linear')   #use for plotting 100m depth line.
obstemp_i=[[[],[],[],[],[]],[[],[],[],[],[]]]

for i in range(len(summer)):
    obstemp_i[0][i]=griddata(np.array(data['lon'][summer[i]]),np.array(data['lat'][summer[i]]),np.array(data['obstemp'][summer[i]]),lon_i,lat_i,interp='linear')
    obstemp_i[1][i]=griddata(np.array(data['lon'][fall[i]]),np.array(data['lat'][fall[i]]),np.array(data['obstemp'][fall[i]]),lon_i,lat_i,interp='linear')
    fig = plt.figure()
    ax = fig.add_subplot(121)
    draw_basemap(fig, ax, lonsize, latsize)
    CS = plt.contourf(lon_i, lat_i, obstemp_i[0][i], np.arange(0,30,1), cmap=plt.cm.rainbow,
                  vmax=30, vmin=0)
    cbar=plt.colorbar(CS)
    cbar.ax.tick_params(labelsize=20)
    cbar.ax.set_ylabel('Temperature($^\circ$C)', fontsize=20)
    CS1=ax.contour(lon_is, lat_is,depth_i,1,colors = 'r',linestyles=':',linewidths=2)
    ax.annotate('100m depth',xy=(-75.289,35.0395),xytext=(-75.0034,34.9842),arrowprops=dict(facecolor='black'))
    #plt.scatter(np.array(data['lon'][summer[i]]),np.array(data['lat'][summer[i]]), marker='o', c='b', s=5, zorder=10)
    ax.set_title('Summer_'+str(i+2009),fontsize=20)
    
    ax = fig.add_subplot(122)
    draw_basemap(fig, ax, lonsize, latsize)
    CS = plt.contourf(lon_i, lat_i, obstemp_i[1][i], np.arange(0,30,1), cmap=plt.cm.rainbow,
                  vmax=30, vmin=0)
    cbar=plt.colorbar(CS)
    cbar.ax.tick_params(labelsize=20)
    cbar.ax.set_ylabel('Temperature($^\circ$C)', fontsize=20)
    CS1=ax.contour(lon_is, lat_is,depth_i,1,colors = 'r',linestyles=':',linewidths=2)
    ax.annotate('100m depth',xy=(-75.289,35.0395),xytext=(-75.0034,34.9842),arrowprops=dict(facecolor='black'))
    #plt.scatter(np.array(data['lon'][fall[i]]),np.array(data['lat'][fall[i]]), marker='o', c='b', s=5, zorder=10)
    ax.set_title('Fall_'+str(i+2009),fontsize=20)
    plt.savefig('summer_fall'+str(i+2009))
plt.show()
