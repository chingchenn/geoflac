#!/usr/bin/env python
import math
import flac
import os,sys
import numpy as np
from matplotlib import cm
import matplotlib.pyplot as plt
model = str(sys.argv[1])
path = '/home/jiching/geoflac/'+model+'/'
path = model
print(model)
os.chdir(path)
fl = flac.Flac();end = fl.nrec
nex = fl.nx - 1;nez = fl.nz - 1

melt = np.zeros(end)
magma = np.zeros(end)
cc=0
for i in range(1,end):
    mm=fl.read_fmelt(i)
    chamber=fl.read_chamber(i)
    melt[i]=np.max(mm)
    magma[i]=np.max(chamber)
    if magma[i] >= 0.01:
        cc += 1

print("-------------------")
print(cc)
print("-------------------")
print('melt=',np.max(melt))
print(fl.time[np.argmax(melt)])
print("-------------------")
print('magma=',np.max(magma))
print(fl.time[np.argmax(magma)])
print("-------------------")
