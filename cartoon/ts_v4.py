#!/usr/local/depot/Python-3.7/bin/python
# /usr/local/depot/Python-3.5.1/bin/python

from ppf import *
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.cm as cm
from matplotlib.colors import Normalize
from hoho import constant_function,read_kk3_2022,global_functions
from paper import constants
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

xlim = (0.85,1)
ylim_te = (0,3.2)
ylim_ne = (0,3.2)

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


    ihdat,iwdat,data_psi,x_psi,time_psi,ier=ppfget(pulse=shot,dda=dda_global,dtyp='PSI')
    data_psi = data_psi.reshape(len(time_psi),len(x_psi))
   
    fig, ax = plt.subplots(figsize=(6,5))
    # ax2 = ax.twinx()

    list_to_include = [93,94,96,108,112,115,116]

    #for it,t in tqdm(enumerate(time_ne[:10])):
    for it,t in tqdm(zip(list_to_include,time_ne[list_to_include])):
        ax.scatter(data_psi[it],data_ne[it],color=ne_color,s=100,marker='h',edgecolor='k')
        ax.scatter(data_psi[it],data_te[it]/1000,color=te_color,s=70,marker='D',edgecolor='k')
        # ax2.scatter(data_psi[it],data_te[it]/1000,color=te_color,marker='D',edgecolor='k')

    # ax.set_ylabel(r'${n_e}_{[10^{19}{\mathrm{m}}^{-3}]}$, ${T_e}_{[\mathrm{keV}]}$', fontsize = fontsizelabel)
    # ax.set_ylabel(r'${n_e}_{[10^{19}{\mathrm{m}}^{-3}]}$',color=ne_color, fontsize = fontsizelabel)
    ax.set_xlabel(r'$\psi_N$',fontsize = fontsizelabel)
    # ax2.set_ylabel(r'${T_e}_{[\mathrm{keV}]}$',color=te_color, fontsize=fontsizelabel)
    ax.text(-0.15, 0.58, r'${n_e}_{[10^{19}{\mathrm{m}}^{-3}]}$', transform=ax.transAxes, color=ne_color, va='top', ha='center', rotation=90, fontsize=fontsizelabel)
    ax.text(-0.15, 0.62, r'${T_e}_{[\mathrm{keV}]}$', transform=ax.transAxes, color=te_color, va='bottom', ha='center', rotation=90, fontsize=fontsizelabel)
    ax.text(-0.15, 0.605, r'-', transform=ax.transAxes, color='k', va='center', ha='center', rotation=90, fontsize=fontsizelabel)


    ax.set_ylim(ylim_ne[0],ylim_ne[1])
    ax.set_xlim(left=xlim[0],right=xlim[1])         
    # ax2.set_ylim(ylim_te[0],ylim_te[1])
    #ax.text(0.95, 0.95, rf'$t={round(float(t),2)}$'+r'$\mathrm{s}$', transform=ax.transAxes, fontsize=fontsizetick, va='top', ha='right')

    ax.text(0.9, ylim_ne[1], r'$p^{\mathrm{pos}}$', transform=ax.transData, ha='center',va='bottom', fontsize=fontsizetick, color='w')

    plt.tick_params(axis='both',labelsize=fontsizetick)

    plt.savefig(f'../../../bouloulou/global2.png')
    plt.close()

    



if __name__ == '__main__':
    main()
