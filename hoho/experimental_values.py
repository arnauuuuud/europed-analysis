import os
from hoho import useful_recurring_functions, startup, europed_hampus as europed, europed_analysis, europed_analysis_2, h5_manipulation, hdf5_data, find_pedestal_values_old, pedestal_values
import matplotlib.pyplot as plt
import h5py
import gzip
import tempfile
import numpy as np
import scipy
import glob
from scipy.optimize import curve_fit
from scipy.interpolate import interp1d,interp2d
from ppf import ppfget, ppfuid
from hoho.ra_flush_v3 import ra_flush_v3

mu_0 = 4*np.pi*10**-7

startup.reload(h5_manipulation)
startup.reload(europed_analysis_2)

def get_my_fit_params(shot, dda, q):
    ppfuid('lfrassin')

    if q == 'pe':
        ihdat,iwdat,temperature_fit,x,time,ier=ppfget(pulse=shot,dda=dda,dtyp='TEF5')
        ihdat,iwdat,density_fit,x,time,ier=ppfget(pulse=shot,dda=dda,dtyp='NEF3')
        ihdat,iwdat,psi_fit,x,time,ier=ppfget(pulse=shot,dda=dda,dtyp='PSIF')
        fit_profile = 1.6 * density_fit * temperature_fit
    elif q == 'te':
        ihdat,iwdat,fit_profile,x,time,ier=ppfget(pulse=shot,dda=dda,dtyp='TEF5')
        ihdat,iwdat,psi_fit,x,time,ier=ppfget(pulse=shot,dda=dda,dtyp='PSIF')
    if q == 'ne':
        ihdat,iwdat,fit_profile,x,time,ier=ppfget(pulse=shot,dda=dda,dtyp='NEF3')
        ihdat,iwdat,psi_fit,x,time,ier=ppfget(pulse=shot,dda=dda,dtyp='PSIF')

    number_points = 700
    params_my_fit = find_pedestal_values_old.fit_mtanh_pressure(psi_fit[-number_points:], fit_profile[-number_points:])
    return params_my_fit


def get_my_fit_width(shot, dda, q):
    params_my_fit = get_my_fit_params(shot, dda, q)
    return params_my_fit[1]

def get_my_fit_pos(shot, dda, q):
    params_my_fit = get_my_fit_params(shot, dda, q)
    return params_my_fit[0]

def get_width_pe(shot, dda):
    ppfuid('lfrassin')
    ihdat,iwdat,wt_array,x,time,ier = ppfget(pulse=shot, dda=dda, dtyp='WTP5')
    wt, wt_error = wt_array[0], wt_array[1]
    ihdat,iwdat,wn_array,x,time,ier = ppfget(pulse=shot, dda=dda, dtyp='WNP3')
    wn, wn_error = wn_array[0], wn_array[1]
    wp = (wn+wt)/2
    wp_error = np.sqrt(wn_error**2 + wt_error**2)/2
    return wp, wp_error


def get_teped(shot, dda):
    ppfuid('lfrassin')
    ihdat,iwdat,teped_array,x,time,ier = ppfget(pulse=shot, dda=dda, dtyp='HT1')
    teped, teped_error = teped_array[0], teped_array[1]


    ihdat,iwdat,temperature_fit,x,time,ier=ppfget(pulse=shot,dda=dda,dtyp='TEF5')
    ihdat,iwdat,density_fit,x,time,ier=ppfget(pulse=shot,dda=dda,dtyp='NEF3')
    ihdat,iwdat,psi_fit,x,time,ier=ppfget(pulse=shot,dda=dda,dtyp='PSIF')
    interp = interp1d(temperature_fit, psi_fit)
    psi_sep = interp(0.1)
    psi_fit = np.array(psi_fit) + 1 - psi_sep
    temperature_fit = np.array(temperature_fit)
    density_fit = np.array(density_fit)

    indexes = np.where(psi_fit>0.8)

    psil = psi_fit[indexes]
    tl = temperature_fit[indexes]
    te_pars = pedestal_values.fit_mtanh(psil, tl)
    tepos = te_pars[0]
    delta = te_pars[1]
    pos = tepos-delta/2
    interpolator_te = interp1d(psil,tl)
    teped = interpolator_te(pos)

    return teped, teped_error

