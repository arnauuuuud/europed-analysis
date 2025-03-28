#!/usr/local/depot/Python-3.7/bin/python
# /usr/local/depot/Python-3.5.1/bin/python

from ppf import ppfuid, ppfget
import pandas as pd
import matplotlib.pyplot as plt
from hoho import pedestal_values, global_functions, experimental_values, europed_analysis_2
import numpy as np
from matplotlib import cm
from matplotlib.colors import Normalize
from scipy.interpolate import interp1d

list_shot = [84794, 84791, 84792, 84793, 84795, 84796, 84797, 84798, 87335, 87336, 87337, 87338, 87339, 87340, 87341, 87342, 87344, 87346, 87348, 87349, 87350]
list_dda = [global_functions.dict_shot_dda[s] for s in list_shot]

bad_shots = [84798, 87335, 87346]


folder_to_save = '/home/jwp9427/work/figures/2025-03-05_paper/'

# Create figure and axes objects

lists = [[], [], []]


phys_quantity = 'TEMPERATURE'
dda_global = 'T052'
dtype_temp = 'TE'
dtype_density = 'NE'
dtype_psi = 'PSIE'
dtype_psi_fit = 'PSIF'
dtype_temp_fit = 'TEF5'
dtype_density_fit = 'NEF3'

frac_uncertainty = 0.1
crit = 'alfven'
list_consid_mode = [1, 2, 3, 4, 5, 7, 10, 20]

fig, axs = plt.subplots(5,4, figsize=(7,10))


k = 0

for (shot, dda) in zip(list_shot, list_dda):


    if shot in bad_shots:
        continue


    ii = k//4
    ij = k-4*(k//4)

    ax = axs[ii,ij]
    k += 1

    betan, betan_err = experimental_values.get_betan(shot, dda)
    neped, neped_err = experimental_values.get_neped(shot, dda)
    gasrate, g_err = experimental_values.get_gasrate(shot, dda)
    nesepneped = experimental_values.get_nesepneped(shot, dda)[0]
    power, p_err = experimental_values.get_power(shot, dda)

    if gasrate <= 0.5e22:
        marker = 's'
        color = 'blue'
        i = 0
    elif gasrate <= 1.5e22:
        marker = 's'
        color = 'green'
        i = 1
    else:
        marker = 's'
        color = 'magenta'
        i = 2


    ihdat,iwdat,temperature_fit,x,time,ier=ppfget(pulse=shot,dda=dda,dtyp=dtype_temp_fit)
    ihdat,iwdat,density_fit,x,time,ier=ppfget(pulse=shot,dda=dda,dtyp=dtype_density_fit)
    ihdat,iwdat,psi_fit,x,time,ier=ppfget(pulse=shot,dda=dda,dtyp=dtype_psi_fit)
    
    interp = interp1d(temperature_fit, psi_fit)
    psi_sep = interp(0.1)
    psi_fit = np.array(psi_fit) + 1 - psi_sep



    ax.plot(psi_fit,1.6*density_fit*temperature_fit,color, zorder=10)

    round_betan = round(float(betan), 2)
    round_neped = round(float(neped), 2)
    round_frac = round(nesepneped, 2)

    for (eta, linestyle, crit_value) in zip([0, 1], [':', '--'],[0.03,0.06]):
        try:
            psis = np.linspace(0.8,1.1,200)
            fixed_width = False
            exclud_mode = None
            europed_name = f'global_v4_{shot}_eta{eta}_betan{round_betan}_neped{round_neped}_nesepneped{round_frac}'

            print(europed_name)

            try:
                te,ne = pedestal_values.create_profiles(europed_name,psis,crit=crit,crit_value=crit_value, fixed_width=fixed_width, list_consid_mode= list_consid_mode,exclud_mode = exclud_mode)
            except KeyError:
                continue
            if eta == 0:
                if color == 'magenta':
                    color = 'lightpink'
                if color == 'green':
                    color = 'lightgreen'
                if color == 'blue':
                    color = 'lightblue'
            elif eta == 1:
                if color == 'lightpink':
                    color = 'darkmagenta'
                if color == 'lightgreen':
                    color = 'darkgreen'
                if color == 'lightblue':
                    color = 'darkblue'

            ax.plot(psis,1.6*ne*te,linewidth=1.5, color=color, linestyle=linestyle)

            try:
                te_m,ne_m = pedestal_values.create_profiles(europed_name,psis,crit=crit,crit_value=crit_value*(1-frac_uncertainty), fixed_width=fixed_width, list_consid_mode= list_consid_mode, exclud_mode = exclud_mode)
                pe_m = 1.6*ne_m*te_m
                te_p,ne_p = pedestal_values.create_profiles(europed_name,psis,crit=crit,crit_value=crit_value*(1+frac_uncertainty), fixed_width=fixed_width, list_consid_mode= list_consid_mode, exclud_mode = exclud_mode)
                pe_p = 1.6*ne_p*te_p
                ax.fill_between(psis, pe_m, pe_p, color=color, alpha=0.3)
            except KeyError:
                te_p,ne_p = pedestal_values.create_profiles(europed_name,psis,crit=crit,crit_value=crit_value*(1+frac_uncertainty), fixed_width=fixed_width, list_consid_mode= list_consid_mode, exclud_mode = exclud_mode)
                pe_p = 1.6*ne_p*te_p
                ax.fill_between(psis, 1.6*ne*te, pe_p, color=color, alpha=0.3)

            # ax.set_xlabel(r'$\psi_N$')
            # ax.set_ylabel(r'$p_e$')

        except FileNotFoundError:
            pass
        except TypeError:
            pass
    ax.text(0.9,0.95,f'{shot} \n ${round(power*10**(-6),2)} MW$', fontsize=8, ha='right', va='top', transform=ax.transAxes)

    ax.set_xlim(0.8,1.1)
    ax.set_ylim(0,6.5)

for i in range(1,4):
    for ax in axs[:,i]:
        ax.tick_params(labelleft=False)
for i in range(4):
    for ax in axs[i]:
        ax.tick_params(labelbottom=False)


plt.subplots_adjust(hspace=0.2, wspace=0.2)
plt.savefig(f'{folder_to_save}alphabeta_ultimate4b.png')
plt.show()
