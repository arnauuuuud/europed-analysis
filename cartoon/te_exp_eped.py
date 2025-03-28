#!/usr/local/depot/Python-3.7/bin/python
# /usr/local/depot/Python-3.5.1/bin/python

from ppf import ppfuid, ppfget
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.cm as cm
from matplotlib.colors import Normalize
from hoho import useful_recurring_functions, constant_function,read_kk3_2022, global_functions, pedestal_values, experimental_values
from thesis import constants
from hoho import useful_recurring_functions, find_pedestal_values_old
from scipy.interpolate import interp1d
from hoho.ra_flush_v3 import ra_flush_v3
major_linewidth = constants.major_linewidth
fontsizelabel = constants.fontsizelabel
fontsizetick = constants.fontsizetick
fontsizetext = constants.fontsizetext

#####################################################################
# TEMPERATURE
phys_quantity = 'TEMPERATURE'
dda_global = 'T052'
dtype_temp = 'TE'
dtype_density = 'NE'
dtype_psi = 'PSIE'
dtype_psi_fit = 'PSIF'
dtype_temp_fit = 'TEF5'
dtype_density_fit = 'NEF3'

uid = 'lfrassin'
n = len(dtype_temp)
shot = 84794
time_inputs = [45.51]
t0 = 45.51
time_range = [44.99997, 45.995216]
europed_names = ['fwi_eta1_rs0.018_neped2.67_betap1.35_w0.063']
color_fit = 'deepskyblue'
europed_names = ['global_v4_84794_eta0_betan3.07_neped2.55_nesepneped0.33']
crit_value = 0.03
# europed_names = ['tan_eta0_rs0.022_neped2.57_betap1.3']
# crit_value = 0.03
mu_0 = 4*np.pi*10**-7
crit = 'alfven'
colors=['red','orange','gold','green']
# exclud_mode = [1,30,40,50]
# exclud_mode = [30,40,50]
exclud_mode = []

# dda_global = 'T037'
# uid = 'lfrassin'
# n = len(dtype_temp)
# shot = 87342
# time_inputs = [46.86]
# t0 = 46.86 
# time_range = [45.31, 48.42]
# crit = 'alfven'
# color_fit = 'orange'
# europed_names = ['global_v4_87342_eta0_betan2.12_neped2.72_nesepneped0.57']
# # europed_names = ['tan_eta0_rs0.022_neped2.85_betap1.3']
# mu_0 = 4*np.pi*10**-7
# crit_value = 0.03
# colors = ['limegreen']
# # exclud_mode = [1,30,40,50]
# exclud_mode = []


# europed_names = ['tb_testmishka_betap0.85_kbm0.15_k','tb_testmishka_betap0.85_kbm0.15_ka','tb_testmishka_betap0.85_kbm0.15_kb','tb_testmishka_betap0.85_kbm0.15_kc','tb_testmishka_betap0.85_kbm0.15_kd']
# europed_names = ['tb_testmishka_betap0.85_kbm0.15_kd']
# europed_names = ['sb_eta0.0_rs0.035_neped2.75_betap0.85','sb_v2_n20_eta2.0_rs0.035_neped2.75_betap0.85']


