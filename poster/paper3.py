#!/usr/local/depot/Python-3.7/bin/python
# /usr/local/depot/Python-3.5.1/bin/python

from hoho import useful_recurring_functions, europed_analysis, global_functions, startup, find_pedestal_values_old, h5_manipulation, spitzer
from poster import plot_canvas
from mpl_toolkits.axes_grid1 import Divider, Size
import sys
from mpl_toolkits.axes_grid1 import make_axes_locatable
import numpy as np
import matplotlib.pyplot as plt
import traceback
from PyQt5.QtWidgets import (
    QApplication, QWidget, QRadioButton, QVBoxLayout, QHBoxLayout,
    QLabel, QCheckBox, QLineEdit, QPushButton, QButtonGroup
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar
import matplotlib.transforms as transforms
import math
import numpy as np

markers = ['.', 'o', 'v', '^', '<', '>', '1', '2', '3', '4', 's', 'p', '*', 'h', 'H', '+', 'x', 'D', 'd']
colors = ['blue', 'green', 'red', 'cyan', 'magenta', 'yellow', 'orange', 'purple', 'brown', 'pink', 'gray', 'olive', 'lime', 'teal', 'navy', 'sky blue', 'lavender', 'peach', 'maroon', 'turquoise', 'gold', 'silver', 'indigo', 'violet', 'burgundy', 'mustard', 'ruby', 'emerald', 'sapphire', 'amethyst']

europed_names = ['sb_eta','0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0,1.5,2.0','_rs0.022_neped2.57','']
y_parameter = 'alpha_helena_max'
crit = 'alfven'
crit_value = 0.05
list_consid_mode = [1,2,3,4,5,7,10,20]
shown = False
whichxparameter = 2
xlabel = 'eta'
is_frac = False
plt.rcParams['ytick.right'] = False

cm = 1/2.54

fig = plt.figure(figsize=(16*cm,14*cm), dpi=300)


# # Define fixed size for the axes in inches
horiz = [Size.Fixed(2*cm),Size.Fixed(12*cm),Size.Fixed(2*cm)]
vert = [Size.Fixed(1.6*cm),Size.Fixed(11*cm)]

divider = Divider(fig, (0, 0, 1, 1), horiz, vert, aspect=True, anchor=(0,0))

ax1 = fig.add_axes(divider.get_position(), axes_locator=divider.new_locator(nx=1, ny=1))
# ax2 = fig.add_axes(divider.get_position(), axes_locator=divider.new_locator(nx=1, ny=1))

# ax_main = fig.add_subplot(111)

# # Add the primary axis with the divider's position and locator
# ax1 = fig.add_axes(divider.get_position(), axes_locator=divider.new_locator(nx=1, ny=1))

# Create the twin axis
ax2 = fig.add_axes(divider.get_position(), axes_locator=divider.new_locator(nx=1, ny=1), sharex=ax1, frameon=False)
ax2.yaxis.tick_right()
ax2.yaxis.set_label_position("right")

color = plt.cm.inferno_r(0.2)

def run(ax,europed_names, y_parameter, crit, crit_value, list_consid_mode, shown, whichxparameter, xlabel, is_frac):

    startup.reload(global_functions)
    startup.reload(useful_recurring_functions)
    startup.reload(find_pedestal_values_old)
    startup.reload(europed_analysis)

    # Clear the existing plot
    ax.clear()

    euroname_1 = europed_names[0].split(',')
    euroname_2 = europed_names[1].split(',')
    euroname_3 = europed_names[2].split(',')
    euroname_4 = europed_names[3].split(',')

    euroname_2 = [''] if euroname_2 == [] else euroname_2
    euroname_3 = [''] if euroname_3 == [] else euroname_3
    euroname_4 = [''] if euroname_4 == [] else euroname_4
    europed_names = [e1+e2+e3+e4 for e1 in euroname_1 for e2 in euroname_2 for e3 in euroname_3 for e4 in euroname_4]

    print()
    print('#######################')
    print(f'List of runs:     {europed_names}')
    print(f'Criterion:        {crit}')
    print(f'Critical value:   {crit_value}')
    print(f'Modes considered: {list_consid_mode}')
    print(f'Show n:           {shown}')
    print(f'Y axis:           {y_parameter}')
    print('#######################')
    print()



    array_4d_y = np.zeros((len(euroname_1), len(euroname_2), len(euroname_3), len(euroname_4)))
    array_4d_ymax = np.zeros((len(euroname_1), len(euroname_2), len(euroname_3), len(euroname_4)))
    array_4d_ymin = np.zeros((len(euroname_1), len(euroname_2), len(euroname_3), len(euroname_4)))
    array_4d_n = np.zeros((len(euroname_1), len(euroname_2), len(euroname_3), len(euroname_4)))
    array_4d_frac = np.zeros((len(euroname_1), len(euroname_2), len(euroname_3), len(euroname_4)))

    array_4d_y[:,:,:,:] = None
    array_4d_n[:,:,:,:] = None
    array_4d_frac[:,:,:,:] = None

    for i1,e1 in enumerate(euroname_1):
        for i2,e2 in enumerate(euroname_2):
            for i3,e3 in enumerate(euroname_3):
                for i4,e4 in enumerate(euroname_4):
                    europed_name = e1+e2+e3+e4
                    try:
                        print(europed_name)

                        x_param = europed_analysis.get_x_parameter(europed_name, y_parameter)
                        gammas, modes = europed_analysis.get_gammas(europed_name, crit)
                        print(modes)
                        print(list_consid_mode)

                        tab, considered_modes = europed_analysis.filter_tab_general(gammas, modes, list_consid_mode)

                        print(considered_modes)

                        has_unstable, y_crit, i_mode, mode = europed_analysis.find_critical(x_param, tab, considered_modes, crit_value)
                        has_unstable, y_critmax, i_mode, mode = europed_analysis.find_critical(x_param, tab, considered_modes, 1.15*crit_value)
                        has_unstable, y_critmin, i_mode, mode = europed_analysis.find_critical(x_param, tab, considered_modes, 0.85*crit_value)
                        if y_crit is  None:
                            raise useful_recurring_functions.CustomError(f"No critical value found")


                        if is_frac:
                            array_4d_frac[i1,i2,i3,i4] = find_pedestal_values_old.get_critical_frac(europed_name, crit, crit_value, list_consid_mode=list_consid_mode)

                        array_4d_y[i1,i2,i3,i4] = y_crit                 
                        array_4d_ymax[i1,i2,i3,i4] = y_critmax                 
                        array_4d_ymin[i1,i2,i3,i4] = y_critmin               
                        array_4d_n[i1,i2,i3,i4] = mode
                        print(mode)


                    except useful_recurring_functions.CustomError:
                        print(f"No critical value found")
                        pass
                    except FileNotFoundError:
                        print(f"File not found")
                        pass
                    except RuntimeError:
                        print(f"Runtime Error")
                        pass
                    except IndexError:
                        print(f"Index Error")
                        pass



    if whichxparameter == 2:
        x_list = np.array([float(e2) for e2 in euroname_2])
        y_lists = [array_4d_y[i1,:,i3,i4] for i1 in range(len(euroname_1)) for i3 in range(len(euroname_3)) for i4 in range(len(euroname_4))]
        y_lists_max = [array_4d_ymax[i1,:,i3,i4] for i1 in range(len(euroname_1)) for i3 in range(len(euroname_3)) for i4 in range(len(euroname_4))]
        y_lists_min = [array_4d_ymin[i1,:,i3,i4] for i1 in range(len(euroname_1)) for i3 in range(len(euroname_3)) for i4 in range(len(euroname_4))]
        n_lists = [array_4d_n[i1,:,i3,i4] for i1 in range(len(euroname_1)) for i3 in range(len(euroname_3)) for i4 in range(len(euroname_4))]

        temp_euroname1_forlabel = [''] if len(euroname_1) ==  1 else euroname_1
        temp_euroname3_forlabel = [''] if len(euroname_3) ==  1 else euroname_3
        temp_euroname4_forlabel = [''] if len(euroname_4) ==  1 else euroname_4

        labels = [l1 + l3 + l4 for l1 in temp_euroname1_forlabel for l3 in temp_euroname3_forlabel for l4 in temp_euroname4_forlabel]
   


    for y_list,n_list,label,y_list_max,y_list_min in zip(y_lists, n_lists,labels,y_lists_max,y_lists_min):
        try:
            nan_indices = np.isnan(y_list)
            x_list_plot = x_list[~nan_indices]
            y_list = y_list[~nan_indices]
            n_list = n_list[~nan_indices]
            y_list_min = y_list_min[~nan_indices]
            y_list_max = y_list_max[~nan_indices]
            # ax.plot(x_list_plot, y_list, marker='o', label=label)
            ax.plot(x_list_plot, y_list, marker='s', label=label, color=color, mec='black', mew=1, markersize=8)
            ax.fill_between(x_list_plot, y_list_min, y_list_max, alpha=0.2, color=color)
            # zax.plot(x_list_plot, y_list_max, marker='o', label=label)
            if shown:
                for x,y,n in zip(x_list_plot,y_list,n_list):
                    if n is None:
                        n = -1
                    if not np.isnan(x) and not np.isnan(y):
                        ax.annotate(int(n), (x, y), textcoords="offset points", fontsize=13, xytext=(0,5), ha='center') 
        except TypeError as e:
            print(e)


    
    y_label = global_functions.get_critical_plot_label(y_parameter)
    ax.set_ylabel(y_label,fontsize=20)

    xlabel = global_functions.eta_label
    ax.set_xlabel(xlabel,fontsize=20)


    ax.set_ylim(bottom=0)

    xlimleft = ax.get_xlim() [0]
    if xlimleft > 0:
        ax.set_xlim(left=0)

    
    # plt.legend()

def run2(ax,europed_names, y_parameter, crit, crit_value, list_consid_mode, shown, whichxparameter, xlabel, is_frac):

    startup.reload(global_functions)
    startup.reload(useful_recurring_functions)
    startup.reload(find_pedestal_values_old)
    startup.reload(europed_analysis)

    # Clear the existing plot
    ax.clear()

    euroname_1 = europed_names[0].split(',')
    euroname_2 = europed_names[1].split(',')
    euroname_3 = europed_names[2].split(',')
    euroname_4 = europed_names[3].split(',')

    euroname_2 = [''] if euroname_2 == [] else euroname_2
    euroname_3 = [''] if euroname_3 == [] else euroname_3
    euroname_4 = [''] if euroname_4 == [] else euroname_4
    europed_names = [e1+e2+e3+e4 for e1 in euroname_1 for e2 in euroname_2 for e3 in euroname_3 for e4 in euroname_4]

    print()
    print('#######################')
    print(f'List of runs:     {europed_names}')
    print(f'Criterion:        {crit}')
    print(f'Critical value:   {crit_value}')
    print(f'Modes considered: {list_consid_mode}')
    print(f'Show n:           {shown}')
    print(f'Y axis:           {y_parameter}')
    print('#######################')
    print()



    array_4d_y = np.zeros((len(euroname_1), len(euroname_2), len(euroname_3), len(euroname_4)))
    array_4d_ymax = np.zeros((len(euroname_1), len(euroname_2), len(euroname_3), len(euroname_4)))
    array_4d_ymin = np.zeros((len(euroname_1), len(euroname_2), len(euroname_3), len(euroname_4)))
    array_4d_n = np.zeros((len(euroname_1), len(euroname_2), len(euroname_3), len(euroname_4)))
    array_4d_frac = np.zeros((len(euroname_1), len(euroname_2), len(euroname_3), len(euroname_4)))

    array_4d_y[:,:,:,:] = None
    array_4d_n[:,:,:,:] = None
    array_4d_frac[:,:,:,:] = None

    for i1,e1 in enumerate(euroname_1):
        for i2,e2 in enumerate(euroname_2):
            for i3,e3 in enumerate(euroname_3):
                for i4,e4 in enumerate(euroname_4):
                    europed_name = e1+e2+e3+e4
                    try:
                        print(europed_name)

                        x_param = europed_analysis.get_x_parameter(europed_name, y_parameter)
                        x_param2 = europed_analysis.get_x_parameter(europed_name, y_parameter2)

                        x_param = np.array(x_param)
                        x_param2 = np.array(x_param2)
                        x_param = x_param*x_param2*1.6
                        gammas, modes = europed_analysis.get_gammas(europed_name, crit)
                        print(modes)
                        print(list_consid_mode)

                        tab, considered_modes = europed_analysis.filter_tab_general(gammas, modes, list_consid_mode)

                        print(considered_modes)

                        has_unstable, y_crit, i_mode, mode = europed_analysis.find_critical(x_param, tab, considered_modes, crit_value)
                        has_unstable, y_critmax, i_mode, mode = europed_analysis.find_critical(x_param, tab, considered_modes, 1.15*crit_value)
                        has_unstable, y_critmin, i_mode, mode = europed_analysis.find_critical(x_param, tab, considered_modes, 0.85*crit_value)
                        if y_crit is  None:
                            raise useful_recurring_functions.CustomError(f"No critical value found")


                        if is_frac:
                            array_4d_frac[i1,i2,i3,i4] = find_pedestal_values_old.get_critical_frac(europed_name, crit, crit_value, list_consid_mode=list_consid_mode)

                        array_4d_y[i1,i2,i3,i4] = y_crit                 
                        array_4d_ymax[i1,i2,i3,i4] = y_critmax                 
                        array_4d_ymin[i1,i2,i3,i4] = y_critmin               
                        array_4d_n[i1,i2,i3,i4] = mode
                        print(mode)


                    except useful_recurring_functions.CustomError:
                        print(f"No critical value found")
                        pass
                    except FileNotFoundError:
                        print(f"File not found")
                        pass
                    except RuntimeError:
                        print(f"Runtime Error")
                        pass
                    except IndexError:
                        print(f"Index Error")
                        pass



    if whichxparameter == 2:
        x_list = np.array([float(e2) for e2 in euroname_2])
        y_lists = [array_4d_y[i1,:,i3,i4] for i1 in range(len(euroname_1)) for i3 in range(len(euroname_3)) for i4 in range(len(euroname_4))]
        y_lists_max = [array_4d_ymax[i1,:,i3,i4] for i1 in range(len(euroname_1)) for i3 in range(len(euroname_3)) for i4 in range(len(euroname_4))]
        y_lists_min = [array_4d_ymin[i1,:,i3,i4] for i1 in range(len(euroname_1)) for i3 in range(len(euroname_3)) for i4 in range(len(euroname_4))]
        n_lists = [array_4d_n[i1,:,i3,i4] for i1 in range(len(euroname_1)) for i3 in range(len(euroname_3)) for i4 in range(len(euroname_4))]

        temp_euroname1_forlabel = [''] if len(euroname_1) ==  1 else euroname_1
        temp_euroname3_forlabel = [''] if len(euroname_3) ==  1 else euroname_3
        temp_euroname4_forlabel = [''] if len(euroname_4) ==  1 else euroname_4

        labels = [l1 + l3 + l4 for l1 in temp_euroname1_forlabel for l3 in temp_euroname3_forlabel for l4 in temp_euroname4_forlabel]
   


    for y_list,n_list,label,y_list_max,y_list_min in zip(y_lists, n_lists,labels,y_lists_max,y_lists_min):
        try:
            nan_indices = np.isnan(y_list)
            x_list_plot = x_list[~nan_indices]
            y_list = y_list[~nan_indices]
            n_list = n_list[~nan_indices]
            y_list_min = y_list_min[~nan_indices]
            y_list_max = y_list_max[~nan_indices]
            ax.plot(x_list_plot, y_list, marker='p', label=label, color='red', mec='black', mew=1, markersize=10)
            ax.fill_between(x_list_plot, y_list_min, y_list_max, alpha=0.2, color='red')
            # zax.plot(x_list_plot, y_list_max, marker='o', label=label)
            if shown:
                for x,y,n in zip(x_list_plot,y_list,n_list):
                    if n is None:
                        n = -1
                    if not np.isnan(x) and not np.isnan(y):
                        ax.annotate(int(n), (x, y), textcoords="offset points", fontsize=13, xytext=(0,5), ha='center') 
        except TypeError as e:
            print(e)


    
    y_label = global_functions.get_critical_plot_label('peped')
    ax.set_ylabel(y_label,fontsize=20)

    xlabel = global_functions.eta_label
    # ax.set_xlabel(xlabel,fontsize=20)

    # ax.xaxis.tick_params(right=False)


    ax.set_ylim(bottom=0)

    xlimleft = ax.get_xlim() [0]
    if xlimleft > 0:
        ax.set_xlim(left=0)

    
    # plt.legend()




run(ax1,europed_names, y_parameter, crit, crit_value, list_consid_mode, shown, whichxparameter, xlabel, is_frac)
# ax2 = ax.twinx()
ax2.tick_params(left=False, labelleft=False, right=True,labelright=True, labelbottom=False, bottom=False,top=False,labeltop=False)
ax1.tick_params(left=True, labelleft=True, right=False,labelright=False)
y_parameter = 'neped'
y_parameter2 = 'teped'
run2(ax2,europed_names, y_parameter, crit, crit_value, list_consid_mode, shown, whichxparameter, xlabel, is_frac)


ax1.axvspan(1.136,2.143,alpha=0.2,color='forestgreen')
mean = (1.136+2.143)/2
ax1.text(mean,1,r'$\eta_{\mathrm{neo}}$',ha='center',va='center',fontsize=40, color='forestgreen')

plt.savefig('/home/jwp9427/cococo/paper3')
plt.close()

