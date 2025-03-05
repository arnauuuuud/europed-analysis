#!/usr/local/depot/Python-3.7/bin/python
# /usr/local/depot/Python-3.5.1/bin/python

import pandas as pd
import matplotlib.pyplot as plt
from hoho import pedestal_values, global_functions, experimental_values, europed_analysis_2
import numpy as np
from matplotlib import cm
from matplotlib.colors import Normalize


list_shot = [87342, 84794, 84791, 84792, 84793, 84795, 84796, 84797, 84798, 87335, 87336, 87337, 87338, 87339, 87340, 87341, 87342, 87344, 87346, 87348, 87349, 87350]
list_dda = [global_functions.dict_shot_dda[s] for s in list_shot]


fig, axs = plt.subplots(1,2)
ax1 = axs[0]
ax2 = axs[1]

lists = [[],[],[]]


crit = 'alfven'
crit_value = 0.09
list_consid_mode = None


for shot, dda in zip(list_shot, list_dda):
    alpha, a_err = experimental_values.get_alpha_max(shot, dda)
    betan, betan_err = experimental_values.get_betan(shot, dda)
    gasrate, g_err = experimental_values.get_gasrate(shot, dda)
    neped, neped_err = experimental_values.get_neped(shot, dda)
    nesepneped = experimental_values.get_nesepneped(shot, dda)[0]


    if gasrate <= 0.5e22:
        marker = 's'
        color = 'blue'
        i=0
    elif gasrate <= 1.5e22:
        marker = 'o'
        color = 'green'
        i=1
    else:
        marker = '^'
        color = 'magenta'
        i=2
    lists[i].append((betan,alpha,nesepneped))
    ax1.scatter(betan,alpha,c=color, marker=marker)
    ax2.scatter(betan,nesepneped,c=color, marker=marker)

    round_betan = round(float(betan), 2)
    round_neped = round(float(neped), 2)
    round_frac = round(nesepneped, 2)

    for (eta,marker) in zip([0,1],['*','D']):
        try:
            europed_name = f'global_v3_{shot}_eta{eta}_betan{round_betan}_neped{round_neped}_nesepneped{round_frac}'
            

            nesepneped = pedestal_values.nesep_neped(europed_name, crit=crit, crit_value=crit_value, list_consid_mode=list_consid_mode, q_ped_def='product')
            neped = pedestal_values.pedestal_value_all_definition('ne',europed_name, crit=crit, crit_value=crit_value, list_consid_mode=list_consid_mode, q_ped_def='product')
            neped2 = pedestal_values.pedestal_value_all_definition('ne',europed_name, crit=crit, crit_value=crit_value, list_consid_mode=list_consid_mode, q_ped_def='tepos-delta')

            print('\n\n\n')
            print(europed_name)
            print(nesepneped)
            print(neped)
            print(neped2)

            betan_list = europed_analysis_2.get_x_parameter(europed_name, 'betan')
            alpha_list = europed_analysis_2.get_x_parameter(europed_name, 'alpha_helena_max')
            deltas = europed_analysis_2.get_x_parameter(europed_name, 'delta')
            dict_gamma = europed_analysis_2.get_filtered_dict(europed_name, crit, list_consid_mode)

            has_unstable, betan, mode = europed_analysis_2.find_critical(betan_list, deltas, dict_gamma, crit_value)
            has_unstable, alpha, mode = europed_analysis_2.find_critical(alpha_list, deltas, dict_gamma, crit_value)

            
            ax1.scatter(betan,alpha,edgecolor=color, c='white', marker=marker)
            ax2.scatter(betan,nesepneped,edgecolor=color, c='white', marker=marker)
        except FileNotFoundError:
            pass


# colors_i = ['blue','green','magenta']
# for i in range(3):
#     ll = lists[i]
#     lbeta = np.array([l[0] for l in ll])
#     lalph = [l[1] for l in ll]
#     lfrac = [l[2] for l in ll]
#     model1 = LinearRegression()
#     model2 = LinearRegression()
#     lbeta = lbeta.reshape(-1, 1)
#     model1.fit(lbeta, lalph)
#     model2.fit(lbeta, lfrac)
#     lbeta_to_plot = np.linspace(min(lbeta),max(lbeta),2).reshape(-1,1)
#     lalph_to_plot = model1.predict(lbeta_to_plot)
#     lfrac_to_plot = model2.predict(lbeta_to_plot)

#     ax1.plot(lbeta_to_plot, lalph_to_plot, c=colors_i[i])
#     ax2.plot(lbeta_to_plot, lfrac_to_plot, c=colors_i[i])



ax1.set_xlabel(global_functions.betan_label)
ax1.set_ylabel(r'$\alpha_{\mathrm{max}}$')
ax1.set_ylim(bottom=0)
ax1.set_xlim(left=0)
ax2.set_xlabel(global_functions.betan_label)
ax2.set_ylabel(global_functions.nesepneped_label)
ax2.set_ylim(bottom=0)
ax2.set_xlim(left=0)
plt.show()



fig, axs = plt.subplots(1,2)
ax1 = axs[0]
ax2 = axs[1]


