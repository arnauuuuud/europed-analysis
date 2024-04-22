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
xlim = (0,1)
ylim_te = (0,6)
ylim_ne = (0,6)


dda_energy = 'EFIT'
dtype_energy = 'WP'
dda_power = 'NBI'
dtype_power = 'NBLM'


#####################################################################
def main():
    
    print('')
    print(shot)

    

    list_psin = []
    list_temperature = []


    ihdat,iwdat,data_energy,x_energy,time_energy,ier=ppfget(pulse=shot,dda=dda_energy,dtyp=dtype_energy)
    data_energy = np.array(data_energy)*10**-6
    ihdat,iwdat,data_power,x_power,time_power,ier=ppfget(pulse=shot,dda=dda_power,dtyp=dtype_power)
    data_power = np.array(data_power)*10**-7

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
   

    #for it,t in tqdm(enumerate(time_ne[:10])):
    for it,t in tqdm(enumerate(time_ne[:120])):
        fig, axs = plt.subplots(3,1,figsize=(9,12),gridspec_kw={'height_ratios': [1,1,3]})
 
        axs[0].plot(time_energy,data_energy, color='k')
        axs[1].plot(time_power,data_power, color='k')

        axs[1].set_xlabel('Time [s]', fontsize=fontsizelabel)
        axs[1].set_xlim(left=40,right=45.5)
        axs[0].set_xlim(left=40,right=45.5)
        axs[1].set_ylim(bottom=0)
        axs[0].set_ylim(bottom=0)
        
        axs[0].axvline(t,color='k')
        axs[1].axvline(t,color='k')

        if t>=44:
            axs[0].axvspan(xmin=41,xmax=44, color='purple',alpha=0.2)
            axs[1].axvspan(xmin=41,xmax=44, color='purple',alpha=0.2)
        elif t>=41:
            axs[0].axvspan(xmin=41,xmax=t, color='purple',alpha=0.2)
            axs[1].axvspan(xmin=41,xmax=t, color='purple',alpha=0.2)

        if t>=44.5:
            axs[0].axvspan(xmin=44.5,xmax=t, color='green',alpha=0.2)
            axs[1].axvspan(xmin=44.5,xmax=t, color='green',alpha=0.2)

        axs[0].set_ylabel(r'$W_[\mathrm{a.u.}]$', fontsize=fontsizelabel)
        axs[1].set_ylabel(r'$P_{\mathrm{NBI}}$ $_[\mathrm{a.u.}]$', fontsize=fontsizelabel) 
 
        ax = axs[2]
        ax.scatter(data_psi[it],data_ne[it],color=ne_color,s=60,marker='h',edgecolor='k')
        # ax.set_ylabel(r'${n_e}_{[10^{19}{\mathrm{m}}^{-3}]}$',color=ne_color, fontsize = fontsizelabel)
        ax.text(-0.07, 0.58, r'${n_e}_{[10^{19}{\mathrm{m}}^{-3}]}$', transform=ax.transAxes, color=ne_color, va='top', ha='center', rotation=90, fontsize=fontsizelabel)
        ax.text(-0.07, 0.62, r'${T_e}_{[\mathrm{keV}]}$', transform=ax.transAxes, color=te_color, va='bottom', ha='center', rotation=90, fontsize=fontsizelabel)
        ax.text(-0.07, 0.605, r'-', transform=ax.transAxes, color='k', va='center', ha='center', rotation=90, fontsize=fontsizelabel)
        ax.set_xlabel(r'$\psi_N$',fontsize = fontsizelabel)

        # ax2 = ax.twinx()
        # ax2.scatter(data_psi[it],data_te[it],color=te_color,marker='D',edgecolor='k')
        ax.scatter(data_psi[it],data_te[it],color=te_color,s=50,marker='D',edgecolor='k')
        
        # ax2.set_ylabel(r'${T_e}_{[\mathrm{keV}]}$',color=te_color, fontsize=fontsizelabel)
    
        ax.text(0.95, 0.95, rf'$t={round(float(t),2)}$'+r'$\mathrm{s}$', transform=ax.transAxes, fontsize=fontsizelabel, va='top', ha='right')

        ax.set_ylim(ylim_ne[0],ylim_ne[1])
        ax.set_xlim(left=xlim[0],right=xlim[1])         
        # ax2.set_ylim(ylim_te[0],ylim_te[1])

        plt.tick_params(axis='both',labelsize=fontsizetick)

        plt.savefig(f'../../../bouloulou/video/{round(float(t),2)}.png')
        plt.close()

    



if __name__ == '__main__':
    main()
