# -*- coding: utf-8 -*-
"""
Created on Tue Jan 19 13:47:35 2015

@author: zhaobin
"""
'''
Extract new data file named "06-08_indexANDlayer.csv "with new column "modNearestIndex" and "modDepthLayer"
'''
import pandas as pd
import numpy as np
import netCDF4
from datetime import datetime, timedelta
from turtleModule import str2ndlist, dist
import watertempModule as wtm   # a module that has all classes using ROMS and FVCOm model.
def nearest_point_index2(lon, lat, lons, lats):
    d = dist(lon, lat, lons ,lats)
    min_dist = np.min(d)
    index = np.where(d==min_dist)
    return index
#################################################################################33
obsData = pd.read_csv('06-08_ch.csv', index_col=0)
obsLon = pd.Series(str2ndlist(obsData['lon'],bracket=True))
obsLat = pd.Series(str2ndlist(obsData['lat'],bracket=True))
url='http://tds.marine.rutgers.edu:8080/thredds/dodsC/roms/espresso/2009_da/his'
modData = netCDF4.Dataset(url)
modLons = modData.variables['lon_rho'][:]
modLats = modData.variables['lat_rho'][:]
s_rho = modData.variables['s_rho'][:]
h = modData.variables['h'][:]
indexNotNull = obsLon[obsLon.isnull()==False].index # some obslat and obslon of point are empty, get rid of them.
                                                    # or this line can be the indices of TF which is less.
                                                    # indexTF = np.where(obsData['TF'].notnull())[0]

loc = []
for i in indexNotNull:
    ind = []
    lon = obsLon[i]
    lat = obsLat[i]
    index = nearest_point_index2(lon, lat, modLons, modLats)
    ind.append(index[0][0])
    ind.append(index[1][0])
    loc.append(ind)
loc = pd.Series(loc, index=indexNotNull)
obsData['modNearestIndex'] = loc #add loc to obsData in case want to save it.

obsDepth = pd.Series(str2ndlist(obsData['depth'],bracket=True), index=obsData.index)
layersAll = []
for i in indexNotNull:
    nearest_index = loc[i]
    layers = []
    depthLayers = h[nearest_index[0], nearest_index[1]] * s_rho
    for j in range(len(obsDepth[i])):
        # depthLayers = h[nearest_index[0], nearest_index[1]] * s_rho
        l = np.argmin(abs(depthLayers+obsDepth[i][j])) # obsDepth is positive and depthLayers is negitive. So the index of min sum is the layer
        layers.append(l)
    layersAll.append(layers)
layersAll = pd.Series(layersAll, index=indexNotNull)
obsData['modDepthLayer'] = layersAll
obsData.to_csv('06-08_indexANDlayer.csv')
