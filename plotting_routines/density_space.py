#!/usr/local/depot/Python-3.7/bin/python
# /usr/local/depot/Python-3.5.1/bin/python

from ppf import *
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.cm as cm
from matplotlib.colors import Normalize
from hoho import constant_function,read_kk3_2022
from thesis import constants

major_linewidth = constants.major_linewidth
fontsizelabel = constants.fontsizelabel
fontsizetick = constants.fontsizetick
fontsizetext = constants.fontsizetext

#####################################################################
# TEMPERATURE
phys_quantity = 'DENSITY'
dda_global = 'KK3'
dtype_temp = list(range(20, 71))
n = len(dtype_temp)
shot = 100247
time_inputs = np.arange(41.5, 49.3, 0.01)



#####################################################################
def main():
    
    print('')
    print(shot)
    out = read_kk3_2022.read_kk3_2022(shot = shot)

    for time_input in time_inputs:
        fig, ax = plt.subplots()
    
        list_psin = []
        list_temperature = []



        for nb in dtype_temp:
            dtype = 'TE' + str(nb)
            ihdat,iwdat,temperature,x,time,ier=ppfget(pulse=shot,dda=dda_global,dtyp=dtype)

            temp = np.interp([time_input], time, temperature)[0]
            psin = np.interp([time_input], out['time'], out['psin'][nb])[0]

            list_psin.append(psin)
            list_temperature.append(temp)

        ax.plot(list_psin,list_temperature,'o')
        ax.set_xlim(0,1)
        ax.set_ylim(0,3000)
        plt.savefig(f'../../../bouloulou/{round(time_input,3)}.png')
        plt.close()

if __name__ == '__main__':
    main()
