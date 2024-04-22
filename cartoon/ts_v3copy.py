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
dda_energy = 'EFIT'
dtype_energy = 'WP'

dda_power = 'NBI'
dtype_power = 'NBLM'

# dda_power = 'S3AD'
# dtype_power = 'AD36'

shot = 84794
ne_color = global_functions.ne_color
te_color = global_functions.te_color
fontsizelabel = 30
fontsizetick = 20


#####################################################################
def main():
    
    print('')
    print(shot)

    ihdat,iwdat,data_energy,x_energy,time_energy,ier=ppfget(pulse=shot,dda=dda_energy,dtyp=dtype_energy)
    data_energy = np.array(data_energy)*10**-6
    ihdat,iwdat,data_power,x_power,time_power,ier=ppfget(pulse=shot,dda=dda_power,dtyp=dtype_power)
    data_power = np.array(data_power)*10**-7

   
    fig, axs = plt.subplots(2,1,sharex=True,figsize=(6,9))
    plt.subplots_adjust(hspace=0.3)
    # ax2 = ax.twinx()
    axs[0].plot(time_energy,data_energy, color='k')
    axs[1].plot(time_power,data_power, color='k')

    axs[1].set_xlabel('Time [s]', fontsize=fontsizelabel)
    axs[1].set_xlim(left=40.1,right=45.5)
    axs[1].set_ylim(bottom=0)
    axs[0].set_ylim(bottom=0)

    axs[0].axvspan(xmin=41,xmax=44, color='purple',alpha=0.2)
    axs[1].axvspan(xmin=41,xmax=44, color='purple',alpha=0.2)

    axs[0].axvspan(xmin=44.5,xmax=45.5, color='green',alpha=0.2)
    axs[1].axvspan(xmin=44.5,xmax=45.5, color='green',alpha=0.2)

    axs[0].set_ylabel('Plasma enery', fontsize=fontsizelabel)
    axs[1].set_ylabel('NBI input power', fontsize=fontsizelabel)


    plt.tick_params(axis='both',labelsize=fontsizetick)

    plt.savefig(f'../../../bouloulou/power.png')
    plt.close()

    



if __name__ == '__main__':
    main()
