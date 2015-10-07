# -*- coding: utf-8 -*-
"""
Created on Tue Jan 13 13:47:35 2015

@author: zhaobin
"""
'''
Extract new data file named "06-08_depth.csv "with new column "modTempByDepth"
'''
import netCDF4
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import watertempModule as wtm
from turtleModule import str2ndlist, closest_num, np_datetime, bottom_value, dist

def getModTemp(modTempAll, obsTime, modLayer, modNearestIndex, s_rho, waterDepth, starttime, oceantime):
    '''
    Return model temp based on observation layers or depth
    '''
    indx = closest_num((starttime -datetime(2006,1,1)).total_seconds(), oceantime)
    modTemp = []
    l = len(modLayer.index)
    for i in modLayer.index:    # Loop the model location
        '''
        # For layers
        print i, l, 'getModTemp'
        timeIndex = closest_num((obsTime[i]-datetime(2006,01,01)).total_seconds(), oceantime)-ind
        modTempTime = modTempAll[timeIndex]
        modTempTime[modTempTime.mask] = 10000
        t = np.array([modTempTime[modLayer[i][j],modNearestIndex[i][0], modNearestIndex[i][1]] \
                          for j in range(len(modLayer[i]))])
        modTemp.append(t)
        '''
        # For depth
        timeIndex1 = closest_num((obsTime[i]-datetime(2006,01,01)).total_seconds(), oceantime)
        timeIndex = timeIndex1 - indx
        temp = modTempAll[timeIndex]
        temp[temp.mask] = 10000 # Assign the temp of island and land to 10000
        a, b = int(modNearestIndex[i][0]), int(modNearestIndex[i][1]) # index of nearest model node
        t = []
        for depth in obsDepth[i]:
            depth = -depth
            locDepth = waterDepth[a, b]# Get the bottom depth of this location. waterDepth is 'h'
            lyrDepth = s_rho * locDepth# Depth of each layer
            if depth > lyrDepth[-1]: # Obs is shallower than last layer which is the surface.
                Temp = (temp[-2,a,b]-temp[-1,a,b])/(lyrDepth[-2]-lyrDepth[-1]) * \
                    (depth-lyrDepth[-1]) + temp[-1,a,b]
            elif depth < lyrDepth[0]: # Obs is deeper than first layer which is the bottom.
                Temp = (temp[1,a,b]-temp[0,a,b])/(lyrDepth[1]-lyrDepth[0]) * \
                    (depth-lyrDepth[0]) + temp[0,a,b]
            else:
                ind = closest_num(depth, lyrDepth)
                Temp = (temp[ind,a,b]-temp[ind-1,a,b])/(lyrDepth[ind]-lyrDepth[ind-1]) * \
                    (depth-lyrDepth[ind-1]) + temp[ind-1,a,b]
            t.append(Temp)
        modTemp.append(t)
    modTemp = np.array(modTemp)
    return modTemp
#####################################################################################
obsData = pd.read_csv('ship06-08_indexANDlayer.csv')
obsLon = pd.Series(str2ndlist(obsData['lon'],bracket=True))
obsLat = pd.Series(str2ndlist(obsData['lat'],bracket=True))
obsTime = pd.Series(obsData['time'])
obsTemp = pd.Series(str2ndlist(obsData['temperature'],bracket=True))
obsDepth = pd.Series(str2ndlist(obsData['depth'],bracket=True))
modLayer = pd.Series(str2ndlist(obsData['modDepthLayer'],bracket=True))
modNearestIndex = pd.Series(str2ndlist(obsData['modNearestIndex'], bracket=True))
for i in obsTime.index:
    obsTime[i]=datetime.strptime(obsTime[i], "%Y-%m-%d %H:%M:%S")  # change str to datatime
url='http://tds.marine.rutgers.edu:8080/thredds/dodsC/roms/espresso/2009_da/his'
modDataAll = netCDF4.Dataset(url)
oceantime = modDataAll['ocean_time']
modTempAll = modDataAll['temp']
s_rho = modDataAll['s_rho']
waterDepth = modDataAll['h']
modTemp = getModTemp(modTempAll, obsTime, modLayer, modNearestIndex, s_rho, waterDepth, starttime, oceantime)
obsData['modTempByDepth'] = pd.Series(modTemp)
obsData.to_csv('06-08_modeltemp.csv')

shipData = pd.read_csv('06-08_modeltemp.csv')     #remove bracket in 'lat','lon'
shipLat=pd.Series(str2ndlist(shipData['lat'],bracket=True),index=shipData.index)
shipLon=pd.Series(str2ndlist(shipData['lon'],bracket=True),index=shipData.index)
for i in range(len(shipLon)):
    shipLat[i]=shipLat[i][0]
    shipLon[i]=shipLon[i][0]
shipData['LAT']=pd.Series(shipLat)
shipData['LON']=pd.Series(shipLon)
shipData=shipData.drop(['Unnamed: 0','0','lat','lon','Unnamed: 0.1'],axis=1)
shipData.to_csv('ship06-08_MODELtemp.csv')
