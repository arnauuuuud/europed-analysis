#!/usr/local/depot/Python-3.7/bin/python
# /usr/local/depot/Python-3.5.1/bin/python

import sys
import numpy as np
import matplotlib.pyplot as plt
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



def run(europed_names, y_parameter, crit, crit_values, list_consid_mode, shown, showlegend, whichxparameter, xlabel, is_frac):

    startup.reload(global_functions)
    startup.reload(useful_recurring_functions)
    startup.reload(find_pedestal_values_old)
    startup.reload(pedestal_values)
    startup.reload(europed_analysis)
    startup.reload(europed_analysis_2)



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

                            if mode == -1:
                                continue

                            if is_frac:
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
                        except KeyError as e:
                            print(e)
                            pass


        if whichxparameter == 2:
            x_list = np.array([float(e2) for e2 in euroname_2])
            y_lists = [array_4d_y[i1,:,i3,i4] for i1 in range(len(euroname_1)) for i3 in range(len(euroname_3)) for i4 in range(len(euroname_4))]
            n_lists = [array_4d_n[i1,:,i3,i4] for i1 in range(len(euroname_1)) for i3 in range(len(euroname_3)) for i4 in range(len(euroname_4))]

            temp_euroname1_forlabel = [''] if len(euroname_1) ==  1 else euroname_1
            temp_euroname3_forlabel = [''] if len(euroname_3) ==  1 else euroname_3
            temp_euroname4_forlabel = [''] if len(euroname_4) ==  1 else euroname_4

            labels = [l1 + l3 + l4 for l1 in temp_euroname1_forlabel for l3 in temp_euroname3_forlabel for l4 in temp_euroname4_forlabel]
    
        elif whichxparameter == 3:
            x_list = np.array([float(e3) for e3 in euroname_3])
            if is_frac:
                x_lists = [array_4d_frac[i1,i2,:,i4] for i1 in range(len(euroname_1)) for i2 in range(len(euroname_2)) for i4 in range(len(euroname_4))]
            y_lists = [array_4d_y[i1,i2,:,i4] for i1 in range(len(euroname_1)) for i2 in range(len(euroname_2)) for i4 in range(len(euroname_4))]
            n_lists = [array_4d_n[i1,i2,:,i4] for i1 in range(len(euroname_1)) for i2 in range(len(euroname_2)) for i4 in range(len(euroname_4))]

            temp_euroname1_forlabel = [''] if len(euroname_1) ==  1 else euroname_1
            temp_euroname2_forlabel = [''] if len(euroname_2) ==  1 else euroname_2
            temp_euroname4_forlabel = [''] if len(euroname_4) ==  1 else euroname_4

            labels = [l1 + l2 + l4 for l1 in temp_euroname1_forlabel for l2 in temp_euroname2_forlabel for l4 in temp_euroname4_forlabel]

        elif whichxparameter == 4:
            x_list = np.array([float(e4) for e4 in euroname_4])
            y_lists = [array_4d_y[i1,i2,i3,:] for i1 in range(len(euroname_1)) for i2 in range(len(euroname_2)) for i3 in range(len(euroname_3))]
            n_lists = [array_4d_n[i1,i2,i3,:] for i1 in range(len(euroname_1)) for i2 in range(len(euroname_2)) for i3 in range(len(euroname_3))]

            temp_euroname1_forlabel = [''] if len(euroname_1) ==  1 else euroname_1
            temp_euroname2_forlabel = [''] if len(euroname_2) ==  1 else euroname_2
            temp_euroname3_forlabel = [''] if len(euroname_3) ==  1 else euroname_3

            labels = [l1 + l2 + l3 for l1 in temp_euroname1_forlabel for l2 in temp_euroname2_forlabel for l3 in temp_euroname3_forlabel]

        
        for i,(y_list,n_list,label) in enumerate(zip(y_lists, n_lists,labels)):
            try:
                nan_indices = np.isnan(y_list)
                x_list_plot = x_list[~nan_indices]
                if is_frac:
                    x_list_plot = x_lists[i][~nan_indices]
                y_list = y_list[~nan_indices]
                n_list = n_list[~nan_indices]
                # y_list = y_list/y_list[0]
                plot_ax.plot(x_list_plot, y_list, marker='o', label=label)
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


fig, plot_ax = plt.subplots()

europed_names = ['tan_eta','0,0.3,0.5,0.8,1','_rs0.022_neped2.57_betap1.3', '']
y_parameter = 'alpha_helena_max'
crit = 'diamag'
crit_values = [0.03,0.05,0.07,0.09,0.11]
crit_values = [0.25,0.5,0.75]
list_consid_mode = [2,3,4,5,7,10,20]
shown = False
showlegend = False
whichxparameter = 2
xlabel = r'$\eta/\eta_{neo}$'
is_frac = False

# for list_consid_mode in [[3],[10],[20],[30],[40],[50]]:
run(europed_names, y_parameter, crit, crit_values, list_consid_mode, shown, showlegend, whichxparameter, xlabel, is_frac)

plt.show()
