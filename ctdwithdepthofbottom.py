# -*- coding: utf-8 -*-
"""
Created on Thu Nov 13 16:12:01 2014
output two files:ctdwithoutbad_roms.csv and ctdWithdepthofbottom_roms.csv
@author: zhaobin
"""
from matplotlib.mlab import griddata
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import netCDF4
from datetime import datetime, timedelta
import math
from turtleModule import str2ndlist,draw_basemap
import watertempModule as wtm  
############################################################################################
obsData = pd.read_csv('ctdWithModTempByDepth.csv') 
tf_index = np.where(obsData['TF'].notnull())[0]
modTemp = pd.Series(str2ndlist(obsData['modTempByDepth'][tf_index],bracket=True), index=tf_index) # if str has '[' and ']', bracket should be True
indx=[]
for j in tf_index:
    if modTemp[j][-1]<100:
        indx.append(j)
obs=obsData.ix[indx]
obs=obs.drop(['Unnamed: 0','Unnamed: 0.1'],axis=1)
obs.to_csv('ctdwithoutbad_roms.csv')
###############################################################################
starttime = datetime(2013,07,10) # starttime and endtime can be any time that included by model, we just want a url to get "lon_rho", "lat_rho","h"in model.
endtime = starttime + timedelta(hours=1)
tempObj = wtm.water_roms()
url = tempObj.get_url(starttime, endtime)
modData = netCDF4.Dataset(url)
modLons = modData.variables['lon_rho'][:]
modLats = modData.variables['lat_rho'][:]
moddepth = modData.variables['h'][:]

modNearestIndex = pd.Series(str2ndlist(obsData['modNearestIndex'][indx], bracket=True), index=indx) # if str has '[' and ']', bracket should be True

newH=[]
for i in indx:
    m, n = int(modNearestIndex[i][0]), int(modNearestIndex[i][1])
    newH.append(moddepth[m][n])
obs['depth_bottom']=pd.Series(newH,index=indx)
obs.to_csv('ctdWithdepthofbottom_roms.csv')
#obs=obs.drop(['Unnamed: 0','Unnamed: 0.1'],axis=1)
