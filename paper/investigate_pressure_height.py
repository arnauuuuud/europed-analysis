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

list_shot = [84798, 87338, 87348, 87341, 84791, 87342,84794]
list_dda = [global_functions.dict_shot_dda[s] for s in list_shot]



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
list_consid_mode = [1, 2, 3, 4, 5, 7, 10, 20, 30, 40, 50]

fig, axs = plt.subplots(1,3, figsize=(9,5))

count = [0,0,0]

for (shot, dda) in zip(list_shot, list_dda):

    betan, betan_err = experimental_values.get_betan(shot, dda)
    neped, neped_err = experimental_values.get_neped(shot, dda)
    gasrate, g_err = experimental_values.get_gasrate(shot, dda)
    nesepneped = experimental_values.get_nesepneped(shot, dda)[0]
    power, p_err = experimental_values.get_power(shot, dda)

    peped, peped_err = experimental_values.get_peped_fixedpos(shot,dda)

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


    if betan <= 1.8:
        k = 0
    elif 1.8 <= betan and betan <= 2.8:
        k = 1
    elif 2.8 <= betan:
        k = 2

    count_here = count[k]
    count[k] += 1
    ax = axs[k]

    ax.plot(psi_fit,1.6*density_fit*temperature_fit,color, zorder=10)
    betan_round = round(betan,1)
    peped = round(float(peped), 1)

    ax.text(0.9,0.95-0.1*count_here,f'{shot} $beta= $'+ str(betan_round) + '  peped = ' + str(peped), color=color, fontsize=8, ha='right', va='top', transform=ax.transAxes)
    ax.axhline(peped, color=color)

    ax.set_xlim(0.8,1.1)
    ax.set_ylim(0,6.5)


plt.savefig(f'{folder_to_save}investigatepressure.png')
plt.show()
