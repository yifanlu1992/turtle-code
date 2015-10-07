# -*- coding: utf-8 -*-
"""
Created on Thu Aug 20 11:11:18 2015
creat ctdWithdepthofbottom_fvcom.csv with FVCOM depth
@author: zdong
"""

import numpy as np
import pandas as pd
from turtleModule import str2ndlist,np_datetime,dist
import netCDF4
##########################################################
url="http://www.smast.umassd.edu:8080/thredds/dodsC/fvcom/hindcasts/30yr_gom3"
nc=netCDF4.Dataset(url)
lat=nc.variables['lat'][:]
lon=nc.variables['lon'][:]
h=nc.variables['h'][:]
obsData = pd.read_csv('ctd_FVcom_temp.csv')
tf_index = np.where(obsData['in FVcom range'].notnull())[0]
obsLon, obsLat = obsData['LON'][tf_index], obsData['LAT'][tf_index]
depth=[]
for i in tf_index:
    nearest_dist=np.argmin(dist(obsLon[i],obsLat[i],lon,lat))
    depth.append(h[nearest_dist])
obsData['depth_of_bottom_fvcom']=pd.Series(depth,index=tf_index)
obsData.to_csv('ctdWithdepthofbottom_fvcom.csv')
