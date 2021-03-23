import os
import numpy as np
import xarray as xr
import netCDF4 as nc
import matplotlib.pyplot as plt
from resample import resample_3d

def get_nc():
    nc_file = r'D:\radar\rademul\simulation\mdvnc_20020612_004800.nc'
    ff = nc.Dataset(nc_file, 'r')
    xx = ff.variables['x0'][:]
    yy = ff.variables['y0'][:]
    zz = ff.variables['z0'][:]
    zz = zz * 2.
    uu = np.squeeze(ff.variables['uwind'][:])
    vv = np.squeeze(ff.variables['vwind'][:])
    ww = np.squeeze(ff.variables['wwind'][:])
    qr = np.squeeze(ff.variables['qr'][:]) + 1e-8
    dbz = 43.1 + 17.5 * np.log10(1.3 * qr)

    return xx, yy, dbz


nc_file = r'D:\radar\rademul\simulation\mdvnc_20020612_004800.nc'
ff = nc.Dataset(nc_file, 'r')
xx = ff.variables['x0'][:]
yy = ff.variables['y0'][:]
zz = ff.variables['z0'][:]
zz = zz * 2.
uu = np.squeeze(ff.variables['uwind'][:])
vv = np.squeeze(ff.variables['vwind'][:])
ww = np.squeeze(ff.variables['wwind'][:])
qr = np.squeeze(ff.variables['qr'][:]) + 1e-8
dbz = 43.1 + 17.5 * np.log10(1.3 * qr)

plt.figure(1)
plt.pcolormesh(xx, yy, dbz[0], shading='auto')
plt.show()

max_rng, reso, x_mid, y_mid = 150., 1., 100, 100
el = np.array([0.5, 1.0, 1.8, 2.6, 3.6, 4.7, 6.5, 9.1, 12.8])
vol = resample_3d(uu, vv, ww, dbz, xx, yy, zz, el, reso, max_rng, xx[x_mid], yy[y_mid], zz[0])

plt.figure(2)
plt.pcolormesh(vol[0]['range'], vol[0]['azimuth'], vol[0]['dbz'], shading='auto')
plt.show()


