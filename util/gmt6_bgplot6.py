#!/usr/bin/env python

import sys, os
import numpy as np

import flac
import flac_interpolate as fi
import gravity as fg


# domain bounds
left = -200
right = 250
up = 10
down = -200
dx = 1.5
dz = 0.6

def find_trench_index(z):
    '''Returns the i index of trench location.'''
    zz = z[:,0]
    # the highest point defines the forearc
    imax = zz.argmax()
    # the trench is the lowest point west of forearc
    i = zz[:imax].argmin()
    return i


def interpolate_phase(frame, xtrench):
    # domain bounds in km
    fi.xmin = xtrench + left
    fi.xmax = xtrench + right
    fi.zmin = down
    fi.zmax = up

    # resolution in km
    fi.dx = dx
    fi.dz = dz

    xx, zz, ph = fi.interpolate(frame, 'phase')
    return xx, zz, ph

def interpolate_srII(frame, xtrench):
   # domain bounds in km
   fi.xmin = xtrench + left
   fi.xmax = xtrench + right
   fi.zmin = down
   fi.zmax = up

   # resolution in km
   fi.dx = dx
   fi.dz = dz

   srx, srz, sr = fi.interpolate(frame, 'srII')
   return srx, srz, sr

def interpolate_sII(frame, xtrench):
   # domain bounds in km
   fi.xmin = xtrench + left
   fi.xmax = xtrench + right
   fi.zmin = down
   fi.zmax = up

   # resolution in km
   fi.dx = dx
   fi.dz = dz

   sx, sz, s = fi.interpolate(frame, 'sII')
   return sx, sz, s




###############################################

frame = int(sys.argv[1])

fl = flac.Flac()
x, z = fl.read_mesh(frame)

itrench = find_trench_index(z)
xtrench = x[itrench,0]

# get interpolated phase either from previous run or from original data
phasefile = 'intp3-phase.%d' % frame
if not os.path.exists(phasefile):
    xx, zz, ph = interpolate_phase(frame, xtrench)
    f = open(phasefile, 'w')
    f.write('%d %d\n' % xx.shape)
    flac.printing(xx, zz, ph, stream=f)
    f.close()
else:
    f = open(phasefile)
    nx, nz = np.fromfile(f, sep=' ', count=2)
    tmp = np.fromfile(f, sep=' ')
    tmp.shape = (nx, nz, 3)
    xx = tmp[:,:,0]
    zz = tmp[:,:,1]
    ph = tmp[:,:,2]
    f.close()

# get interpolated strain_rate either from previous run or from original data
strain_ratefile = 'intp3-srII.%d' % frame
if not os.path.exists(strain_ratefile):
    srx, srz, sr = interpolate_srII(frame, xtrench)
    f = open(strain_ratefile, 'w')
    f.write('%d %d\n' % srx.shape)
    flac.printing(srx, srz, sr, stream=f)
    f.close()
else:
    f = open(strain_ratefile)
    nx, nz = np.fromfile(f, sep=' ', count=2)
    strr = np.fromfile(f, sep=' ')
    strr.shape = (nx, nz, 3)
    srx = strr[:,:,0]
    srz = strr[:,:,1]
    sr = strr[:,:,2]
    f.close()


# get interpolated phase either from previous run or from original data
stressfile = 'intp3-sII.%d' % frame
if not os.path.exists(stressfile):
    sx, sz, s = interpolate_sII(frame, xtrench)
    f = open(stressfile, 'w')
    f.write('%d %d\n' % xx.shape)
    flac.printing(sx, sz, s, stream=f)
    f.close()
else:
    f = open(stressfile)
    nx, nz = np.fromfile(f, sep=' ', count=2)
    str = np.fromfile(f, sep=' ')
    str.shape = (nx, nz, 3)
    sx = str[:,:,0]
    sz = str[:,:,1]
    s = str[:,:,2]
    f.close()



# get interpolated T either from previous run or from original data
tfile = 'intp3-T.%d' % frame
if not os.path.exists(tfile):
    T = fl.read_temperature(frame)
    f = open(tfile, 'w')
    f.write('%d %d\n' % x.shape)
    flac.printing(x, z, T, stream=f)
    f.close()
else:
    f = open(tfile)
    nx, nz = np.fromfile(f, sep=' ', count=2)
    tmp = np.fromfile(f, sep=' ')
    tmp.shape = (nx, nz, 3)
    T = tmp[:,:,2]
    f.close()


# get topography and gravity at uniform spacing
px, topo, topomod, fagravity, bggravity = fg.compute_gravity2(frame)
# convert to km and mGal before saving
px *= 1e-3
topo *= 1e-3
topomod *= 1e-3
fagravity *= 1e5
bggravity *= 1e5
gfile = 'topo-grav.%d' % frame
f = open(gfile, 'w')
flac.printing(px, topo, fagravity, bggravity, topomod, stream=f)
f.close()


###############
model = os.path.split(os.getcwd())[-1]
psfile = 'result3.%d' % frame
pngfile = 'result3.%d.png' % frame
phgrd = 'phase3.%d.grd' % frame
strrgrd = 'strain_rate3.%d.grd' %frame
strgrd = 'stress3.%d.grd' %frame
tgrd = 'temperature3.%d.grd' % frame
phcpt = '/home/jiching/geoflac/util/phase15.cpt'
strrcpt= '/home/jiching/geoflac/util/strain_rate.cpt'
strcpt= '/home/jiching/geoflac/util/stress.cpt'

xmin = xtrench + left
xmax = xtrench + right
zmin = down
zmax = up
aspect_ratio = float(up - down) / (right - left)
width = 6.5
height = width * aspect_ratio
shiftz = height + 1

