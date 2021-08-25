#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 10 13:11:24 2021
@author: jiching
"""
import flac
import os,sys
import numpy as np
import pandas as pd
import gravity as fg
import matplotlib
matplotlib.use('Agg')
from matplotlib import cm
import function_savedata as fs
import function_for_flac as f2
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure


#---------------------------------- DO WHAT -----------------------------------
## creat data
vtp = 0
trench_location = 0
magma = 1
gravity = 0
gravity_frame=0
# plot data
trench_plot = 0
magma_plot = 1
marker_number = 0
gravity_plot = 0
phase_plot=0
phase_accre = 0

#---------------------------------- setting -----------------------------------
path = '/home/jiching/geoflac/'
#path = '/scratch2/jiching/'
savepath='/home/jiching/geoflac/data/'
figpath='/home/jiching/geoflac/figure/'
sys.path.append("/home/jiching/geoflac/util")
model = sys.argv[1]
os.chdir(path+model)

fl = flac.Flac()
end = fl.nrec
nex = fl.nx - 1
nez = fl.nz - 1
#------------------------------------------------------------------------------

def read_time(start_vts,model_steps):
    timestep=[0]
    for step in range(start_vts,model_steps+1):
        timestep.append(fl.time[step])
    # timestep=np.array(timestep)
    return timestep
time=read_time(1,end-1)
def trench(start_vts=1,model_steps=end):
    trench_x=[0]
    trench_z=[0]
    trench_index=[0]
    for i in range(start_vts,model_steps):
        x,z = fl.read_mesh(i+1)
        sx,sz=f2.get_topo(x,z,i+1)
        arc_ind,trench_ind=f2.find_trench_index(z)
        trench_index.append(sx[trench_ind])
        trench_x.append(sx[trench_ind])
        trench_z.append(sx[trench_ind])
    return trench_index,trench_x,trench_z
def get_topo(start=1,end_frame=end):
    topo = [];dis = [];time = []
    trench_index, xtrench, ztrench=trench(start,end_frame)
    for step in range(start,end_frame):
        x,z = fl.read_mesh(step+1)
        sx,sz=f2.get_topo(x,z,step+1)
        topo.append(sz) 
        dis.append(sx)
        for ii in range(len(sx)):
            time.append(fl.time[step])
    return  dis, time,topo
trenchfile=path+'data/trench_for_'+model+'.csv'
def nodes_to_elements(xmesh,zmesh,frame):
    ele_x = (xmesh[:fl.nx-1,:fl.nz-1] + xmesh[1:,:fl.nz-1] + xmesh[1:,1:] + xmesh[:fl.nx-1,1:]) / 4.
    ele_z = (zmesh[:fl.nx-1,:fl.nz-1] + zmesh[1:,:fl.nz-1] + zmesh[1:,1:] + zmesh[:fl.nx-1,1:]) / 4.
    return ele_x, ele_z
def plot_phase_in_depth(depth=0):
    time=[];ph=[];xx=[]
    for step in range(end):
        x, z = fl.read_mesh(step+1)
        phase=fl.read_phase(step+1)
        ele_x, ele_z = nodes_to_elements(x,z,step)
        xt = ele_x[:,0]
        zt = ele_z[:,0]
        pp = np.zeros(xt.shape)
        t = np.zeros(zt.shape)
        t[:]=fl.time[step]
        for gg in range(len(ele_z)):
            pp[gg]=phase[gg,depth]
        time.append(t)
        ph.append(pp)
        xx.append(xt)
    return xx, time, ph
def get_gravity(start=1,end_frame=end):
    fa=[];bg=[];dis=[];time=[];to=[];tom=[]
    for step in range(start+1,end_frame+1):
        px, topo, topomod, fa_gravity, gb_gravity=fg.compute_gravity2(step)
        px *= 10**-3
        topo *= 10**-3
        topomod *=10**-3
        fa_gravity *= 10**5
        gb_gravity *= 10**5
        if gravity_frame:
            if not os.path.exists(savepath+model):
                os.makedirs(savepath+model)
            fs.save_5array('topo-grav.'+str(step), savepath+model, px, topo, topomod, fa_gravity,
                           gb_gravity, 'disX', 'topo', 'topomod', 'free-air', 'bourger')
        fa.append(fa_gravity)
        bg.append(gb_gravity)
        dis.append(px)
        to.append(topo)
        tom.append(topomod)
        for yy in range(len(px)):
            time.append(fl.time[step])
    return dis,time,to,tom,fa,bg
def get_magma(start_vts=1,model_steps=end-1):
    melt=np.zeros(end)
    magma=np.zeros(end)
    yymelt=np.zeros(end)
    yychamber=np.zeros(end)
    rrr=np.zeros(end)
    for i in range(1,end):
        x,z=fl.read_mesh(i)
        mm=fl.read_fmelt(i)
        chamber=fl.read_fmagma(i)
        melt[i] = np.max(mm)
        magma[i] = np.max(chamber)
        if np.max(chamber) !=0:
            rrr[i]=np.max(mm)/np.max(chamber)
        yymelt[i]=(fl.read_fmelt(i)*fl.read_area(i)/1e6).sum()
        yychamber[i]=(fl.read_fmagma(i)*fl.read_area(i)/1e6).sum()
    return melt,magma,yymelt,yychamber,rrr
magmafile=path+'data/magma_for_'+model+'.csv' 
def count_marker(phase,start=1,end_frame=end):
    mr = np.zeros(end_frame-start)
    for i in range(start,end_frame):
        x,y,age,ph,id=fl.read_markers(i)
        ppp=(ph==phase)
        select1 = id[ppp]
        if len(select1)==0:
            continue
        xk,yk,dk,phk,idk=fl.read_markers(i+1)
        count = 0
        ind_p = idk[(phk==phase)]
        for j in select1:
            if j in ind_p:
                count += 1
        mr[end_frame-i-1]=count   
    return mr
#------------------------------------------------------------------------------
if vtp:
   file=path+model
   cmd = '''
cd %(file)s 
python /home/jiching/geoflac/util/flacmarker2vtk.py . -1
''' % locals()
   os.system(cmd)
# if not os.path.exists(trenchfile):

if trench_location:
    print('-----creat trench database-----')
    name='trench_for_'+model
    trench_index,trench_x,trench_z=trench()
    fs.save_3array(name,savepath,time,trench_x,trench_z,
                'time','trench_x','trench_z')
    print('=========== DONE =============')
if gravity:
    print('-----creat gravity database----- ')
    name='gravity_all_'+model
    dis,time,to,tom,fa,bg=get_gravity()
    fs.save_6array(name, savepath, time, dis, to, tom, fa, bg,
                   'time', 'disX', 'topo', 'topomod', 'free-air', 'bourger')
    print('=========== DONE =============')
# if not os.path.exists(magmafile):
if magma:
    print('-----creat magma database-----')
    name='magma_for_'+model
    melt,chamber,yymelt,yychamber,rrr=get_magma()      
    fs.save_6array(name,savepath,time,melt,chamber,yymelt,yychamber,rrr,
                   'time','fmelt','chamber','production','volume','ratio')
    print('=========== DONE =============')

##------------------------------------ plot -----------------------------------
if trench_plot:
    name='trench_for_'+model
    df = pd.read_csv(path+'data/'+name+'.csv')
    fig, (ax)= plt.subplots(1,1,figsize=(10,12))
    dis,time,topo=get_topo(start=1,end_frame=end)
    qqq=ax.scatter(dis,time,c=topo,cmap='gist_earth',vmax=8,vmin=-10)
    cbar=fig.colorbar(qqq,ax=ax)
    ax.plot(df.trench_x,df.time,c='k',lw=2)
    ax.set_xlim(0,dis[-1][-1])
    ax.set_ylim(0,40)
    ax.set_ylabel('Time (Myr)',fontsize=20)
    ax.set_xlabel('distance (km)',fontsize=20)
    cbar.set_label('topography (km)',fontsize=20)
    plt.savefig(figpath+model+'_topo.jpg')
if magma_plot:
    name='magma_for_'+model
    df = pd.read_csv(path+'data/'+name+'.csv')
    fig, (ax,ax2,ax3,ax4) = plt.subplots(4,1,figsize=(15,15))
    ax.plot(df.time,df.production,color='tomato')
    ax2.plot(df.time,df.volume,color='orange')
    ax3.bar(df.time,df.fmelt,width=0.1,color='tomato',label='fmelt')
    ax4.bar(df.time,df.chamber,width=0.1,color='orange',label='magma')
    #ax.set_xlabel('Time (Myr)',fontsize=20)
    #ax2.set_xlabel('Time (Myr)',fontsize=20)
    #ax3.set_xlabel('Time (Myr)',fontsize=20)
    ax4.set_xlabel('Time (Myr)',fontsize=20)
    ax.set_ylabel('melt * area',fontsize=20)
    ax2.set_ylabel('chamber *area',fontsize=20)
    ax3.set_ylabel('max melt',fontsize=20)
    ax4.set_ylabel('max magma fraction',fontsize=20)
    #ax.set_ylim(0,0.8)
    #ax2.set_ylim(0,10*1e-3)
    #ax3.set_ylim(0,10*1e-3)
    #ax4.set_ylim(0,3*1e-5)
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
    fig.savefig(figpath+model+'_magma.png')
#--------------------------------------------------------------------
'''
    fig2,(ax,ax2)=plt.subplots(1,2,figsize=(25,8))
    cb_plot=ax.scatter(df.fmelt,df.chamber,c=df.time,cmap='rainbow')
    ax_cbin =fig2.add_axes([0.13,0.78,0.23,0.03]) 
    cb = fig2.colorbar(cb_plot,cax=ax_cbin,orientation='horizontal')
    ax_cbin.set_title('Myr')
    rrr1=f2.moving_window_smooth(df.ratio,10)
    ax2.plot(df.time,rrr1,color='k',lw=3)
    ax2.plot(df.time,df.ratio,color='gray',linestyle=':')
    ax.set_ylim(0,max(df.chamber))
    ax.set_xlim(0,max(df.fmelt))
    ax.set_ylabel('max magma fraction')
    ax.set_xlabel('max melt fraction')
    ax2.set_xlabel('Myr')
    ax2.set_ylim(0,max(df.ratio))
    ax2.set_xlim(0,max(df.time))
    fig2.savefig(figpath+model+'_ratio.png')
'''
#--------------------------------------------------------------------
if marker_number != 0:
    mr = count_marker(marker_number)
    #plt.plot(mr,c='b')
if gravity_plot:
    name='gravity_for_'+model
    fig, (ax,ax2)= plt.subplots(1,2,figsize=(22,12)) 
    dis,time,to,tom,fa,bg=get_gravity(1,end)
    qqq=ax.scatter(dis,time,c=fa,cmap='Spectral',vmax=400,vmin=-400)
    ax2.scatter(dis,time,c=bg,cmap='Spectral',vmax=400,vmin=-400)
    fig.colorbar(qqq,ax=ax)
    ax2.set_title('bourger gravoty anomaly')
    ax.set_title('free-air gravity anomaly')
    plt.savefig(figpath+model+'_gravity.jpg')
if phase_plot:
    name = 'phase_for'+model
    fig, (ax)= plt.subplots(1,1,figsize=(10,12))
    colors = ["#CECCD0","#FF00FF","#8BFF8B","#7158FF","#FF966F",
          "#9F0042","#660000","#524B52","#D14309","#5AB245",
          "#004B00","#008B00","#455E45","#B89FCE","#C97BEA",
          "#525252","#FF0000","#00FF00","#FFFF00","#7158FF"]
    phase15= matplotlib.colors.ListedColormap(colors)
    xt,t,pp= plot_phase_in_depth(depth=0)    
    mmm=ax.scatter(xt,t,c=pp,cmap=phase15,vmin=1, vmax=18)
    ax.set_ylabel("Time (Ma)")
    ax.set_xlabel("Distance (km)")
    ax.set_title(str(model)+" Phase")
    ax.set_ylim(0,t[-1][-1])
    ax.set_xlim(xt[0][0],xt[-1][-1])
    cb_plot1 = ax.scatter([-1],[-1],s=0.1,c=[1],cmap=phase15,vmin=1, vmax=18)
    ax_cbin = fig.add_axes([0.27, 0.03, 0.23, 0.03])
    cb = fig.colorbar(cb_plot1,cax=ax_cbin,orientation='horizontal')
    ax_cbin.set_title('Phase')
    fig.savefig(figpath+model+'_phase.jpg')
if phase_accre:
    name='trench_for_'+model
    df = pd.read_csv(path+'data/'+name+'.csv')
    fig, (ax)= plt.subplots(1,1,figsize=(10,12))
    dis,time,topo=get_topo(start=1,end_frame=end)
    colors = ["#CECCD0","#FF00FF","#8BFF8B","#7158FF","#FF966F",
          "#9F0042","#660000","#524B52","#D14309","#5AB245",
          "#004B00","#008B00","#455E45","#B89FCE","#C97BEA",
          "#525252","#FF0000","#00FF00","#FFFF00","#7158FF"]
    phase15= matplotlib.colors.ListedColormap(colors)
    xt,t,pp= plot_phase_in_depth(depth=0)
    mmm=ax.scatter(xt,t,c=pp,cmap=phase15,vmin=1, vmax=18)
    ax.set_ylabel("Time (Ma)")
    ax.set_xlabel("Distance (km)")
    ax.set_title(str(model)+" Phase")
    ax.set_ylim(0,t[-1][-1])
    ax.set_xlim(xt[0][0],xt[-1][-1])
    cb_plot1 = ax.scatter([-1],[-1],s=0.1,c=[1],cmap=phase15,vmin=1, vmax=18)
    ax_cbin = fig.add_axes([0.27, 0.03, 0.23, 0.03])
    cb = fig.colorbar(cb_plot1,cax=ax_cbin,orientation='horizontal')
    ax_cbin.set_title('Phase')
    ax.plot(df.trench_x,df.time,c='k',lw=2)    
    fig.savefig(figpath+model+'_acc.jpg')
