import base64
import time
from io import BytesIO

from matplotlib.figure import Figure
from matplotlib.patches import Circle
import matplotlib.colors as colors

import numpy as np
import netCDF4 as nc

from sim_radar_api.utils.radar.resample import resample_3d


nc_file_path = r'D:\radar\rademul\simulation\mdvnc_20020612_004800.nc'


def get_nc():
    nc_file = nc_file_path
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


def plt_value(x_value, y_value, rng_value, weather_radio):
    fig = Figure()
    ax = fig.subplots()

    xx, yy, dbz = get_nc()

    hid_colors = ['white', '#00FEFE', '#00ACFE', '#0064FE', '#00FE00', '#00AC00', '#006400', '#FEFE00',
                  '#FEAC00', '#FE6400', '#FE0000', '#AC0000', '#640000', '#FE00FE', '#AC00AC', '#640064']
    cmaphid = colors.ListedColormap(hid_colors)
    ax.pcolormesh(xx, yy, dbz[8], shading='auto', cmap=cmaphid, vmin=-10, vmax=70)

    ax.plot(xx[x_value], yy[y_value], '+', color='navy')
    ax.add_artist(Circle((xx[x_value], yy[y_value]), rng_value, fc='None', ec='navy', ls='--', lw=1.))

    # Save it to a temporary buffer.
    buf = BytesIO()
    fig.savefig(buf, format="png")
    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return f"data:image/png;base64,{data}"


def plt_value2(x_value, y_value, rng_value, weather_radio):
    fig = Figure()
    ax = fig.subplots()

    xx, yy, dbz = get_nc()

    hid_colors = ['white', '#00FEFE', '#00ACFE', '#0064FE', '#00FE00', '#00AC00', '#006400', '#FEFE00',
                  '#FEAC00', '#FE6400', '#FE0000', '#AC0000', '#640000', '#FE00FE', '#AC00AC', '#640064']
    cmaphid = colors.ListedColormap(hid_colors)

    ax.pcolormesh(xx, yy, dbz[8], cmap=cmaphid, vmin=-10, vmax=70, shading='auto')

    # Save it to a temporary buffer.
    buf = BytesIO()
    fig.savefig(buf, format="png")
    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return f"data:image/png;base64,{data}"


def get_dbz(x_value, y_value, rng_value):
    nc_file = nc_file_path
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

    max_rng, reso, x_mid, y_mid = rng_value, 1., x_value, y_value

    el = np.array([0.5, 1.0, 1.8, 2.6, 3.6, 4.7, 6.5, 9.1, 12.8])
    vol = resample_3d(uu, vv, ww, dbz, xx, yy, zz, el, reso, max_rng, xx[x_mid], yy[y_mid], zz[0])

    ret = []
    for ele in range(len(el)):
        db = vol[ele]['dbz']
        vr = vol[ele]['vr']
        xMAX, yMAX = db.shape

        dbzData = [[j, i, round(db.values[i, j], 2)] for i in range(0, xMAX, 2) for j in range(yMAX)]

        vrData = [[j, i, round(vr.values[i, j], 2)] if db.values[i, j] > -5 else [j, i, -99] for i in range(0, xMAX, 2)
                  for j
                  in range(yMAX)]
        ret.append({"dbzData": dbzData, "vrData": vrData})

    return ret


def get_one_dbz(x_value, y_value, rng_value):
    nc_file = nc_file_path
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

    max_rng, reso, x_mid, y_mid = rng_value, 1., x_value, y_value

    el = np.array([0.5, 1.0, 1.8, 2.6, 3.6, 4.7, 6.5, 9.1, 12.8])
    vol = resample_3d(uu, vv, ww, dbz, xx, yy, zz, el, reso, max_rng, xx[x_mid], yy[y_mid], zz[0])

    ret = []

    db = vol[0]['dbz']
    vr = vol[0]['vr']
    xMAX, yMAX = db.shape

    dbzData = [[j, i, round(db.values[i, j], 2)] for i in range(xMAX) for j in range(yMAX)]

    # dbzData = []
    # for i in range(xMAX):
    #     for j in range(yMAX):
    #         if db.values[i, j] > -5:
    #             dbzData.append([j, i, round(db.values[i, j], 2)])

    # dbzData = db.values.tolist()

    vrData = [[j, i, round(vr.values[i, j], 2)] if db.values[i, j] > -5 else [j, i, -99] for i in range(xMAX) for j
              in range(yMAX)]
    ret.append({"dbzData": dbzData, "vrData": vrData})

    return ret