def get_neped(shot, dda):
    ppfuid('lfrassin')
    ihdat,iwdat,neped_array,x,time,ier = ppfget(pulse=shot, dda=dda, dtyp='HN1')
    neped, neped_error = neped_array[0], neped_array[1]

    ihdat,iwdat,temperature_fit,x,time,ier=ppfget(pulse=shot,dda=dda,dtyp='TEF5')
    ihdat,iwdat,density_fit,x,time,ier=ppfget(pulse=shot,dda=dda,dtyp='NEF3')
    ihdat,iwdat,psi_fit,x,time,ier=ppfget(pulse=shot,dda=dda,dtyp='PSIF')
    interp = interp1d(temperature_fit, psi_fit)
    psi_sep = interp(0.1)
    psi_fit = np.array(psi_fit) + 1 - psi_sep
    temperature_fit = np.array(temperature_fit)
    density_fit = np.array(density_fit)

    indexes = np.where(psi_fit>0.8)

    psil = psi_fit[indexes]
    nl = density_fit[indexes]
    tl = temperature_fit[indexes]
    te_pars = pedestal_values.fit_mtanh(psil, tl)
    tepos = te_pars[0]
    delta = te_pars[1]
    pos = tepos-delta/2
    interpolator_ne = interp1d(psil,nl)
    neped = interpolator_ne(pos)
    return neped, neped_error

def get_width_te(shot, dda):
    ppfuid('lfrassin')
    ihdat,iwdat,wt_array,x,time,ier = ppfget(pulse=shot, dda=dda, dtyp='WTP5')
    wt, wt_error = wt_array[0], wt_array[1]
    return wt, wt_error

def get_width_ne(shot, dda):
    ppfuid('lfrassin')
    ihdat,iwdat,wn_array,x,time,ier = ppfget(pulse=shot, dda=dda, dtyp='WNP3')
    wn, wn_error = wn_array[0], wn_array[1]
    return wn, wn_error


dict_known_alpha = {
    84794: 4.251168450492189,
    87342: 2.4693747923866014,
    84791 : 5.30078746039505,
    84792 : 5.637044610284497,
    84793 : 3.376640781221048,
    84795 : 4.400344136754867,
    84796 : 4.284376291322177,
    84797 : 4.490848110766276,
    84798 : 3.492851796378698,
    87335 : 3.2145258080393733,
    87336 : 2.6937048198874582,
    87337 : 2.9628846241750293,
    87338 : 4.060332121522577,
    87339 : 3.27855592717966,
    87340 : 2.853733535060872,
    87341 : 3.3464982254001887,
    87344 : 2.264110783392558,
    87346 : 2.980412684566791,
    87348 : 2.8999068858479897,
    87349 : 2.3376408829634463,
    87350 : 2.8813639390643355,
}

