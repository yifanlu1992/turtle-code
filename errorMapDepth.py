'''
plot 4 maps in 1 figure to show which depth has the most errors. Also plot the errorbar and ratio
Plot error bar and ratio of error.
'''
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import netCDF4
import watertempModule as wtm   # A module of classes that using ROMS, FVCOM
from turtleModule import str2ndlist, np_datetime, bottom_value, dist
FONTSIZE = 25
criteria = 10                                      # error criteria
depth = -10                                        # The first depth map wanted to plot
depth_interval = 25                                # the interval depth of each map.
obsData = pd.read_csv('ctdWithModTempByDepth.csv') # extracted from ctdWithModTempByDepth.py
tf_index = np.where(obsData['TF'].notnull())[0]    # get the index of good data
obsLon, obsLat = obsData['LON'][tf_index], obsData['LAT'][tf_index]
obsTime = pd.Series(np_datetime(obsData['END_DATE'][tf_index]), index=tf_index)
obsTemp = pd.Series(str2ndlist(obsData['TEMP_VALS'][tf_index]), index=tf_index)
# obsTemp = pd.Series(bottom_value(obs['TEMP_VALS'][tf_index]), index=tf_index)
obsDepth = pd.Series(str2ndlist(obsData['TEMP_DBAR'][tf_index]), index=tf_index)
modLayer = pd.Series(np.array(str2ndlist(obsData['modDepthLayer'][tf_index],bracket=True)), index=tf_index) # bracket is to get rid of symbol "[" and "]" in string
modNearestIndex = pd.Series(str2ndlist(obsData['modNearestIndex'][tf_index], bracket=True), index=tf_index)
modTemp = pd.Series(np.array(str2ndlist(obsData['modTempByDepth'][tf_index], bracket=True)), index=tf_index)
data = pd.DataFrame({'lon': obsLon, 'lat': obsLat,
                     'obstemp': obsTemp.values,'modtemp':modTemp,
                     'depth': obsDepth, 'time': obsTime.values,
                     'layer': modLayer}, index=tf_index)

ind,Ind = [],[] # the indices needed
obst,Obst = [],[]
modt,Modt = [],[]
lyr,Lyr = [],[]
dep,Dep=[],[]
text = '|modtemp-obstemp|>10 degC' # remember to keep consistent with "diff" argument below
for i in data.index:
    diff = np.array(data['modtemp'][i])-np.array(data['obstemp'][i])
    indx = np.where(diff > criteria)[0]
    if not indx.size: continue
    ind.extend([i] * indx.size)
    obst.extend(np.array(data['obstemp'][i])[indx])
    modt.extend(np.array(data['modtemp'][i])[indx])
    lyr.extend(np.array(data['layer'][i])[indx])
    dep.extend(np.array(data['depth'][i])[indx])
    
    dif =np.array(data['obstemp'][i])-np.array(data['modtemp'][i])
    Indx = np.where(dif > criteria)[0]
    if not Indx.size: continue
    Ind.extend([i] * Indx.size)
    Obst.extend(np.array(data['obstemp'][i])[Indx])
    Modt.extend(np.array(data['modtemp'][i])[Indx])
    Lyr.extend(np.array(data['layer'][i])[Indx])
    Dep.extend(np.array(data['depth'][i])[Indx])
    '''
    for j in range(len(a['obstemp'][i])):
        print i, j
        y = data['modtemp'][i][j]
        x = data['obstemp'][i][j]
        if abs(x - y) > 10:     # |mod-obstemp|>10
        # if y - x > 10:          # modtemp-obstemp>10
        # if x - y > 10:          # obstemp-modtenp>10
            ind.append(i)
            obst.append(x)
            modt.append(y)
            lyr.append(data['layer'][i][j])
            dep.append(data['depth'][i][j])
    '''
dataFinal = pd.DataFrame({'lon': data['lon'][ind].values,
                          'lat': data['lat'][ind].values,
                          'time': data['time'][ind].values,
                          'obstemp': np.array(obst),
                          'modtemp': np.array(modt),
                          'layer': np.array(lyr),
                          'dep': np.array(dep),
                          'nearestIndex': modNearestIndex[ind].values
                          })
