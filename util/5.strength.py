#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 15 17:01:45 2021

@author: jiching
"""
import flac
import math
import os,sys
import numpy as np
import pandas as pd
import matplotlib
from math import sqrt
from scipy.special import erf
from matplotlib import cm
import function_savedata as fs
import function_for_flac as f2
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
print('wwwww')
model='w0533'
yy=70
path = '/home/jiching/geoflac/'+model+'/'
os.chdir(path)
fl = flac.Flac()
end = fl.nrec
nex = fl.nx - 1
nez = fl.nz - 1
frame=end

def read_depth(zmesh,x_index,z_index):
    depth=zmesh[x_index,0]-zmesh[x_index,z_index]
    return depth
def nodes_to_elements(xmesh,zmesh,frame):
    ele_x = (xmesh[:fl.nx-1,:fl.nz-1] + xmesh[1:,:fl.nz-1] + xmesh[1:,1:] + xmesh[:fl.nx-1,1:]) / 4.
    ele_z = (zmesh[:fl.nx-1,:fl.nz-1] + zmesh[1:,:fl.nz-1] + zmesh[1:,1:] + zmesh[:fl.nx-1,1:]) / 4.
    return ele_x, ele_z
x,z=fl.read_mesh(frame)
ele_x,ele_z=nodes_to_elements(x,z,frame)
temp=fl.read_temperature(frame) #on node
phase =fl.read_phase(frame) #on element
visc=fl.read_visc(frame)
strainrate=fl.read_srII(frame)
edot= 1e-15
density = fl.read_density(frame)
g=9.81
pressure=fl.read_pres(frame)
pres = density * g 

v = 10**visc[yy,:]
s = 10**strainrate[yy,:]
p = pressure[yy,:]
dddepth=ele_z[yy,:]
depth=dddepth-dddepth[0]
den=density[yy,:]
visco_strength=2.0 * v * edot
# visco_strength=2.0 * v * s

frico_strength = -p * np.tan(np.pi*(30.0/180.0))
frico_strength2 = -depth  * den * g * np.tan(np.pi*(30.0/180.0))

#-------------------
visco_strength=visco_strength/1e8
frico_strength2=frico_strength2/1e3
#-------------------

fig, ax = plt.subplots(1,1,figsize=(6,10))
applied_strength = np.amin((visco_strength,frico_strength2),axis=0)
ax.plot(visco_strength,depth,'--r',alpha=0.5)
ax.plot(frico_strength2,depth,'--b',alpha=0.5)
ax.plot(applied_strength,depth,'k',lw=3)
ax.set_ylim(-80,0)
ax.set_xlim(0,1000)
ax.set_title('Rock Strength',fontsize=26)
ax.set_xlabel('Strength (MPa)',fontsize=22)
ax.set_ylabel('Depth (km)',fontsize=22)
ax.grid()
fig.savefig('/home/jiching/geoflac/figure/'+str(model)+'_'+str(yy)+'strength'+'.png')