def get_alpha(shot, dda):
    ppfuid('lfrassin')
    ihdat,iwdat,teped_array,x,time,ier = ppfget(pulse=shot, dda=dda, dtyp='HT1')
    teped, teped_error = teped_array[0], teped_array[1]
    ihdat,iwdat,neped_array,x,time,ier = ppfget(pulse=shot, dda=dda, dtyp='HN1')
    neped, neped_error = neped_array[0], neped_array[1]
    peped = 1.6 * neped * teped
    peped_error = np.sqrt((neped_error/neped)**2 + (teped_error/teped)**2) * peped    
    ihdat,iwdat,wt_array,x,time,ier = ppfget(pulse=shot, dda=dda, dtyp='WTP5')
    wt, wt_error = wt_array[0], wt_array[1]
    ihdat,iwdat,wn_array,x,time,ier = ppfget(pulse=shot, dda=dda, dtyp='WNP3')
    wn, wn_error = wn_array[0], wn_array[1]
    wp = (wn+wt)/2
    wp_error = np.sqrt(wn_error**2 + wt_error**2)/2
    gradp = peped/wp
    gradp_error = np.sqrt((peped_error/peped)**2 + (wp_error/wp)**2) * gradp
    


    if shot in list(dict_known_alpha.keys()):
        alpha_max = dict_known_alpha[shot]
    else:
        ppfuid('lfrassin')
        ihdat,iwdat,temperature_fit,x,time,ier=ppfget(pulse=shot,dda=dda,dtyp='TEF5')
        ihdat,iwdat,density_fit,x,time,ier=ppfget(pulse=shot,dda=dda,dtyp='NEF3')
        ihdat,iwdat,psi_fit,x,time,ier=ppfget(pulse=shot,dda=dda,dtyp='PSIF')

        interp = interp1d(temperature_fit, psi_fit)
        psi_sep = interp(0.1)
        psi_fit = np.array(psi_fit) + 1 - psi_sep

        ihdat,iwdat,t1,x,time,ier=ppfget(pulse=shot,dda=dda,dtyp='KT1')
        ihdat,iwdat,t2,x,time,ier=ppfget(pulse=shot,dda=dda,dtyp='KT2')
        t1 = t1[0]
        t2 = t2[0]
        ppfuid('JETPPF')
        ihdat,iwdat,rmag,x,time,ier=ppfget(pulse=shot,dda='EFTP',dtyp='RMAG') 
        ihdat,iwdat,zmag,x,time,ier=ppfget(pulse=shot,dda='EFTP',dtyp='ZMAG') 
        ihdat,iwdat,zeff,x,time_zeff,ier=ppfget(pulse=shot,dda='KS3',dtyp='ZEFV') 
        ihdat,iwdat,rgeo,x,time,ier=ppfget(pulse=shot,dda='EFTP',dtyp='RGEO')
        ihdat,iwdat,volma,x,time,ier=ppfget(pulse=shot,dda='EFTP',dtyp='VOLM')
        ihdat,iwdat,psi1a,x,time,ier=ppfget(pulse=shot,dda='EFTP',dtyp='FBND')
        ihdat,iwdat,psi0a,x,time,ier=ppfget(pulse=shot,dda='EFTP',dtyp='FAXS')


        time_filtered = (time>t1) & (time<t2)
        timez_filtered = (time_zeff>t1) & (time_zeff<t2)

        
        psi1 = np.nanmean(psi1a[time_filtered])
        psi0 = np.nanmean(psi0a[time_filtered])
        volm = np.nanmean(volma[time_filtered])
        rmag_0 = np.nanmean(rmag[time_filtered])
        zmag_0 = np.nanmean(zmag[time_filtered])
        rgeo_0 = np.nanmean(rgeo[time_filtered])
        zeff_0 = np.nanmean(zeff[timez_filtered])

        dpdpsi_1 = np.gradient(1.6*density_fit*temperature_fit, psi_fit)
        corr=1+(5-zeff_0)/4
        dpdpsi_1 = corr*dpdpsi_1

        R = np.linspace(rmag_0, 4.5, 1000)
        Z = np.linspace(zmag_0, zmag_0, 1000)


        # # plt.scatter(R,Z, c = PSNI[:len(R)])
        # # plt.show()

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

        alpha_max = np.nanmax(alpha)

    alpha_error = alpha_max * gradp_error / gradp
    return alpha_max, alpha_error
    

def get_qprofile(shot, dda):
    ihdat,iwdat,q_ppf,x,time_efit,ier = ppfget(pulse=shot, dda='EFIT', dtyp='Q')
    ihdat,iwdat,psi_ppf,x,time_efit,ier = ppfget(pulse=shot, dda='EFIT', dtyp='PSNI')

    q_reshape = q_ppf.reshape(len(time_efit), len(x))
    psi_reshape = psi_ppf.reshape(len(time_efit), len(x))



    ppfuid('lfrassin')
    ihdat,iwdat,t0,x,time,ier = ppfget(pulse=shot, dda=dda, dtyp='KT1')
    ihdat,iwdat,t1,x,time,ier = ppfget(pulse=shot, dda=dda, dtyp='KT2')
    t0 = t0[0]
    t1 = t1[0]
    time_filtered = (time_efit>t0) & (time_efit<t1)
    q_filtered = q_reshape[time_filtered]
    psi_filtered = psi_reshape[time_filtered]
    q_error = np.nanstd(q_filtered, axis=0)
    q_mean = np.nanmean(q_filtered, axis=0)
    psi_mean = np.nanmean(psi_filtered, axis=0)
    return psi_mean, q_mean, q_error


