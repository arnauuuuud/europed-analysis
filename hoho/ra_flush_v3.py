import numpy as np
import py_flush as Flush
from scipy.interpolate import interp1d

def ra_flush_v3(pulse, time, r, z, UID='JETPPF', DDA='EFTP', seq='0'):
    time = float(time)

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
    rho = np.sqrt(psi)

    # print(psi)
    # print(psi<1)

    rmid, ierr = Flush.Flush_getMidPlaneProjRight(npts, r*100.0, z*100.0)
    # volume, ierr = Flush.Flush_getVolume(npts, [1 if p<1 else 0 for p in psi])
    psi_for_volume = [min(p, 1) for p in psi]
    volume, ierr = Flush.Flush_getVolume(npts, psi_for_volume)

    psitor, ierr = Flush.Flush_getFtorProfile(npts, psi)

    idum=np.argmin(psi)
    psi[:idum] = -psi[:idum]
    
    rmid=rmid/100
    psi_norm=psi
    psi_tot=fpol
    psi_axis=fpol_ax
    psi_sep=fpol_sep
    rho_pol=rho
    psi_tor_tot=abs(psitor)
    
    volume_tot=volume/100**3
    interp = interp1d(psi, volume_tot)
    volume_sep = interp(1)
    volume_norm=volume_tot/volume_sep



    interp = interp1d(psi,psi_tor_tot)
    psi_tor_sep=interp(1)
    psi_tor_norm=psi_tor_tot/psi_tor_sep
    rho_tor=np.sqrt(abs(psi_tor_norm))




    
    return psi_norm, volume_tot
