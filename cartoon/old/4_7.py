#!/usr/local/depot/Python-3.7/bin/python
# /usr/local/depot/Python-3.5.1/bin/python

from paper import constants
import matplotlib.pyplot as plt
from hoho import getprofile, europed_analysis, global_functions, startup, find_pedestal_values
import matplotlib.transforms as transforms
from matplotlib.colors import Normalize
import math
from hoho import europed_hampus as europed
import numpy as np
import matplotlib as mpl

major_linewidth = constants.major_linewidth
fontsizelabel = constants.fontsizelabel
fontsizetick = constants.fontsizetick
fontsizetext = constants.fontsizetext
colorv = constants.colorv
colorh = constants.colorh

ne_color = constants.ne_color
te_color = constants.te_color
j_color = constants.j_color
pe_color = constants.pe_color

# europed_name1 = 'eagle_eta0_ds0'
# europed_name2 = 'eagle_eta0_ds2'
# europed_name3 = 'eagle_eta0_ds3'

min_value = 1.04
max_value = 5.14
ticks=[1,2,3,4,5]
label = r'${n_e^{\mathrm{ped}}}_{[10^{19}m^{-3}]}$'
cmap = constants.neped_cmap


list_neped = [1.04, 1.29, 1.55, 1.80, 2.06, 2.31, 2.57, 2.83, 3.35, 3.86, 5.14]


def main():

    fig, ax = plt.subplots(1,1,figsize = (5,5))

    for neped in list_neped:

        color = constants.get_color_neped(float(neped))

        w1 = 0.022
        europed_run = f'kudu_{neped}' if neped != 1.8 else 'kudu_1.80'

        iax = 0
        a1 = europed.EuropedHDF5(europed_run)
        deltas = a1.get_scan_data("delta")
        ne = a1.get_scan_data("ne")
        te = a1.get_scan_data("te")
        profiles = 1.6*ne*te
        psis =  a1.get_scan_data("psi")
        del a1


        index1 = np.where(np.around(deltas,5) == w1)[0]
        psi_1 = psis[index1][0]
        ne_1 = ne[index1][0]
        te_1 = te[index1][0]

        y_1 = ne_1
        ax.plot(psi_1,y_1, color=color)


    ax.set_ylim(bottom=0,top=5.2)
    ax.set_ylabel(r'$n_e$ $_{[10^{19}\mathrm{m}^{-3}]}$',fontsize=fontsizelabel)
    ax.set_xlim(left=0.95,right=1)
    ax.set_xlabel(r'$\psi_N$',fontsize=fontsizelabel)
    
    plt.savefig('/home/jwp9427/bouloulou/4_7')
    plt.close()
    # plt.show()

if __name__ == '__main__':
    main()