def get_peped(shot, dda):
    ppfuid('lfrassin')
    ihdat,iwdat,teped_array,x,time,ier = ppfget(pulse=shot, dda=dda, dtyp='HT1')
    teped, teped_error = teped_array[0], teped_array[1]
    ihdat,iwdat,neped_array,x,time,ier = ppfget(pulse=shot, dda=dda, dtyp='HN1')
    neped, neped_error = neped_array[0], neped_array[1]
    peped = 1.6 * neped * teped
    peped_error = np.sqrt((neped_error/neped)**2 + (teped_error/teped)**2) * peped    


    ihdat,iwdat,temperature_fit,x,time,ier=ppfget(pulse=shot,dda=dda,dtyp='TEF5')
    ihdat,iwdat,density_fit,x,time,ier=ppfget(pulse=shot,dda=dda,dtyp='NEF3')
    ihdat,iwdat,psi_fit,x,time,ier=ppfget(pulse=shot,dda=dda,dtyp='PSIF')
    interp = interp1d(temperature_fit, psi_fit)
    psi_sep = interp(0.1)
    psi_fit = np.array(psi_fit) + 1 - psi_sep
    temperature_fit = np.array(temperature_fit)
    density_fit = np.array(density_fit)

    indexes = np.where(psi_fit>0.8)

    psil = psi_fit[indexes]
    nl = density_fit[indexes]
    tl = temperature_fit[indexes]
    pl = nl * tl * 1.6
    te_pars = pedestal_values.fit_mtanh(psil, tl)
    tepos = te_pars[0]
    delta = te_pars[1]
    pos = tepos-delta/2
    interpolator_pe = interp1d(psil,pl)
    peped = interpolator_pe(pos)


    return peped, peped_error 

def get_nesepneped(shot, dda):
    ppfuid('lfrassin')
    ihdat,iwdat,ne_profile,x,time,ier = ppfget(pulse=shot, dda=dda, dtyp='NEF3')
    ihdat,iwdat,te_profile,x,time,ier = ppfget(pulse=shot, dda=dda, dtyp='TEF5')
    ihdat,iwdat,psif,x,time,ier = ppfget(pulse=shot, dda=dda, dtyp='PSIF')
    interp_ne = interp1d(psif, ne_profile)            
    interp_te = interp1d(te_profile, psif)
    psi_sep = interp_te(0.1)
    nesep = interp_ne(psi_sep)
    ihdat,iwdat,neped_array,x,time,ier = ppfget(pulse=shot, dda=dda, dtyp='HN1')
    neped, neped_error = neped_array[0], neped_array[1]
    nesepneped = nesep/neped
    nesepneped_error = np.sqrt(neped_error**2 + (nesep/neped*neped_error)**2)
    return nesepneped, nesepneped_error

def get_betan(shot, dda):
    ppfuid('JETPPF')
    ihdat,iwdat,betan_profile,x,time_eftp,ier = ppfget(pulse=shot, dda='EFTP', dtyp='BTNM')
    ppfuid('lfrassin')
    ihdat,iwdat,t0,x,time,ier = ppfget(pulse=shot, dda=dda, dtyp='KT1')
    ihdat,iwdat,t1,x,time,ier = ppfget(pulse=shot, dda=dda, dtyp='KT2')
    t0 = t0[0]
    t1 = t1[0]
    betan_filtered = betan_profile[(time_eftp>t0) & (time_eftp<t1)]
    betan_mean = np.mean(betan_filtered)
    betan_error = np.std(betan_filtered)
    return betan_mean, betan_error

