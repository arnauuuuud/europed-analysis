#!/usr/local/depot/Python-3.7/bin/python
# /usr/local/depot/Python-3.5.1/bin/python

from hoho import useful_recurring_functions, europed_analysis, global_functions, startup, find_pedestal_values_old, h5_manipulation, spitzer
from poster import plot_canvas
from mpl_toolkits.axes_grid1 import Divider, Size
import sys
import numpy as np
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import (
    QApplication, QWidget, QRadioButton, QVBoxLayout, QHBoxLayout,
    QLabel, QCheckBox, QLineEdit, QPushButton, QButtonGroup,  QSpacerItem, QSizePolicy
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import matplotlib.transforms as transforms
import math
import numpy as np
from matplotlib.patches import FancyArrowPatch
from scipy.interpolate import interp1d
import matplotlib
from thesis import constants

fontsizelabel = 50
fontsizetick = 20

matplotlib.rcParams['font.size'] = 14
matplotlib.rcParams['font.family'] = 'sans-serif'
matplotlib.rcParams['font.sans-serif'] = ['Droid Sans']

markers = [ 'D', 's', 'p', '*', 'h', 'H', '+', 'x', 'd', 'o', 'v', '^', '<', '>', '1', '2', '3', '4']
colors = ['blue', 'green', 'red', 'cyan', 'magenta', 'yellow', 'orange', 'purple', 'brown', 'pink', 'gray', 'olive', 'lime', 'teal', 'navy', 'sky blue', 'lavender', 'peach', 'maroon', 'turquoise', 'gold', 'silver', 'indigo', 'violet', 'burgundy', 'mustard', 'ruby', 'emerald', 'sapphire', 'amethyst']

etas = [0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0,1.5,2.0]

europed_names = [f'sb_eta{eta}_rs0.022_neped2.57' for eta in [0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0,1.5,2.0]]
x_parameter = 'alpha_helena_max'
crit = 'alfven'
crit_value = 0.05
envelope = True
list_consid_mode = [20]
hline = False
vline = False
legend = False

cm = 1/2.54

# fig, ax = plt.subplots(figsize=(13.7*cm,13.4*cm))

fig = plt.figure(figsize=(12.2*cm,14*cm),dpi=300)


# Define fixed size for the axes in inches
horiz = [Size.Fixed(2.5*cm),Size.Fixed(9.5*cm)]
vert = [Size.Fixed(1.6*cm),Size.Fixed(11*cm)]
divider = Divider(fig, (0, 0, 1, 1), horiz, vert, aspect=True, anchor=(0,0))

ax = fig.add_axes(divider.get_position(), axes_locator=divider.new_locator(nx=1, ny=1))


consid_mode_input = None
consid_mode_input_global = [3,7,10,20]
exclud_mode = None
main_delta = 4.5

dict_results = {}
for n in consid_mode_input_global:
    dict_results[str(n)] = []


for ieta,(eta,europed_name) in enumerate(zip(etas,europed_names)):
    europed_run = europed_name

    x_param = europed_analysis.get_x_parameter(europed_run, x_parameter)
    gammas, modes = europed_analysis.get_gammas(europed_run, crit)
    tab, consid_mode = europed_analysis.filter_tab_general(gammas, modes, consid_mode_input_global, exclud_mode)

    sorted_indices = np.argsort(x_param)
    x_param = x_param[sorted_indices]
    tab = tab[sorted_indices]

    deltas = europed_analysis.get_x_parameter(europed_run, 'delta')


    for icm,cm in enumerate(consid_mode):
        temp_x = x_param
        temp_y = tab[:,icm]
        nan_indices = np.isnan(temp_y)
        delta_filtered = temp_x[~nan_indices]
        y_filtered = temp_y[~nan_indices]

        print(delta_filtered)

        x_index1 = np.where(np.around(delta_filtered,5) == main_delta)[0]

        interpolator = interp1d(delta_filtered,y_filtered)
        


        print('yaaaaa')
        print(y_filtered)
        try:
            gamma_present = interpolator(main_delta)
            print('popopo')
            dict_results[str(cm)].append((eta,gamma_present))
            print('yiiiiiiiiii')
        except IndexError:
            continue


print(dict_results)

for mode in consid_mode_input_global:
    list_eta = []
    list_gamma = []

    for item in dict_results[str(mode)]:
        eta = item[0]
        gamma = item[1]
        list_eta.append(float(eta))
        list_gamma.append(gamma)


    ax.plot(list_eta,list_gamma,'o-', markersize=7,color = global_functions.dict_mode_newnew_color[int(mode)],mec='k',mew=0.5)



poop, y_label = global_functions.get_plot_labels_gamma_profiles(x_parameter, crit)

ax.set_xlabel('$\eta/\eta_{\mathrm{Sp}}$')
ax.set_ylim(bottom=0)

ax.set_ylabel(y_label)
# ax.set_ylim(bottom=0,top=0.8)
ax.text(0.5, 0.01, rf'$n=3$', transform=ax.transData, fontsize=fontsizetick, va='bottom', ha='left', color = global_functions.dict_mode_newnew_color[int(3)])
ax.text(0.5, 0.04, rf'$n=7$', transform=ax.transData, fontsize=fontsizetick, va='bottom', ha='left', color = global_functions.dict_mode_newnew_color[int(7)])
ax.text(0.5, 0.065, rf'$n=10$', transform=ax.transData, fontsize=fontsizetick, va='bottom', ha='left', color = global_functions.dict_mode_newnew_color[int(10)])
ax.text(0.5, 0.09, rf'$n=20$', transform=ax.transData, fontsize=fontsizetick, va='bottom', ha='left', color = global_functions.dict_mode_newnew_color[int(20)])
# ax.text(0.5, 0.45, r'$\mathbf{5}$', transform=ax.transData, fontsize=fontsizetick, va='bottom', ha='left', color = constants.get_new_color_mode(int(5)))
# ax.text(0.1, 0.55, r'$\mathbf{7}$', transform=ax.transData, fontsize=fontsizetick, va='bottom', ha='left', color = constants.get_new_color_mode(int(7)))
# ax.text(0.1, 0.37, rf'$20$', transform=ax.transData, fontsize=fontsizetick, va='bottom', ha='left', color = constants.get_new_color_mode(int(20)))
# ax.text(0.1, 0.19, rf'$30$', transform=ax.transData, fontsize=fontsizetick, va='bottom', ha='left', color = constants.get_new_color_mode(int(30)))
# ax.text(0.5, 0.03, rf'$40$', transform=ax.transData, fontsize=fontsizetick, va='bottom', ha='center', color = constants.get_new_color_mode(int(40)))

# ax.set_yticks([0,0.3,0.6])

ax.axvspan(1.136,2.143,alpha=0.2,color='forestgreen')
mean = (1.136+2.143)/2
ax.text(mean,0.03,r'$\eta_{\mathrm{neo}}$',ha='center',va='center',fontsize=40, color='forestgreen')
        
# ax.text(0.95, 0.95,'(c)', transform=ax.transAxes, fontsize=fontsizetick, va='top', ha='right', color = 'black')


# plt.subplots_adjust(top=0.99,
# bottom=0.17,
# left=0.17,
# right=0.99,
# hspace=0.2,
# wspace=0.2)

plt.savefig('/home/jwp9427/cococo/2b')
plt.close()
 