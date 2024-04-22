import numpy as np
from hoho import ra_flush_v3_fast, read_kk3radii_2022
from ppf import *
from scipy.interpolate import interp1d

def read_kk3_2022(shot=96208, tr=[41,53], xr=[0,5], equi_dda=None, equi_uid=None, equi_seq=None, out=None, kk3_r_shift=0):

    print('   ')
    print('   - reading KK3 Te data')
    
    stup = ppfdata(pulse=shot, dda='KK3 ', dtyp='GEN ', reshape=1)
    gen3, ierr = stup[0],stup[-1]
    npt3, npx3 = gen3.shape

    cherr = np.zeros(npx3)
    te = np.zeros(npt3)
    strte = ''
    for i in range(npx3):
        if i+1 < 10:
            strte = 'TE0' + str(i+1)
        else:
            strte = 'TE' + str(i+1)
        stup = ppfdata(pulse=shot, dda='KK3 ', dtyp=strte, reshape=1)
        te, time, npt, ierr = stup[0], stup[2], stup[5], stup[-1]
        if ierr == 0:
            if out is None:
                out = {}
            if out is not None and 'tear' not in out:
                out['tear'] = np.zeros((npx3, npt))
            out['tear'][i,:] = te
        cherr[i] = ierr
    t = out['tear']/1e3

    ind = np.where((time >= tr[0]) & (time <= tr[1]))
    te = t[:,ind]
    time = time[ind]

    print('   - reading and mapping KK3 radii')
    timer, rad, psi = read_kk3radii_2022.read_kk3radii_2022(shot=shot)

    print('   - interpolating KK3 radii')
    rr = np.zeros((npx3, len(time)))
    psin = np.zeros((npx3, len(time)))
    for i in range(npx3):
        f = interp1d(timer, rad[:,i], kind='linear',bounds_error = False)
        rr[i,:] = f(time)
        g = interp1d(timer, psi[:,i], kind='linear', bounds_error = False)
        psin[i,:] = g(time)
    
    ind = np.where(rr[:,0] > 3.5)

    kk3_r_shift = 0
    dum = interp1d(rr[ind,0][0], psin[ind,0][0], kind='linear', bounds_error = False)
    dpsi = dum(3.8+kk3_r_shift)-dum(3.8)
    dpsi = 0

    if not out:
        out = {}
    out['te'] = te
    out['rad'] = rr + kk3_r_shift
    out['psin'] = psin + dpsi
    out['time'] = time

    return out