def get_betap(shot, dda):
    ppfuid('JETPPF')
    ihdat,iwdat,betap_profile,x,time_eftp,ier = ppfget(pulse=shot, dda='EFTP', dtyp='BTPM')
    ppfuid('lfrassin')
    ihdat,iwdat,t0,x,time,ier = ppfget(pulse=shot, dda=dda, dtyp='KT1')
    ihdat,iwdat,t1,x,time,ier = ppfget(pulse=shot, dda=dda, dtyp='KT2')
    t0 = t0[0]
    t1 = t1[0]
    betap_filtered = betap_profile[(time_eftp>t0) & (time_eftp<t1)]
    betap_error = np.std(betap_filtered)
    betap_mean = np.mean(betap_filtered)
    return betap_mean, betap_error

def get_gasrate(shot, dda):
    ppfuid('JETPPF')
    ihdat,iwdat,gasrate_profile,x,time_eftp,ier = ppfget(pulse=shot, dda='GASH', dtyp='ELER')
    ppfuid('lfrassin')
    ihdat,iwdat,t0,x,time,ier = ppfget(pulse=shot, dda=dda, dtyp='KT1')
    ihdat,iwdat,t1,x,time,ier = ppfget(pulse=shot, dda=dda, dtyp='KT2')
    t0 = t0[0]
    t1 = t1[0]
    time_filtered = (time_eftp>t0) & (time_eftp<t1)
    gasrate_filtered = gasrate_profile[time_filtered]
    gasrate_error = np.nanstd(gasrate_filtered)
    gasrate_mean = np.nanmean(gasrate_filtered)
    return gasrate_mean, gasrate_error

def get_power(shot, dda):
    ppfuid('JETPPF')
    ihdat,iwdat,power_profile,x,time_eftp,ier = ppfget(pulse=shot, dda='NBI', dtyp='PTOT')
    ppfuid('lfrassin')
    ihdat,iwdat,t0,x,time,ier = ppfget(pulse=shot, dda=dda, dtyp='KT1')
    ihdat,iwdat,t1,x,time,ier = ppfget(pulse=shot, dda=dda, dtyp='KT2')
    t0 = t0[0]
    t1 = t1[0]
    time_filtered = (time_eftp>t0) & (time_eftp<t1)
    power_filtered = power_profile[time_filtered]
    power_error = np.nanstd(power_filtered)
    power_mean = np.nanmean(power_filtered)
    return power_mean, power_error

def get_nepostepos(shot, dda):
    ppfuid('lfrassin')
    ihdat,iwdat,nepos_array,x,time,ier = ppfget(pulse=shot, dda=dda, dtyp='PPSN')
    nepos,nepos_error = nepos_array[0], nepos_array[1]
    ihdat,iwdat,tepos_array,x,time,ier = ppfget(pulse=shot, dda=dda, dtyp='PPST')
    tepos,tepos_error = tepos_array[0], tepos_array[1]

    nepostepos = nepos-tepos
    neposteposerror = np.sqrt(nepos_error**2 + tepos_error**2)
    return nepostepos, neposteposerror

def get_nepostepos_myfit(shot, dda):
    nepostepos, neposteposerror = get_nepostepos(shot, dda)
    nepostepos_myfit = get_my_fit_pos(shot, dda, 'ne')-get_my_fit_pos(shot, dda, 'te')
    nepostepos_myfit_error = nepostepos_myfit * neposteposerror / nepostepos

    return nepostepos, neposteposerror



def get_values(par, shot, dda='0', t0=0, time_range=[0,0]):
    if par == 'frac':
        value, value_error = get_nesepneped(shot, dda)
    elif par == 'peped':
        value, value_error = get_peped(shot, dda)
    elif par == 'teped':
        value, value_error = get_teped(shot, dda)
    elif par == 'neped':
        value, value_error = get_neped(shot, dda)
    elif par == 'betan':
        value, value_error = get_betan(shot, t0, time_range)
    elif par == 'betap':
        value, value_error = get_betap(shot, t0, time_range)
    elif par == 'alpha':
        value, value_error = get_alpha(shot, dda)

    return value, value_error