# height of gravity plot
height2 = 1.0

# gravity grid
gravgridsize = 100
#gmin = int(gravity.min() / gravgridsize - 1) * gravgridsize
#gmax = int(gravity.max() / gravgridsize + 1) * gravgridsize
gmin = int(bggravity.min() / gravgridsize - 1) * gravgridsize
gmax = int(bggravity.max() / gravgridsize + 1) * gravgridsize
gravann = max(abs(gmin), abs(gmax))

# topography grid
topogridsize = 2
tpmin = int(topo.min() / topogridsize - 1) * topogridsize
tpmax = int(topo.max() / topogridsize + 1) * topogridsize
topoann = max(abs(tpmin), abs(tpmax))
# interval of temperature contours
cint = 200

if not os.path.exists(phgrd):
    cmd = 'tail -n +2 %(phasefile)s | xyz2grd -G%(phgrd)s -I%(dx)f/%(dz)f -R%(xmin)f/%(xmax)f/%(zmin)f/%(zmax)f' % locals()
    #print cmd
    os.system(cmd)


if not os.path.exists(strrgrd):
    cmd = 'tail -n +2 %(strain_ratefile)s | xyz2grd -G%(strrgrd)s -I%(dx)f/%(dz)f -R%(xmin)f/%(xmax)f/%(zmin)f/%(zmax)f' % locals()
    #print cmd
    os.system(cmd)


if not os.path.exists(strgrd):
    cmd = 'tail -n +2 %(stressfile)s | xyz2grd -G%(strgrd)s -I%(dx)f/%(dz)f -R%(xmin)f/%(xmax)f/%(zmin)f/%(zmax)f' % locals()
    #print cmd
    os.system(cmd)


if not os.path.exists(tgrd):
    cmd = 'tail -n +2 %(tfile)s | surface -G%(tgrd)s -Ll0 -I%(dx)f/%(dz)f -R%(xmin)f/%(xmax)f/%(zmin)f/%(zmax)f' % locals()
    #print cmd
    os.system(cmd)

cmd = '''
rm -f .gmtcommands* .gmtdefaults*

gmtset PROJ_LENGTH_UNIT = inch
gmtset FONT_LABEL=14 FONT_ANNOT_PRIMARY=10
gmtset PS_MEDIA A3

gmt begin %(psfile)s jpg
# axis annotation
gmt basemap -JX%(width)f/%(height)f -R%(xmin)f/%(xmax)f/%(zmin)f/%(zmax)f -BWSne -Bxa100f10+l"stress" -Bya20f5 -X0.9

# stress plot
gmt grdimage %(strgrd)s -C%(strcpt)s -R%(xmin)f/%(xmax)f/%(zmin)f/%(zmax)f

# axis annotation
gmt basemap -JX%(width)f/%(height)f -BWSne -Bxa100f10+l"strain rate" -Bya20f5 -R%(left)f/%(right)f/%(zmin)f/%(zmax)f -Y4.5

# strain_rate plot
gmt grdimage %(strrgrd)s -C%(strrcpt)s -R%(xmin)f/%(xmax)f/%(zmin)f/%(zmax)f

# axis annotation
gmt basemap -JX%(width)f/%(height)f -BWSne -Bxa100f10+l"phase" -Bya20f5 -R%(left)f/%(right)f/%(zmin)f/%(zmax)f -Y4.5
# phase plot
gmt grdimage %(phgrd)s -C%(phcpt)s -R%(xmin)f/%(xmax)f/%(zmin)f/%(zmax)f

# temperature contours
gmt grdcontour %(tgrd)s -C%(cint)f -A200 -W1p

# baseline plot
gmt basemap -B+t"Model=%(model)s   Frame=%(frame)d   Trench location=%(xtrench).3f km" -JX%(width)f/%(height2)f -R%(xmin)f/%(xmax)f/-1/1 -Y%(shiftz)f
gmt plot -A -Wthin,0,.  <<END
%(xmin)f 0
%(xmax)f 0
END

# gravity plot
color=red
cut -f1,3 %(gfile)s | \
gmt plot -JX%(width)f/%(height2)f -R%(xmin)f/%(xmax)f/-%(gravann)f/%(gravann)f -Bya%(gravann)ff%(gravgridsize)f+l"@;$color;mGal@;;" -BE -A -Wthin,$color
cut -f1,4 %(gfile)s | \
gmt plot -Wthin,0/102/0,--

# topography plot
color=blue
cut -f1,2 %(gfile)s | \
gmt plot -JX%(width)f/%(height2)f -R%(xmin)f/%(xmax)f/-%(topoann)f/%(topoann)f -Bya%(topoann)ff%(topogridsize)f+l"@;$color;km@;;" -BW -A -Wthin,$color
cut -f1,5 %(gfile)s | \
gmt plot -Wthin,$color,--

# colorbar
gmt colorbar -C%(phcpt)s -DjMR+w2.5i/0.3i+o-0.5i/-2.7i+m -Ba1f0.5 -V
gmt colorbar -C%(strrcpt)s -DjMR+w2.5i/0.3i+o-0.5i/-7.5i+m -Ba1f0.5 -V
gmt colorbar -C%(strcpt)s -DjMR+w2.5i/0.3i+o-0.5i/-12i+m -Ba2f0.5 -V
#echo %(xmin)f %(topogridsize)d 14 0 1 LB "Model=%(model)s   Frame=%(frame)d   Trench location=%(xtrench).3f km" | \
#gmt text -D0/1 -N -J -R -P -O >> %(psfile)s
gmt end
#convert -flatten -density 150 -rotate 90 -trim +repage  %(psfile)s %(pngfile)s
''' % locals()
#print cmd
os.system(cmd)
