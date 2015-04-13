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
from turtleModule import mon_alpha2num, np_datetime, dist,str2ndlist,colors,str2list
###################################################################################
r = 10                          # the obs position that has shipboard position within (r) kilometers might be considered as good data.
day = 3                        # the obs time that has shipboard time within (day) days might be considered as good data.
obsData=pd.read_csv('ctdWithModTempByDepth.csv',index_col=0)
tf_index=np.where(obsData['TF'].notnull())[0]
obslat = pd.Series(obsData['LAT'][tf_index],index=tf_index)
obslon = pd.Series(obsData['LON'][tf_index],index=tf_index)
obstime = pd.Series(np_datetime(obsData['END_DATE'][tf_index]),index=tf_index)
obsDepth=pd.Series(str2ndlist(obsData['TEMP_DBAR'][tf_index]),index=tf_index)
obstemp=pd.Series(str2ndlist(obsData['TEMP_VALS'][tf_index]),index=tf_index)
modtemp=pd.Series(str2ndlist(obsData['modTempByDepth'][tf_index],bracket=True),index=tf_index)
obsData1=pd.read_csv('ctd_FVcom_TEMP.csv')                       #this ctd`s FVCOM temperature
tf_index_FVCOM=np.where(obsData1['modtempBYdepth'].notnull())[0]
modtemp_FVCOM=pd.Series(obsData1['modtempBYdepth'],index=tf_index_FVCOM)
for i in tf_index_FVCOM:
    modtemp_FVCOM[i]=str2list(modtemp_FVCOM[i],bracket=True)
obsData2=pd.read_csv('ctd_withHYCOMtemp.csv')                       #this ctd`s HYCOM temperature
tf_index_HYCOM=np.where(obsData2['modtemp_HYCOM'].notnull())[0]
modtemp_HYCOM=pd.Series(obsData2['modtemp_HYCOM'],index=tf_index_HYCOM)   
for i in tf_index_HYCOM:
    modtemp_HYCOM[i]=str2list(modtemp_HYCOM[i],bracket=True)
shipData=pd.read_csv('ship06-08_MODELtemp.csv',index_col=0)
shiplat=pd.Series(shipData['LAT'],index=shipData.index)
shiplon=pd.Series(shipData['LON'],index=shipData.index)
shiptime=pd.Series(shipData['time'],index=shipData.index)
shipdepth=pd.Series(str2ndlist(shipData['depth'],bracket=True),index=shipData.index)
shiptemp=pd.Series(str2ndlist(shipData['temperature'],bracket=True),index=shipData.index)
MODtemp=pd.Series(str2ndlist(shipData['modTempByDepth'],bracket=True),index=shipData.index)
for i in range(len(shiptime)):
    shiptime[i]=datetime.strptime(shiptime[i], "%Y-%m-%d %H:%M:%S")  # change str to datatime
shipData1=pd.read_csv('ship_FVcom_temp.csv')         #this ship`s FVCOM temperature
tf_index_fvcom=np.where(shipData1['modtempBYdepth'].notnull())[0]
modtemp_fvcom=pd.Series(shipData1['modtempBYdepth'],index=tf_index_fvcom)
for i in tf_index_fvcom:
    modtemp_fvcom[i]=str2list(modtemp_fvcom[i],bracket=True)
shipData2=pd.read_csv('ship_withHYCOMtemp1.csv')
tf_index_hycom=np.where(shipData2['modtemp_HYCOM'].notnull())[0]
modtemp_hycom=pd.Series(shipData2['modtemp_HYCOM'],index=tf_index_hycom)#this ship`s HYCOM temperature
for i in tf_index_hycom:
    modtemp_hycom[i]=str2list(modtemp_hycom[i],bracket=True)
