#!/usr/local/depot/Python-3.7/bin/python
# /usr/local/depot/Python-3.5.1/bin/python

from ppf import ppfuid, ppfget
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import interp1d
from hoho.ra_flush_v3 import ra_flush_v3

def alpha_operational_point(shot=84794, dda='T052', uid='lfrassin', plot=False, alpha=None,
                            pos_alpha=None, corr_zeff=False, only_pe=False, out=None,
                            equi_dda='EFTP', equi_uid='JETPPF', equi_seq=0):
    

    def ppfread(shot, dda, dtype, uid, seq=0):
        ppfuid(uid)
        ihdat,iwdat,data,x,time,ier = ppfget(pulse=shot,dda=dda,dtyp=dtype)
        return data, time

    nefit, _ = ppfread(shot, dda, 'NEF3', uid)
    tefit, _ = ppfread(shot, dda, 'TEF5', uid)
    psif, _ = ppfread(shot, dda, 'PSIF', uid)
    volf, _ = ppfread(shot, dda, 'VOLF', uid)
    kt1, _ = ppfread(shot, dda, 'KT1', uid)
    kt2, _ = ppfread(shot, dda, 'KT2', uid)
    psi0a, tpsi = ppfread(shot, equi_dda, 'FAXS', equi_uid, equi_seq)
    
    if tpsi is None:
        equi_seq = 0
        psi0a, tpsi = ppfread(shot, equi_dda, 'FAXS', equi_uid, equi_seq)
    
    psi1a, _ = ppfread(shot, equi_dda, 'FBND', equi_uid, equi_seq)
    volma, _ = ppfread(shot, equi_dda, 'VOLM', equi_uid, equi_seq)
    rgeoa, _ = ppfread(shot, equi_dda, 'RGEO', equi_uid, equi_seq)
    cr0a, _ = ppfread(shot, equi_dda, 'CR0', equi_uid, equi_seq)
    zeff, tz = ppfread(shot, 'KS3', 'ZEFV', 'JETPPF')
    
    if tz is None:
        tz = tpsi
        zeff = np.full_like(tz, 1.7 if shot <= 80000 else 1.3)
    
    print(kt1[0], kt2[0])
    ind = np.where((tpsi >= kt1[0]) & (tpsi <= kt2[0]))
    psi0 = np.mean(psi0a[ind])
    psi1 = np.mean(psi1a[ind])
    volm = np.mean(volma[ind])
    rgeo = np.mean(rgeoa[ind])
    cr0 = np.mean(cr0a[ind])
    ind = np.where((tz >= kt1[0]) & (tz <= kt2[0]))
    zeff = np.mean(zeff[ind])
    corr = 2
    
    if corr_zeff:
        corr = 1 + (7 - zeff) / 6 if shot <= 80000 else 1 + (5 - zeff) / 4
    
    if only_pe:
        corr = 1

    
    isep = np.argmin(np.abs(tefit - 0.1))
    ilcfs = np.argmin(np.abs(psif - 1))
    dpsi = psif[ilcfs] - psif[isep]
    psif += dpsi


    ilcfs = np.argmin(np.abs(volf - 1))
    dvol = volf[ilcfs] - volf[isep]
    volf += dvol

    der = -np.gradient(1.6 * nefit * tefit * corr, psif)
    ind = np.where(psif >= 0.8)
    gradmax = np.max(der[ind])
    psimax = psif[ind][np.argmax(der[ind])]
    
    vol = volf * volm
    mu0 = 4 * np.pi * 1e-7

    alpha = 2 / (2 * np.pi) ** 2 * np.sqrt(vol / (2 * np.pi ** 2 * rgeo)) * np.gradient(vol,psif) * (der * 1e3) * mu0 / (psi1 - psi0) ** 2


    plt.figure(1)
    plt.plot(psif[ind],alpha[ind])

    plt.figure(2)
    plt.plot(psif,vol)

    plt.figure(3)
    plt.plot(psif[ind],np.gradient(vol,psif)[ind])

    plt.figure(4)
    plt.plot(psif[ind],-der[ind]*1000)

    
    alphamax = np.nanmax(alpha[ind])
    psiamax = psif[ind][np.argmax(alpha[ind])]
    
    print(psi0)
    print(psi1)
    print(psi1 - psi0)
    
    print(np.mean(vol))

    if plot:
        plt.figure(figsize=(7, 9))
        plt.subplot(2, 1, 1)
        plt.plot(psif, np.gradient(vol, psif), label='grad(p) (kPa/psi)')
        plt.xlabel('w')
        plt.ylabel('grad(p) (kPa/psi)')
        plt.legend()
        
        plt.subplot(2, 1, 2)
        plt.plot(psif, alpha, label='alpha')
        plt.xlabel('w')
        plt.ylabel('alpha')
        plt.legend()
        
        plt.show()
    
    print(alphamax, psiamax)
    
    out = {'alphamax': alphamax, 'pos_alpha': psiamax, 'psi': psif, 'alpha': alpha}
    return out

