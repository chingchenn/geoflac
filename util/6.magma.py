#!/usr/bin/env python
import math
import flac
import os,sys
import numpy as np
from matplotlib import cm
import creat_database as cd
import matplotlib.pyplot as plt
model = str(sys.argv[1])
path = '/home/jiching/geoflac/'+model+'/'
#path = model
print(model)
os.chdir(path)
fl = flac.Flac();end = fl.nrec
nex = fl.nx - 1;nez = fl.nz - 1
def get_magma(start_vts=1,model_steps=end-1):
    melt=np.zeros(end)
    magma=np.zeros(end)
    yymelt=np.zeros(end)
    yychamber=np.zeros(end)
    arc_vol=np.zeros(end)
    for i in range(1,end):
        x,z=fl.read_mesh(i)
        phase = fl.read_phase(i)
        mm=fl.read_fmelt(i)
        chamber=fl.read_fmagma(i)
        melt[i] = np.max(mm)
        magma[i] = np.max(chamber)
        arc_vol[i]=np.sum(fl.read_area(i)[phase ==14])/1e6
        yymelt[i]=(fl.read_fmelt(i)*fl.read_area(i)/1e6).sum()
        yychamber[i]=(fl.read_fmagma(i)*fl.read_area(i)/1e6).sum()
    return melt,magma,yymelt,yychamber,arc_vol
time =cd.read_time(1,end-1) 
melt,magma,yymelt,yychamber,arc_vol=get_magma(1,end)
fig, (ax,ax2,ax3,ax4) = plt.subplots(4,1,figsize=(15,15))
ax.bar(time,yymelt,width=0.1,color='tomato')
ax2.plot(time,yychamber,color='orange')
ax3.bar(time,melt,width=0.1,color='tomato',label='fmelt')
ax4.plot(time,arc_vol,color='orange',label='magma')
#ax.set_xlabel('Time (Myr)',fontsize=20)
#ax2.set_xlabel('Time (Myr)',fontsize=20)
#ax3.set_xlabel('Time (Myr)',fontsize=20)
ax4.set_xlabel('Time (Myr)',fontsize=20)
ax.set_ylabel('melt * area',fontsize=20)
ax2.set_ylabel('chamber *area',fontsize=20)
ax3.set_ylabel('max melt',fontsize=20)
ax4.set_ylabel('arc area',fontsize=20)
ax.set_ylim(0,2)
ax2.set_ylim(0,500)
ax3.set_ylim(0,0.04)
ax4.set_ylim(0,160)
ax.set_xlim(0,24)
ax2.set_xlim(0,24)
ax3.set_xlim(0,24)
ax4.set_xlim(0,24)
ax.grid()
ax2.grid()
ax3.grid()
ax4.grid()
ax.tick_params(axis='x', labelsize=16 )
ax2.tick_params(axis='x', labelsize=16 )
ax3.tick_params(axis='x', labelsize=16 )
ax4.tick_params(axis='x', labelsize=16 )
ax.tick_params(axis='y', labelsize=16 )
ax2.tick_params(axis='y', labelsize=16 )
ax3.tick_params(axis='y', labelsize=16 )
ax4.tick_params(axis='y', labelsize=16 )
ax.set_title('Model : '+model,fontsize=25)
fig.savefig('/home/jiching/geoflac/figure/'+model+'_arc+magma.png')
