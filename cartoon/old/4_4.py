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
from scipy.interpolate import interp1d
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

europed_name = 'eagle_eta0_ds0'

min_value = -1
max_value = 3
ticks=[-1,0,1,2,3]
label = r'$\Delta [\%]$'
cmap = constants.rs_cmap

list_ds = [-1,-0.5,0,0.5,1,2,3]
w = 0.021



def main():

    fig, ax = plt.subplots(1,1,figsize = (5,5))

    list_eta = [0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1]
    crit = 'diamag'
    crit_value = 0.25
    x_parameter = 'alpha_helena_max'
    plot_hline = True
    consid_mode_input_global = ['1','3','4','5']
    list_emptys = [[],[],[],[],[],[],[],[],[],[],[]]
    dict_results = dict(zip(consid_mode_input_global, list_emptys))
    exclud_mode = None

    consid_mode_input = None

    for irs,eta in enumerate(list_eta):

        color = constants.get_color_eta(eta)

        europed_run = f'eagle_eta0_ds0'

        a1 = europed.EuropedHDF5(europed_run)
        deltas = a1.get_scan_data("delta")
        ne = a1.get_scan_data("ne")
        te = a1.get_scan_data("te")
        profiles = 1.6*ne*te
        psis =  a1.get_scan_data("psi")
        del a1


        index1 = np.where(np.around(deltas,5) == w)[0]
        psi_1 = psis[index1][0]
        ne_1 = ne[index1][0]
        te_1 = te[index1][0]

        y_1 = te_1**(-3/2)*eta
        ax.set_ylim(bottom=0,top=35)
        ax.set_ylabel(r'$\eta$ $_{[\mathrm{a.u.}]}$',fontsize=fontsizelabel)
        ax.set_xlabel(r'$\psi_N$',fontsize=fontsizelabel)
        
        ax.plot(psi_1,y_1, color=color)
        ax.set_xlim(left=0.95,right=1)
        #ax.set_yticks([0,1,2,3],[0,1,2,3])

    # plt.show()
    plt.savefig('/home/jwp9427/bouloulou/4_4b')
    plt.close()

if __name__ == '__main__':
    main()

