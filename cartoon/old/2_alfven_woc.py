#!/usr/local/depot/Python-3.7/bin/python
# /usr/local/depot/Python-3.5.1/bin/python

from paper import constants
import matplotlib.pyplot as plt
from hoho import europed_analysis, global_functions, startup
import matplotlib.transforms as transforms
from matplotlib.colors import Normalize
from matplotlib.colors import ListedColormap, BoundaryNorm
import math
import numpy as np
from matplotlib.gridspec import GridSpec,GridSpecFromSubplotSpec
import matplotlib.patches as patches

major_linewidth = constants.major_linewidth
fontsizelabel = constants.fontsizelabel
fontsizetick = constants.fontsizetick
fontsizetext = constants.fontsizetext
colorv = constants.colorv
colorh = constants.colorh


def main():
   
    fig, ax = plt.subplots(figsize=(4.8,4.32))



    europed_run = 'eagle_eta1_ds0'
    crit = "diamag"
    crit_value=0.25
    plot_hline = True
    plot_vline = True
    x_parameter = 'delta'
    consid_mode_input = [1]
    exclud_mode = None
    list_legends = {}
    


    x_param = europed_analysis.get_x_parameter(europed_run, x_parameter)
    gammas, modes = europed_analysis.get_gammas(europed_run, crit)
    tab, consid_mode = europed_analysis.filter_tab_general(gammas, modes, consid_mode_input, exclud_mode)

    sorted_indices = np.argsort(x_param)
    x_param = x_param[sorted_indices]
    tab = tab[sorted_indices]

    consid_mode = sorted(consid_mode, key=lambda x: int(x))
    for i, mode in enumerate(consid_mode):
        
        temp_x = x_param
        temp_y = tab[:,i]
        nan_indices = np.isnan(temp_y)
        x_filtered = temp_x[~nan_indices]
        y_filtered = temp_y[~nan_indices]


        list_legends[mode], = ax.plot(x_filtered,y_filtered,"-",linewidth=major_linewidth, label=mode, color='k',mec='black', mew=0.5)

    #ax.axhline(crit_value, linestyle="-",color=colorh,linewidth=major_linewidth)

        
            

    x_label, y_label = global_functions.get_plot_labels_gamma_profiles(x_parameter, crit)
    ax.set_xlabel(x_label, fontsize = fontsizelabel)
    ax.set_ylabel(y_label, fontsize = fontsizelabel)
    plt.tick_params(axis='both', which='major', labelsize=fontsizetick)
    ax.set_ylim(bottom=0)
    ax.set_xlim(left=0)

    plt.savefig('/home/jwp9427/bouloulou/2_alfven0')
    plt.close()



if __name__ == '__main__':
    main()