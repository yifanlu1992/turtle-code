# -*- coding: utf-8 -*-
"""
Created on Thu Feb 19 12:06:47 2015

@author: zhobin
"""
'compare temperature before and after a storm'
import numpy as np
import pandas as pd
import matplotlib as mpl
from datetime import datetime,timedelta
import matplotlib.pyplot as plt
from turtleModule import str2ndlist,dist,np_datetime
##################################################################
obsData=pd.read_csv('ctdwithoutbad_roms.csv',index_col=0)
turtle_id=pd.Series(obsData['PTT'],index=obsData.index)
obslat = pd.Series(obsData['LAT'],index=obsData.index)
obslon = pd.Series(obsData['LON'],index=obsData.index)
obstime = pd.Series(np_datetime(obsData['END_DATE']),index=obsData.index)
obsDepth=pd.Series(str2ndlist(obsData['TEMP_DBAR']),index=obsData.index)
obstemp=pd.Series(str2ndlist(obsData['TEMP_VALS']),index=obsData.index)

buoyData=pd.read_csv('ndbc_2011.csv')                          #data of wind speed and wave height in 2011
tf_index=np.where(buoyData['TF'].notnull())[0]
buoylat = pd.Series(buoyData['lat'],index=tf_index)
buoylon = pd.Series(buoyData['lon'],index=tf_index)
buoyspeed=pd.Series(buoyData['wind_speed'],index=tf_index)
buoywave=pd.Series(buoyData['wave_height'],index=tf_index)
buoytime = pd.Series(buoyData['Date'],index=tf_index)
indx=[]
for i in tf_index:
    buoytime[i]=datetime.strptime(buoytime[i], "%Y-%m-%d %H:%M")  # change str to datatime
    if 17.2<buoyspeed[i]:
        if buoywave[i]>5.5:
            indx.append(i)                                      #choose which day has storm
data=pd.DataFrame({'time':buoytime,'wind_speed':buoyspeed,'wave_height':buoywave,
                  'lat':buoylat,'lon':buoylon},index=tf_index)
data = data.sort_index(by='time')

buoyData2=pd.read_csv('ndbc_2013.csv')                           #data of wind speed and wave height in 2013
tf_index2=np.where(buoyData2['TF'].notnull())[0]
buoylat2 = pd.Series(buoyData2['lat'],index=tf_index2)
buoylon2= pd.Series(buoyData2['lon'],index=tf_index2)
buoyspeed2=pd.Series(buoyData2['wind_speed'],index=tf_index2)
buoywave2=pd.Series(buoyData2['wave_height'],index=tf_index2)
buoytime2 = pd.Series(buoyData2['Date'],index=tf_index2)
indx2=[]
for i in tf_index2:
    buoytime2[i]=datetime.strptime(buoytime2[i], "%Y-%m-%d %H:%M")  # change str to datatime
    if 17.2<buoyspeed2[i]:
        indx2.append(i)                                            #choose which day has storm
data2=pd.DataFrame({'time':buoytime2,'wind_speed':buoyspeed2,'wave_height':buoywave2,
                  'lat':buoylat2,'lon':buoylon2},index=tf_index2)
data2 = data.sort_index(by='time')

early_2011=[]
after_2011=[]
early_2013=[]
after_2013=[]
for i in obsData.index:
    for j in indx:
        if dist(buoylat[0],buoylon[0],obslat[i],obslon[i])<50:        #distance is smaller than 50km
            if obstime[i].month==8 and obstime[i].year==2011:
                if obstime[i].day>28:                                 #choose day after storm 
                    after_2011.append(i) 
        if dist(buoylat[0],buoylon[0],obslat[i],obslon[i])<50:
            if obstime[i].month==8 and obstime[i].year==2011:
                if obstime[i].day==27:                                 #choose day before storm
                    early_2011.append(i)
    for j in indx2:
        if dist(buoylat2[0],buoylon2[0],obslat[i],obslon[i])<50:
            if obstime[i].month==5 and obstime[i].year==2013:
                if obstime[i].day==26:                                 #choose day after storm
                    after_2013.append(i)
        if dist(buoylat2[0],buoylon2[0],obslat[i],obslon[i])<50:
            if obstime[i].month==5 and obstime[i].year==2013:
                if obstime[i].day==24:                                #choose day before storm
                    early_2013.append(i)
