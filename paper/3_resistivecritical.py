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
list_eta = [0,0.3,0.5,0.8,1]
europed_runs = [f'tan_eta{eta}_rs0.022_neped2.57_betap1.3' for eta in list_eta]
crit = 'alfven'
crit_value = 0.1
fixed_width = False
color_exp = plot_canvas.colorHPLG
color_europed_n20 = plot_canvas.color_n20
color_europed_n50 = plot_canvas.color_n50
linestyle_n20 = plot_canvas.linestyle_n20
shot = 84794
dda = 'T052'
markersize = 20
alpha = 0.5
x_parameter = 'alpha_helena_max'
q_ped_def = 'tepos-delta'

fig, ax = plt.subplots()


crit_value = 0.1
linestyle = plot_canvas.linestyle_t01

list_x = []
list_y = []
list_consid_mode = [1, 2, 3, 4, 5, 7, 10, 20, 30, 40, 50]
for eta,europed_run in zip(list_eta,europed_runs):
    list_x.append(eta)
    y = europed_analysis_2.critical_value_europed_name_withoutlowerpoint(europed_run, crit, crit_value, x_parameter, q_ped_def='tepos-delta', list_consid_mode=list_consid_mode)
    list_y.append(y)
ax.plot(list_x, list_y, marker='o', color=color_europed_n50, linestyle=linestyle)

list_x = []
list_y = []
list_consid_mode = [1, 2, 3, 4, 5, 7, 10, 20]
for eta,europed_run in zip(list_eta,europed_runs):
    list_x.append(eta)
    y = europed_analysis_2.critical_value_europed_name_withoutlowerpoint(europed_run, crit, crit_value, x_parameter, q_ped_def='tepos-delta', list_consid_mode=list_consid_mode)
    list_y.append(y)
ax.plot(list_x, list_y, marker='o', color=color_europed_n20, linestyle=linestyle)




crit_value = 0.03
linestyle = plot_canvas.linestyle_t003

list_x = []
list_y = []
list_consid_mode = [1, 2, 3, 4, 5, 7, 10, 20, 30, 40, 50]
for eta,europed_run in zip(list_eta,europed_runs):
    list_x.append(eta)
    y = europed_analysis_2.critical_value_europed_name_withoutlowerpoint(europed_run, crit, crit_value, x_parameter, q_ped_def='tepos-delta', list_consid_mode=list_consid_mode)
    list_y.append(y)
ax.plot(list_x, list_y, marker='o', color=color_europed_n50, linestyle=linestyle)

list_x = []
list_y = []
list_consid_mode = [1, 2, 3, 4, 5, 7, 10, 20]
for eta,europed_run in zip(list_eta,europed_runs):
    list_x.append(eta)
    y = europed_analysis_2.critical_value_europed_name_withoutlowerpoint(europed_run, crit, crit_value, x_parameter, q_ped_def='tepos-delta', list_consid_mode=list_consid_mode)
    list_y.append(y)
ax.plot(list_x, list_y, marker='o', color=color_europed_n20, linestyle=linestyle)

alpha, alpha_error = experimental_values.get_alpha_max(shot, dda)

ax.axhline(alpha, color = color_exp)
(r,g,b) = mcolors.to_rgb(color_exp)
backgroundcolor = (r, g, b, 0.2)
ax.text(0.5, alpha, r'$\alpha_{\mathrm{max}}(\mathrm{exp})$', ha='center', va='center', color=color_exp,
         bbox=dict(facecolor='white', edgecolor='none', pad=3))

ax.axhspan(alpha-alpha_error, alpha+alpha_error, color=color_exp, alpha=0.2, zorder=100)

ax.axvline(1, color='black')
ax.text(1,0.5,r'$\eta=\eta_{\mathrm{neo}}$', rotation=90, backgroundcolor='white', ha='center', va='bottom')

ax.set_xlim(left=0, right=1.05)
ax.set_ylim(bottom=0)



ax.set_ylabel(global_functions.get_critical_plot_label(x_parameter))
ax.set_xlabel(global_functions.eta_label)

plt.show()