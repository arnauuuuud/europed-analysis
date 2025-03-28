#!/usr/local/depot/Python-3.7/bin/python
# /usr/local/depot/Python-3.5.1/bin/python

import pandas as pd
import matplotlib.pyplot as plt
from hoho import pedestal_values, global_functions, experimental_values, europed_analysis_2
import numpy as np
from matplotlib import cm
from matplotlib.colors import Normalize

list_shot = [84794, 84791, 84792, 84793, 84795, 84796, 84797, 84798, 87335, 87336, 87337, 87338, 87339, 87340, 87341, 87342, 87344, 87346, 87348, 87349, 87350]
list_dda = [global_functions.dict_shot_dda[s] for s in list_shot]

# list_shot = list_shot[::3]
# list_dda = list_dda[::3]

# Create figure and axes objects
fig1, ax1 = plt.subplots()
fig2, ax2 = plt.subplots()
fig3, ax3 = plt.subplots()
fig4, ax4 = plt.subplots()

lists = [[], [], []]

bad_shots = [84798, 87335, 87346]

crit = 'alfven'
crit_value = 0.03
list_consid_mode = [1, 2, 3, 4, 5, 7, 10, 20, 30, 40, 50]

for shot, dda in zip(list_shot, list_dda):
    if shot in bad_shots:
        continue
    alpha, a_err = experimental_values.get_alpha_max(shot, dda)
    betan, betan_err = experimental_values.get_betan(shot, dda)
    gasrate, g_err = experimental_values.get_gasrate(shot, dda)
    neped, neped_err = experimental_values.get_neped(shot, dda)
    peped, peped_err = experimental_values.get_peped(shot, dda)
    nesepneped = experimental_values.get_nesepneped(shot, dda)[0]

    if gasrate <= 0.5e22:
        marker = 's'
        color = 'blue'
        i = 0
    elif gasrate <= 1.5e22:
        marker = 's'
        color = 'green'
        i = 1
    else:
        marker = 's'
        color = 'magenta'
        i = 2
    lists[i].append((betan, alpha, nesepneped))

    # Use the axes objects to plot
    ax1.scatter(betan, alpha, c=color, edgecolor='k', marker=marker)
    ax2.scatter(betan, nesepneped, c=color, edgecolor='k', marker=marker)
    ax3.scatter(betan, neped, c=color, edgecolor='k', marker=marker)
    ax4.scatter(betan, peped, c=color, edgecolor='k', marker=marker)

    round_betan = round(float(betan), 2)
    round_neped = round(float(neped), 2)
    round_frac = round(nesepneped, 2)

    for (eta, marker) in zip([0, 1], ['D', '^']):
        try:
            europed_name = f'global_v4_{shot}_eta{eta}_betan{round_betan}_neped{round_neped}_nesepneped{round_frac}'

            print('\n\n\n')
            print(europed_name)

            nesepneped = pedestal_values.nesep_neped(europed_name, crit=crit, crit_value=crit_value, list_consid_mode=list_consid_mode, q_ped_def='positionTeped')
            neped = pedestal_values.pedestal_value_all_definition('ne', europed_name, crit=crit, crit_value=crit_value, list_consid_mode=list_consid_mode, q_ped_def='positionTeped')
            peped = pedestal_values.pedestal_value_all_definition('pe', europed_name, crit=crit, crit_value=crit_value, list_consid_mode=list_consid_mode, q_ped_def='positionTeped')
            neped2 = pedestal_values.pedestal_value_all_definition('ne', europed_name, crit=crit, crit_value=crit_value, list_consid_mode=list_consid_mode, q_ped_def='tepos-delta')

            print(nesepneped)
            print(neped)
            print(neped2)

            betan_list = europed_analysis_2.get_x_parameter(europed_name, 'betan')
            alpha_list = europed_analysis_2.get_x_parameter(europed_name, 'alpha_helena_max')
            deltas = europed_analysis_2.get_x_parameter(europed_name, 'delta')
            dict_gamma = europed_analysis_2.get_filtered_dict(europed_name, crit, list_consid_mode)

            has_unstable, betan, mode = europed_analysis_2.find_critical(betan_list, deltas, dict_gamma, crit_value)
            has_unstable, alpha, mode = europed_analysis_2.find_critical(alpha_list, deltas, dict_gamma, crit_value)


            if mode == -1:
                continue

            # Use the axes objects to plot
            ax1.scatter(betan, alpha, c=color, marker=marker)
            ax2.scatter(betan, nesepneped, c=color, marker=marker)
            ax3.scatter(betan, neped, c=color, marker=marker)
            ax4.scatter(betan, peped, c=color, marker=marker)
        except FileNotFoundError:
            pass

# Set labels and limits using the axes objects
ax1.set_xlabel(global_functions.betan_label)
ax1.set_ylabel(r'$\alpha_{\mathrm{max}}$')
ax1.set_ylim(bottom=0)
ax1.set_xlim(left=0)

ax2.set_xlabel(global_functions.betan_label)
ax2.set_ylabel(global_functions.nesepneped_label)
ax2.set_ylim(bottom=0)
ax2.set_xlim(left=0)

ax3.set_xlabel(global_functions.betan_label)
ax3.set_ylabel(global_functions.neped_label)
ax3.set_ylim(bottom=0)
ax3.set_xlim(left=0)

ax4.set_xlabel(global_functions.betan_label)
ax4.set_ylabel(global_functions.peped_label)
ax4.set_ylim(bottom=0)
ax4.set_xlim(left=0)

# Display the plots
plt.show()
