# -*- coding: utf-8 -*-
"""
Created on Thu Jul 15 13:43:54 2021

@author: 88691
"""

import sys
sys.path.append('/home/summer-tan2/Wang,_Yu_Hsiang/geoflac/util')

import flac
import numpy as np
from matplotlib import pyplot as plt

fl=flac.Flac()

stat=0
while stat!=1:
    while stat!=1:
        while stat!=1:
            print('Input ID')
            Num = input('>>')
            try:
                Num=int(Num)
            except ValueError:
                print(Num+' is not an integer.')
                stat=-1
            stat=stat+1
            
        if Num<0:
            print('ID should be positive.')
            stat=0

    xn=np.zeros((fl.nrec),dtype=float)
    zn=np.zeros((fl.nrec),dtype=float)
    Tn=np.zeros((fl.nrec),dtype=float)
    timen=np.zeros((fl.nrec),dtype=float)
    start=1
    end=fl.nrec

    for frame in range (1,fl.nrec+1):
        x, z, age, phase, idt, a1, a2, ntriag = fl.read_markers(frame)
        pos=idt[idt==Num]
        if len(pos)!=0:
            T = fl.read_temperature(frame)
            Tm = flac.marker_interpolate_node(ntriag, a1, a2, fl.nz, T)
            xn[frame-start]=x[idt==Num];zn[frame-start]=z[idt==Num]
            Tn[frame-start]=Tm[idt==Num];timen[frame-start]=fl.time[frame-1]
        elif start==frame:
            start=frame+1
        elif frame<=end:
            end=frame-1
            break

    if start>end:
        print('ID do not exist.')
        stat=0

xn=np.resize(xn,end-start+1)
zn=np.resize(zn,end-start+1)
Tn=np.resize(Tn,end-start+1)
timen=np.resize(timen,end-start+1)

fig,ax=plt.subplots(2,1)
ax[0].plot(xn,zn)
ax[1].plot(timen,Tn)
plt.tight_layout()

print('Start from Frame '+str(start)+' to Frame '+str(end))

stat=0
while stat!=1:
    print('plot[p] or save[s] or both[b] ?')
    Ans = input('>>')
    if Ans in ('p'):
        plt.show()
    elif Ans in ('s'):
        print('figurename ?')
        Name = input('>>')
        plt.savefig(Name)
    elif Ans in ('b'):
        print('figurename ?')
        Name = input('>>')
        plt.savefig(Name)
        plt.show()
    else:
        print('Plz input [s] or [p] or [b].')
        stat=-1
    stat=stat+1
