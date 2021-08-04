#!/usr/bin/env python
import math
import flac
import os,sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
from matplotlib import cm
import matplotlib.pyplot as plt

#model_list=['w0524','w0525','w0526','w0527','w0528','w0529','w0530','w0531','w0532']
model_list=['w0506','w0544','w0545']
rainbow = cm.get_cmap('rainbow',len(model_list))
newcolors = rainbow(np.linspace(0, 1, len(model_list)))
fig, (ax,ax2)= plt.subplots(2,1,figsize=(15,8))
for qq,model in enumerate(model_list):
    #path = '/scratch2/jiching/'+model+'/'
    path = '/home/jiching/geoflac/'+model+'/'
    os.chdir(path)
    fl = flac.Flac();end = fl.nrec
    nex = fl.nx - 1;nez = fl.nz - 1
    melt = np.zeros(end)
    magma = np.zeros(end)
    time=np.zeros(end)
    for i in range(1,end):
        mm=fl.read_fmelt(i)
        chamber=fl.read_chamber(i)
        melt[i]=np.max(mm)
        magma[i]=np.max(chamber)
        
    ax.plot(fl.time,melt,c=newcolors[qq],label=model)
    ax2.plot(fl.time,magma,c=newcolors[qq],label=model)
#    ax2.set_yscale('log')
    ax2.legend(title = "model",fontsize = 12) 
    print(model)
fig.savefig('/home/jiching/geoflac/magma.png')