def get_all_canvas(x_value, y_value, rng_value):
    nc_file = nc_file_path
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

    max_rng, reso, x_mid, y_mid = rng_value, 1., x_value, y_value

    el = np.array([0.5, 1.0, 1.8, 2.6, 3.6, 4.7, 6.5, 9.1, 12.8])
    vol = resample_3d(uu, vv, ww, dbz, xx, yy, zz, el, reso, max_rng, xx[x_mid], yy[y_mid], zz[0])

    ret = {"dbzData": [], "vrData": []}
    for ele in range(2, len(el)):
        db = vol[ele]['dbz'].values
        vr = vol[ele]['vr'].values
        vr[db < 5] = -999  # dbz强度小于 -5 时 vr为0
        dbzData = db.tolist()
        vrData = vr.tolist()
        ret["dbzData"].append(dbzData)
        ret["vrData"].append(vrData)

    return ret


def get_canvas(x_value, y_value, rng_value, ele):
    nc_file = nc_file_path
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

    max_rng, reso, x_mid, y_mid = rng_value, 1., x_value, y_value

    el = np.array([0.5, 1.0, 1.8, 2.6, 3.6, 4.7, 6.5, 9.1, 12.8])
    vol = resample_3d(uu, vv, ww, dbz, xx, yy, zz, el, reso, max_rng, xx[x_mid], yy[y_mid], zz[0])

    ret = {"dbzData": [], "vrData": []}
    db = vol[ele]['dbz'].values
    vr = vol[ele]['vr'].values
    vr[db < 5] = -21  # dbz强度小于 -5 时 vr为0
    db = np.around(db, 1)
    vr = np.around(vr, 1)
    dbzData = db.tolist()
    vrData = vr.tolist()

    ret["dbzData"].append(dbzData)
    ret["vrData"].append(vrData)
    return ret


def get_canvas2(x_value, y_value, rng_value, ele, numA, numB):
    nc_file = nc_file_path
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

    max_rng, reso, x_mid, y_mid = rng_value, 1., x_value, y_value
    el = np.array([0.5, 1.0, 1.8, 2.6, 3.6, 4.7, 6.5, 9.1, 12.8])
    if numA == '1':
        reso = 1.
    elif numA == '2':
        reso = 0.5
    elif numA == '3':
        reso = 0.2
    else:
        reso = 1.

    if numB == '1':
        resoB = 1.
    elif numB == '2':
        resoB = 0.5
    elif numB == '3':
        resoB = 0.2
    else:
        resoB = 1.

    ret = {"dbzData": [], "vrData": [], "dbzData_B": [], "vrData_B": []}

    vol = resample_3d(uu, vv, ww, dbz, xx, yy, zz, el, reso, max_rng, xx[x_mid], yy[y_mid], zz[0])
    db = vol[ele]['dbz'].values
    vr = vol[ele]['vr'].values
    vr[db < 5] = -21  # dbz强度小于 -5 时 vr为0
    db = np.around(db, 1)
    vr = np.around(vr, 1)
    dbzData = db.tolist()
    vrData = vr.tolist()

    ret["dbzData"].append(dbzData)
    ret["vrData"].append(vrData)

    vol = resample_3d(uu, vv, ww, dbz, xx, yy, zz, el, resoB, max_rng, xx[x_mid], yy[y_mid], zz[0])

    db = vol[ele]['dbz'].values
    vr = vol[ele]['vr'].values
    vr[db < 5] = -21  # dbz强度小于 -5 时 vr为0
    db = np.around(db, 1)
    vr = np.around(vr, 1)
    dbzData = db.tolist()
    vrData = vr.tolist()

    ret["dbzData_B"].append(dbzData)
    ret["vrData_B"].append(vrData)
    return ret
