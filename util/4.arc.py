#!/usr/bin/env python
import math
import time
import flac
import os,sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
from matplotlib import cm
import function_for_flac as f2
import matplotlib.pyplot as plt
fig, (ax,ax2,ax3,ax4)= plt.subplots(4,1,figsize=(15,15))
start = time.time()
model = str(sys.argv[1]) 
path = '/home/jiching/geoflac/'+model+'/'
os.chdir(path)
fl = flac.Flac();end = fl.nrec
nex = fl.nx - 1;nez = fl.nz - 1
melt = np.zeros(end)
magma = np.zeros(end)
kkmelt = np.zeros(end)
kkchamber=np.zeros(end)
rrr=np.zeros(end)
for i in range(1,end):
    mm=fl.read_fmelt(i)
    chamber=fl.read_chamber(i)
    melt[i]=np.max(mm)
    magma[i]=np.max(chamber)
    x,z=fl.read_mesh(i)
    mm=fl.read_fmelt(i)
    cc=fl.read_chamber(i)
    tempmagma=np.max(chamber)
    tempmelt=np.max(mm)
    if tempmagma !=0:
        rrr[i]=tempmelt/tempmagma
    kkmelt[i]=(fl.read_fmelt(i)*fl.read_area(i)/1e6).sum()
    kkchamber[i]=(fl.read_chamber(i)*fl.read_area(i)/1e6).sum()
ax.plot(fl.time,kkmelt,color='tomato')
ax2.plot(fl.time,kkchamber,color='orange')
ax3.bar(fl.time,melt,width=0.1,color='tomato')
ax4.bar(fl.time,magma,width=0.1,color='orange')
ax.set_title('melt * area',fontsize=20)
ax2.set_title('magma friction * area',fontsize=20)
ax3.set_title('max melt fraction',fontsize=20)
ax4.set_title('max chamber fraction',fontsize=20)
ax.set_ylim(0,0.8)
ax2.set_ylim(0,10*1e-3)
ax3.set_ylim(0,10*1e-3)
ax4.set_ylim(0,3*1e-5)
ax.set_xlim(0,40)
ax2.set_xlim(0,40)
ax3.set_xlim(0,40)
ax4.set_xlim(0,40)

fig2,(ax,ax2)=plt.subplots(1,2,figsize=(25,12))
cb_plot=ax.scatter(melt,magma,c=fl.time,cmap='rainbow')
ax_cbin = fig2.add_axes([0.13, 0.78, 0.23, 0.03])
cb = fig2.colorbar(cb_plot,cax=ax_cbin,orientation='horizontal')
ax_cbin.set_title('Myr (km)')
rrr1=f2.moving_window_smooth(rrr,12)
ax2.plot(fl.time,rrr1,color='k',lw=3)
ax2.plot(fl.time,rrr,color='gray',linestyle=':')
end = time.time()
print(end - start)
fig.savefig('/home/jiching/geoflac/figure/'+model+'_magma_parameter_time_series.png')
fig2.savefig('/home/jiching/geoflac/figure/'+model+'_max_ratio.png')
