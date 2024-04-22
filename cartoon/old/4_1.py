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
   
    fig = plt.figure(figsize=(6, 5))

    gs1 = GridSpec(1, 1)
    gs1.update(left=0.085, right=0.15, bottom=0.2, top=0.98, wspace=0.05)
    gs2 = GridSpec(1, 1)
    gs2.update(left=0.42, right=0.98, bottom=0.2, top=0.98, wspace=0.02)



    ax = plt.subplot(gs1[0])

    dict_mode_color=global_functions.dict_mode_new_color

    colors = list(dict_mode_color.values())
    cmap = ListedColormap(colors)

    # Create a colorbar with specified colors
    bounds = list(dict_mode_color.keys()) + [max(dict_mode_color.keys()) + 1]
    norm = BoundaryNorm(bounds, cmap.N)
    cm = plt.cm.ScalarMappable(norm=norm, cmap=cmap)
    cm.set_array([])
    cb = plt.colorbar(cm, cax=ax, orientation='vertical')
    ticks_positions = [(i + j) / 2 for i, j in zip(bounds[:-1], bounds[1:])]
    cb.set_ticks(ticks_positions)
    cb.set_ticklabels(list(dict_mode_color.keys()))
    ax.text(0.5, -0.01, r'$n$', ha='center', va='top', fontsize=fontsizelabel)   

    ax.tick_params(axis='both', which='both', length=0)
    ax.yaxis.set_ticks_position('left')




    ax = plt.subplot(gs2[0])
    europed_run = 'eagle_eta0.5_ds0'
    crit = "diamag"
    crit_value=0.25
    plot_hline = True
    plot_vline = True
    x_parameter = 'alpha_helena_max'
    consid_mode_input = None
    exclud_mode = None
    list_legends = {}
    


    x_param = europed_analysis.get_x_parameter(europed_run, x_parameter)
    delta = europed_analysis.get_x_parameter(europed_run, 'delta')
    gammas, modes = europed_analysis.get_gammas(europed_run, crit)
    tab, consid_mode = europed_analysis.filter_tab_general(gammas, modes, consid_mode_input, exclud_mode)

    sorted_indices = np.argsort(x_param)
    x_param = x_param[sorted_indices]
    tab = tab[sorted_indices]
    delta = delta[sorted_indices]

    consid_mode = sorted(consid_mode, key=lambda x: int(x))
    for i, mode in enumerate(consid_mode):
        
        temp_x = x_param
        temp_y = tab[:,i]
        nan_indices = np.isnan(temp_y)
        x_filtered = temp_x[~nan_indices]
        delta_filtered = delta[~nan_indices]
        y_filtered = temp_y[~nan_indices]

        minus = np.where(x_filtered<6.9)
        x_filtered = x_filtered[minus]
        y_filtered = y_filtered[minus]
        delta_filtered = delta_filtered[minus]

        minus = np.where(delta_filtered>0.0145)
        x_filtered = x_filtered[minus]
        y_filtered = y_filtered[minus]

        # list_legends[mode], = ax.plot(x_filtered,y_filtered,"o-",label=mode, color=constants.get_new_color_mode(int(mode)),mec='black', mew=0.5)

    # minus = np.where(x_param<6.9)
    # x_param = x_param[minus]
    # tab = tab[minus]
    # delta = delta[minus]

    # minus = np.where(delta>0.0145)
    # x_param = x_param[minus]
    # tab = tab[minus]

    x_plot,y_plot = europed_analysis.give_envelop(tab, x_param)
    ax.plot(x_plot,y_plot,'k')

    ax.axhline(crit_value, linestyle="-",color=colorh,linewidth=major_linewidth)
    ax.axhspan(ymin=0.85*crit_value,ymax=1.15*crit_value, color=colorh, alpha=0.2)
        
            

    x_label, y_label = global_functions.get_plot_labels_gamma_profiles(x_parameter, crit)
    ax.set_xlabel(x_label, fontsize = fontsizelabel)
    ax.set_ylabel(y_label, fontsize = fontsizelabel)
    plt.tick_params(axis='both', which='major', labelsize=fontsizetick)
    ax.set_ylim(bottom=0,top=1.1)
    ax.set_xlim(left=0,right=7)

    plt.savefig('/home/jwp9427/bouloulou/4_1')
    plt.close()



if __name__ == '__main__':
    main()