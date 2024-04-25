#!/usr/local/depot/Python-3.7/bin/python
# /usr/local/depot/Python-3.5.1/bin/python

from ppf import *
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.cm as cm
from matplotlib.colors import Normalize
from hoho import constant_function,read_kk3_2022,global_functions
from thesis import constants
from tqdm import tqdm

major_linewidth = constants.major_linewidth
fontsizelabel = constants.fontsizelabel
fontsizetick = constants.fontsizetick
fontsizetext = constants.fontsizetext

#####################################################################
# TEMPERATURE
dda_global = 'HRTS'
dtype_ne = 'NE'
dtype_te = 'TE'
shot = 84794
ne_color = global_functions.ne_color
te_color = global_functions.te_color
fontsizelabel = 30
fontsizetick = 20
xlim = (0,1)
ylim_te = (0,6)
ylim_ne = (0,6)

#####################################################################
def main():
    
    print('')
    print(shot)

    

    list_psin = []
    list_temperature = []




    ihdat,iwdat,data_ne,x_ne,time_ne,ier=ppfget(pulse=shot,dda=dda_global,dtyp=dtype_ne)
    data_ne = np.array(data_ne)
    x_ne = np.array(x_ne)
    time_ne = np.array(time_ne)
    data_ne = data_ne.reshape(len(time_ne),len(x_ne))
    data_ne = data_ne*10**(-19)

    ihdat,iwdat,data_te,x_te,time_te,ier=ppfget(pulse=shot,dda=dda_global,dtyp=dtype_te)
    data_te = np.array(data_te)
    x_te = np.array(x_te)
    time_te = np.array(time_te)
    data_te = data_te.reshape(len(time_te),len(x_te))
    data_te = data_te/1000


    ihdat,iwdat,data_psi,x_psi,time_psi,ier=ppfget(pulse=shot,dda=dda_global,dtyp='PSI')
    data_psi = data_psi.reshape(len(time_psi),len(x_psi))
   
    fig, ax = plt.subplots(1,2,figsize=(10,5))

    #for it,t in tqdm(enumerate(time_ne[:10])):
    for it,t in tqdm(zip([63,90],[time_ne[63],time_ne[90]])):
        color = 'purple' if it == 63 else 'green'

        ax[0].scatter(data_psi[it],data_ne[it],s=60,marker='h',edgecolor='k',color=color)
        ax[1].scatter(data_psi[it],data_te[it],s=50,marker='D',edgecolor='k',color=color)
        ax[0].set_ylabel(r'${n_e}_{[10^{19}{\mathrm{m}}^{-3}]}$',color='k', fontsize = fontsizelabel)
        ax[1].set_ylabel(r'${T_e}_{[keV]}$',color='k', fontsize = fontsizelabel)
        ax[0].set_xlabel(r'$\psi_N$',fontsize = fontsizelabel)
        ax[1].set_xlabel(r'$\psi_N$',fontsize = fontsizelabel)


        ax[0].set_ylim(ylim_ne[0],ylim_ne[1])
        ax[1].set_ylim(ylim_ne[0],ylim_ne[1])
        ax[0].set_xlim(left=xlim[0],right=xlim[1])         
        ax[1].set_xlim(left=xlim[0],right=xlim[1])         
        # ax2.set_ylim(ylim_te[0],ylim_te[1])

    plt.tick_params(axis='both',labelsize=fontsizetick)

    plt.savefig(f'../../../bouloulou/zoompopo.png')
    plt.close()

    



if __name__ == '__main__':
    main()
