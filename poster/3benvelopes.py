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
import matplotlib.transforms as transforms
import math
import numpy as np
from matplotlib.patches import FancyArrowPatch
import matplotlib as mpl
import matplotlib.colors as mcolors

markers = [ 'D', 's', 'p', '*', 'h', 'H', '+', 'x', 'd', 'o', 'v', '^', '<', '>', '1', '2', '3', '4']
colors = ['blue', 'green', 'red', 'cyan', 'magenta', 'yellow', 'orange', 'purple', 'brown', 'pink', 'gray', 'olive', 'lime', 'teal', 'navy', 'sky blue', 'lavender', 'peach', 'maroon', 'turquoise', 'gold', 'silver', 'indigo', 'violet', 'burgundy', 'mustard', 'ruby', 'emerald', 'sapphire', 'amethyst']


europed_names = [f'sb_eta{eta}_rs0.022_neped2.57' for eta in [0.0,0.5,1.0,1.5,2.0]]
etas = [0.0,0.5,1.0,1.5,2.0]
x_parameter = 'alpha_helena_max'
crit = 'alfven'
crit_value = 0.05
envelope = True
list_consid_mode = [1,2,3,4,5,7,10,20]
hline = True
vline = False
legend = False
cm = 1/2.54
# fig, axs = plt.subplots(1,2,figsize=(13.7*cm,13.4*cm), gridspec_kw={'width_ratios': [10, 1]})
fig = plt.figure(figsize=(14*cm,14*cm),dpi=300)

# Define fixed size for the axes in inches
horiz = [Size.Fixed(2.5*cm),Size.Fixed(9.5*cm),Size.Fixed(0.2*cm),Size.Fixed(0.7*cm)]
vert = [Size.Fixed(1.6*cm),Size.Fixed(11*cm)]

divider = Divider(fig, (0, 0, 1, 1), horiz, vert, aspect=True, anchor=(0,0))

ax = fig.add_axes(divider.get_position(), axes_locator=divider.new_locator(nx=1, ny=1))
ax1 = fig.add_axes(divider.get_position(), axes_locator=divider.new_locator(nx=3, ny=1))

def get_color_eta(eta, cmap='inferno_r'):

    normalized_eta = eta*0.8/2 + 0.2
    print(normalized_eta)
    color = plt.get_cmap(cmap)(normalized_eta)
    return color

