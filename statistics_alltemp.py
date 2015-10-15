'''
draw the correlation of observation and model between deep and shallow(50m)'
'''
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from scipy import stats
import netCDF4
from turtleModule import str2ndlist, np_datetime, bottom_value, closest_num
def histogramPoints(x, y, bins):
    H, xedges, yedges = np.histogram2d(x, y, bins=bins)
    H = np.rot90(H)
    H = np.flipud(H)
    Hmasked = np.ma.masked_where(H==0, H)
    return xedges, yedges, Hmasked
    
def show2pic(rng,tempobs, tempmod,fontsize,text,number):
    n = np.arange(0, 30, 0.01)
    for i in range(len(rng)):
        fig = plt.figure(figsize=[12,12])
        for j in range(len(text)):
            print(i,j)
            ax = fig.add_subplot(len(text),1,j+1)
            tempObs=tempobs[i][j]
            tempMod=tempmod[i][j]
            x, y ,Hmasked = histogramPoints(tempObs, tempMod, 200)
            c = ax.pcolormesh(x, y, Hmasked,vmin=number[i][0],vmax=number[i][1])
            ax.plot(n, n, 'r-')
            fit = np.polyfit(tempObs, tempMod, 1)
            fit_fn = np.poly1d(fit)
            ax.plot(tempObs, fit_fn(tempObs), 'y-', linewidth=2)
            gradient, intercept, r_value, p_value, std_err = stats.linregress(tempObs, tempMod)
            r_squared=r_value**2
            if j==0:
                ax.set_title('%s' %rng[i], fontsize=FONTSIZE)
            if j==2:
                ax.set_xlabel('Observed temperature($^\circ$C)', fontsize=FONTSIZE)
            if j==1:
                ax.set_ylabel('Model temperature($^\circ$C)', fontsize=FONTSIZE)
            plt.xticks(fontsize=20)
            plt.yticks(fontsize=20)
            cbar = plt.colorbar(c)
            if j==1:
                cbar.ax.set_ylabel('Quantity', fontsize=FONTSIZE)
            cbar.ax.tick_params(labelsize=20)
            plt.text(x=1,y=27,s=text[j],fontsize=15)
            plt.text(x=1,y=23,s=r'$\mathregular{R^2}$='+str(round(r_squared,3)),fontsize=15)
        plt.savefig('obsVSmodelDeepShallow'+str(i)+'.png', dpi=200)
#########################################MAIN CODE#####################################################################################################
FONTSIZE = 25
##################################roms#########################################
obs = pd.read_csv('ctdWithModTempByDepth.csv') 
tf_index = np.where(obs['TF'].notnull())[0]    # Get the index of good data.
obsTemp = pd.Series(str2ndlist(obs['TEMP_VALS'][tf_index]), index=tf_index)
obsDepth = pd.Series(str2ndlist(obs['TEMP_DBAR'][tf_index]), index=tf_index)
tempMod = pd.Series(str2ndlist(obs['modTempByDepth'][tf_index],bracket=True), index=tf_index)
tempObs1_roms, tempObs2_roms, tempObs3_roms, tempObs4_roms, tempObs5_roms, tempObs6_roms = [],[],[],[],[],[]
tempMod1_roms, tempMod2_roms, tempMod3_roms, tempMod4_roms, tempMod5_roms, tempMod6_roms = [],[],[],[],[],[]
for i in range(len(obsTemp.values)):
    for j in range(len(obsDepth.values[i])):
        d = obsDepth.values[i][j]
        if tempMod.values[i][j] > 100: continue
        if d<25.0:
            tempObs1_roms.append(obsTemp.values[i][j])
            tempMod1_roms.append(tempMod.values[i][j])
        if d>=25.0 and d<50.0:
            tempObs2_roms.append(obsTemp.values[i][j])
            tempMod2_roms.append(tempMod.values[i][j])
        if d>=50.0 and d<75:
            tempObs3_roms.append(obsTemp.values[i][j])
            tempMod3_roms.append(tempMod.values[i][j])
        if d>=75.0:
            tempObs4_roms.append(obsTemp.values[i][j])
            tempMod4_roms.append(tempMod.values[i][j])
        if d>0:
            tempObs5_roms.append(obsTemp.values[i][j])
            tempMod5_roms.append(tempMod.values[i][j])
        if d<50:
            tempObs6_roms.append(obsTemp.values[i][j])
            tempMod6_roms.append(tempMod.values[i][j])
