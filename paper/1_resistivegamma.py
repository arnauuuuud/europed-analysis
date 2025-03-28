#!/usr/local/depot/Python-3.7/bin/python
# /usr/local/depot/Python-3.5.1/bin/python

from hoho import pedestal_values, experimental_values, global_functions, europed_analysis_2
from matplotlib.colors import LinearSegmentedColormap
from paper import plot_canvas
from mpl_toolkits.axes_grid1 import Divider, Size
from ppf import *
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.cm as cm
from matplotlib.colors import Normalize
import matplotlib.colors as mcolors
from scipy.interpolate import interp1d

#####################################################################
europed_name = 'global_v4_84794_eta0_betan3.07_neped2.55_nesepneped0.33'
crit = 'alfven'
crit_value = 0.03
fixed_width = False
exclud_mode = []
color_exp = plot_canvas.colorHPLG
color_eta0 = plot_canvas.color_eta0
color_eta1 = plot_canvas.color_eta1
shot = 84794
dda = 'T052'
markersize = 20
alpha = 0.5
folder_to_save = '/home/jwp9427/work/figures/2025-03-05_paper/'
x_parameter = 'alpha_helena_max'
q_ped_def = 'positionTeped'
fig, axs = plt.subplots(1, 3)


cmap = LinearSegmentedColormap.from_list('custom_gradient', [color_eta0, color_eta1], N=256)
list_eta = [0,0.2,0.6,1]

consid_modes = [[10],[20],[50]]
labels = ['a', 'b', 'c']

for i,list_consid_mode in enumerate(consid_modes):
    for eta in list_eta:
        if eta == 1:
            color = 'green'
        else:
            color = cmap(eta)
        europed_run = f'global_v4_84794_eta{eta}_betan3.07_neped2.55_nesepneped0.33'
        x_param = europed_analysis_2.get_x_parameter(europed_run, x_parameter, q_ped_def)
        if not fixed_width:
            deltas = europed_analysis_2.get_x_parameter(europed_run, 'delta')
        else:
            deltas = europed_analysis_2.get_x_parameter(europed_run, 'betaped')

        dict_gamma = europed_analysis_2.get_gammas(europed_run, crit, fixed_width)
        dict_gamma = europed_analysis_2.filter_dict(dict_gamma, list_consid_mode)
        dict_gamma_r = europed_analysis_2.reverse_nested_dict(dict_gamma)


        for mode in dict_gamma_r.keys():
            dict_gamma_n = dict_gamma_r[mode]
            deltas_to_plot = list(dict_gamma_n.keys())
            x_to_plot = europed_analysis_2.give_matching_x_with_deltas(sorted(deltas), sorted(x_param), deltas_to_plot)
            y = list(dict_gamma_n.values())
            axs[i].plot(x_to_plot, y, color=color)
    axs[i].set_ylim(bottom=0)
    axs[i].set_xlim(left=1.8,right=5.8)
    axs[i].set_xlabel(global_functions.alpha_label)
    axs[i].set_xlabel(global_functions.gammaalfven_label)

    axs[i].text(0.05,0.95, rf'({labels[i]}) $n={list_consid_mode[0]}$', transform=axs[i].transAxes, ha='left', va='top')

plt.savefig(folder_to_save+'1.png')
plt.show()