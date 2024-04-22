import numpy as np
import py_flush as Flush

def ra_flush_v3_fast(pulse, time, r, z, psi_norm=None, btot=None, corr_bt=1, UID='JETPPF', DDA='EFIT', seq='0'):
    time = float(time)

    if not UID:
        UID = 'JETPPF'
    if not DDA:
        DDA = 'EFIT'
    if not seq:
        seq = '0'

    psi = 0
    npts = len(r)
    f = np.zeros(npts)
    flux = np.zeros(npts)
    fpol = np.zeros(npts)
    rmid = np.zeros(npts)
    volume = np.zeros(npts)
    psit = np.zeros(npts)
    psitor = np.zeros(npts)
    bt = np.zeros(npts)
    bz = np.zeros(npts)
    br = np.zeros(npts)
    fpol_ax = 0.0
    fpol_sep = 0.0
    rho_tmp = np.zeros(npts)
    ierr = 0

    ierr = Flush.flushinit(15, int(pulse), float(time), 0, int(seq), UID, DDA, 0)
    fpol, ierr = Flush.Flush_getAbsoluteFlux(npts, r * 100.0, z * 100.0)
    fpol_ax, ierr = Flush.Flush_getMagAxisFlux()
    fpol_sep, ierr = Flush.Flush_getlcfsFlux()
    psi = (fpol - fpol_ax) / (fpol_sep - fpol_ax)
    bt, ierr = Flush.Flush_getBt(npts, r * 100.0, z * 100.0)
    bz, ierr = Flush.Flush_getBz(npts, r * 100.0, z * 100.0)
    br, ierr = Flush.Flush_getBr(npts, r * 100.0, z * 100.0)
    bt = bt * 1e-4 * corr_bt
    bz = bz * 1e-4
    br = br * 1e-4
    btot = np.sqrt(bt**2 + bz**2 + br**2)

    idum = np.where(psi == np.min(psi))[0]
    if idum[0] > 0:
        ineg = np.arange(idum[0])
        psi[ineg] = -psi[ineg]

    psi_norm = psi
    
    return psi_norm, btot