'''
index_hycom = []     #index of turtle
indx_hycom=[]        #index of shipboard 
for i in tf_index_HYCOM:
    for j in tf_index_hycom:
        l = dist(obslon[i], obslat[i],shiplon[j],shiplat[j])
        if l<r:
            print l        #distance
            maxtime = obstime[i]+timedelta(days=day)
            mintime = obstime[i]-timedelta(days=day)
            mx = shiptime[j]<maxtime
            mn = shiptime[j]>mintime
            TF = mx*mn  
            if TF==1:      #time
                index_hycom.append(i)     #turtle index
                indx_hycom.append(j)      #ship index
print index_hycom,indx_hycom
'''
index_hycom=[139, 393, 395, 761, 762, 763, 764, 858, 859, 2496, 2497, 4749, 4750, 4751, 4753, 4754, 4755, 4757, 5325, 5327, 5328, 5660, 6337, 6337, 6338, 6338, 6933, 6934, 7055, 7547, 7547, 7548, 7549, 7678, 7805, 8267, 8268, 8273, 8273, 8274, 8274, 8275, 8275, 9252, 9464, 9465, 9466, 9467, 9467, 9469, 9470, 9708, 10021, 10067, 10069, 11049, 11050, 11547, 11548, 12335, 12336, 12339, 12340, 13235, 13237, 13315, 13315, 13316, 13316, 13497, 13498, 13499, 13500, 13501, 13757, 13758, 13960, 13961, 13962, 13963, 15906, 15907, 19073, 19074, 22574, 22574, 22575, 22575, 22576, 22576, 23955, 23956, 23957, 23958, 23959, 23960, 28148, 28968] 
indx_hycom= [1153, 1203, 1202, 336, 336, 336, 336, 331, 331, 1284, 1284, 695, 695, 695, 695, 695, 695, 695, 690, 690, 690, 925, 691, 692, 691, 692, 1067, 1067, 1067, 923, 924, 924, 924, 995, 919, 697, 698, 697, 698, 697, 698, 697, 698, 924, 924, 924, 924, 924, 925, 924, 925, 692, 919, 692, 692, 692, 692, 695, 695, 1265, 1265, 1265, 1265, 322, 322, 924, 925, 924, 925, 850, 850, 850, 850, 850, 850, 850, 690, 690, 690, 690, 1217, 1217, 40, 40, 41, 217, 41, 217, 41, 217, 21, 21, 21, 37, 37, 37, 324, 1160]
index,indx=[],[]
for i in index_hycom:
    if i in tf_index_FVCOM:
        index.append(i)
for i in indx_hycom:
    if i in tf_index_fvcom:
        indx.append(i)