# Example usage
result = alpha_operational_point(plot=False)
print(result)

    
mu_0 = 4*np.pi*10**-7

def profile(shot, dda):

    ppfuid('lfrassin')


    dtype_psi_fit = 'PSIF'
    dtype_temp_fit = 'TEF5'
    dtype_density_fit = 'NEF3'
    dtype_t1 = 'KT1'
    dtype_t2 = 'KT2'


    ihdat,iwdat,temperature_fit,x,time,ier=ppfget(pulse=shot,dda=dda,dtyp=dtype_temp_fit)
    ihdat,iwdat,density_fit,x,time,ier=ppfget(pulse=shot,dda=dda,dtyp=dtype_density_fit)
    ihdat,iwdat,psi_fit,x,time,ier=ppfget(pulse=shot,dda=dda,dtyp=dtype_psi_fit)
    ihdat,iwdat,t1_,x,time,ier=ppfget(pulse=shot,dda=dda,dtyp=dtype_t1)
    ihdat,iwdat,t2_,x,time,ier=ppfget(pulse=shot,dda=dda,dtyp=dtype_t2)


    t1 = t1_[0]
    t2 = t2_[0]
    interp = interp1d(temperature_fit, psi_fit)
    psi_sep = interp(0.1)
    psi_fit = np.array(psi_fit) + 1 - psi_sep

    dpdpsi_1 = np.gradient(1.6*density_fit*temperature_fit, psi_fit)

    ppfuid('JETPPF')


    ihdat,iwdat,rmag,x,time,ier=ppfget(pulse=shot,dda='EFTP',dtyp='RMAG') 
    ihdat,iwdat,zmag,x,time,ier=ppfget(pulse=shot,dda='EFTP',dtyp='ZMAG') 
    ihdat,iwdat,psi1a,x,time,ier=ppfget(pulse=shot,dda='EFTP',dtyp='FBND')
    ihdat,iwdat,psi0a,x,time,ier=ppfget(pulse=shot,dda='EFTP',dtyp='FAXS')
    ihdat,iwdat,rgeo,x,time,ier=ppfget(pulse=shot,dda='EFTP',dtyp='RGEO')

    ihdat,iwdat,zeff,x,time_zeff,ier=ppfget(pulse=shot,dda='KS3',dtyp='ZEFV') 

    
    time_filtered = (time>t1) & (time<t2)
    timez_filtered = (time_zeff>t1) & (time_zeff<t2)


    psi1 = np.nanmean(psi1a[time_filtered])
    psi0 = np.nanmean(psi0a[time_filtered])
    rmag_0 = np.nanmean(rmag[time_filtered])
    zmag_0 = np.nanmean(zmag[time_filtered])
    rgeo_0 = np.nanmean(rgeo[time_filtered])
    zeff_0 = np.nanmean(zeff[timez_filtered])


    corr=1+(5-zeff_0)/4
    corr = 2
    dpdpsi_1 = corr*dpdpsi_1


    R = np.linspace(rmag_0, 4.5, 100)
    Z = np.linspace(zmag_0, zmag_0, 100)



    psi_N_array = []
    V_array = []
    for t in np.linspace(t1,t2,100):
        psi_N, V = ra_flush_v3(shot, t, R, Z)
        psi_N_array.append(psi_N)
        V_array.append(V)

    psi_N_array = np.array(psi_N_array)
    V_array = np.array(V_array)
    psi_N = np.nanmean(psi_N_array, axis=0)
    V = np.nanmean(V_array, axis=0)

    print(np.mean(V))

    interpolator = interp1d(psi_fit, dpdpsi_1, bounds_error=False)
    dpdpsi_alpha = []
    for psi in psi_N:
        dpdpsi_alpha.append(interpolator(psi))


    dpdpsi_alpha = np.array(dpdpsi_alpha)*1000
    dVdpsi = np.gradient(V, psi_N)



    alpha = -2 * dVdpsi / (2*np.pi)**2 * np.sqrt(V / (2*np.pi**2*rgeo_0)) * mu_0 * dpdpsi_alpha / (psi1-psi0)**2

    plt.figure(1)
    plt.plot(psi_N,alpha)

    plt.figure(2)
    plt.plot(psi_N,V)

    plt.figure(3)
    plt.plot(psi_N,dVdpsi)

    plt.figure(4)
    plt.plot(psi_N, dpdpsi_alpha)


    return psi_N, alpha


profile(84794, 'T052')
plt.show()

def alpha_max(shot, dda):
    psi, alpha = profile(shot, dda)
    return np.nanmax(alpha)