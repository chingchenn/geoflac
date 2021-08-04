#!/usr/bin/env python
import math
import flac
import os,sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
from matplotlib import cm
import matplotlib.pyplot as plt
import function_for_flac as f2
model_list=['w0410','w0412','w0506','w0413','w0538','w0537','w0414','w0415','w0540','w0541','w0542','w0543']
name_list=['50-5.5','60-5.5','70-5.5','80-5.5','50-6.5','55-6.5','60-6.5','70-6.5','55-7.5','60-7.5','70-7.5','80-7.5']
rainbow = cm.get_cmap('rainbow',len(model_list))
newcolors = rainbow(np.linspace(0, 1, len(model_list)))
case =sys.argv[1]
if int(case)==1:
    print(11111111111111111)
    fig, (ax2)= plt.subplots(1,1,figsize=(13,8))
if int(case)==2: 
    print(22222222222222222)
    fig, (ax,ax2)= plt.subplots(2,1,figsize=(10,10))
for qq,model in enumerate(model_list):
    path = '/scratch2/jiching/'+model+'/'
    os.chdir(path)
    fl = flac.Flac();end = fl.nrec
    nex = fl.nx - 1;nez = fl.nz - 1
    
    phase_oceanic = 3
    phase_ecolgite = 13
    phase_oceanic_1 = 17
    phase_ecolgite_1 = 18
    angle = np.zeros(end)


    for i in range(1,end):
        x, z = fl.read_mesh(i)
        ele_x = (x[:fl.nx-1,:fl.nz-1] + x[1:,:fl.nz-1] + x[1:,1:] + x[:fl.nx-1,1:]) / 4.
        ele_z = (z[:fl.nx-1,:fl.nz-1] + z[1:,:fl.nz-1] + z[1:,1:] + z[:fl.nx-1,1:]) / 4.
        phase = fl.read_phase(i)
        trench_ind = np.argmin(z[:,0]) 
        crust_x = np.zeros(nex)
        crust_z = np.zeros(nex)
        for j in range(trench_ind,nex):
            ind_oceanic = (phase[j,:] == phase_oceanic) + (phase[j,:] == phase_ecolgite)+(phase[j,:] == phase_oceanic_1) + (phase[j,:] == phase_ecolgite_1)
            if True in ind_oceanic:
                crust_x[j] = np.average(ele_x[j,ind_oceanic])
                crust_z[j] = np.average(ele_z[j,ind_oceanic])

        ind_within_80km = (crust_z >= -80) * (crust_z < -5)
        if not True in (crust_z < -80):
            continue
    
        crust_xmin = np.amin(crust_x[ind_within_80km])
        crust_xmax = np.amax(crust_x[ind_within_80km])
        crust_zmin = np.amin(crust_z[ind_within_80km])
        crust_zmax = np.amax(crust_z[ind_within_80km])
        dx = crust_xmax - crust_xmin
        dz = crust_zmax - crust_zmin
        angle[i] = math.degrees(math.atan(dz/dx))
    if int(case)==2:
        nnewangle = f2.moving_window_smooth(angle[angle>0],2)
        ax.plot(fl.time[angle>0],nnewangle,c=newcolors[qq],lw=2,label=name_list[qq])
        ax.legend(title = "convergent velocity mm/year")
        ax.set_xlim(0,40)
        ax.set_title('Angle Variation')
        ax.set_ylabel('Angel ($^\circ$)')
        ax.grid(axis='both',linestyle='dotted')
    ax2.plot(fl.time[angle>0],angle[angle>0],c=newcolors[qq],lw=2,label=name_list[qq])
    ax2.legend(title = "velocity mm/year",fontsize = 8)
    ax2.set_xlim(0,40)
    #ax2.set_xticks(np.linspace(0,31,10))
    # ax2.set_ylim(15,30)
    ax2.set_xlabel('Time (Myr)')
    ax2.set_ylabel('Angel ($^\circ$)')
    ax2.grid(axis='both',linestyle='dotted')
    ax2.set_title('Angle Variation')
plt.savefig('/home/jiching/geoflac/'+'figure/'+'convergent dip.png')