def old_style_profile(pars, x, idete = 2):
    """Creates a (old-type) profile, equivalent to mtanhcore in old
    version of EDGESTAB.

    Arguments
    ---------
    pars : list
        Set of parameters describing profile, should be of length 9
        [  0   ][  1   ][     2      ][ 3 ][  4  ][    5    ][   6   ][   7   ][   8   ]
        [height][offset][core incline][pos][width][core-edge][corepar][corepar][corepar]  
    x : np.ndarray
        ??? Positions of psi ???
    idete : int
        HELENA input parameter for defining the temperature profile type,
        interchangeable for idede (density profile type) here for the sake
        of calculations
    """

    ex = np.exp(pars[5] / pars[4])
    ext = np.exp(pars[3] / pars[4])
    denom = 2.0 * pars[4] * (ex + ext)
    dtdpsico = (pars[0] - pars[1]) * ext * (pars[4] * ((4.0 + pars[2]) * ex + pars[2] * ext)
                                            - pars[2] * ex * (pars[5] - pars[3])) / (denom ** 2)

    ztmp = (pars[3] - pars[5]) / (2.0 * pars[4])
    tefte = 0.5 * (pars[0] - pars[1]) * (((1.0 + pars[2] * ztmp) * np.exp(ztmp)
                                            - np.exp(-ztmp)) / (np.exp(ztmp)
                                                                + np.exp(-ztmp))
                                            + 1.0) + pars[1]

    if (idete == 1) or (idete == 3):
        conste = tefte + dtdpsico * (pars[6] + (1 - pars[6]) / (pars[7] + 1.0
                                                                )) * pars[5]
    elif idete > 4:
        conste = tefte
    else:
        conste = tefte + dtdpsico * ((2 / 3 * pars[6] + 0.5 * pars[7])
                                        / (pars[6] + pars[7]) + 0.5 * pars[8]
                                        ) * pars[5]
                                        
    l = len(x)
    xprofile = np.zeros(l)
    for i in range(l):
        if (x[i] > pars[5]) or (idete > 4):
            z = (pars[3] - x[i]) / (2.0 * pars[4])
            denom = ((1.0 + pars[2] * z) * np.exp(z) - np.exp(-z))
            nom = np.exp(z) + np.exp(-z)
            xprofile[i] = 0.5 * (pars[0] - pars[1]) * (denom / nom + 1.0) + pars[1]
            if (x[i] < pars[5]) and (idete > 4):
                xprofile[i] += pars[6] * tefte * (1 - (x[i] / pars[5]) ** pars[7]
                                                    ) ** pars[8]
        else:
            if (idete == 1) or (idete == 3):
                xprofile[i] = -dtdpsico * (pars[6] * x[i] + (1 - pars[6]) / (
                        (pars[7] + 1.0) * (
                        pars[5] ** pars[7]))
                                            * x[i] ** (pars[7] + 1.0)) + conste
            elif idete < 5:
                xprofile[i] = -dtdpsico * ((2 / 3 * pars[6] * (x[i] / pars[5]) ** 1.5
                                            + 0.5 * pars[7] * (x[i] / pars[5]) ** 2.0)
                                            / (pars[6] + pars[7]) + pars[8] * (
                                                    x[i] / pars[5] - 0.5 * (
                                                    x[i] / pars[5]) ** 2.0)
                                            ) * pars[5] + conste
    return xprofile


#####################################################################
def get_value_at_t0(array, time, t0):
    interpolator = interp1d(time, array, axis=0)
    valueatt0 = interpolator(t0)
    return valueatt0



