# -*- coding: utf-8 -*-
"""
Created on Wed Jan  7 10:49:27 2015

@author: zhaobin
"""
'plot temperature of turtles and shipboard '
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from turtleModule import mon_alpha2num, np_datetime, dist,str2ndlist,colors
###################################################################################
r = 10                          # the obs position that has shipboard position within (r) kilometers might be considered as good data.
day = 3                        # the obs time that has shipboard time within (day) days might be considered as good data.
obsData=pd.read_csv('ctdWithdepthofbottom.csv',index_col=0)
obslat = pd.Series(obsData['LAT'],index=obsData.index)
obslon = pd.Series(obsData['LON'],index=obsData.index)
obstime = pd.Series(np_datetime(obsData['END_DATE']),index=obsData.index)
obsDepth=pd.Series(str2ndlist(obsData['TEMP_DBAR']),index=obsData.index)
obstemp=pd.Series(str2ndlist(obsData['TEMP_VALS']),index=obsData.index)
modtemp=pd.Series(str2ndlist(obsData['modTempByDepth'],bracket=True),index=obsData.index)
shipData=pd.read_csv('06-08_modeltemp.csv',index_col=0)
shiplat=pd.Series(str2ndlist(shipData['lat'],bracket=True),index=shipData.index)
shiplon=pd.Series(str2ndlist(shipData['lon'],bracket=True),index=shipData.index)
shiptime=pd.Series(shipData['time'],index=shipData.index)
shipdepth=pd.Series(str2ndlist(shipData['depth'],bracket=True),index=shipData.index)
shiptemp=pd.Series(str2ndlist(shipData['temperature'],bracket=True),index=shipData.index)
MODtemp=pd.Series(str2ndlist(shipData['modTempByDepth'],bracket=True),index=shipData.index)
for i in range(len(shiptime)):
    shiptime[i]=datetime.strptime(shiptime[i], "%Y-%m-%d %H:%M:%S")  # change str to datatime

index = []     #index of turtle
indx=[]        #index of shipboard 
for i in obsData.index:
    for j in shipData.index:
        l = dist(obslon[i], obslat[i],shiplon[j],shiplat[j])
        if l<r:
            print l        #distance
            maxtime = obstime[i]+timedelta(days=day)
            mintime = obstime[i]-timedelta(days=day)
            mx = shiptime[j]<maxtime
            mn = shiptime[j]>mintime
            TF = mx*mn  
            if TF==1:      #time
                index.append(i)
                indx.append(j)
print index,indx

INDX=pd.Series(indx).unique()      #
color=['blue','green','black','grey','orange','cyan','yellow','red','blue','green','black','grey','orange','cyan','yellow','red']
Mean_turtle,Mean_model,Rms_turtle,Rms_model=[],[],[],[]
for i in range(len(INDX)):
    q=0          #plot different color
    diff_turtle=[]
    fig=plt.figure()
    for j in range(len(indx)):
        if indx[j]==INDX[i]:
            for k in range(len(obsDepth[index[j]])):
                for m in range(len(shipdepth[INDX[i]])):
                    if obsDepth[index[j]][k]==shipdepth[INDX[i]][m]:
                        dif=obstemp[index[j]][k]-shiptemp[INDX[i]][m]
                        diff_turtle.append(dif)
            '''
            plt.plot(obstemp[index[j]],obsDepth[index[j]],color=color[q] ,linewidth=2)
            plt.plot(modtemp[index[j]],obsDepth[index[j]],color=color[q] ,linewidth=2,linestyle='--')
            '''
            plt.plot(obstemp[index[j]],obsDepth[index[j]],color=color[q] ,linewidth=2,label='tur'+str(index[j]))
            plt.plot(modtemp[index[j]],obsDepth[index[j]],color=color[q] ,linewidth=2,linestyle='--',label='mod'+str(index[j]))
            q+=1
    '''    
    plt.plot(shiptemp[INDX[i]],shipdepth[INDX[i]],color=color[-1] ,linewidth=6)
    plt.plot(MODtemp[INDX[i]],shipdepth[INDX[i]],color=color[-1] ,linewidth=6,linestyle='--')
    '''    
    plt.plot(shiptemp[INDX[i]],shipdepth[INDX[i]],color=color[-1] ,linewidth=6,label='ship'+str(INDX[i]))
    plt.plot(MODtemp[INDX[i]],shipdepth[INDX[i]],color=color[-1] ,linewidth=6,linestyle='--',label='mod'+str(INDX[i]))
    plt.legend(loc='best')
    
    diff_model=np.array(shiptemp[INDX[i]])-np.array(MODtemp[INDX[i]])
    mean_turtle=np.mean(np.array(diff_turtle))
    mean_model=np.mean(diff_model)
    rms_turtle=np.sqrt(np.sum(np.array(diff_turtle)*np.array(diff_turtle))/len(np.array(diff_turtle)))
    rms_model=np.sqrt(np.sum(diff_model*diff_model)/len(diff_model))
    Mean_turtle.append(mean_turtle)
    Mean_model.append(mean_model)
    Rms_turtle.append(rms_turtle)
    Rms_model.append(rms_model)
    plt.ylabel('depth(m)',fontsize=20)
    plt.xlabel('temperature(degC)',fontsize=20)
    plt.xlim([0,30])
    plt.ylim([max(shipdepth[INDX[i]])+1,0])
    plt.xticks(np.arange(0,30,5),fontsize=25)
    plt.yticks(np.arange(max(shipdepth[INDX[i]])+1,0,-5),fontsize=25)
    plt.text(1,min(shipdepth[INDX[i]])+2,'mean ship-turtle temp:'+str(round(mean_turtle,2)),fontsize=25)
    plt.text(1,min(shipdepth[INDX[i]])+4,'mean ship-model temp:'+str(round(mean_model,2)),fontsize=25)
    plt.text(1,min(shipdepth[INDX[i]])+6,'RMS ship-turtle:'+str(round(rms_turtle,2)),fontsize=25)
    plt.text(1,min(shipdepth[INDX[i]])+8,'RMS ship-model:'+str(round(rms_model,2)),fontsize=25)
    plt.title('ship vs turtle vs model profiles',fontsize=25)
    plt.savefig('turtlesVSshipboard'+str(INDX[i])+'.png')
plt.show()