DataFinal = pd.DataFrame({'lon': data['lon'][Ind].values,
                          'lat': data['lat'][Ind].values,
                          'time': data['time'][Ind].values,
                          'obstemp': np.array(Obst),
                          'modtemp': np.array(Modt),
                          'layer': np.array(Lyr),
                          'dep': np.array(Dep),
                          'nearestIndex': modNearestIndex[Ind].values
                          })
starttime = datetime(2013,7,10) # the temp contour below ploted is from this time
endtime = starttime + timedelta(hours=1)
# layer = 15
'''
tempObj = wtm.water_roms()
url = tempObj.get_url(starttime, endtime)
modData = tempObj.get_data(url)
h, s_rho = modData['h'], modData['s_rho']
lons, lats = modData['lon_rho'], modData['lat_rho']
lonsize = np.amin(lons)-0.1, np.amax(lons)+0.1
latsize = np.amin(lats)-0.1, np.amax(lats)+0.1

fig = plt.figure()
ax = []
for i in range(0, 4):
    ax.append(plt.subplot(2,2,i+1))
    # l = layer+i*6
    l = depth - i*depth_interval
    # lon, lat = dataFinal.ix[5]['lon'], dataFinal.ix[5]['lat']
    # p = np.where(dataFinal['layer']==l)[0]
    a = dataFinal['dep'] < 5-l
    b = dataFinal['dep'] > -5-l
    p = np.where(a & b)[0]      # Get the index of 5m above and 5m below current depth.
    ''
    # if use code below, the error map ploted would just show the erors with 20 days of starttime
    m = dataFinal['time'][p]>starttime-timedelta(days=10)
    n = dataFinal['time'][p]<starttime+timedelta(days=10)
    b = np.where(m & n)[0]
    indx = dataFinal.ix[p].index[b]
    ''
    indx = dataFinal.ix[p].index
    colorValues = dataFinal['obstemp'][indx]/32
    # modLayerTemp = tempObj.layerTemp(l, url)  #grab new layer temp
    modLayerTemp = tempObj.depthTemp(l, url)
    fig.sca(ax[i])
    dmap = Basemap(projection = 'cyl',
               llcrnrlat = min(latsize)-0.01,
               urcrnrlat = max(latsize)+0.01,
               llcrnrlon = min(lonsize)-0.01,
               urcrnrlon = max(lonsize)+0.01,
               resolution = 'h', ax=ax[i])
    dmap.drawparallels(np.arange(int(min(latsize)), int(max(latsize))+1, 2),
                   labels = [1,0,0,0])
    dmap.drawmeridians(np.arange(int(min(lonsize)), int(max(lonsize))+1, 2),
                   labels = [0,0,0,1])
    dmap.drawcoastlines()
    dmap.fillcontinents(color='grey')
    dmap.drawmapboundary()
    if i == 0:
        c = plt.contourf(lons, lats, modLayerTemp, extend ='both')
        clrmap = c.cmap
    else:
        plt.contourf(lons, lats, modLayerTemp, extend ='both', cmap=clrmap)
    plt.scatter(dataFinal['lon'][indx], dataFinal['lat'][indx], s=40, c=colorValues.values, cmap=clrmap)
    ax[i].set_title('Depth: {0}'.format(l))
fig.subplots_adjust(right=0.8)
cbar_ax = fig.add_axes([0.85, 0.15, 0.05, 0.7])
plt.colorbar(c, cax=cbar_ax, ticks=range(0, 32, 4))     #c is the contour of first subplot
plt.suptitle('obsVSmodel, %s' % text, fontsize=25)
plt.savefig('errorMapDepth4In1.png',dpi=200)
'''
# for layer
fig = plt.figure()
ax = fig.add_subplot(111)
x = np.arange(1,37)
bar = np.array([0]*36)
for i in dataFinal['layer']:
    if i in x:
        print(i)
        bar[i-1] = bar[i-1]+1
