import numpy as np
from hoho import ra_flush_v3_fast
from ppf import *


def read_kk3radii_2022(shot, equi_dda='EFIT', equi_uid='JETPPF', equi_seq=0, nchannels=None):
    
    equi_dda = equi_dda.strip()
    equi_uid = equi_uid.strip()
    equi_seq = int(equi_seq)
    
    gen,x,t,nd,nx,nt,dunits,xunits,tunits,desc,comm,seq,ier=ppfdata(pulse = shot,dda = 'KK3',dtyp='GEN',seq=0,uid="jetppf",device="JET",fix0=0,reshape=1,no_x=0,no_t=0,no_data=0)
    maxch = nx

    count = np.count_nonzero(gen[:,0]>0)
    if nchannels is None:
        channels = np.arange(1, maxch+1)

    fr = gen[15,channels-1]
    n_harm = gen[11,channels-1]

    # KK3 line of sight
    RANT = 4.126
    ZANT = 0.133
    AANT = 0   

    npr = 100
    rmin = 1.8
    rmax = 4.1
    rlos = np.linspace(rmin, rmax, npr)

    zlos = np.ones((npr,)) * ZANT

    # Calculate equivalent magnetic field
    me = 9.10956e-31
    qe = 1.60219e-19
    b_factor = qe / me

    # Resonant mangetic field for each KK3 channel
    bchan = 2 * np.pi * fr * 1.e9 / b_factor / n_harm

    # Calculate radii for KK3 channels (using FLUSH subroutines)
    data,x,time,nd,nx,nt,dunits,xunits,tunits,desc,comm,seq,ierr = ppfdata(pulse = shot,dda = equi_dda,dtyp='BVAC',seq=equi_seq,uid=equi_uid,device="JET")
    
    # ppfuid(equi_uid,"r")
    # bullshit = ppfget(pulse=shot, dda=equi_dda, dtyp='BVAC')
    # time = bullshit[2]
    # nt = len(time)
    rad = np.zeros((nt, maxch))
    psin = np.zeros((nt, maxch))
    r0 = np.zeros((nt,))
    b0 = np.zeros((nt,))

    for i in range(nt):
        psi, btot = ra_flush_v3_fast.ra_flush_v3_fast(shot, time[i], rlos, zlos, UID=equi_uid, DDA=equi_dda, seq=equi_seq)
        
        indm = np.argmin(btot)
        xp0 = rlos[indm]

        r0[i] = xp0
        count = np.count_nonzero(rlos < r0[i])
        
        if count == 0:
            itp = 1
        elif count == npr:
            itp = npr-1
        else:
            itp = count
        
        b0[i] = btot[itp-1] + (r0[i] - rlos[itp-1]) * (btot[itp] - btot[itp-1]) / (rlos[itp] - rlos[itp-1])
        
        sort_indices = np.argsort(btot)
        rr = rlos[sort_indices]
        bt = btot[sort_indices]
        rm = psi[sort_indices]
        
        for j in range(len(channels)):
            count = np.count_nonzero(bt <= bchan[j])
            if count <= 0:
                ir = 1
            elif count == npr:
                ir = npr-1
            else:
                ir = count
            m1 = (rr[ir] - rr[ir-1]) / (bt[ir] - bt[ir-1])
            rad[i,j] = rr[ir-1] + (bchan[j] - bt[ir-1]) * m1
            m2 = (rm[ir] - rm[ir-1]) / (bt[ir] - bt[ir-1])
            psin[i,j] = rm[ir-1] + (bchan[j] - bt[ir-1]) * m2
    
    return time, rad, psin
               

