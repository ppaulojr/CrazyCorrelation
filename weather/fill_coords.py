#!/usr/bin/env python
import math
from collections import defaultdict
from matplotlib.mlab import griddata
import matplotlib.pyplot as plt
import numpy as np

# http://en.wikipedia.org/wiki/Extreme_points_of_the_United_States#Westernmost
top = 49.3457868 # north lat
left = -124.7844079 # west long
right = -66.9513812 # east long
bottom =  24.7433195 # south lat
 
def is_Continental(lat,lng): # 
    if bottom <= lat <= top and left <= lng <= right:
        return True
    return False
            
# funcs from OpenStreetMap
def merc_x(lon):
  r_major=6378137.000
  return r_major*math.radians(lon)
 
def merc_y(lat):
  if lat>89.5:lat=89.5
  if lat<-89.5:lat=-89.5
  r_major=6378137.000
  r_minor=6356752.3142
  temp=r_minor/r_major
  eccent=math.sqrt(1-temp**2)
  phi=math.radians(lat)
  sinphi=math.sin(phi)
  con=eccent*sinphi
  com=eccent/2
  con=((1.0-con)/(1.0+con))**com
  ts=math.tan((math.pi/2-phi)/2)/con
  y=0-r_major*math.log(ts)
  return y

def joinTables (fname1, fname2):
    t1 = [i.strip().split() for i in open(fname1).readlines()]
    t2 = [i.strip().split() for i in open(fname2).readlines()]
    merged = list()
    for i in t1:
        result = [element for element in t2 if element[0] == i[0]]
        if (len(result)>0):
            merged.append([i[0],float(i[1]),float(result[0][1]),float(result[0][2])])
    return merged

def mercatorize (t):
    return [(merc_x(i[3]),merc_y(i[2]),i[1]) for i in t if is_Continental(i[2],i[3])]
    

tbl = mercatorize(joinTables("results/us_corr.txt","results/us_coords.txt"))
x = [i[0] for i in tbl]
y = [i[1] for i in tbl]
z = [i[2] for i in tbl]

mx  = max(x)
_mx = min(x)
my  = max(y)
_my = min(y)

# define grid
xi = np.linspace(_mx, mx, 2000)
yi = np.linspace(_my, my, 3000)

# grid the data.
zi = griddata(x, y, z, xi, yi, interp='linear')

# contour the gridded data, plotting dots at the nonuniform data points.
#CS = plt.contour(xi, yi, zi, 15, linewidths=0.5, colors='k')
CS = plt.contourf(xi, yi, zi, 15, cmap=plt.cm.rainbow,
                  vmax=abs(zi).max(), vmin=-abs(zi).max())

plt.colorbar()  # draw colorbar

plt.show()
