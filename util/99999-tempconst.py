#!/usr/bin/env python
import math
import flac
import os,sys
import numpy as np
from matplotlib import cm
import matplotlib.pyplot as plt
model = str(sys.argv[1])
path = '/home/jiching/geoflac/'+model+'/'
#path = '/scratch2/jiching/'+model+'/'
os.chdir(path)
fl = flac.Flac();end = fl.nrec
nex = fl.nx - 1;nez = fl.nz - 1
fig, (ax,ax2)= plt.subplots(2,1,figsize=(10,12))

phase_oceanic = 3
phase_ecolgite = 13
phase_oceanic_1 = 17
phase_ecolgite_1 = 18
angle = np.zeros(end)

rainbow = cm.get_cmap('gray_r',end)
newcolors = rainbow(np.linspace(0, 1, end))

for i in range(1,end):
    x, z = fl.read_mesh(i)
    ele_x = (x[:fl.nx-1,:fl.nz-1] + x[1:,:fl.nz-1] + x[1:,1:] + x[:fl.nx-1,1:]) / 4.
    ele_z = (z[:fl.nx-1,:fl.nz-1] + z[1:,:fl.nz-1] + z[1:,1:] + z[:fl.nx-1,1:]) / 4.
    phase = fl.read_phase(i)
    trench_ind = np.argmin(z[:,0])
    temp = fl.read_temperature(i)
    if z[trench_ind,0] > -2:  
        print (i)
        continue
    crust_x = np.zeros(nex)
    crust_z = np.zeros(nex)
    for j in range(trench_ind,nex):
        ind_oceanic = (phase[j,:] == phase_oceanic) + (phase[j,:] == phase_ecolgite)+(phase[j,:] == phase_oceanic_1) + (phase[j,:] == phase_ecolgite_1)
        if True in ind_oceanic:
            crust_x[j] = np.average(ele_x[j,ind_oceanic])
            crust_z[j] = np.average(ele_z[j,ind_oceanic])
    ax.plot(crust_x[crust_z < 0],crust_z[crust_z < 0],color=newcolors[i],zorder=1)
    
    ind_within_80km = (crust_z >= -80) * (crust_z < -25)
    if not True in (crust_z < -80):
        continue

    crust_xmin = np.amin(crust_x[ind_within_80km])
    crust_xmax = np.amax(crust_x[ind_within_80km])
    crust_zmin = np.amin(crust_z[ind_within_80km])
    crust_zmax = np.amax(crust_z[ind_within_80km])
    dx = crust_xmax - crust_xmin
    dz = crust_zmax - crust_zmin
    angle[i] = math.degrees(math.atan(dz/dx))
ax.plot([100,600],[-100,-100],'--',zorder=0,color='grey')
ax.set_aspect('equal')
ax.set_xlabel('Distance (km)')
ax.set_ylabel('Depth (km)')
# ax.set_xlim(100,600)
ax.set_title('Geometry of Subducted Slab')

ax2.plot(fl.time[angle>0],angle[angle>0],c='blue',lw=2)
# ax2.set_xlim(0,24)
ax2.set_xticks(np.linspace(0,30,6))
# ax2.set_ylim(15,30)
ax2.set_title('Angle Variation')
ax2.set_xlabel('Time (Myr)')
ax2.set_ylabel('Angel ($^\circ$)')
#plt.savefig('/home/jiching/geoflac/'+'figure/'+model+'_tempdip.jpg')
