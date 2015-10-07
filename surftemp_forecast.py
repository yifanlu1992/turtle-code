# -*- coding: utf-8 -*-
"""
Created on Thu May 23 09:10:22 2013
creat temperature animation in massbay in recent 6 days.
@author: zhaobin
"""
from mpl_toolkits.basemap import Basemap
from pylab import *
import matplotlib.tri as Tri
import matplotlib.pyplot as plt
import datetime as dt
import netCDF4
from matplotlib import animation
import numpy as np
import os
from datetime import timedelta,datetime
def draw_basemap(fig, ax, lonsize, latsize, interval_lon=2, interval_lat=2):
    ax = fig.sca(ax)
    dmap = Basemap(projection='cyl',
                   llcrnrlat=min(latsize)-0.01,
                   urcrnrlat=max(latsize)+0.01,
                   llcrnrlon=min(lonsize)-0.01,
                   urcrnrlon=max(lonsize)+0.01,
                   resolution='h',ax=ax)
    dmap.drawparallels(np.arange(int(min(latsize)),
                                 int(max(latsize))+1,interval_lat),
                       labels=[1,0,0,0], linewidth=0,fontsize=20)
    dmap.drawmeridians(np.arange(int(min(lonsize))-1,
                                 int(max(lonsize))+1,interval_lon),
                       labels=[0,0,0,1], linewidth=0,fontsize=20)
    dmap.drawcoastlines()
    dmap.fillcontinents(color='grey')
    dmap.drawmapboundary()
###########################################################
method='gif' #use for plotting mp4 or gif
url="http://www.smast.umassd.edu:8080/thredds/dodsC/FVCOM/NECOFS/Forecasts/NECOFS_FVCOM_OCEAN_MASSBAY_FORECAST.nc"
nc = netCDF4.Dataset(url)
lat = nc.variables['lat'][:]
lon = nc.variables['lon'][:]
latc = nc.variables['latc'][:]
lonc = nc.variables['lonc'][:]
temp=nc.variables['temp']
sali=nc.variables["salinity"]
siglay=nc.variables['siglay']
h = nc.variables['h'][:]
nv = nc.variables['nv'][:].T - 1 # read connectivity array
time = nc.variables['time'][:]
latsize=[min(lat)-0.1,max(lat)+0.1]
lonsize=[min(lon)-0.1,max(lon)+0.1]   #set range you want to plot
tri = Tri.Triangulation(lon,lat, triangles=nv)# create a triangulation object, specifying the triangle connectivity array
levels=np.arange(1,30,0.1) #colorbar range
if method=="mp4":
    #plot a mp4
    fig,ax=plt.subplots()
    draw_basemap(fig, ax, lonsize, latsize)
    def animate(i):
        del ax.lines[:]
        temprature=temp[3*i,0,]
        temprature=np.array(temprature)
        TIME=datetime(1858,11,17,0,0,0)+timedelta(days=float(time[3*i])) #change time to datetime
        tri_temp=tricontourf(tri,temprature,levels=levels)
        plt.title('Temperature model, Time:'+str(TIME)[5:16],fontsize=30)
    anim = animation.FuncAnimation(fig, animate, frames=48)    
    anim.save('massbay_temperature.mp4',writer='mencoder',fps=2)
    #plt.show()
if method=='gif':
    #plot a gif
    for i in range(48):  #legnth of time is 114,48 is every 3 hours. 
        fig,ax=plt.subplots()
        draw_basemap(fig, ax, lonsize, latsize)
        temprature=temp[3*i,0,]
        temprature=np.array(temprature)
        TIME=datetime(1858,11,17,0,0,0)+timedelta(days=float(time[3*i])) #change time to datetime 
        tri_temp=tricontourf(tri,temprature,levels=levels)
        plt.title('Temperature model, Time:'+str(TIME)[5:16],fontsize=30)
        cbar=colorbar(ticks=[1,5,9,13,17,21,25,29])
        cbar.ax.tick_params(labelsize=20) 
        if i<10:
            plt.savefig('MASSBAY_temperature_00'+str(i)+'.png')  #save pic as 00X.png
        elif i<100:
            plt.savefig('MASSBAY_temperature_0'+str(i)+'.png')  #save pic as 0XX.png
        else:
            plt.savefig('MASSBAY_temperature_'+str(i)+'.png')  #save pic as XXX.png
    cmd='convert -delay 40 -loop 0 MASSBAY_temperature_*.png massbay_temperature.gif' 
    os.system(cmd)              #convert png to gif
