#!/usr/local/depot/Python-3.7/bin/python
# /usr/local/depot/Python-3.5.1/bin/python

from ppf import *
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.cm as cm
from matplotlib.colors import Normalize
from hoho import useful_recurring_functions, constant_function,read_kk3_2022, global_functions, pedestal_values
from thesis import constants
from hoho import useful_recurring_functions, find_pedestal_values_old
from scipy.interpolate import interp1d
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
europed_names = ['taj211a11']
crit_value = 0.03

# dda_global = 'T037'
# uid = 'lfrassin'
# n = len(dtype_temp)
# shot = 87342
# time_inputs = [46.86]
# europed_names = ['tb_eta1_rs0.04_neped3_betap0.85','fwa_eta1_rs0.04_neped3_betap0.85_w0.07']
# crit_value = 0.105


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

    ax1.scatter(psi,temperature,color='white',edgecolors='red')
    ax1.plot(psi_fit,temperature_fit,'red')

    ax2.scatter(psi,density,color='white',edgecolors='red')
    ax2.plot(psi_fit,density_fit,'red')

    ax3.scatter(psi,1.6*density*temperature,color='white',edgecolors='red')
    ax3.plot(psi_fit,1.6*density_fit*temperature_fit,'red')
    
    print(len(psi_fit))
    pressure_fit = 1.6*density_fit*temperature_fit


    number_points = 700
    ax3.plot(psi_fit[-number_points:], pressure_fit[-number_points:],'orange', zorder=10)
    ax1.plot(psi_fit[-number_points:], temperature_fit[-number_points:],'orange', zorder=10)
    ax2.plot(psi_fit[-number_points:], density_fit[-number_points:],'orange', zorder=10)

    params_pe_my_fit = find_pedestal_values_old.fit_mtanh_pressure(psi_fit[-number_points:], pressure_fit[-number_points:])
    params_te_my_fit = find_pedestal_values_old.fit_mtanh_pressure(psi_fit[-number_points:], temperature_fit[-number_points:])
    params_ne_my_fit = find_pedestal_values_old.fit_mtanh_pressure(psi_fit[-number_points:], density_fit[-number_points:])

    pressure_my_fit2 = []
    temperature_my_fit2 = []
    density_my_fit2 = []
    for psi in psi_fit:
        pressure_my_fit2.append(find_pedestal_values_old.mtanh_offset(psi, params_pe_my_fit[0], params_pe_my_fit[1], params_pe_my_fit[2], params_pe_my_fit[3], params_pe_my_fit[4]))
        temperature_my_fit2.append(find_pedestal_values_old.mtanh_offset(psi, params_te_my_fit[0], params_te_my_fit[1], params_te_my_fit[2], params_te_my_fit[3], params_te_my_fit[4]))
        density_my_fit2.append(find_pedestal_values_old.mtanh_offset(psi, params_ne_my_fit[0], params_ne_my_fit[1], params_ne_my_fit[2], params_ne_my_fit[3], params_ne_my_fit[4]))

    ax3.plot(psi_fit,pressure_my_fit2,'purple')
    ax1.plot(psi_fit,temperature_my_fit2,'purple')
    ax2.plot(psi_fit,density_my_fit2,'purple')

    print(params_pe_my_fit)
    print(params_te_my_fit)
    print(params_ne_my_fit)
    


    for europed_name in europed_names:

        # psi_fit = np.r

        # params = find_pedestal_values_old.fit_mtanh_pressure(psi_fit, temperature_fit)
        # print('Te parameters exp')
        # print(params)

        # params = find_pedestal_values_old.fit_mtanh_pressure(psi_fit, density_fit)
        # print('ne parameters exp')
        # print(params)
 

        # ax2.plot(psi_fit,density_fit,'red')


        psis = np.linspace(0,1,1200)
        # te,ne,dump2 = find_pedestal_values_old.create_profiles(europed_name,psis,profile=4)
        # te,ne,dump2 = find_pedestal_values_old.create_profiles(europed_name,psis,crit='alfven')

        fixed_width = europed_name.startswith('fw')
        te,ne = pedestal_values.create_profiles(europed_name,psis,crit='alfven',crit_value=crit_value, fixed_width=fixed_width)
        pe = 1.6*ne*te

        ax1.plot(psis,te,linewidth=3, label=europed_name)
        ax2.plot(psis, ne,linewidth=3)
        ax3.plot(psis,pe,linewidth=3)


        number_points = 200
        ax3.plot(psis[-number_points:], pe[-number_points:],'orange', zorder=10)
        ax1.plot(psis[-number_points:], te[-number_points:],'orange', zorder=10)
        ax2.plot(psis[-number_points:], ne[-number_points:],'orange', zorder=10)

        params_pe_my_fit = find_pedestal_values_old.fit_mtanh_pressure(psis[-number_points:], pe[-number_points:])
        params_te_my_fit = find_pedestal_values_old.fit_mtanh_pressure(psis[-number_points:], te[-number_points:])
        params_ne_my_fit = find_pedestal_values_old.fit_mtanh_pressure(psis[-number_points:], ne[-number_points:])

        pressure_my_fit2 = []
        temperature_my_fit2 = []
        density_my_fit2 = []
        for psi in psis:
            pressure_my_fit2.append(find_pedestal_values_old.mtanh_offset(psi, params_pe_my_fit[0], params_pe_my_fit[1], params_pe_my_fit[2], params_pe_my_fit[3], params_pe_my_fit[4]))
            temperature_my_fit2.append(find_pedestal_values_old.mtanh_offset(psi, params_te_my_fit[0], params_te_my_fit[1], params_te_my_fit[2], params_te_my_fit[3], params_te_my_fit[4]))
            density_my_fit2.append(find_pedestal_values_old.mtanh_offset(psi, params_ne_my_fit[0], params_ne_my_fit[1], params_ne_my_fit[2], params_ne_my_fit[3], params_ne_my_fit[4]))

        ax3.plot(psis,pressure_my_fit2,'purple')
        ax1.plot(psis,temperature_my_fit2,'purple')
        ax2.plot(psis,density_my_fit2,'purple')

        print(params_pe_my_fit)
        print(params_te_my_fit)
        print(params_ne_my_fit)


    # ax1.text(0.05,0.05,europed_name,ha='left',va='bottom', transform=ax1.transAxes, fontsize=6)

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


    # te_pars_stability = [0.916564923,   0.000168641,  0.175359510,   0.970902795,   0.014508467,   0.349803251,   1.080884726,  -0.790751421,  -0.098976684]
    # ne_pars_stability = [2.573570444,  -0.045010339,  0.023317174,   0.991201398,   0.014834018,   0.548335008,  -0.003244445,   0.002995164,   0.002162317]

    # te_profile_hampus = old_style_profile(te_pars_stability, psis)
    # ne_profile_hampus = old_style_profile(ne_pars_stability, psis)

    # ax2.plot(psis, ne_profile_hampus)
    # ax1.plot(psis, te_profile_hampus)


    plt.show()

    # fig,ax = plt.subplots()

    # ax.plot(psis, 1.6*ne_profile_hampus*te_profile_hampus, label='essive')
    # ax.plot(psis, 1.6*ne*te, label='europed')
    # plt.legend()
    # plt.show()


    # dpdpsi_1 = np.gradient(1.6*ne_profile_hampus*te_profile_hampus, psis)
    # dpdpsi_2 = np.gradient(1.6*ne*te, psis)
    # plt.plot(psis,dpdpsi_1, label='essive')
    # plt.plot(psis,dpdpsi_2, label='europed')
    # plt.legend()
    # plt.show()

if __name__ == '__main__':
    main()

