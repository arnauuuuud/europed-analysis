#!/usr/local/depot/Python-3.7/bin/python
# /usr/local/depot/Python-3.5.1/bin/python

from hoho import pedestal_values, experimental_values, europed_analysis_2, global_functions
from paper import plot_canvas
from mpl_toolkits.axes_grid1 import Divider, Size
from ppf import *
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.cm as cm
from matplotlib.colors import Normalize
from thesis import constants
import matplotlib.colors as mcolors
from scipy.interpolate import interp1d
major_linewidth = constants.major_linewidth
fontsizelabel = constants.fontsizelabel
fontsizetick = constants.fontsizetick
fontsizetext = constants.fontsizetext

#####################################################################
europed_run_eta0 = 'global_v4_84794_eta0_betan3.07_neped2.55_nesepneped0.33'
europed_run_eta1 = 'global_v4_84794_eta1_betan3.07_neped2.55_nesepneped0.33'
crit = 'alfven'
crit_value = 0.03
crit_value_update = 0.08
fixed_width = False
color_exp = plot_canvas.colorHPLG
color_europed_eta0 = plot_canvas.color_eta0
color_europed_n50 = plot_canvas.color_n50
color_europed_n20 = plot_canvas.color_n20
linestyle_n20 = plot_canvas.linestyle_n20
shot = 84794
dda = 'T052'
markersize = 20
alpha = 0.5
x_parameter = 'alpha_helena_max'
q_ped_def = 'tepos-delta'
folder_to_save = '/home/jwp9427/work/figures/2025-03-05_paper/'


fig, ax = plt.subplots()



list_consid_mode = [1, 2, 3, 4, 5, 7, 10, 20, 30, 40, 50]
x_param = europed_analysis_2.get_x_parameter(europed_run_eta0, x_parameter, q_ped_def)
deltas = europed_analysis_2.get_x_parameter(europed_run_eta0, 'delta')
dict_gamma = europed_analysis_2.get_gammas(europed_run_eta0, crit, fixed_width)
dict_gamma = europed_analysis_2.filter_dict(dict_gamma, list_consid_mode)
deltas_to_plot = list(dict_gamma.keys())
x_to_plot = europed_analysis_2.give_matching_x_with_deltas(sorted(deltas), sorted(x_param), deltas_to_plot)
delta_gamma_n = europed_analysis_2.give_maximal_n(dict_gamma)
for x_par,(delta,gamma,n) in zip(x_to_plot[::4],delta_gamma_n[::4]):
    if x_par>7:
        continue
    if x_par>5:
        ax.text(x_par, gamma, n, fontsize=10, verticalalignment='top', horizontalalignment='left', color=color_europed_eta0)
    else:
        ax.text(x_par, gamma, n, fontsize=10, verticalalignment='bottom', horizontalalignment='right', color=color_europed_eta0)
x_envelope, y_envelope = europed_analysis_2.give_envelop(dict_gamma, deltas, x_parameter=x_param)
ax.plot(x_envelope, y_envelope, color=color_europed_eta0, label=europed_run_eta0)


list_consid_mode = [1, 2, 3, 4, 5, 7, 10, 20, 30, 40, 50]
x_param = europed_analysis_2.get_x_parameter(europed_run_eta1, x_parameter, q_ped_def)
deltas = europed_analysis_2.get_x_parameter(europed_run_eta1, 'delta')
dict_gamma = europed_analysis_2.get_gammas(europed_run_eta1, crit, fixed_width)
dict_gamma = europed_analysis_2.filter_dict(dict_gamma, list_consid_mode)
deltas_to_plot = list(dict_gamma.keys())
x_to_plot = europed_analysis_2.give_matching_x_with_deltas(sorted(deltas), sorted(x_param), deltas_to_plot)
delta_gamma_n = europed_analysis_2.give_maximal_n(dict_gamma)
for x_par,(delta,gamma,n) in zip(x_to_plot[::4],delta_gamma_n[::4]):
    if n == 40 or x_par>5.4:
        continue
    ax.text(x_par, gamma, n, fontsize=10, verticalalignment='bottom', horizontalalignment='right', color=color_europed_n50)
x_envelope, y_envelope = europed_analysis_2.give_envelop(dict_gamma, deltas, x_parameter=x_param)
ax.plot(x_envelope, y_envelope, color=color_europed_n50, label=europed_run_eta1)



list_consid_mode = [1, 2, 3, 4, 5, 7, 10, 20]
x_param = europed_analysis_2.get_x_parameter(europed_run_eta1, x_parameter, q_ped_def)
deltas = europed_analysis_2.get_x_parameter(europed_run_eta1, 'delta')
dict_gamma = europed_analysis_2.get_gammas(europed_run_eta1, crit, fixed_width)
dict_gamma = europed_analysis_2.filter_dict(dict_gamma, list_consid_mode)
deltas_to_plot = list(dict_gamma.keys())
x_to_plot = europed_analysis_2.give_matching_x_with_deltas(sorted(deltas), sorted(x_param), deltas_to_plot)
delta_gamma_n = europed_analysis_2.give_maximal_n(dict_gamma)
for x_par,(delta,gamma,n) in zip(x_to_plot[::4],delta_gamma_n[::4]):
    if x_par>7 or (x_par>4.5 and x_par<5.2):
        continue
    ax.text(x_par, gamma, n, fontsize=10, verticalalignment='bottom', horizontalalignment='right', color=color_europed_n20)
x_envelope, y_envelope = europed_analysis_2.give_envelop(dict_gamma, deltas, x_parameter=x_param)
ax.plot(x_envelope, y_envelope, color=color_europed_n20, label=europed_run_eta1)

linestyle_t003 = plot_canvas.linestyle_t003
linestyle_t01 = plot_canvas.linestyle_t01
ax.axhline(crit_value, color='black', linestyle=linestyle_t003)
ax.axhline(crit_value_update, color='black', linestyle=linestyle_t01)
ax.text(0.05,crit_value, rf'$t = {crit_value}$', fontsize=10, va='bottom', ha='left')
ax.text(0.05,crit_value_update, rf'$t = {crit_value_update}$', fontsize=10, va='bottom', ha='left')
ax.set_xlim(left=0, right=7)
ax.set_ylim(bottom=0)

xlabel, ylabel = global_functions.get_plot_labels_gamma_profiles(x_parameter, crit)
ax.set_xlabel(xlabel)
ax.set_ylabel(ylabel)


plt.savefig(folder_to_save+'2.png')
plt.show()