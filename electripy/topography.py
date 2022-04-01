import os
from os.path import join as jp

import geopy.distance as gpd
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import rasterio


def datread(file=None, header=0):
    """Reads space separated dat file"""
    with open(file, 'r') as fr:
        op = np.array([list(map(float, l.split())) for l in fr.readlines()[header:]])
    return op

cc = datread('coords2.txt')
cc = cc.reshape((cc.shape[0], 2, 2))
cc = np.flip(cc, axis=2)

ft = "n11_e108_1arc_v3.tif"
dataset = rasterio.open(ft)
# dataset.bounds
# dataset.indexes
# Elevation data:
r = dataset.read(1)
# dataset.height
# dataset.width
# row, col = dataset.index(108.246179,11.063655)  # Enter long, lat to get row col of corresponding elevation.
# elp = r[row, col]


def get_topo(sp, ep):
    # Format geopy should be : lat/long
    d = int(gpd.distance(sp, ep).m)
    nsteps = int(d/5)
    lats = np.linspace(sp[0], ep[0], nsteps)
    longs = np.linspace(sp[1], ep[1], nsteps)
    coords = list(zip(longs, lats))
    rc = [dataset.index(b[0], b[1]) for b in coords]
    elevs = [r[t[0], t[1]] for t in rc]
    dists = [gpd.distance(sp, cc[::-1]).m for cc in coords]

    return np.array(list(zip(dists, elevs)))


cross = [get_topo(a[0], a[1]) for a in cc]

names = ['CD', 'EF']
for c in range(len(cross)):
    # np.savetxt(names[c].rstrip()+'.dat', cross[c], fmt='%.3f', delimiter=',')
    df = pd.DataFrame(cross[c])
    filepath = names[c].rstrip()+'.xlsx'
    df.to_excel(filepath, index=False, header=['x', 'z'])
#
# p1s = (11.1871594, 108.5334544)
# p1e = (11.2074242, 108.5344572)
# test = get_topo(p1s, p1e)
#
# fig, ax = plt.subplots()
# plt.plot(test[:, 0], test[:, 1])
# plt.title("Elevation profile")
# plt.xlabel("Distance (m)")
# plt.ylabel("Elevation (m)")
# plt.xlim(0, test[:, 0].max())
# ax.set_aspect(7)
# plt.show()
# plt.savefig('{}.png'.format('linh'), dpi=300, bbox_inches='tight')
# plt.close()

for test in cross:
    fig, ax = plt.subplots()
    plt.plot(test[:, 0], test[:, 1])
    plt.title("Elevation profile")
    plt.xlabel("Distance (m)")
    plt.ylabel("Elevation (m)")
    plt.xlim(0, test[:, 0].max())
    ax.set_aspect(7)
    plt.show()
