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
import matplotlib as mpl
import matplotlib.colors as mcolors
from matplotlib.colors import ListedColormap

cmap = 'inferno_r'
markers = [ 'D', 's', 'p', '*', 'h', 'H', '+', 'x', 'd', 'o', 'v', '^', '<', '>', '1', '2', '3', '4']
colors = ['blue', 'green', 'red', 'cyan', 'magenta', 'yellow', 'orange', 'purple', 'brown', 'pink', 'gray', 'olive', 'lime', 'teal', 'navy', 'sky blue', 'lavender', 'peach', 'maroon', 'turquoise', 'gold', 'silver', 'indigo', 'violet', 'burgundy', 'mustard', 'ruby', 'emerald', 'sapphire', 'amethyst']


europed_names = [f'sb_eta{eta}_rs0.022_neped2.57' for eta in [0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0,1.5,2.0]]
etas = [0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0,1.5,2.0]
x_parameter = 'alpha_helena_max'
crit = 'alfven'
crit_value = 0.05
envelope = True
list_consid_mode = [20]
hline = False
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
ax2 = fig.add_axes(divider.get_position(), axes_locator=divider.new_locator(nx=3, ny=1))

def draw_gradient_arrow(ax, start, end, cmap=cmap, n_points=100):
    
    x = np.linspace(start[0], end[0], n_points)
    y = np.linspace(start[1], end[1], n_points)
    colors = plt.get_cmap(cmap)(np.linspace(0.3, 1, n_points))
    # arrow = FancyArrowPatch(start, end, color=colors[-1], zorder=-1,linewidth=1)
    # ax.add_patch(arrow)
    for i in range(n_points - 1):
        ax.plot([x[i], x[i + 1]], [y[i], y[i + 1]], color=colors[i])

    ax.plot([end[0],end[0]-0.1],[end[1],end[1]-0.005], color='k')
    ax.plot([end[0],end[0]+0.1],[end[1],end[1]-0.005], color='k')

    
def get_color_eta(eta, cmap=cmap):

    normalized_eta = eta*0.6/2 + 0.2
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
                ax.plot(x_envelope, y_envelope, color=get_color_eta(eta), label=europed_run)


            if vline:
                has_unstable, x_crit, col, critn = europed_analysis.find_critical(x_param, tab, list_mode_to_plot, crit_value)
                if has_unstable:
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
                    ax.text(x_crit, 1.0, str(x_crit_round), color=colorvline, horizontalalignment='center', verticalalignment='bottom',transform=trans)
        except RuntimeError:
            print(f"{europed_run:>40} RUNTIME ERROR : NO FIT FOUND")
        except FileNotFoundError:
            print(f"{europed_run:>40} FILE DOES NOT EXIST")
        except IndexError as e:
            print(e)
            continue


    if hline:
        ax.axhline(crit_value, linestyle="--",color="k")

    x_label, y_label = global_functions.get_plot_labels_gamma_profiles(x_parameter, crit)
    ax.set_xlabel(x_label)#,fontsize=20)
    ax.set_ylabel(y_label)#,fontsize=20)
    if crit != 'omega':
        ax.set_ylim(bottom=0)
    ax.set_xlim(left=2)

    if legend:
        ax.legend()

run(europed_names, x_parameter, crit, crit_value, envelope, list_consid_mode, hline, vline, legend)

ax.set_xlim(left=2, right=4.7)
ax.set_ylim(bottom=0, top=0.1)
ax.text(0.05,0.95,r'$n=20$',transform=ax.transAxes, fontsize=25, ha='left', va='top')
# ax.text(2.9,0.05,r'Increasing $\eta$',transform=ax.transData, fontsize=20, ha='right', va='center', rotation=90)

min_value = 0
max_value = 2
cmap = 'inferno_r'
cmap = plt.cm.inferno_r
new_cmap = cmap(np.linspace(0.2, 0.8, 256))
new_cmap = mcolors.ListedColormap(new_cmap)

norm = mpl.colors.Normalize(vmin=min_value, vmax=max_value)
cm = mpl.cm.ScalarMappable(norm=norm, cmap=new_cmap)
cm.set_array([])
cbar = fig.colorbar(cm, cax=ax2, orientation='vertical', extend='neither')
ax2.text(0.5, 1.01, r'$\eta/\eta_{\mathrm{Sp}}$',transform=ax2.transAxes, ha='center', va='bottom', fontsize=20)   
cbar.set_ticks([0,0.5,1,1.5,2],[0,0.5,1,1.5,2])

start = [3.1,0.02]
end = [3.1,0.08]
# arrow = FancyArrowPatch(start, end, mutation_scale=15, color=plt.get_cmap('inferno_r')(1.0), zorder=10)
# ax.add_patch(arrow)
# draw_gradient_arrow(ax, start, end)


plt.savefig('/home/jwp9427/cococo/2a')
plt.close()