def main():
    

    ppfuid(uid)
    fig, axs = plt.subplots(1,3,figsize=(18,5))
    ax1 = axs[0]
    ax2 = axs[1]
    ax3 = axs[2]

    list_psin = []
    list_temperature = []

    ihdat,iwdat,temperature,x,time,ier=ppfget(pulse=shot,dda=dda_global,dtyp=dtype_temp)
    ihdat,iwdat,density,x,time,ier=ppfget(pulse=shot,dda=dda_global,dtyp=dtype_density)
    ihdat,iwdat,psi,x,time,ier=ppfget(pulse=shot,dda=dda_global,dtyp=dtype_psi)
    ihdat,iwdat,temperature_fit,x,time,ier=ppfget(pulse=shot,dda=dda_global,dtyp=dtype_temp_fit)
    ihdat,iwdat,density_fit,x,time,ier=ppfget(pulse=shot,dda=dda_global,dtyp=dtype_density_fit)
    ihdat,iwdat,psi_fit,x,time,ier=ppfget(pulse=shot,dda=dda_global,dtyp=dtype_psi_fit)
    
    interp = interp1d(temperature_fit, psi_fit)
    psi_sep = interp(0.1)
    psi = np.array(psi) + 1 - psi_sep
    psi_fit = np.array(psi_fit) + 1 - psi_sep

    ax1.scatter(psi,temperature,color='white',edgecolors='black')
    ax1.plot(psi_fit,temperature_fit,color_fit, zorder=10)

    ax2.scatter(psi,density,color='white',edgecolors='black')
    ax2.plot(psi_fit,density_fit,color_fit, zorder=10)

    ax3.scatter(psi,1.6*density*temperature,color='white',edgecolors='black')
    ax3.plot(psi_fit,1.6*density_fit*temperature_fit,color_fit, zorder=10)

    psi_fit = np.array(psi_fit)
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


    interpolator_te = interp1d(psil,tl)
    te_ped = interpolator_te(pos)
    interpolator_ne = interp1d(psil,nl)
    ne_ped = interpolator_ne(pos)
    interpolator_pe = interp1d(psil,pl)
    pe_ped = interpolator_pe(pos)

    # ax1.axhline(te_ped, color='purple')
    # ax2.axhline(ne_ped, color='purple')
    # ax3.axhline(pe_ped, color='purple')


    
    for europed_name,color in zip(europed_names,colors):

        # psi_fit = np.r

        # params = find_pedestal_values_old.fit_mtanh_pressure(psi_fit, temperature_fit)
        # print('Te parameters exp')
        # print(params)

        # params = find_pedestal_values_old.fit_mtanh_pressure(psi_fit, density_fit)
        # print('ne parameters exp')
        # print(params)
 

        # ax2.plot(psi_fit,density_fit,'red')


        psis = np.linspace(0,1.2,500)
        # te,ne,dump2 = find_pedestal_values_old.create_profiles(europed_name,psis,profile=4)
        # te,ne,dump2 = find_pedestal_values_old.create_profiles(europed_name,psis,crit='alfven')

        fixed_width = europed_name.startswith('fw')
        te,ne = pedestal_values.create_profiles(europed_name,psis,crit=crit,crit_value=crit_value, fixed_width=fixed_width, exclud_mode = exclud_mode)


        ax1.plot(psis,te,linewidth=1.5, label=europed_name, color=color)
        ax2.plot(psis, ne,linewidth=1.5, color=color)
        ax3.plot(psis,1.6*ne*te,linewidth=1.5, color=color)

    # ax1.text(0.05,0.05,europed_name,ha='left',va='bottom', transform=ax1.transAxes, fontsize=6)

    ne_sep = pedestal_values.nesep(europed_name, crit=crit, crit_value=crit_value)
    ne_ped = pedestal_values.pedestal_value_all_definition('ne', europed_name, crit=crit, crit_value=crit_value)

    # ax2.axhline(ne_sep)
    # ax2.axhline(ne_ped)

    ylabel = global_functions.get_profiles_label('te') 
    ax1.set_ylabel(ylabel, fontsize=20)
    ax1.set_xlabel(global_functions.psiN_label, fontsize=20)

    ylabel = global_functions.get_profiles_label('ne') 
    ax2.set_ylabel(ylabel, fontsize=20)
    ax2.set_xlabel(global_functions.psiN_label, fontsize=20)

    ylabel = global_functions.get_profiles_label('pe') 
    ax3.set_ylabel(ylabel, fontsize=20)
    ax3.set_xlabel(global_functions.psiN_label, fontsize=20)
    ax1.legend()

    ax1.set_ylim(bottom=0)
    ax1.set_xlim(left=0,right=1)

    ax2.set_ylim(bottom=0)
    ax2.set_xlim(left=0,right=1)

    ax3.set_ylim(bottom=0)
    ax3.set_xlim(left=0,right=1)
    ax3.text(0.05,0.05, f'Threshold: {crit_value}', transform=ax3.transAxes)

    # posped = pedestal_values.te_pos_minus_hdelta(europed_name, crit=crit, crit_value=crit_value)
    # tepos = pedestal_values.te_pos(europed_name, crit=crit, crit_value=crit_value, fixed_width=fixed_width)

    # neped = pedestal_values.pedestal_value('ne', europed_name, crit=crit, crit_value=crit_value)
    # teped = pedestal_values.pedestal_value('te', europed_name, crit=crit, crit_value=crit_value)
    # peped = pedestal_values.pedestal_value('pe', europed_name, crit=crit, crit_value=crit_value)

    # ax1.axhline(teped, color='green')
    # ax2.axhline(neped, color='green')
    # ax3.axhline(peped, color='green')

    # ax1.axvline(posped, color='green')
    # ax2.axvline(posped, color='green')
    # ax3.axvline(posped, color='green')
    # ax3.axvline(tepos, color='green', linestyle=':')



    # peped, peped_error = experimental_values.get_peped(shot, dda_global)  
    # ax3.axhline(peped, color='red')
    # ax3.axhspan(peped-peped_error,peped+peped_error, color='red', alpha=0.1)

    # neped, neped_error = experimental_values.get_neped(shot, dda_global)  
    # ax2.axhline(neped, color='red')
    # ax2.axhspan(neped-neped_error,neped+neped_error, color='red', alpha=0.1)

    # teped, teped_error = experimental_values.get_teped(shot, dda_global)  
    # ax1.axhline(teped, color='red')
    # ax1.axhspan(teped-teped_error,teped+teped_error, color='red', alpha=0.1)

    te_pars_stability = [0.916564923,   0.000168641,  0.175359510,   0.970902795,   0.014508467,   0.349803251,   1.080884726,  -0.790751421,  -0.098976684]
    ne_pars_stability = [2.573570444,  -0.045010339,  0.023317174,   0.991201398,   0.014834018,   0.548335008,  -0.003244445,   0.002995164,   0.002162317]

    te_pars_stability = [0.585575876,   0.001238676,   0.218952723,   0.973043884,   0.017929085,   0.402505001,   0.683709442,  -0.628992276,  -0.066085070]
    ne_pars_stability = [2.727138318,   0.018564261,   0.025430139,   1.005226231,   0.019424242,   0.909686493,   0.422774810,   0.002478595,  -0.003707925]

    te_profile_hampus = old_style_profile(te_pars_stability, psis)
    ne_profile_hampus = old_style_profile(ne_pars_stability, psis)

    # ax2.plot(psis, ne_profile_hampus)
    # ax1.plot(psis, te_profile_hampus)
    # ax3.plot(psis, 1.6*ne_profile_hampus*te_profile_hampus)

    plt.show()


    ppfuid('JETPPF')

    ihdat,iwdat,dVdpsi,x1,time1,ier=ppfget(pulse=shot,dda='EFTP',dtyp='VJAC') 
    dVdpsi = dVdpsi.reshape(len(time1), len(x1))

    ihdat,iwdat,psi_eftp,x,time2,ier=ppfget(pulse=shot,dda='EFTP',dtyp='PSNM') 
    psi_eftp = psi_eftp.reshape(len(time2), len(x))
    ihdat,iwdat,V,x,time3,ier=ppfget(pulse=shot,dda='EFTP',dtyp='VOLM') 
    V = V.reshape(len(time3), len(x))
    ihdat,iwdat,R0,x,time4,ier=ppfget(pulse=shot,dda='EFTP',dtyp='RGEO')
    R0 = R0.reshape(len(time4), len(x))



    ihdat,iwdat,rmag,x,time,ier=ppfget(pulse=shot,dda='EFTP',dtyp='RMAG') 
    ihdat,iwdat,zmag,x,time,ier=ppfget(pulse=shot,dda='EFTP',dtyp='ZMAG') 
    ihdat,iwdat,zeff,x,time_zeff,ier=ppfget(pulse=shot,dda='KS3',dtyp='ZEFV') 
    ihdat,iwdat,rgeo,x,time,ier=ppfget(pulse=shot,dda='EFTP',dtyp='RGEO')
    ihdat,iwdat,volma,x,time,ier=ppfget(pulse=shot,dda='EFTP',dtyp='VOLM')
    ihdat,iwdat,psi1a,x,time,ier=ppfget(pulse=shot,dda='EFTP',dtyp='FBND')
    ihdat,iwdat,psi0a,x,time,ier=ppfget(pulse=shot,dda='EFTP',dtyp='FAXS')

    ppfuid('lfrassin')
    ihdat,iwdat,t1,x,time,ier=ppfget(pulse=shot,dda=dda,dtyp='KT1')
    ihdat,iwdat,t2,x,time,ier=ppfget(pulse=shot,dda=dda,dtyp='KT2')
    t1 = t1[0]
    t2 = t2[0]

    time_filtered = (time>t1) & (time<t2)
    timez_filtered = (time_zeff>t1) & (time_zeff<t2)

    
    psi1 = np.nanmean(psi1a[time_filtered])
    psi0 = np.nanmean(psi0a[time_filtered])
    volm = np.nanmean(volma[time_filtered])
    rmag_0 = np.nanmean(rmag[time_filtered])
    zmag_0 = np.nanmean(zmag[time_filtered])
    rgeo_0 = np.nanmean(rgeo[time_filtered])
    zeff_0 = np.nanmean(zeff[timez_filtered])


    # # print(len(zeff))
    # # print(len(rgeo))
    # # print(len(time))
    # # # psi1 = get_value_at_t0(psi1a, time, t0)
    # # # psi0 = get_value_at_t0(psi0a, time, t0)
    # # # psi0 = get_value_at_t0(psi0a, time, t0)
    # # # rmag_0 = get_value_at_t0(rmag, time, t0)
    # # # zmag_0 = get_value_at_t0(zmag, time, t0)
    # # # rgeo_0 = get_value_at_t0(rgeo, time, t0)
    # # # zeff_0 = get_value_at_t0(zeff, time_zeff, t0)

    # # print(zeff_0)


    # dndpsi = np.gradient(density_fit, psi_fit)
    # interpolator = interp1d(psi_fit, dndpsi, bounds_error=True)
    # dndpsi_sep = interpolator(1)

    # interpolator = interp1d(psi_fit, density_fit, bounds_error=True)
    # n_sep = interpolator(1)

    # print(f'gradn/n: {dndpsi_sep/n_sep}')


    dpdpsi_1 = np.gradient(1.6*density_fit*temperature_fit, psi_fit)
    dpdpsi_2 = np.gradient(1.6*ne*te, psis)
    corr=1+(5-zeff_0)/4
    dpdpsi_1 = corr*dpdpsi_1

    R = np.linspace(rmag_0, 4.5, 1000)
    Z = np.linspace(zmag_0, zmag_0, 1000)


    # # plt.scatter(R,Z, c = PSNI[:len(R)])
    # # plt.show()

    psi_N_array = []
    V_array = []
    
    for t in np.linspace(time_range[0],time_range[1],100):
        psi_N, V = ra_flush_v3(84794, t, R, Z)
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

    # plt.plot(psi_N, dpdpsi_alpha)
    # plt.plot(psi_fit, dpdpsi_1)
    # plt.show()
    dpdpsi_alpha = np.array(dpdpsi_alpha)*1000
    dVdpsi = np.gradient(V, psi_N)

    # # print(np.max(V))
    # # print(np.mean(rgeo_0))
    # # print(np.nanmean(dVdpsi))
    # # # print(np.nanmin(dpdpsi_alpha))
    # # # print(np.nanmax(volumeppf))

    # # plt.plot(psi_N, dVdpsi)
    # # plt.show()


    alpha = -2 * dVdpsi / (2*np.pi)**2 * np.sqrt(V / (2*np.pi**2*rgeo_0)) * mu_0 * dpdpsi_alpha / (psi1-psi0)**2

    plt.plot(psi_N, alpha)
    plt.text(0,0,f'alpha_max={np.nanmax(alpha)}')
    plt.show()





    # # plt.show()

    # dpdpsi_1 = np.gradient(1.6*ne_profile_hampus*te_profile_hampus, psis)
    # dpdpsi_2 = np.gradient(1.6*ne*te, psis)
    # # plt.plot(psis,dpdpsi_1, label='essive')
    # # plt.plot(psis,dpdpsi_2, label='europed')
    # # plt.legend()
    # # plt.show()

    # dpdpsi_1 = np.gradient(1.6*density_fit*temperature_fit, psi_fit)
    # dpdpsi_2 = np.gradient(1.6*ne*te, psis)

    # # # plt.plot(psi_fit, dpdpsi_1)
    # # # plt.plot(psis, dpdpsi_2)
    # # # plt.show()
    # dVdpsi_0 = get_value_at_t0(dVdpsi, time1, t0)
    # psi_eftp_0 = get_value_at_t0(psi_eftp, time2, t0)
    # V_0 = get_value_at_t0(V, time3, t0)
    # R0_0 = get_value_at_t0(R0, time4, t0)

    # interpolator = interp1d(psi_fit, dpdpsi_1)
    # dpdpsi_eftp = []
    # for psi in psi_eftp_0:
    #     dpdpsi_eftp.append(interpolator(psi))


    # dpdpsi_eftp = np.array(dpdpsi_eftp)

    # alpha = -2 * dVdpsi_0 / (2*np.pi)**2 * (V_0/(2*np.pi*R0_0))**1/2 * mu_0 * dpdpsi_eftp

    # # print(psi_eftp_0)
    # # print(alpha)
    # # print(len(alpha[0]))
    # # print(len(psi_eftp[0]))

    # index = np.argmin(psi_eftp_0)

    # for i in range(index):
    #     psi_eftp_0[i] = -psi_eftp_0[i]

    # plt.plot(psi_eftp_0, alpha)
    # plt.show()

    # corr=1+(5-zeff_0)/4
    # dpdpsi_1 = corr*dpdpsi_1

if __name__ == '__main__':
    main()

