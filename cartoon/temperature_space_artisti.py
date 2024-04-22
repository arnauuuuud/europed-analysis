#!/usr/local/depot/Python-3.7/bin/python
# /usr/local/depot/Python-3.5.1/bin/python

from ppf import *
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.cm as cm
from matplotlib.colors import Normalize
from hoho import constant_function,read_kk3_2022
from paper import constants

major_linewidth = constants.major_linewidth
fontsizelabel = constants.fontsizelabel
fontsizetick = constants.fontsizetick
fontsizetext = constants.fontsizetext

#####################################################################
# TEMPERATURE
phys_quantity = 'TEMPERATURE'
dda_global = 'KK3'
dtype_temp = list(range(20, 71))
n = len(dtype_temp)
shot = 100247
time_inputs = [46.69,48.58]


def get_color_temperature(value):
    value = max(0, min(3000, value))
    norm = Normalize(vmin=0, vmax=3000)
    normalized_value = norm(value)
    sm = plt.cm.ScalarMappable(cmap='inferno_r')
    rgba_color = sm.cmap(normalized_value)
    return rgba_color



#####################################################################
def main():
    
    print('')
    print(shot)
    out = read_kk3_2022.read_kk3_2022(shot = shot)
    fig, axs = plt.subplots(2,1, sharex=True)

       


    for ax,time_input in zip(axs,time_inputs):
        list_psin = []
        list_temperature = []


        for nb in dtype_temp:
            dtype = 'TE' + str(nb)
            ihdat,iwdat,temperature,x,time,ier=ppfget(pulse=shot,dda=dda_global,dtyp=dtype)

            temp = np.interp([time_input], time, temperature)[0]
            psin = np.interp([time_input], out['time'], out['psin'][nb])[0]

            list_psin.append(psin)
            list_temperature.append(temp)

        # list_psin = np.linspace(0,1,1000)
        # list_temperature = np.linspace(0,1500,1000) if time_input==46.69 else np.linspace(0,3000,1000)

        #ax.plot(list_psin,list_temperature,'o')



        # x = list_psin[::-1]
        # z = list_temperature[::-1]
        # norm = Normalize(vmin=0, vmax=3000)

        list_temperature = np.array(list_temperature)
        list_psin = np.array(list_psin)

        nan_indices = ~np.isnan(list_temperature) & ~np.isnan(list_psin)
        list_temperature_new = list_temperature[nan_indices][::-1]
        list_psin_new = list_psin[nan_indices][::-1]

        print('\n')
        print('\n')
        print('\n')
        print(list_psin_new)
        print('\n')
        print(list_temperature_new)



        interpolated_psin = np.linspace(list_psin_new[0], list_psin_new[-1], 1000) 
        interpolated_temp = np.interp(interpolated_psin,list_psin_new,list_temperature_new)

        print('\n')
        print(interpolated_psin)
        print('\n')
        print(interpolated_temp)

        for x,temp in zip(interpolated_psin,interpolated_temp):
            ax.axvline(x, color=get_color_temperature(temp))

        #Z, X = np.meshgrid(z, x)

        #ax.imshow(Z, cmap='inferno_r', norm=norm, aspect='auto', extent=[0, 1, 0, 1]) 
        #ax.set_xlim(0,1)
        ax.set_yticks([]) 

    plt.show()

if __name__ == '__main__':
    main()