INDX=pd.Series(indx).unique()      
color=['blue','green','black','grey','orange','cyan','yellow','red','blue','green','black','grey','orange','cyan','yellow','red']
Mean_turVSship,Mean_modVSship,Mean_turVSmod,Rms_turVSship,Rms_modVSship,Rms_turVSmod=[],[],[],[],[],[]
Mean_modVSship_fvcom,Mean_turVSmod_fvcom,Rms_modVSship_fvcom,Rms_turVSmod_fvcom=[],[],[],[]
Mean_modVSship_hycom,Mean_turVSmod_hycom,Rms_modVSship_hycom,Rms_turVSmod_hycom=[],[],[],[]
hycom_depth=[1,10,20,30,50,75,100,125,150,200]
for i in range(len(INDX)):
    q=0          #plot different color
    diff_turVSship=[]
    diff_turVSmod=[]
    diff_turVSmod_fvcom=[]
    diff_turVSmod_hycom=[]
    fig=plt.figure()
    for j in range(len(indx)):
        if indx[j]==INDX[i]:
            for k in range(len(obsDepth[index[j]])):
                for m in range(len(shipdepth[INDX[i]])):
                    if obsDepth[index[j]][k]==shipdepth[INDX[i]][m]:
                        dif_turVSship=obstemp[index[j]][k]-shiptemp[INDX[i]][m]
                        dif_turVSmod=obstemp[index[j]][k]-modtemp[index[j]][k]
                        diff_turVSship.append(dif_turVSship)
                        diff_turVSmod.append(dif_turVSmod)                     #roms
                        
                        
                        dif_turVSmod_fvcom=obstemp[index[j]][k]-modtemp_FVCOM[index[j]][k]
                        diff_turVSmod_fvcom.append(dif_turVSmod_fvcom)                     #fvcom
                        
                        dif_turVSmod_hycom=obstemp[index[j]][k]-modtemp_HYCOM[index[j]][k]
                        diff_turVSmod_hycom.append(dif_turVSmod_hycom)                     #hycom
           
            plt.plot(obstemp[index[j]],obsDepth[index[j]],color='black' ,linewidth=2)
            #plt.plot(modtemp[index[j]],obsDepth[index[j]],color=color[q] ,linewidth=2,linestyle='--')
            #plt.plot(modtemp_FVCOM[index[j]],obsDepth[index[j]],color=color[q] ,linewidth=2,linestyle='dotted')
            #plt.plot(pd.Series(modtemp_HYCOM[index[j]]).unique(),hycom_depth[0:len(pd.Series(modtemp_HYCOM[index[j]]).unique())],color=color[q] ,linewidth=2,linestyle='-.',marker='o')
            
            q+=1
        
    plt.plot(shiptemp[INDX[i]],shipdepth[INDX[i]],color=color[-1] ,linewidth=6)
    plt.plot(MODtemp[INDX[i]],shipdepth[INDX[i]],color=color[-2] ,linewidth=6,linestyle='--')
    plt.plot(modtemp_fvcom[INDX[i]],shipdepth[INDX[i]],color=color[-3] ,linewidth=6,linestyle='dotted')
    plt.plot(pd.Series(modtemp_hycom[INDX[i]]).unique(),hycom_depth[0:len(pd.Series(modtemp_hycom[INDX[i]]).unique())],color=color[-4] ,linewidth=6,linestyle='-.',marker='o')
    
    diff_modVSship=np.array(shiptemp[INDX[i]])-np.array(MODtemp[INDX[i]])      
    mean_turVSship=np.mean(np.array(diff_turVSship))                           
    mean_modVSship=np.mean(diff_modVSship)
    mean_turVSmod=np.mean(np.array(diff_turVSmod))
    rms_turVSship=np.sqrt(np.sum(np.array(diff_turVSship)*np.array(diff_turVSship))/len(np.array(diff_turVSship)))
    rms_turVSmod=np.sqrt(np.sum(np.array(diff_turVSmod)*np.array(diff_turVSmod))/len(np.array(diff_turVSmod)))
    rms_modVSship=np.sqrt(np.sum(diff_modVSship*diff_modVSship)/len(diff_modVSship))
    Mean_turVSship.append(mean_turVSship)
    Mean_modVSship.append(mean_modVSship)
    Mean_turVSmod.append(mean_turVSmod)
    Rms_turVSship.append(rms_turVSship)
    Rms_modVSship.append(rms_modVSship)
    Rms_turVSmod.append(rms_turVSmod)                                           #roms
    
    diff_modVSship_fvcom=np.array(shiptemp[INDX[i]])-np.array(modtemp_fvcom[INDX[i]])                                 
    mean_modVSship_fvcom=np.mean(diff_modVSship_fvcom)
    mean_turVSmod_fvcom=np.mean(np.array(diff_turVSmod_fvcom))
    rms_turVSmod_fvcom=np.sqrt(np.sum(np.array(diff_turVSmod_fvcom)*np.array(diff_turVSmod_fvcom))/len(np.array(diff_turVSmod_fvcom)))
    rms_modVSship_fvcom=np.sqrt(np.sum(diff_modVSship_fvcom*diff_modVSship_fvcom)/len(diff_modVSship_fvcom))
    Mean_modVSship_fvcom.append(mean_modVSship_fvcom)
    Mean_turVSmod_fvcom.append(mean_turVSmod_fvcom)
    Rms_modVSship_fvcom.append(rms_modVSship_fvcom)
    Rms_turVSmod_fvcom.append(rms_turVSmod_fvcom)                                         #fvcom
    
    diff_modVSship_hycom=np.array(shiptemp[INDX[i]])-np.array(modtemp_hycom[INDX[i]])                                 
    mean_modVSship_hycom=np.mean(diff_modVSship_hycom)
    mean_turVSmod_hycom=np.mean(np.array(diff_turVSmod_hycom))
    rms_turVSmod_hycom=np.sqrt(np.sum(np.array(diff_turVSmod_hycom)*np.array(diff_turVSmod_hycom))/len(np.array(diff_turVSmod_hycom)))
    rms_modVSship_hycom=np.sqrt(np.sum(diff_modVSship_hycom*diff_modVSship_hycom)/len(diff_modVSship_hycom))
    Mean_modVSship_hycom.append(mean_modVSship_hycom)
    Mean_turVSmod_hycom.append(mean_turVSmod_hycom)
    Rms_modVSship_hycom.append(rms_modVSship_hycom)
    Rms_turVSmod_hycom.append(rms_turVSmod_hycom)                                         #hycom
    plt.ylabel('Depth(m)',fontsize=20)
    plt.xlabel('Temperature(degC)',fontsize=20)
    plt.xlim([0,30])
    plt.ylim([max(shipdepth[INDX[i]])+1,0])
    plt.xticks(np.arange(0,30,5),fontsize=25)
    plt.yticks(np.arange(max(shipdepth[INDX[i]])+1,0,-5),fontsize=25)
    
    plt.text(1,min(shipdepth[INDX[i]])+1,'mean ship-turtle:  '+str(round(mean_turVSship,2))+u'°C',fontsize=20)
    plt.text(1,min(shipdepth[INDX[i]])+3,'mean ship-model(ROMS):  '+str(round(mean_modVSship,2))+u'°C',fontsize=20)
    #plt.text(1,min(shipdepth[INDX[i]])+4,'mean turtle-model temp(roms):'+str(round(mean_turVSmod,2)),fontsize=15)
    plt.text(1,min(shipdepth[INDX[i]])+5,'RMS ship-turtle:  '+str(round(rms_turVSship,2))+u'°C',fontsize=20)
    plt.text(1,min(shipdepth[INDX[i]])+7,'RMS ship-model(ROMS):  '+str(round(rms_modVSship,2))+u'°C',fontsize=20)
    #plt.text(1,min(shipdepth[INDX[i]])+8.5,'RMS turtle-model(roms):'+str(round(rms_turVSmod,2)),fontsize=15)       #roms
    
    plt.text(1,min(shipdepth[INDX[i]])+9,'mean ship-model (FVCOM):  '+str(round(mean_modVSship_fvcom,2))+u'°C',fontsize=20)
    #plt.text(1,max(shipdepth[INDX[i]])-5,'mean turtle-model temp(FVCOM):'+str(round(mean_turVSmod_fvcom,2)),fontsize=15)
    plt.text(1,min(shipdepth[INDX[i]])+11,'RMS ship-model(FVCOM):  '+str(round(rms_modVSship_fvcom,2))+u'°C',fontsize=20)
   # plt.text(1,max(shipdepth[INDX[i]])-1,'RMS turtle-model(FVCOM):'+str(round(rms_turVSmod_fvcom,2)),fontsize=15)  #FVCOM
    
    plt.text(1,min(shipdepth[INDX[i]])+13,'mean ship-model (HYCOM):  '+str(round(mean_modVSship_hycom,2))+u'°C',fontsize=20)
    #plt.text(1,min(shipdepth[INDX[i]])+11.5,'mean turtle-model temp(HYCOM):'+str(round(mean_turVSmod_hycom,2)),fontsize=15)
    plt.text(1,min(shipdepth[INDX[i]])+15,'RMS ship-model(HYCOM):  '+str(round(rms_modVSship_hycom,2))+u'°C',fontsize=20)
    #plt.text(1,min(shipdepth[INDX[i]])+14.5,'RMS turtle-model(HYCOM):'+str(round(rms_turVSmod_hycom,2)),fontsize=15)  #HYCOM
      
    plt.title('Ship vs Turtle vs Model Profiles (~'+str(shiptime[INDX[i]].date())+')',fontsize=25)
    plt.savefig('turtlesVSshipboard'+str(INDX[i])+'.png')
