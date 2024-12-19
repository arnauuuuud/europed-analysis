#!/usr/local/depot/Python-3.7/bin/python
# /usr/local/depot/Python-3.5.1/bin/python

import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import Normalize
import traceback
from PyQt5.QtWidgets import (
    QApplication, QWidget, QRadioButton, QVBoxLayout, QHBoxLayout,
    QLabel, QCheckBox, QLineEdit, QPushButton, QButtonGroup,QScrollArea 
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar
from hoho import useful_recurring_functions, europed_analysis, global_functions, startup, find_pedestal_values_old, pedestal_values, europed_analysis_2
import matplotlib.pyplot as plt
import matplotlib.transforms as transforms
import math
import numpy as np

markers = ['.', 'o', 'v', '^', '<', '>', '1', '2', '3', '4', 's', 'p', '*', 'h', 'H', '+', 'x', 'D', 'd']
colors = ['blue', 'green', 'red', 'cyan', 'magenta', 'gold', 'orange', 'purple', 'brown', 'pink', 'gray', 'olive', 'lime', 'teal', 'navy', 'sky blue', 'lavender', 'peach', 'maroon', 'turquoise', 'gold', 'silver', 'indigo', 'violet', 'burgundy', 'mustard', 'ruby', 'emerald', 'sapphire', 'amethyst']



# def run(europed_names, y_parameter, crit, crit_values, list_consid_mode, shown, showlegend, whichxparameter, xlabel, is_frac):

europed_names = ['tan_eta1_rs','0.0,0.01,0.015,0.022,0.04','_neped2.57_betap','0.55,0.7,0.85,1.0,1.15,1.3,1.45,1.6']
# europed_names = ['tan_eta1_rs','0.0','_neped2.57_betap','0.55,0.7']
y_parameter = 'alpha_helena_max'
crit = 'alfven'
crit_values = ['0.1']
list_consid_mode = [1,2,3,4,5,7,10,20,30,40,50]
shown = False
showlegend = False
whichxparameter = 4
xlabel = r'$\beta_p$'
is_frac = False

# Clear the existing plot
fig,plot_ax = plt.subplots()

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
print(f'Critical value:   {crit_values}')
print(f'Modes considered: {list_consid_mode}')
print(f'Show n:           {shown}')
print(f'Y axis:           {y_parameter}')
print('#######################')
print()



array_4d_y = np.zeros((len(euroname_1), len(euroname_2), len(euroname_3), len(euroname_4)))
array_4d_n = np.zeros((len(euroname_1), len(euroname_2), len(euroname_3), len(euroname_4)))
array_4d_frac = np.zeros((len(euroname_1), len(euroname_2), len(euroname_3), len(euroname_4)))

array_4d_y[:,:,:,:] = None
array_4d_n[:,:,:,:] = None
array_4d_frac[:,:,:,:] = None

counter = 0
for crit_value in crit_values:
    crit_value = float(crit_value)
    for i1,e1 in enumerate(euroname_1):
        for i2,e2 in enumerate(euroname_2):
            for i3,e3 in enumerate(euroname_3):
                for i4,e4 in enumerate(euroname_4):
                    europed_name = e1+e2+e3+e4

                    try:

                        x_param = europed_analysis_2.get_x_parameter(europed_name, y_parameter)
                        deltas = europed_analysis_2.get_x_parameter(europed_name, 'delta')
                        dict_gamma = europed_analysis_2.get_filtered_dict(europed_name, crit, list_consid_mode)

                        has_unstable, y_crit, mode = europed_analysis_2.find_critical(x_param, deltas, dict_gamma, crit_value)
                        if y_crit is  None:
                            raise useful_recurring_functions.CustomError(f"No critical value found")


                        array_4d_frac[i1,i2,i3,i4] = pedestal_values.nesep_neped(europed_name, crit=crit, crit_value=crit_value, list_consid_mode=list_consid_mode)
                        array_4d_y[i1,i2,i3,i4] = y_crit                 
                        array_4d_n[i1,i2,i3,i4] = mode


                    except useful_recurring_functions.CustomError as e:
                        print(e)
                        pass
                    except FileNotFoundError as e:
                        print(e)
                        pass
                    except IndexError as e:
                        print(e)
                        pass




    norm = Normalize(vmin=0, vmax=1)  # Normalize the data between -100 and 100
    cmap = cm.inferno_r  # Use the 'viridis' colormap
    # Create a scatter plot with colors mapped to 'z'
    colors = cmap(norm(array_4d_frac))

    x_list = np.array([float(e4) for e4 in euroname_4])
    y_lists = [array_4d_y[i1,i2,i3,:] for i1 in range(len(euroname_1)) for i2 in range(len(euroname_2)) for i3 in range(len(euroname_3))]
    n_lists = [array_4d_n[i1,i2,i3,:] for i1 in range(len(euroname_1)) for i2 in range(len(euroname_2)) for i3 in range(len(euroname_3))]
    color_lists = [colors[i1,i2,i3,:] for i1 in range(len(euroname_1)) for i2 in range(len(euroname_2)) for i3 in range(len(euroname_3))]

    temp_euroname1_forlabel = [''] if len(euroname_1) ==  1 else euroname_1
    temp_euroname2_forlabel = [''] if len(euroname_2) ==  1 else euroname_2
    temp_euroname3_forlabel = [''] if len(euroname_3) ==  1 else euroname_3

    labels = [l1 + l2 + l3 for l1 in temp_euroname1_forlabel for l2 in temp_euroname2_forlabel for l3 in temp_euroname3_forlabel]

    
    for i,(y_list,n_list,label,color) in enumerate(zip(y_lists, n_lists,labels,color_lists)):
        try:
            nan_indices = np.isnan(y_list)
            x_list_plot = x_list[~nan_indices]
            if is_frac:
                x_list_plot = x_lists[i][~nan_indices]
            y_list = y_list[~nan_indices]
            n_list = n_list[~nan_indices]
            color = color[~nan_indices]
            plot_ax.scatter(x_list_plot, y_list, marker='o', label=label, c=color, edgecolors='black')
            if len(x_list_plot)>1:
                counter += 1
            if shown:
                for x,y,n in zip(x_list_plot,y_list,n_list):
                    if n is None:
                        n = -1
                    if not np.isnan(x) and not np.isnan(y):
                        plot_ax.annotate(int(n), (x, y), textcoords="offset points", fontsize=13, xytext=(0,5), ha='center') 
        except TypeError as e:
            print(e)



y_label = global_functions.get_critical_plot_label(y_parameter)
plot_ax.set_ylabel(y_label)

if xlabel is not None:
    plot_ax.set_xlabel(xlabel)


plot_ax.set_ylim(bottom=0)

xlimleft = plot_ax.get_xlim() [0]
if xlimleft > 0:
    plot_ax.set_xlim(left=0)

if showlegend:
    plt.legend()

sm = cm.ScalarMappable(norm=norm, cmap=cmap)
sm.set_array([])

plt.colorbar(sm, ax=plot_ax, label=global_functions.nesepneped_label)

plt.plot()
plt.show()



