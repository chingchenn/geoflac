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
model='w0506'

path = '/home/jiching/geoflac/'+model+'/'
os.chdir(path)
fl = flac.Flac()
end = fl.nrec
nex = fl.nx - 1
nez = fl.nz - 1
strength_profile=317  # xindex of zcolumn
def get_strength(xindex,frame=end,edot=1e-15,g=9.81):
    def nodes_to_elements(xmesh,zmesh,frame):
        ele_x = (xmesh[:fl.nx-1,:fl.nz-1] + xmesh[1:,:fl.nz-1] + xmesh[1:,1:] + xmesh[:fl.nx-1,1:]) / 4.
        ele_z = (zmesh[:fl.nx-1,:fl.nz-1] + zmesh[1:,:fl.nz-1] + zmesh[1:,1:] + zmesh[:fl.nx-1,1:]) / 4.
        return ele_x, ele_z
    x,z = fl.read_mesh(frame) #node
    ele_x,ele_z=nodes_to_elements(x,z,frame) #element
    visc=fl.read_visc(frame) #element
    strainrate=fl.read_srII(frame) #element
    density = fl.read_density(frame) #element
    pressure=fl.read_pres(frame) #element

    ## get zcolumn data [in x index] of different field 
    ve = 10**visc[xindex,:]
    se = 10**strainrate[xindex,:]
    pe = pressure[xindex,:]
    dddepth=ele_z[xindex,:]
    depth=dddepth-dddepth[0]
    dene=density[xindex,:]
    ## interp in different field by depth
    zmin=depth[0]
    zmax=depth[-1]
    pz = np.linspace(zmin,zmax,5*(fl.nz-1))
    v = np.interp(pz,depth,ve)
    s = np.interp(pz,depth,se)
    p = np.interp(pz,depth,pe)
    den = np.interp(pz,depth,dene)
    ##
    ## calculate strength 
    visco_strength=2.0 * v * edot
    visco_strength2=2.0 * v * s

    frico_strength = -p * np.tan(np.pi*(30.0/180.0))
    frico_strength2 = -pz  * den * g * np.tan(np.pi*(30.0/180.0))

    #-------------------
    visco_strength=visco_strength/1e8
    frico_strength2=frico_strength2/1e3
    #-------------------
    return visco_strength, firco_strength2 

if strength_profile:
    visco_strength, frico_strength = get_strength(strength_profile,frame=end,edot=1e-15,g=9.81):
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
    fig.savefig('/home/jiching/geoflac/figure/'+str(model)+'_'+str(frame)+str(strength_profile)+'strengthfortest'+'.png')
