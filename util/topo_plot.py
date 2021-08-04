#!/usr/bin/env python
import flac
import sys,os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import function_for_flac as fn

def read_time(start_vts,model_steps):
    timestep=[0]
    for step in range(start_vts,model_steps+1):
        timestep.append(fl.time[step])
    # timestep=np.array(timestep)
    return timestep
def trench_topo_plot(model): 
    sys.path.append("/home/jiching/geoflac/util/")
    path = '/home/jiching/geoflac/'+model+'/'
    os.chdir(path)
    
    fl = flac.Flac()
    end = fl.nrec
    
    fig, (ax) = plt.subplots(1,1,figsize=(10,12))
    cmap = plt.cm.get_cmap('gist_earth')

    x_time=[]
    z_time=[]
    time=fn.read_time(1,end)
    for i in range(1,end):
        x,z,=fl.read_mesh(i)
        xtop,ztop=fn.get_topo(x,z,i)
        x_time.append(xtop)
        z_time.append(ztop)
    
    plt.pcolormesh(x_time[0], time,z_time)
    plt.savefig('/home/jiching/geoflac'+'/'+str(model)+'_topo_image.jpg')

if __name__ == '__main__':
    model = sys.argv[1]
    trench_topo_plot(model)