##################################fvcom########################################
obs = pd.read_csv('ctdWithdepthofbottom_fvcom.csv') 
tf_index = np.where(obs['in FVcom range'].notnull())[0]    # Get the index of good data.
obsTemp = pd.Series(str2ndlist(obs['TEMP_VALS'][tf_index]), index=tf_index)
obsDepth = pd.Series(str2ndlist(obs['TEMP_DBAR'][tf_index]), index=tf_index)
tempMod = pd.Series(str2ndlist(obs['modtempBYdepth'][tf_index],bracket=True), index=tf_index)
tempObs1_fvcom, tempObs2_fvcom, tempObs3_fvcom, tempObs4_fvcom, tempObs5_fvcom, tempObs6_fvcom = [],[],[],[],[],[]
tempMod1_fvcom, tempMod2_fvcom, tempMod3_fvcom, tempMod4_fvcom, tempMod5_fvcom, tempMod6_fvcom = [],[],[],[],[],[]
for i in range(len(obsTemp.values)):
    for j in range(len(obsDepth.values[i])):
        d = obsDepth.values[i][j]
        if tempMod.values[i][j] > 100: continue
        if d<25.0:
            tempObs1_fvcom.append(obsTemp.values[i][j])
            tempMod1_fvcom.append(tempMod.values[i][j])
        if d>=25.0 and d<50.0:
            tempObs2_fvcom.append(obsTemp.values[i][j])
            tempMod2_fvcom.append(tempMod.values[i][j])
        if d>=50.0 and d<75:
            tempObs3_fvcom.append(obsTemp.values[i][j])
            tempMod3_fvcom.append(tempMod.values[i][j])
        if d>=75.0:
            tempObs4_fvcom.append(obsTemp.values[i][j])
            tempMod4_fvcom.append(tempMod.values[i][j])
        if d>0:
            tempObs5_fvcom.append(obsTemp.values[i][j])
            tempMod5_fvcom.append(tempMod.values[i][j])
        if d<50:
            tempObs6_fvcom.append(obsTemp.values[i][j])
            tempMod6_fvcom.append(tempMod.values[i][j])
##################################hycom########################################
obs = pd.read_csv('ctd_withHYCOMtemp.csv') 
tf_index = np.where(obs['TF'].notnull())[0]    # Get the index of good data.
obsTemp = pd.Series(str2ndlist(obs['TEMP_VALS'][tf_index]), index=tf_index)
obsDepth = pd.Series(str2ndlist(obs['TEMP_DBAR'][tf_index]), index=tf_index)
tempMod = pd.Series(str2ndlist(obs['modtemp_HYCOM'][tf_index],bracket=True), index=tf_index)
tempObs1_hycom, tempObs2_hycom, tempObs3_hycom, tempObs4_hycom, tempObs5_hycom, tempObs6_hycom = [],[],[],[],[],[]
tempMod1_hycom, tempMod2_hycom, tempMod3_hycom, tempMod4_hycom, tempMod5_hycom, tempMod6_hycom = [],[],[],[],[],[]
for i in range(len(obsTemp.values)):
    for j in range(len(obsDepth.values[i])):
        d = obsDepth.values[i][j]
        if tempMod.values[i][j] < -10: continue
        if d<25.0:
            tempObs1_hycom.append(obsTemp.values[i][j])
            tempMod1_hycom.append(tempMod.values[i][j])
        if d>=25.0 and d<50.0:
            tempObs2_hycom.append(obsTemp.values[i][j])
            tempMod2_hycom.append(tempMod.values[i][j])
        if d>=50.0 and d<75:
            tempObs3_hycom.append(obsTemp.values[i][j])
            tempMod3_hycom.append(tempMod.values[i][j])
        if d>=75.0:
            tempObs4_hycom.append(obsTemp.values[i][j])
            tempMod4_hycom.append(tempMod.values[i][j])
        if d>0:
            tempObs5_hycom.append(obsTemp.values[i][j])
            tempMod5_hycom.append(tempMod.values[i][j])
        if d<50:
            tempObs6_hycom.append(obsTemp.values[i][j])
            tempMod6_hycom.append(tempMod.values[i][j])
tempObs=[[tempObs1_roms,tempObs1_fvcom,tempObs1_hycom],
         [tempObs2_roms,tempObs2_fvcom,tempObs2_hycom],
         [tempObs3_roms,tempObs3_fvcom,tempObs3_hycom],
         [tempObs4_roms,tempObs4_fvcom,tempObs4_hycom],
         [tempObs5_roms,tempObs5_fvcom,tempObs5_hycom],
         [tempObs6_roms,tempObs6_fvcom,tempObs6_hycom]]
tempMod=[[tempMod1_roms,tempMod1_fvcom,tempMod1_hycom],
         [tempMod2_roms,tempMod2_fvcom,tempMod2_hycom],
         [tempMod3_roms,tempMod3_fvcom,tempMod3_hycom],
         [tempMod4_roms,tempMod4_fvcom,tempMod4_hycom],
         [tempMod5_roms,tempMod5_fvcom,tempMod5_hycom],
         [tempMod6_roms,tempMod6_fvcom,tempMod6_hycom]]
rng = ['25.0', '25.0~50.0', '50.0~75.0', '75.0','Using the entire profiles','<50']
number=[[0,200],[0,25],[0,12],[0,5],[0,200],[0,200]]
text=['ROMS','FVCOM','HYCOM']
show2pic(rng,tempObs,tempMod,FONTSIZE,text,number)
plt.show()
