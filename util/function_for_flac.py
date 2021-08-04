#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Thu May  8 13:28:16 2021

@author: jiching
"""

import flac
import sys,os, math
import numpy as np
import function_savedata as fs

sys.path.append('/home/jiching/geoflac/util')

def get_topo(xmesh,zmesh,frame):
    xtop=xmesh[:,0]
    ztop=zmesh[:,0]
    return xtop,ztop

def find_trench_index(z):
    zz = z[:,0]
    imax = zz.argmax()
    i = zz[:imax].argmin()
    return imax,i
"""   
def nodes_to_elements(xmesh,zmesh,frame):
    ele_x = (x[:fl.nx-1,:fl.nz-1] + x[1:,:fl.nz-1] + x[1:,1:] + x[:fl.nx-1,1:]) / 4.
    ele_z = (z[:fl.nx-1,:fl.nz-1] + z[1:,:fl.nz-1] + z[1:,1:] + z[:fl.nx-1,1:]) / 4.
    return ele_x, ele_z
"""
def read_depth(z_array,x_index,z_index):
    depth=z_array[x_index,0]-z_array[x_index,z_index]
    return depth

def read_area(xmesh,zmesh,x_index,z_index):
    x1 = xmesh[x_index,z_index]
    y1 = zmesh[x_index,z_index]
    x2 = xmesh[x_index,z_index+1]
    y2 = zmesh[x_index,z_index+1]
    x3 = xmesh[x_index+1,z_index+1]
    y3 = zmesh[x_index+1,z_index+1]
    x4 = xmesh[x_index+1,z_index]
    y4 = zmesh[x_index+1,z_index]
    area1 = ((x1-x2)*(y3-y2))-((x3-x2)*(y1-y2))
    area2 = ((x1-x4)*(y3-y4))-((x3-x4)*(y1-y4))    
    area = (abs(area1)+abs(area2))*0.5           
    return area
"""
def read_time(start_vts,model_steps):
    timestep=[0]
    for step in range(start_vts,model_steps+1):
        timestep.append(fl.time[step])
    # timestep=np.array(timestep)
    return timestep
"""

#find melt element
def melt_element(xmesh,zmesh,frame,mm):
    melt_xele=[]
    melt_zele=[]
    melt_number=[]
    for xx in range(len(mm)):
        for zz in range(len(mm[0])):
            if mm[xx,zz] != 0:
                melt_xele.append(xx)
                melt_zele.append(zz)
                melt_number.append(mm[xx,zz])
    return melt_xele,melt_zele,melt_number

def chamber_element(xmesh,zmesh,frame,mm):
    chamber_xele=[]
    chamber_zele=[]
    chamber_number=[]
    for xx in range(len(mm)):
        for zz in range(len(mm[0])):
            if mm[xx,zz] != 0:
                chamber_xele.append(xx)
                chamber_zele.append(zz)
                chamber_number.append(mm[xx,zz])
    return chamber_xele,chamber_zele,chamber_number

def moving_window_smooth(array,window_width):
    new_array=[0]
    temp=int(window_width/2)    
    for kk in range(2,temp+1):
        new_array.append(array[kk-1])
    for kk in range(temp,len(array)-(temp)):
        q=sum(array[kk-temp:kk+temp+1])/window_width
        new_array.append(q)
    for kk in range((len(array)-temp+1),len(array)+1):
        new_array.append(array[kk-1])
    return new_array
