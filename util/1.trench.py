#!/usr/bin/env python
import flac
import sys,os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def trench_topo_plot(model): 
    path = '/home/jiching/geoflac/'+model+'/'
    os.chdir(path)
    
    fl = flac.Flac()
    end = fl.nrec
    
    cmap = plt.cm.get_cmap('gist_earth')
    zmax, zmin =10, -10
    trench_x = np.zeros(end)
    trench_t = np.zeros(end)
    arc_x = np.zeros(end)
    fig, (ax) = plt.subplots(1,1,figsize=(10,12))
    
    for i in range(end):
        x, z = fl.read_mesh(i+1)
        xmax = np.amax(x)
        xmin = np.amin(x)
    
        xt = x[:,0]
        zt = z[:,0]
        t = np.zeros(xt.shape)
        t[:] = i*0.2
        ax.scatter(xt,t,c=zt,cmap=cmap,vmin=zmin, vmax=zmax)
        trench_t[i] = t[0]
        trench_x[i] = xt[np.argmin(zt)]
        arc_x[i] = xt[np.argmax(zt)]
    ind_within=(arc_x<900)*(trench_x>100)
    #ax.plot(arc_x[ind_within],trench_t[ind_within],c='r',lw=4)
    ax.plot(trench_x[ind_within],trench_t[ind_within],'k-',lw='4')
    ax.set_xlim(xmin,xmax)
    ax.set_ylim(0,t[0])
    ax.set_title(str(model)+" Bathymetry Evolution")
    ax.set_ylabel("Time (Ma)")
    ax.set_xlabel("Distance (km)")
    distance=arc_x-trench_x
    #ax2.plot(distance[ind_within],trench_t[ind_within],c='b',lw=4)    
    #ax2.set_ylim(0,t[0])
    #ax2.set_xlabel('Distance between arc and trench (km)')

    ax_cbin = fig.add_axes([0.67, 0.18, 0.23, 0.03])
    cb_plot = ax.scatter([-1],[-1],s=0.1,c=[1],cmap=cmap,vmin=zmin, vmax=zmax)
    cb = fig.colorbar(cb_plot,cax=ax_cbin,orientation='horizontal')
    ax_cbin.set_title('Bathymetry (km)')
    plt.savefig('/home/jiching/geoflac/figure'+'/'+str(model)+'_topo.jpg')


if __name__ == '__main__':
    model = sys.argv[1]
    trench_topo_plot(model)
