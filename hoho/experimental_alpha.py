import numpy as np
from scipy.interpolate import interp1d
from hoho.ra_flush_v3 import ra_flush_v3
from ppf import ppfuid, ppfget

    
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
    dpdpsi_1 = corr*dpdpsi_1


    R = np.linspace(rmag_0, 4.5, 1000)
    Z = np.linspace(zmag_0, zmag_0, 1000)



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

    interpolator = interp1d(psi_fit, dpdpsi_1, bounds_error=False)
    dpdpsi_alpha = []
    for psi in psi_N:
        dpdpsi_alpha.append(interpolator(psi))


    dpdpsi_alpha = np.array(dpdpsi_alpha)*1000
    dVdpsi = np.gradient(V, psi_N)


    alpha = -2 * dVdpsi / (2*np.pi)**2 * np.sqrt(V / (2*np.pi**2*rgeo_0)) * mu_0 * dpdpsi_alpha / (psi1-psi0)**2

    return psi_N, alpha


def alpha_max(shot, dda):
    psi, alpha = profile(shot, dda)
    return np.max(alpha)