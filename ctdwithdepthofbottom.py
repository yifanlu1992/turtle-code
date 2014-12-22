# -*- coding: utf-8 -*-
"""
Created on Thu Nov 13 16:12:01 2014

@author: zhaobin
"""
import numpy as np
import pandas as pd
from turtleModule import str2ndlist
obsData = pd.read_csv('ctdWithModTempByDepth.csv') 
tf_index = np.where(obsData['TF'].notnull())[0]
modTemp = pd.Series(str2ndlist(obsData['modTempByDepth'][tf_index],bracket=True), index=tf_index) # if str has '[' and ']', bracket should be True
indx=[]
for j in tf_index:
    if modTemp[j][-1]<100:
        indx.append(j)
obs=obsData.ix[indx]
obs=obs.drop(['Unnamed: 0','Unnamed: 0.1'],axis=1)
obs.to_csv('ctdwithoutbad.csv')

obsDepth = pd.Series(str2ndlist(obsData['TEMP_DBAR'][indx]), index=indx)
modLayer = pd.Series(str2ndlist(obsData['modDepthLayer'][indx], bracket=True), index=indx)
obslon,obslat= obsData['LON'],obsData['LAT']
data = pd.DataFrame({'depth':obsDepth,'layer':modLayer,'lon':obslon,'lat':obslat},index=indx)
depth_bottom=[]
j=0
for i in indx:
    d_each=(data['depth'][i][-1]-data['depth'][i][0]) *1.0/((data['layer'][i][0]-data['layer'][i][-1])+0.00000000000000000000001)# except divded by zero 
    if  36*d_each<200:   
        depth_bottom.append(36*d_each)
    else:
        depth_bottom.append(200)
depth_bottom=pd.Series(depth_bottom,index=indx)
obs['depth_bottom']=pd.Series(depth_bottom)
#obs=obs.drop(['Unnamed: 0','Unnamed: 0.1'],axis=1)
obs.to_csv('ctdWithdepthofbottom.csv')