plt.show()
print 'mean(mean ship-turtle)',np.mean(np.array(Mean_turVSship))
print 'mean(mean ship-model(roms))',np.mean(np.array(Mean_modVSship))
print 'mean(mean turtle-model(roms))',np.mean(np.array(Mean_turVSmod))
print 'mean(rms ship-turtle)',np.mean(np.array(Rms_turVSship))
print 'mean(rms ship-model(roms))',np.mean(np.array(Rms_modVSship))
print 'mean(rms turtle-model(roms))',np.mean(np.array(Rms_turVSmod))

print 'mean(mean ship-model(fvcom))',np.mean(np.array(Mean_modVSship_fvcom))
print 'mean(mean turtle-model(fvcom))',np.mean(np.array(Mean_turVSmod_fvcom))
print 'mean(rms ship-model(fvcom))',np.mean(np.array(Rms_modVSship_fvcom))
print 'mean(rms turtle-model(fvcom))',np.mean(np.array(Rms_turVSmod_fvcom))

print 'mean(mean ship-model(hycom))',np.mean(np.array(Mean_modVSship_hycom))
print 'mean(mean turtle-model(hycom))',np.mean(np.array(Mean_turVSmod_hycom))
print 'mean(rms ship-model(hycom))',np.mean(np.array(Rms_modVSship_hycom))
print 'mean(rms turtle-model(hycom))',np.mean(np.array(Rms_turVSmod_hycom))
