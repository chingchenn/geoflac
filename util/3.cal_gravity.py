#!/usr/bin/env python
import flac
import sys,os
import numpy as np
import gravity as fg
import matplotlib 
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def plot_gravity(frame,model):
    sys.path.append("/home/jiching/geoflac/util/")
    path = '/home/jiching/geoflac/'+model+'/'
    os.chdir(path)
    G=6.6726e-11
    fl = flac.Flac()
    end = fl.nrec
    x, z = fl.read_mesh(frame)
    px, topo, topomod, fa_gravity, gb_gravity=fg.compute_gravity2(frame)
    ## ===============================================================
    fig, ax = plt.subplots(1,1,figsize=(15,8))
    ax.plot(px/1000,topo/1000,lw=2,c='k', linestyle='dashed',label='topo')
    ax2 = ax.twinx()
    ax2.plot(px/1000,fa_gravity*10**5,lw=3,c='r',label='free-air')
    ax2.tick_params(axis='y', labelcolor='r',labelsize=20)
    ax.tick_params(axis='y',labelsize=20)
    ax.tick_params(axis='x',labelsize=20)
    ax2.plot(px/1000,gb_gravity*10**5,lw=3,c='b',label='bouger')
    ax2.set_xlabel('Distance (km)',fontsize=40)
    ax2.set_ylabel('Gravity Anomaly (mgal)',c='r',fontsize=30)
    ax.set_ylabel('height (m)',fontsize=30)
    # ax2.set_ylim(-100,300)
    ax.set_xlim(0,900)
    ax.set_title(str(model)+'_frame-'+str(frame),fontsize=25)
    lines = [];labels = []
    for ax in fig.axes:
        axLine, axLabel = ax.get_legend_handles_labels()
        lines.extend(axLine)
        labels.extend(axLabel)
    plt.savefig('/home/jiching/geoflac/'+str(model)+'_frame-'+str(frame)+'_gravity.jpg')

if __name__ == '__main__':
    model = sys.argv[1]
    frame = int(sys.argv[2])
    plot_gravity(frame,model)
