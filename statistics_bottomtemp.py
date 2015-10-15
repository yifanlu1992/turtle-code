# -*- coding: utf-8 -*-
"""
Created on Wed Oct 14 13:05:12 2015
If the deepest observation depth is >50m(or <50m, or all), draw the correlation of this observation and appriate model data.
@author: zdong
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import netCDF4
import matplotlib.pyplot as plt
from scipy import stats
from turtleModule import mon_alpha2num, np_datetime, mean_value, bottom_value, index_by_depth,str2ndlist
def show2pic(x1, y1, fontsize,text,tp):
    r_squared=[]
    fig = plt.figure(figsize=[12,12])
    for j in range(len(text)):
        FONTSIZE = fontsize
        x = np.arange(0.0, 30.0, 0.01)
        i = x1[j][x1[j].isnull()==False].index
        fit = np.polyfit(x1[j][i], y1[j][i], 1)
        fit_fn = np.poly1d(fit)
        x2, y2 = x1[j][i], fit_fn(x1[j][i])
        gradient, intercept, r_value, p_value, std_err = stats.linregress(y1[j][i], x1[j][i])
        r_squared.append(r_value**2)
        ax =  fig.add_subplot(len(text),1,j+1)
        nbins = 200
        H, xedges, yedges = np.histogram2d(x1[j][i], y1[j][i], bins=nbins)
        H = np.rot90(H)
        H = np.flipud(H)
        Hmasked = np.ma.masked_where(H==0, H)
        plt.pcolormesh(xedges, yedges, Hmasked,vmin=1,vmax=20)
        if j==2:
            plt.xlabel('Model ($^\circ$C)', fontsize=FONTSIZE)
        if j==1:
            plt.ylabel('Observed ($^\circ$C)', fontsize=FONTSIZE)
        cbar = plt.colorbar(ticks=[1,5,10,15,20])
        if j==1:
            cbar.ax.set_ylabel('Quantity', fontsize=FONTSIZE+5)
        cbar.ax.tick_params(labelsize=20)
        cbar.ax.set_yticks(fontsize=20)
        plt.axis([0, 30, 0, 30])
        plt.xticks(fontsize=20)
        plt.yticks(fontsize=20)
        plt.plot(x, x, 'r-', linewidth=2)
        plt.plot(x2, y2, 'y-', linewidth=2)
        plt.text(x=1,y=27,s=text[j],fontsize=15)
        plt.text(x=1,y=23,s=r'$\mathregular{R^2}$='+str(round(r_squared[j],3)),fontsize=15)
        if j==0:
            plt.title('%s'%tp,fontsize=FONTSIZE)
    plt.savefig('obsVSmodel_%s.png'%tp,dpi=200)
    return r_squared
####################################roms#######################################
FONTSIZE = 25
obs = pd.read_csv('ctdWithModTempByDepth.csv')
tf_index = np.where(obs['TF'].notnull())[0]
obsdepth = pd.Series(obs['MAX_DBAR'][tf_index],index=tf_index)
obstemp = pd.Series(bottom_value(obs['TEMP_VALS'][tf_index]),index=tf_index)
obsdata_roms= pd.DataFrame({'depth':obsdepth, 'temp':obstemp}).sort_index(by='depth')
Temp_roms=pd.Series(str2ndlist(obs['modTempByDepth'][obsdata_roms['temp'].index],bracket=True),index=obsdata_roms['temp'].index)
temp_roms=[]
for i in obsdata_roms['temp'].index:
    if Temp_roms[i][-1]>100:   #get rid of some bad data
        temp_roms.append(obsdata_roms['temp'][i])
    else:
        temp_roms.append(Temp_roms[i][-1])
temp_roms=pd.Series(temp_roms,index=obsdata_roms['temp'].index)
index_roms=index_by_depth(obsdata_roms['depth'], 50)
###################################fvcom#######################################
obs = pd.read_csv('ctdWithdepthofbottom_fvcom.csv')
tf_index = np.where(obs['in FVcom range'].notnull())[0]
obsdepth = pd.Series(obs['MAX_DBAR'][tf_index],index=tf_index)
obstemp = pd.Series(bottom_value(obs['TEMP_VALS'][tf_index]),index=tf_index)
obsdata_fvcom = pd.DataFrame({'depth':obsdepth, 'temp':obstemp}).sort_index(by='depth')
Temp_fvcom =pd.Series(str2ndlist(obs['modtempBYdepth'][obsdata_fvcom['temp'].index],bracket=True),index=obsdata_fvcom['temp'].index)
temp_fvcom =[]
for i in obsdata_fvcom['temp'].index:
    if Temp_fvcom[i][-1]>100:   #get rid of some bad data
        temp_fvcom.append(obsdata_fvcom['temp'][i])
    else:
        temp_fvcom.append(Temp_fvcom[i][-1])
temp_fvcom=pd.Series(temp_fvcom,index=obsdata_fvcom['temp'].index)
index_fvcom=index_by_depth(obsdata_fvcom['depth'], 50)
###################################hycom#######################################
obs = pd.read_csv('ctd_withHYCOMtemp.csv')
tf_index = np.where(obs['TF'].notnull())[0]
obsdepth = pd.Series(obs['MAX_DBAR'][tf_index],index=tf_index)
obstemp = pd.Series(bottom_value(obs['TEMP_VALS'][tf_index]),index=tf_index)
obsdata_hycom= pd.DataFrame({'depth':obsdepth, 'temp':obstemp}).sort_index(by='depth')
Temp_hycom=pd.Series(str2ndlist(obs['modtemp_HYCOM'][obsdata_hycom['temp'].index],bracket=True),index=obsdata_hycom['temp'].index)
temp_hycom=[]
for i in obsdata_hycom['temp'].index:
    if Temp_hycom[i][-1]<-10:   #get rid of some bad data
        temp_hycom.append(obsdata_hycom['temp'][i])
    else:
        temp_hycom.append(Temp_hycom[i][-1])
temp_hycom=pd.Series(temp_hycom,index=obsdata_hycom['temp'].index)
index_hycom=index_by_depth(obsdata_hycom['depth'], 50)
tp='Bottom Temperature'
if tp == 'Bottom Temperature':
    x=[temp_roms,temp_fvcom,temp_hycom]
    y=[obsdata_roms['temp'], obsdata_fvcom['temp'],obsdata_hycom['temp']]
    text=['ROMS','FVCOM','HYCOM']
    r_squared = show2pic(x, y, FONTSIZE,text,tp)   
elif tp == '<50m':
    x=[temp_roms[index_roms[0]],temp_fvcom[index_fvcom[0]],temp_hycom[index_hycom[0]]]
    y=[obsdata_roms['temp'][index_roms[0]], obsdata_fvcom['temp'][index_fvcom[0]],obsdata_hycom['temp'][index_hycom[0]]]
    text=['ROMS','FVCOM','HYCOM']
    r_squared = show2pic(x, y, FONTSIZE,text,tp)
elif tp == '>50m':
    x=[temp_roms[index_roms[1]],temp_fvcom[index_fvcom[1]],temp_hycom[index_hycom[1]]]
    y=[obsdata_roms['temp'][index_roms[1]], obsdata_fvcom['temp'][index_fvcom[1]],obsdata_hycom['temp'][index_hycom[1]]]
    text=['ROMS','FVCOM','HYCOM']
    r_squared = show2pic(x, y, FONTSIZE,text,tp)
plt.show()
