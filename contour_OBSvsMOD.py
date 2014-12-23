# -*- coding: utf-8 -*-
"""
Created on Thu Nov 20 10:57:43 2014

@author: zhaobin
"""
'plot contour of observe and model temperature in the bottom'
from matplotlib.mlab import griddata
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from turtleModule import str2ndlist,draw_basemap,whichArea
##############################main code########################################
lonsize = [-79.5, -72.5]
latsize = [34.5, 41]                # range of basemap

obsData = pd.read_csv('ctdWithdepthofbottom.csv')
modTemp = pd.Series(str2ndlist(obsData['modTempByDepth'],bracket=True), index=obsData.index) # if str has '[' and ']', bracket should be True
obsTemp = pd.Series(str2ndlist(obsData['TEMP_VALS']), index=obsData.index)
obsDepth = pd.Series(str2ndlist(obsData['TEMP_DBAR']), index=obsData.index)
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
lon_i = np.linspace(lonsize[0],lonsize[1],1000)
lat_i = np.linspace(latsize[0],latsize[1],1000)     #use for mean error,absolute mean error and rms
lon_is = np.linspace(lonsize[0],lonsize[1],100)
lat_is = np.linspace(latsize[0],latsize[1],100)     #use for depth line
modtemp_i = griddata(np.array(obsLon),np.array(obsLat),np.array(modtemp),lon_i,lat_i)
obstemp_i = griddata(np.array(obsLon),np.array(obsLat),np.array(obstemp),lon_i,lat_i)
depth_i = griddata(np.array(obsLons),np.array(obsLats),np.array(depthBottom),lon_is,lat_is)
temp_i=[modtemp_i,obstemp_i]
title=['modtemp','obstemp']
for k in range(len(temp_i)):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    draw_basemap(fig, ax, lonsize, latsize)
    CS = plt.contourf(lon_i, lat_i, temp_i[k], np.arange(0,30,1), cmap=plt.cm.rainbow,
                  vmax=abs(temp_i[k]).max(), vmin=-abs(temp_i[k]).max())
    CS1=plt.contour(lon_is, lat_is,depth_i,1,colors = 'r',linestyles=':')
    plt.colorbar(CS)
    #plt.scatter(np.array(obsLon),np.array(obsLat), marker='o', c='b', s=5, zorder=10)
    ax.set_title(title[k],fontsize=30)
    ax.annotate('100m depth',xy=(-75.289,35.0395),xytext=(-75.0034,34.9842),arrowprops=dict(facecolor='black'))
    plt.savefig('contour_'+title[k]+'.png')
plt.show()