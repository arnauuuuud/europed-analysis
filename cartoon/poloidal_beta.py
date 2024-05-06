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
dda_global = 'EFIT'
dtype_temp = 'BTPM'
shot = 84794
time_inputs = [45.51]




#####################################################################
def main():
    

    for time_input in time_inputs:
        fig, ax = plt.subplots()
    
        list_psin = []
        list_temperature = []



        for dtype in dtype_temp:
            
            ihdat,iwdat,temperature,x,time,ier=ppfget(pulse=shot,dda=dda_global,dtyp=dtype)

            print(temperature[0])


            list_psin.append(psin)
            list_temperature.append(temp)

        ax.plot(list_psin,list_temperature,'o')
        ax.set_xlim(0,1)
        # ax.set_ylim(0,3000)
        plt.show()
        plt.close()

if __name__ == '__main__':
    main()