plt.bar(x, bar)
plt.xlabel('Layer', fontsize=25)
plt.ylabel('Quantity', fontsize=25)
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
plt.title('error bar that %s, based on layers' % text, fontsize=25)

#draw errorbar based on depth.
fig = plt.figure()
ax = fig.add_subplot(111)
y = dataFinal['dep'].order().values
x = np.arange(1, np.amax(y)+1)
bar = np.array([0]*np.amax(y))
for i in y:
    # if i in x:
    bar[int(i)-1] = bar[int(i)-1]+1
plt.barh(x, bar)
plt.ylim(50, 0)
# plt.ylabel('depth', fontsize=25)
plt.ylabel('Depth(meters)', fontsize=25)
plt.xlabel('Quantity', fontsize=25)
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
# plt.title('error bar that |obstemp-modtemp|>10, based on depth',fontsize=25)
plt.title('modeled-observed Temperature>10 degC', fontsize=25)
plt.savefig('errorMapDepthErrorBar.png',dpi=200)
dep_num=[0]*int(np.amax(y))
for i in data.index:
    for j in range(1,int(np.amax(y))):
        for q in range(len(obsDepth[i])):
            if obsDepth[i][q]==j:
                dep_num[j-1]+=1
bar_pre=bar*100.0/dep_num
fig = plt.figure()
ax = fig.add_subplot(111)
plt.barh(x, bar_pre)
plt.ylim(50, 0)
# plt.ylabel('depth', fontsize=25)
plt.ylabel('Depth(meters)', fontsize=25)
plt.xlabel('Percent', fontsize=25)
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
# plt.title('error bar that |obstemp-modtemp|>10, based on depth',fontsize=25)
plt.title('Percent of modeled-observed Temperature>10 degC', fontsize=25)
plt.savefig('errorMapDepthErrorBar.png',dpi=200)

Fig = plt.figure()
ax = fig.add_subplot(111)
y = DataFinal['dep'].order().values
x = np.arange(1, np.amax(y)+1)
bar = np.array([0]*np.amax(y))
for i in y:
    # if i in x:
    bar[int(i)-1] = bar[int(i)-1]+1
plt.barh(x, bar)
plt.ylim(50, 0)
# plt.ylabel('depth', fontsize=25)
plt.ylabel('Depth(meters)', fontsize=25)
plt.xlabel('Quantity', fontsize=25)
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
# plt.title('error bar that |obstemp-modtemp|>10, based on depth',fontsize=25)
plt.title('observed-modeled Temperature>'+str(criteria)+' degC', fontsize=25)
plt.savefig('errorMapDepthErrorBar1.png',dpi=200)
'''
modDepth = []
for i in dataFinal.index:
    m = dataFinal['nearestIndex'][i]
    modDepth.append(h[int(m[0]), int(m[1])])
fig=plt.figure()
ax = fig.add_subplot(111)
rate = dataFinal['dep']/modDepth
x = [0]*50
y = np.arange(0,5,0.1)
for i in rate:
    x[int(i*10)] += 1
plt.barh(y, x, height=0.08)
plt.ylim(5, 0)
plt.yticks(np.arange(0,5,0.1))
plt.ylabel('obsErrorDep/modH', fontsize=25)
plt.xlabel('Quantity', fontsize=25)
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
plt.title('Ratio of obs error(>10) (depth)', fontsize=25)
plt.savefig('erorMapDepthRatioeOfError.png', dpi=200)
'''
fig = plt.figure()
ax = fig.add_subplot(111)
plt.barh(x, bar_pre,color='r',label='model warmer')
plt.barh(x,-bar[0:49]*100.0/dep_num,label='model colder')
plt.legend(loc='best')
plt.ylim(50, 0)
plt.xlim(-1,15)
# plt.ylabel('depth', fontsize=25)
plt.ylabel('Depth(meters)', fontsize=25)
plt.xlabel('Percent', fontsize=25)
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
plt.title('Percent time |modeled-observed| Temperature>10 degC', fontsize=25)
plt.show()

