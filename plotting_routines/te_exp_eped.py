#!/usr/local/depot/Python-3.7/bin/python
# /usr/local/depot/Python-3.5.1/bin/python

from ppf import *
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.cm as cm
from matplotlib.colors import Normalize
from hoho import useful_recurring_functions, constant_function,read_kk3_2022
from thesis import constants
from hoho import useful_recurring_functions, find_pedestal_values
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

# europed_names = [f'kbm_v2_0{kbm}_FIPM{fipm}_Q0{q0}' for kbm in ['096'] for fipm in [2] for q0 in [1]]
europed_names = [f'kbm_v2_0096_FIPM{fipm}_Q0{q0}' for fipm in [0,2] for q0 in [0,1]]
europed_names = ['kbm_0096_fipm1.83','kbm_0096_fipm1.83_q01']



#####################################################################
def main():
    
    for europed_name in europed_names:
        print('')
        print(shot)

        ppfuid(uid)
        fig, axs = plt.subplots(1,2,figsize=(12,5))
        ax1 = axs[0]
        ax2 = axs[1]

        list_psin = []
        list_temperature = []

        ihdat,iwdat,temperature,x,time,ier=ppfget(pulse=shot,dda=dda_global,dtyp=dtype_temp)
        ihdat,iwdat,density,x,time,ier=ppfget(pulse=shot,dda=dda_global,dtyp=dtype_density)
        ihdat,iwdat,psi,x,time,ier=ppfget(pulse=shot,dda=dda_global,dtyp=dtype_psi)
        ihdat,iwdat,temperature_fit,x,time,ier=ppfget(pulse=shot,dda=dda_global,dtyp=dtype_temp_fit)
        ihdat,iwdat,density_fit,x,time,ier=ppfget(pulse=shot,dda=dda_global,dtyp=dtype_density_fit)
        ihdat,iwdat,psi_fit,x,time,ier=ppfget(pulse=shot,dda=dda_global,dtyp=dtype_psi_fit)
        
        interp = interp1d(temperature_fit, psi_fit)
        psi_sep = np.interp([0.1], temperature_fit, psi_fit)[0]
        psi_sep = interp(0.1)



        psi = np.array(psi) + 1 - psi_sep
        psi_fit = np.array(psi_fit) + 1 - psi_sep

        params = find_pedestal_values.fit_mtanh_pressure(psi_fit, temperature_fit)
        print('Te parameters exp')
        print(params)
        params = find_pedestal_values.fit_mtanh_pressure(psi_fit, density_fit)
        print('ne parameters exp')
        print(params)

        ax1.scatter(psi,temperature,color='white',edgecolors='red')
        ax1.plot(psi_fit,temperature_fit,'red')

        ax2.scatter(psi,density,color='white',edgecolors='red')
        ax2.plot(psi_fit,density_fit,'red')


        psis = np.linspace(0.2,1.2,100)
        # te,ne,dump2 = find_pedestal_values.create_profiles(europed_name,psis,profile=1)
        te,ne,dump2 = find_pedestal_values.create_profiles(europed_name,psis,crit='diamag')


        ax1.plot(psis,te,color='orange',linewidth=3)
        ax2.plot(psis,ne,color='orange',linewidth=3)

        ax1.text(0.05,0.05,europed_name,ha='left',va='bottom', transform=ax1.transAxes)

        params = find_pedestal_values.fit_mtanh_pressure(psis, te)
        print('Te parameters model')
        print(params)
        params = find_pedestal_values.fit_mtanh_pressure(psis, ne)
        print('ne parameters model')
        print(params)


        plt.show()

if __name__ == '__main__':
    main()
