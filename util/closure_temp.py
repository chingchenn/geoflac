# -*- coding: utf-8 -*-
"""
Created on Tue Jul 20 10:56:57 2021

@author: 88691
"""

import sys
sys.path.append('/home/summer-tan2/Wang,_Yu_Hsiang/geoflac/util')

import flac
import numpy as np
from matplotlib import pyplot as plt
from scipy import interpolate

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
            Tn[frame-start]=Tm[idt==Num];timen[frame-start]=fl.time[frame-1]
        elif start==frame:
            start=frame+1
        elif frame<=end:
            end=frame-1
            break

    if start>end:
        print('ID do not exist.')
        stat=0

print('Start from Frame '+str(start)+' to Frame '+str(end))
if start==end:
    print('Only have one piece of deta at '+str(timen[0])+' Ma, '+str(Tn[0])+' °C.')
    sys.exit()

framen=end-start+1
Tn=np.resize(Tn,framen)
timen=np.resize(timen,framen)
zirt=np.loadtxt('zircon.txt')
f1 = interpolate.splrep(timen,Tn, s=0)
f2 = interpolate.splrep(zirt[:,0],zirt[:,1], s=0)
tx = np.arange(round(fl.time[start-1],2),round(fl.time[end-1],2)+0.01,0.01)
Tf1= interpolate.splev(tx, f1, der=0)
dTf1= interpolate.splev(tx, f1, der=1)
Tcf2= interpolate.splev(-dTf1,f2,der=0)

crosst=[]
Tdiff1=[]
Tdiff2=[]
for frame in range(0,len(tx)):
    if dTf1[frame]>0:
        Tcf2[frame]= np.nan
    elif frame!=0 and dTf1[frame-1]<=0 and (Tf1[frame-1]-Tcf2[frame-1])*(Tf1[frame]-Tcf2[frame])<0:
        crosst+=[tx[frame-1]]
        Tdiff1+=[Tf1[frame-1]-Tcf2[frame-1]]
        Tdiff2+=[Tf1[frame]-Tcf2[frame]]

crosst=np.array(crosst)
plt.clf()
plt.plot(tx,Tf1, color = "red")
plt.plot(tx,Tcf2, color = "blue")

if len(crosst)!=0:
    print('Found '+str(len(crosst))+' possible closure tempture(s) between ',end='')
    for frame in range(0,len(crosst)):
        print(str(crosst[frame])+' Ma to '+str(crosst[frame]+0.01)+' Ma/ ',end='')
    print('')
    stat=0
    atime=np.zeros((2,2),dtype=float)
    print('Need more accurate time? Press[y]')
    Ans = input('>>')
    if Ans in ('y'):
        while stat!=1:
            while stat!=1:
                print('Input digits [2,8]')
                Num = input('>>')
                try:
                    Num=int(Num)
                except ValueError:
                    print(Num+' is not an integer.')
                    stat=-1
                stat=stat+1
                        
            if Num<2 or Num>8:
                print('Digits should be [2,8].')
                stat=0
        for frame in range(0,len(crosst)):
            atime[0,0]=crosst[frame]
            atime[1,0]=atime[0,0]+0.01
            atime[0,1]=Tdiff1[frame]
            atime[1,1]=Tdiff2[frame]
            while round(atime[0,0],Num)!=round(atime[1,0],Num):
                half=(atime[0,0]+atime[1,0])/2
                hT= interpolate.splev(half, f1, der=0)
                hdT= interpolate.splev(half, f1, der=1)
                hTc= interpolate.splev(-hdT,f2,der=0)
                if (hT-hTc)*atime[0,1]<=0:
                    atime[1,0]=half
                    atime[1,1]=hT-hTc
                else:
                    atime[0,0]=half
                    atime[0,1]=hT-hTc
            
            crosst[frame]=round(atime[0,0],Num)
        
        print('Possibly reach closure tempture at '+str(crosst)+' Ma.')
    else:
        print('End sub.')
else:
    print('Closure temperature is not defined.')

plt.show()