def run(europed_names, x_parameter, crit, crit_value, envelope, list_consid_mode, hline, vline, legend):

    # Clear the existing plot
    ax.clear()

    print('')
    print('')
    print('############### Updated parameters ###############')
    print(f'# List of runs:        {europed_names}')
    print(f'# X-axis parameter:    {x_parameter}')
    print(f'# Critical value:      {crit_value}')
    print(f'# Stability criterion: {crit}')
    print(f'# Plot envelope:       {envelope}')
    print(f'# Modes:               {list_consid_mode}')
    print(f'# Plot H-line:         {hline}')
    print(f'# Plot V-line:         {vline}')
    print('##################################################')
    print('')


    sample_points = np.linspace(0.2, 0.8, len(europed_names))
    colors = plt.cm.inferno_r(sample_points)

    for iplot,(europed_run,eta) in enumerate(zip(europed_names,etas)):
        try:
            res = europed_analysis.get_x_parameter(europed_run, x_parameter)
            if type(res) == str and res == 'File not found':
                continue
            else:
                x_param = res
            gammas, modes = europed_analysis.get_gammas(europed_run, crit)
            try:
                tab, consid_mode = europed_analysis.filter_tab_general(gammas, modes, list_consid_mode,[])
            except TypeError as e:
                print(e)
                continue        
            sorted_indices = np.argsort(x_param)
            x_param = x_param[sorted_indices]
            tab = tab[sorted_indices]
            
            list_mode_to_plot = [mode for mode in list_consid_mode if mode in modes]


            if not envelope:
                for i, mode in enumerate(list_mode_to_plot):
                    temp_x = x_param
                    temp_y = tab[:,i]
                    nan_indices = np.isnan(temp_y)
                    x_filtered = temp_x[~nan_indices]
                    y_filtered = temp_y[~nan_indices]
                    ax.plot(x_filtered,y_filtered, color=global_functions.dict_mode_color[int(mode)], marker=markers[iplot], label=f'{europed_run} - {mode}')
            
            else:
                x_envelope, y_envelope = europed_analysis.give_envelop(tab, x_param)
                ax.plot(x_envelope, y_envelope, color=colors[iplot], label=europed_run)


            has_unstable, x_crit, col, critn = europed_analysis.find_critical(x_param, tab, list_mode_to_plot, crit_value)
            colorvline = colors[iplot]
            if has_unstable and vline:
                if not envelope:
                    colorvline = 'r'
                else:
                    colorvline = colors[iplot] 

                ax.axvline(x_crit, color=colorvline, linestyle=':')
            xmin,xmax,ymin,ymax = ax.axis()
            ratio = (x_crit-xmin)/(xmax-xmin)
            trans = transforms.blended_transform_factory(ax.transData, ax.transAxes)
            x_crit = np.abs(x_crit)
            x_crit_order = math.floor(math.log10(x_crit))
            x_crit_round = np.around(np.around(x_crit*10**-x_crit_order,1)*10**x_crit_order,6)

            ax.scatter(x_crit, crit_value, color=colorvline,transform=ax.transData,marker='o', linewidths=1, edgecolors='black', s=70, zorder=20, clip_on=False)
        except RuntimeError:
            print(f"{europed_run:>40} RUNTIME ERROR : NO FIT FOUND")
        except FileNotFoundError:
            print(f"{europed_run:>40} FILE DOES NOT EXIST")
        except IndexError as e:
            print(e)
            continue

    # ax.scatter(x_crit, crit_value, color=colorvline,transform=trans,zorder=20,marker='x', clip_on=False)
    # ax.axvline(x_crit, color='red', linestyle=':',ymin=crit_value/0.1)

    has_unstable, x_crit_min, col, critn = europed_analysis.find_critical(x_param, tab, list_mode_to_plot, 0.85*crit_value)
    has_unstable, x_crit_max, col, critn = europed_analysis.find_critical(x_param, tab, list_mode_to_plot, 1.15*crit_value)

    # ax.spines['top'].set_position(('outward', 10))

    # ax.axvline(x_crit_min, color='red', linestyle=':',ymin=0.85*crit_value/0.1,linewidth=0.5)
    # ax.axvline(x_crit_max, color='red', linestyle=':',ymin=1.15*crit_value/0.1,linewidth=0.5)    
    # # ax.axvspan(x_crit_min, x_crit_max, color='red', ymin=1.15*crit_value/0.1, alpha=0.2)
    # p2 = FancyArrowPatch((x_crit_min, 1.03*0.1), (x_crit_max, 1.03*0.1), arrowstyle='|-|', mutation_scale=2, clip_on=False,shrinkA=0, shrinkB=0)
    # ax.add_patch(p2)

    if hline:
        ax.axhline(crit_value, linestyle="--",color="black")
        # ax.axhspan(0.85*crit_value, 1.15*crit_value, color="blue", alpha=0.1)

    # p3 = FancyArrowPatch((4.8, 0.85*crit_value), (4.8, 1.15*crit_value), arrowstyle='|-|', mutation_scale=5, clip_on=False,shrinkA=0, shrinkB=0, color='blue')
    # ax.add_patch(p3)

    # ax.text(4.8, crit_value, r'$\pm 15 \%$', color='blue', rotation=-90, clip_on=False, ha='left', va='center')

    x_label, y_label = global_functions.get_plot_labels_gamma_profiles(x_parameter, crit)

    y_label = r'$\max(\gamma/\omega_A)$'
    ax.set_xlabel(x_label, fontsize=20)
    ax.set_ylabel(y_label, fontsize=20)
    if crit != 'omega':
        ax.set_ylim(bottom=0)
    ax.set_xlim(left=0)

    if legend:
        ax.legend()

run(europed_names, x_parameter, crit, crit_value, envelope, list_consid_mode, hline, vline, legend)

# ax1 = axs[1]

min_value = 0
max_value = 2
cmap = plt.cm.inferno_r
new_cmap = cmap(np.linspace(0.2, 0.8, 256))
new_cmap = mcolors.ListedColormap(new_cmap)

norm = mpl.colors.Normalize(vmin=min_value, vmax=max_value)
cm = mpl.cm.ScalarMappable(norm=norm, cmap=new_cmap)
cm.set_array([])
cbar = fig.colorbar(cm, cax=ax1, orientation='vertical', extend='neither')
cbar.set_ticks([0,0.5,1,1.5,2],[0,0.5,1,1.5,2])
# axs[1].set_ylabel(r'$\eta/\eta_{\mathrm{Sp}}$')
ax1.text(0.5, 1.01, r'$\eta/\eta_{\mathrm{Sp}}$',transform=ax1.transAxes, ha='center', va='bottom', fontsize=20)   


ax.set_xlim(left=1.8, right=4.7)
ax.set_ylim(bottom=0, top=0.1)

plt.savefig('/home/jwp9427/cococo/3b')
plt.close()