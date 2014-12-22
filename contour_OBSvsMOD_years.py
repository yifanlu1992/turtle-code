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

obsData = pd.read_csv('ctdWithModTempByDepth.csv')
tf_index = np.where(obsData['TF'].notnull())[0]
obsLon = pd.Series(obsData['LON'][tf_index], index=tf_index)
index_inside=[]
for i in tf_index:
    if lonsize[0]<obsLon[i]<lonsize[1]:
        index_inside.append(i)
obsTemp = pd.Series(str2ndlist(obsData['TEMP_VALS'][index_inside]), index=index_inside)
obsDepth = pd.Series(str2ndlist(obsData['TEMP_DBAR'][index_inside]), index=index_inside)
modLayer = pd.Series(str2ndlist(obsData['modDepthLayer'][index_inside], bracket=True), index=index_inside)
obsLon = pd.Series(obsData['LON'][index_inside], index=index_inside) 
obsLat = pd.Series(obsData['LAT'][index_inside], index=index_inside)
indx=[]
obstemp=[]
for i in obsTemp.index:
    d_each=(obsDepth[i][-1]-obsDepth[i][0]) *1.0/((modLayer[i][0]-modLayer[i][-1])+0.00000000000000000000001)# except divded by zero 
    if 36*d_each-obsDepth[i][-1]<10:
        indx.append(i)
        obstemp.append(obsTemp[i][-1])
Obstemp = pd.Series(obstemp,index=indx)
obsLon = pd.Series(obsData['LON'][indx], index=indx) 
obsLat = pd.Series(obsData['LAT'][indx], index=indx)
obsTime = pd.Series(np_datetime(obsData['END_DATE'][indx]), index=indx)
data = pd.DataFrame({'lon':obsLon,'lat':obsLat,'time':obsTime,'obstemp':Obstemp},index=indx)
summer = [[],[],[],[],[]]
fall = [[],[],[],[],[]]
for i in indx:
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
lat_i = np.linspace(latsize[0],latsize[1],1000)
obstemp_i=[[[],[],[],[],[]],[[],[],[],[],[]]]

for i in range(len(summer)):
    obstemp_i[0][i]=griddata(np.array(data['lon'][summer[i]]),np.array(data['lat'][summer[i]]),np.array(data['obstemp'][summer[i]]),lon_i,lat_i)
    obstemp_i[1][i]=griddata(np.array(data['lon'][fall[i]]),np.array(data['lat'][fall[i]]),np.array(data['obstemp'][fall[i]]),lon_i,lat_i)
    fig = plt.figure()
    ax = fig.add_subplot(121)
    draw_basemap(fig, ax, lonsize, latsize)
    CS = plt.contourf(lon_i, lat_i, obstemp_i[0][i], np.arange(0,30,2), cmap=plt.cm.rainbow,
                  vmax=abs(obstemp_i[0][i]).max(), vmin=-abs(obstemp_i[0][i]).max())
    plt.colorbar(CS)
    #plt.scatter(np.array(data['lon'][summer[i]]),np.array(data['lat'][summer[i]]), marker='o', c='b', s=5, zorder=10)
    ax.set_title('summer_'+str(i+2009),fontsize=20)
    
    ax = fig.add_subplot(122)
    draw_basemap(fig, ax, lonsize, latsize)
    CS = plt.contourf(lon_i, lat_i, obstemp_i[1][i], np.arange(0,30,2), cmap=plt.cm.rainbow,
                  vmax=abs(obstemp_i[1][i]).max(), vmin=-abs(obstemp_i[1][i]).max())
    plt.colorbar(CS)
    #plt.scatter(np.array(data['lon'][fall[i]]),np.array(data['lat'][fall[i]]), marker='o', c='b', s=5, zorder=10)
    ax.set_title('fall_'+str(i+2009),fontsize=20)
    plt.savefig('summer_fall'+str(i+2009))
plt.show()
