import math
import numba
import numpy as np
import xarray as xr


@numba.njit()
def interpolate(uu, vv, ww, dbz, xx, yy, zz, px, py, pz, x0, y0, z0):
    fillv = -999.
    NZ, NY, NX = uu.shape
    vr = np.ones_like(px) * fillv
    cdbz = np.ones_like(px) * fillv
    M, N, L = vr.shape
    for ie in range(M):
        for ia in range(N):
            for ir in range(L):

                lox = int((px[ie, ia, ir] + x0 - xx[0]) / (xx[1] - xx[0]))
                if lox >= 0 and lox < NX - 1:
                    upx = lox + 1
                    lorx = px[ie, ia, ir] + x0 - xx[lox]
                    uprx = xx[upx] - (px[ie, ia, ir] + x0)
                else:
                    continue

                loy = int((py[ie, ia, ir] + y0 - yy[0]) / (yy[1] - yy[0]))
                if loy >= 0 and loy < NY - 1:
                    upy = loy + 1
                    lory = py[ie, ia, ir] + y0 - yy[loy]
                    upry = yy[upy] - (py[ie, ia, ir] + y0)
                else:
                    continue

                loz = int((pz[ie, ir] + z0 - zz[0]) / (zz[1] - zz[0]))
                if loz >= 0 and loz < NZ - 1:
                    upz = loz + 1
                    lorz = pz[ie, ir] + z0 - zz[loz]
                    uprz = zz[upz] - (pz[ie, ir] + z0)
                else:
                    continue

                lo_tmp = uprx * uu[loz, loy, lox] + lorx * uu[loz, loy, upx]
                up_tmp = uprx * uu[loz, upy, lox] + lorx * uu[loz, upy, upx]
                p_1 = (lo_tmp * upry + up_tmp * lory) / (lorx + uprx) / (lory + upry)
                lo_tmp = uprx * uu[upz, loy, lox] + lorx * uu[upz, loy, upx]
                up_tmp = uprx * uu[upz, upy, lox] + lorx * uu[upz, upy, upx]
                p_2 = (lo_tmp * upry + up_tmp * lory) / (lorx + uprx) / (lory + upry)
                p_u = (p_1 * uprz + p_2 * lorz) / (lorz + uprz)

                lo_tmp = uprx * vv[loz, loy, lox] + lorx * vv[loz, loy, upx]
                up_tmp = uprx * vv[loz, upy, lox] + lorx * vv[loz, upy, upx]
                p_1 = (lo_tmp * upry + up_tmp * lory) / (lorx + uprx) / (lory + upry)
                lo_tmp = uprx * vv[upz, loy, lox] + lorx * vv[upz, loy, upx]
                up_tmp = uprx * vv[upz, upy, lox] + lorx * vv[upz, upy, upx]
                p_2 = (lo_tmp * upry + up_tmp * lory) / (lorx + uprx) / (lory + upry)
                p_v = (p_1 * uprz + p_2 * lorz) / (lorz + uprz)

                lo_tmp = uprx * ww[loz, loy, lox] + lorx * ww[loz, loy, upx]
                up_tmp = uprx * ww[loz, upy, lox] + lorx * ww[loz, upy, upx]
                p_1 = (lo_tmp * upry + up_tmp * lory) / (lorx + uprx) / (lory + upry)
                lo_tmp = uprx * ww[upz, loy, lox] + lorx * ww[upz, loy, upx]
                up_tmp = uprx * ww[upz, upy, lox] + lorx * ww[upz, upy, upx]
                p_2 = (lo_tmp * upry + up_tmp * lory) / (lorx + uprx) / (lory + upry)
                p_w = (p_1 * uprz + p_2 * lorz) / (lorz + uprz)

                lo_tmp = uprx * dbz[loz, loy, lox] + lorx * dbz[loz, loy, upx]
                up_tmp = uprx * dbz[loz, upy, lox] + lorx * dbz[loz, upy, upx]
                p_1 = (lo_tmp * upry + up_tmp * lory) / (lorx + uprx) / (lory + upry)
                lo_tmp = uprx * dbz[upz, loy, lox] + lorx * dbz[upz, loy, upx]
                up_tmp = uprx * dbz[upz, upy, lox] + lorx * dbz[upz, upy, upx]
                p_2 = (lo_tmp * upry + up_tmp * lory) / (lorx + uprx) / (lory + upry)
                p_dbz = (p_1 * uprz + p_2 * lorz) / (lorz + uprz)

                slantrg = math.sqrt(
                    px[ie, ia, ir] * px[ie, ia, ir] +
                    py[ie, ia, ir] * py[ie, ia, ir] +
                    pz[ie, ir] * pz[ie, ir])
                cdbz[ie, ia, ir] = p_dbz
                vr[ie, ia, ir] = (px[ie, ia, ir] * p_u +
                                  py[ie, ia, ir] * p_v + pz[ie, ir] * p_w) / slantrg
    return vr, cdbz


def resample_3d(uu, vv, ww, dbz, xx, yy, zz, el, reso, maxr, x0, y0, z0):
    """resample a mode output in Cartsian coordinate to produce a radar volume data
        @param uu,vv,ww,dbz wind field[nx,ny,nz]
        @param xx,yy,zz coordinate value of each point
        @param el elevation to sample
        @param reso range resolution [km]
        @param maxr maximum range [km]
        @param x0,y0,z0 radar center in the cartsian data set
        @return vr radial velocity
        @return az azimuth angle
        @return rg range of each gate
    """
    dtr = np.pi / 180.
    azi = np.arange(0., 360., .5)
    rng = np.arange(reso, maxr, reso)
    ele = np.asarray(el)
    px = np.sin(azi[np.newaxis, :, np.newaxis] * dtr) * \
         np.cos(ele[:, np.newaxis, np.newaxis] * dtr) * \
         rng[np.newaxis, np.newaxis, :]
    py = np.cos(azi[np.newaxis, :, np.newaxis] * dtr) * \
         np.cos(ele[:, np.newaxis, np.newaxis] * dtr) * \
         rng[np.newaxis, np.newaxis, :]
    pz = np.sin(ele[:, np.newaxis] * dtr) * rng[np.newaxis, :]
    vr, cdbz = interpolate(uu, vv, ww, dbz, xx, yy, zz, px, py, pz, x0, y0, z0)

    vol = []
    for i in range(len(el)):
        ds = xr.Dataset()
        ds['vr'] = (['time', 'range'], vr[i, ...])
        ds['dbz'] = (['time', 'range'], cdbz[i, ...])
        ds.coords['elevation'] = (('time',), np.full_like(azi, ele[i]))
        ds.coords['azimuth'] = (('time',), azi)
        ds.coords['range'] = (('range',), rng * 1e3)
        vol.append(ds)
    return vol
