#!/usr/bin/env python
"""
Ji Ching Chen in 2021.Feb.20
可調整要找的marker數量
"""
import flac
import sys,os
import numpy as np
import matplotlib.pyplot as plt

path = '/home/jiching/geoflac/'
#path = '/scratch2/jiching/'
sys.path.append("/home/jiching/geoflac/util")
model = sys.argv[1]
os.chdir(path+model)

fl = flac.Flac();end = fl.nrec
plt.rcParams['figure.figsize'] =30,18
ss=[];marker = [];mm=[]
x,y,d,ph,id,a1,a2,ntring=fl.read_markers(1)
c=['lightcoral','tomato','saddlebrown','tan','orange',
   'olive','lawngreen','darkseagreen','lightseagreen','darkslategray',
   'darkturquoise','deepskyblue','steelblue','cornflowerblue',
   'navy','rebeccapurple','plum','mediumvioletred','hotpink','crimson']
fig, (ax)= plt.subplots(1,1,figsize=(10,12))
number_of_marker = 1 
mrange=50
start = 138
for i in range(int(1200/mrange)):
    x,y,d,ph,id,a1,a2,ntring=fl.read_markers(start)
    marker.append([])
    print('====='+str(i*mrange)+','+str(mrange+i*mrange)+'====')
    select1 = id[(x>i*mrange)&(x<mrange+i*mrange)&(ph==3)]
    if len(select1)==0:
        continue
    xk,yk,dk,phk,idk,a1k,a2k,ntringk=fl.read_markers(start+50)
    for j in select1:
        if j in idk:
            marker[i].append({'x':float(x[id==j]),'y':float(y[id==j]),
              'd':float(d[id==j]),'ph':int(ph[id==j]),'id':int(j)})
    if len(marker[i])==0:
        continue
    xx1=np.zeros(end);yy1=np.zeros(end)
    for jj in range(1,end+1):
        x,y,d,ph,id,a1,a2,nstring=fl.read_markers(jj)
        if len(x[id==marker[i][-1]['id']])==0:
            continue
        xx1[jj-1]=(float(x[id==marker[i][-1]['id']]))
        yy1[jj-1]=(float(y[id==marker[i][-1]['id']]))
    ax.scatter(xx1[xx1>0],yy1[xx1>0],lw=4,c=c[i],s=2,label=str(i*mrange)+'-'+str(mrange+i*mrange))
    ax.legend(fontsize=6)
    ax.set_xlim(600,800)
    ax.set_ylim(-100,0)
    #ax.xticks(fontsize=20)
    #ax.yticks(fontsize=20)
    ax.set_aspect('equal')
    ax.grid()
fig.savefig('/home/jiching/geoflac/'+'marker_'+str(start)+'.png')
# plt.show()
plt.close(fig)