after_2011=pd.Series(after_2011).unique()
early_2011=pd.Series(early_2011).unique()
early_id_2011=pd.Series(turtle_id[early_2011])                       #get id of turtle
after_id_2011=pd.Series(turtle_id[after_2011])
for i in early_2011:
    for j in after_2011:
        if early_id_2011[i]==after_id_2011[j]:
            if max(obsDepth[i])>30:
                if max(obsDepth[j])>30:
                    fig=plt.figure()
                    ax=fig.add_subplot(111)
                    plt.text(7,4,'id:'+str(early_id_2011[i])+'',fontsize=25)
                    ax.set_xlim([5, 25])
                    ax.set_ylim([50, 0])
                    ax.set_xlabel('Tempature(degC)', fontsize=30)
                    ax.set_ylabel('Depth(m)', fontsize=30)
                    ax.set_title('Temperature before and after 2011 storm',fontsize=35)
                    plt.xticks(fontsize=35)
                    plt.yticks(fontsize=35)
                    ax.plot(obstemp[i],obsDepth[i],'bo--', label=str(obstime[i]),linewidth=2)      
                    ax.plot(obstemp[j],obsDepth[j],'ro-', label=str(obstime[j]), linewidth=2)
                    ax.legend(loc='lower right', borderpad=1.5, labelspacing=1.5)
                    leg = plt.gca().get_legend()
                    ltext  = leg.get_texts()
                    plt.setp(ltext, fontsize='xx-large') 
                    

after_2013=pd.Series(after_2013).unique()
early_2013=pd.Series(early_2013).unique()
early_id_2013=pd.Series(turtle_id[early_2013])
after_id_2013=pd.Series(turtle_id[after_2013])
for i in early_2013:
    for j in after_2013:
        if early_id_2013[i]==after_id_2013[j]:
            fig=plt.figure()
            ax=fig.add_subplot(111)
            plt.text(7,4,'id:'+str(early_id_2013[i])+'',fontsize=25)
            ax.set_xlim([5, 25])
            ax.set_ylim([50, 0])
            ax.set_xlabel('Tempature(degC)', fontsize=30)
            ax.set_ylabel('Depth(m)', fontsize=30)
            ax.set_title('Temperature before and after 2013 storm',fontsize=35)
            plt.xticks(fontsize=35)
            plt.yticks(fontsize=35)
            ax.plot(obstemp[i],obsDepth[i],'bo--', label=str(obstime[i]),linewidth=2)      
            ax.plot(obstemp[j],obsDepth[j],'ro-', label=str(obstime[j]), linewidth=2)
            ax.legend(loc='lower right', borderpad=1.5, labelspacing=1.5)
            leg = plt.gca().get_legend()
            ltext = leg.get_texts()
            plt.setp(ltext, fontsize='xx-large') 

'''
fig=plt.figure()
ax = fig.add_subplot(111)
ax.plot(data['time'], data['wind_speed'], color='b', linewidth=1,label='wind speed')
ax.plot(data['time'], data['wave_height'], color='y', linewidth=1,label='wave height')
ax.plot(data['time'],[17.2]*len(tf_index),color='r',linewidth=0.5)
ax.plot(data['time'],[5.5]*len(tf_index),color='r',linewidth=0.5)
ax.legend(loc='upper right')
ax.set_xlabel('time', fontsize=20)
ax.set_ylabel('wind speed', fontsize=20)
dates = mpl.dates.drange(np.amin(buoytime), np.max(buoytime), timedelta(days=50))
dateFmt = mpl.dates.DateFormatter('%b,%Y')
ax.set_xticks(dates)
ax.xaxis.set_major_formatter(dateFmt)
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
plt.title('2011')          #plot wind and wave
'''       
plt.show()
