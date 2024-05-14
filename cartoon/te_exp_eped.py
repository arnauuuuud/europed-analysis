#!/usr/local/depot/Python-3.7/bin/python
# /usr/local/depot/Python-3.5.1/bin/python

from ppf import *
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.cm as cm
from matplotlib.colors import Normalize
from hoho import constant_function,read_kk3_2022
from thesis import constants
from hoho import find_pedestal_values
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

europed_names = ['frog10_vj_t2','kbm_v3_fipm2_alphat24','kbm_v3_fipm2_alphat24','kbm_v3_fipm2_alphat23','kbm_v3_fipm1_alphat22','kbm_v3_fipm1_alphat24','kbm_v3_fipm1_alphat23','kbm_v3_fipm1_alphat23_q01','kbm_v3_fipm2_alphat22_q01','kbm_v3_fipm1_alphat22_q01','kbm_v3_fipm1_alphat24_q01','kbm_v3_fipm2_alphat24_q01','kbm_v3_fipm2_alphat23_q01']


# europed_names = ['m2_neped2.57_density_shift0.0200',
#  'm2_neped2.57_density_shift0.0200_fi',
#  'm2_neped2.57_density_shift0.0000_fi',
#  'm2_neped2.57_density_shift0.0000_fi_bp0',
#  'm2_neped2.57_density_shift0.0000_fi_bp0_an7',
#  'm2_neped2.57_density_shift0.0000_fi_bp0_an7_nesep',
#  'm2_neped2.57_density_shift0.0000_fi_bp0_an7_nesep_rgeom',
#  'm2_neped2.57_density_shift0.0000_fi_bp0_an7_nesep_rgeom_minor',
#  'm2_neped2.57_density_shift0.0000_fi_bp0_an7_nesep_rgeom_minor_smoothsoft',
#  'm2_neped2.57_density_shift0.0000_fi_bp0_an7_nesep_rgeom_minor_smoothsoft_at1',
#  'm2_neped2.57_density_shift0.0000_fi_bp0_an7_nesep_rgeom_minor_smoothsoft_at1_ind',
#  'm2_neped2.57_density_shift0.0000_fi_bp0_an7_nesep_rgeom_minor_smoothsoft_at1_ind_bk',
#  'm2_neped2.57_density_shift0.0000_fi_bp0_an7_nesep_rgeom_minor_smoothsoft_at1_ind_bk_cc']

# europed_names = ['m2_neped2.57_density_shift0.0000_fi_bp0_an7_nesep_rgeom_minor_smoothsoft_mishka']

# europed_names=['jet84794_lfrassinT052_standard_eped','jet84794_lfrassinT052_standard_eped_q0']
# europed_names=['kbm_v4','kbm_v4_ind', 'kbm_v4_ind_q0']
# europed_names=['m2_ds0.02','m2_ds0.02_ind', 'm2_ds0.02_ind_q0', 'm2_ds0.02_ind_fi','m2_ds0.02_ind_fi_kbm']


# europed_names=['m2_ds0.02_ind_fi_kbm','m2_ds0.02_fi1_kbm','m2_ds0.02_fi1.3_kbm','m2_ds0.02_fi1.6_kbm','m2_ds0.02_fi1.9_kbm','m2_ds0.02_fi2.3_kbm','m2_ds0.02_fi3_kbm']
# # europed_names=['m4_q0']
# europed_names=['frog_20','frog_21','frog_22','frog_23']
europed_names=['jet84794_lfrassinT052_standard_eped','jet84794_lfrassinT052_standard_eped_kbm0096']

europed_names = [ 
'jet84794_lfrassinT052_standard_eped_kbm0096',
'jet84794_lfrassinT052_standard_eped_nesep_kbm_an2',
'jet84794_lfrassinT052_standard_eped_q01.05_kbm',
'jet84794_lfrassinT052_standard_eped_q0_kbm',
'jet84794_lfrassinT052_standard_eped_kbm0096_fixedfi',
'jet84794_lfrassinT052_standard_eped_nesep_kbm'
]

europed_names = [ 
'jet84794_lfrassinT052_standard_eped',
'jet84794_lfrassinT052_standard_eped_nesep_kbm',
'starting_point'
]

europed_names = ['kbm_0.092','kbm_0.093','kbm_0.094','kbm_0.095','kbm_0096','kbm_0.097','kbm_0.098','kbm_0.099','kbm_0.1']
europed_names = ['kbm_v2_0096','kbm_v2_0106']
# europed_names = ['sp_v1b','sp_v2b']
europed_names = ['sp_v2b','sp_v3b','sp_v4a','sp_v4b','sp_v4c','sp_v4d']
europed_names = ['sp_v6a','sp_v6b','sp_v6c']

# europed_names = ['frog_30']+[f'frog_30_va_t{i}' for i in range(1,81)]


europed_names = ['sp_v8a','sp_v8b','sp_v8c','sp_v8d','sp_v8e','sb_eta0.0_rs0.022_neped2.57']
europed_names = ['sb_eta0.0_rs0.022_neped2.57']

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


        # psi_fit = np.r

        params = find_pedestal_values.fit_mtanh_pressure(psi_fit, temperature_fit)
        print('Te parameters exp')
        print(params)
        te_2 = []
        ppos, delta, h, s, offset  = params
        for p in psi:
            te_2.append(find_pedestal_values.mtanh_offset(p,ppos, delta, h, s, offset))
        ax1.plot(psi,te_2,color='y')



        params = find_pedestal_values.fit_mtanh_pressure(psi_fit, density_fit)
        print('ne parameters exp')
        print(params)
        ne_2 = []
        ppos, delta, h, s, offset  = params
        for p in psi:
            ne_2.append(find_pedestal_values.mtanh_offset(p,ppos, delta, h, s, offset))
        ax2.plot(psi,ne_2,color='y')

        ax1.scatter(psi,temperature,color='white',edgecolors='red')
        ax1.plot(psi_fit,temperature_fit,'red')

        ax2.scatter(psi,density,color='white',edgecolors='red')
        ax2.plot(psi_fit,density_fit,'red')


        psis = np.linspace(0,1.2,100)
        # te,ne,dump2 = find_pedestal_values.create_profiles(europed_name,psis,profile=3)
        te,ne,dump2 = find_pedestal_values.create_profiles(europed_name,psis,crit='alfven')


        ax1.plot(psis,te,color='orange',linewidth=3)
        ax2.plot(psis,ne,color='orange',linewidth=3)

        ax1.text(0.05,0.05,europed_name,ha='left',va='bottom', transform=ax1.transAxes, fontsize=6)

        # params = find_pedestal_values.fit_mtanh_pressure(psis, te)
        # print('Te parameters model')
        # print(params)
        # params = find_pedestal_values.fit_mtanh_pressure(psis, ne)
        # print('ne parameters model')
        # print(params)


        plt.show()

if __name__ == '__main__':
    main()

