# -*- coding: utf-8 -*-
"""
Created on Tue Oct 13 10:38:00 2015
output 4second_turtle_up_down.csv and 4second_turtle_tdr.csv
@author: zdong
"""

import pandas as pd
import numpy as np
from turtleModule import str2ndlist
##################################3
data1=pd.read_csv('12487up_down.csv') #read file 
up1=pd.Series(str2ndlist(data1['up'],bracket=True))
down1=pd.Series(str2ndlist(data1['down'],bracket=True))
data2=pd.read_csv('13137up_down.csv')
up2=pd.Series(str2ndlist(data2['up'],bracket=True))
down2=pd.Series(str2ndlist(data2['down'],bracket=True))

up,down=[],[]
for i in range(len(up1)): #add two file together
    up.append(up1[i])
    down.append(down1[i])
for i in range(len(up2)):
    up.append(up2[i])
    down.append(down2[i])
data={'up':up,'down':down}
Data=pd.DataFrame(data)
Data.to_csv('4second_turtle_up_down.csv')

second_data1=pd.read_csv('turtle_12487_tdr.csv') #read file 
depth1=pd.Series(second_data1['Depth'])
temp1=pd.Series(second_data1['temp'])
time1=pd.Series(second_data1['Date'])

second_data2=pd.read_csv('turtle_13137_tdr.csv')
depth2=pd.Series(second_data2['Depth'])
temp2=pd.Series(second_data2['temp'])
time2=pd.Series(second_data2['Date'])


depth,temp,time=[],[],[]
for i in range(len(depth1)): #add two file together
    depth.append(depth1[i])
    temp.append(temp1[i])
    time.append(time1[i])
for i in range(len(depth2)):
    depth.append(depth2[i])
    temp.append(temp2[i])
    time.append(time2[i])
data={'Depth':depth,'temp':temp,'Date':time}
Data=pd.DataFrame(data)
Data.to_csv('4second_turtle_tdr.csv')