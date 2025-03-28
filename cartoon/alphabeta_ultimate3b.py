#!/usr/local/depot/Python-3.7/bin/python
# /usr/local/depot/Python-3.5.1/bin/python

import pandas as pd
import matplotlib.pyplot as plt
from hoho import pedestal_values, global_functions, experimental_values, europed_analysis_2
import numpy as np
from matplotlib import cm
from matplotlib.colors import Normalize
from sklearn.linear_model import LinearRegression

list_shot = [84794, 84791, 84792, 84793, 84795, 84796, 84797, 84798, 87335, 87336, 87337, 87338, 87339, 87340, 87341, 87342, 87344, 87346, 87348, 87349, 87350]
list_dda = [global_functions.dict_shot_dda[s] for s in list_shot]

bad_shots = [84798, 87335, 87346]


# Create figure and axes objects
fig1, ax1 = plt.subplots()
fig2, ax2 = plt.subplots()
fig3, ax3 = plt.subplots()

lists = [[], [], []]

crit = 'alfven'
crit_value = 0.08
list_consid_mode = [1, 2, 3, 4, 5, 7, 10, 20, 30, 40, 50]


list_a0=[]
list_p0=[]
list_d0=[]
list_a1_n20=[]
list_p1_n20=[]
list_d1_n20=[]
list_a1_n50=[]
list_p1_n50=[]
list_d1_n50=[]

for shot, dda in zip(list_shot, list_dda):

    if shot in bad_shots:
        continue

    alpha_exp, a_err = experimental_values.get_alpha_max(shot, dda)
    betan, betan_err = experimental_values.get_betan(shot, dda)
    gasrate, g_err = experimental_values.get_gasrate(shot, dda)
    neped, neped_err = experimental_values.get_neped(shot, dda)
    peped_exp, peped_err = experimental_values.get_peped(shot, dda)
    nesepneped = experimental_values.get_nesepneped(shot, dda)[0]
    delta_exp, width_error = experimental_values.get_width_pe(shot, dda)

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

    round_betan = round(float(betan), 2)
    round_neped = round(float(neped), 2)
    round_frac = round(nesepneped, 2)

    for i,(eta, marker) in enumerate(zip([0, 1, 1], ['D', '^', 's'])):
        if i == 0:
            crit_value = 0.09
            list_consid_mode = [1,2,3,4,5,7,10,20,30,40,50]
        elif i == 1:
            crit_value = 0.09
            list_consid_mode = [1,2,3,4,5,7,10,20,30,40,50]
        elif i == 2:
            crit_value = 0.09
            list_consid_mode = [1,2,3,4,5,7,10,20]

        try:
            europed_name = f'global_v4_{shot}_eta{eta}_betan{round_betan}_neped{round_neped}_nesepneped{round_frac}'

            print('\n\n\n')
            print(europed_name)

            nesepneped = pedestal_values.nesep_neped(europed_name, crit=crit, crit_value=crit_value, list_consid_mode=list_consid_mode, q_ped_def='tepos-delta')
            neped = pedestal_values.pedestal_value_all_definition('ne', europed_name, crit=crit, crit_value=crit_value, list_consid_mode=list_consid_mode, q_ped_def='tepos-delta')
            peped = pedestal_values.pedestal_value_all_definition('pe', europed_name, crit=crit, crit_value=crit_value, list_consid_mode=list_consid_mode, q_ped_def='tepos-delta')

            print(nesepneped)
            print(neped)

            betan_list = europed_analysis_2.get_x_parameter(europed_name, 'betan')
            alpha_list = europed_analysis_2.get_x_parameter(europed_name, 'alpha_helena_max')
            deltas = europed_analysis_2.get_x_parameter(europed_name, 'delta')
            dict_gamma = europed_analysis_2.get_filtered_dict(europed_name, crit, list_consid_mode)

            has_unstable, betan, mode = europed_analysis_2.find_critical(betan_list, deltas, dict_gamma, crit_value)
            has_unstable, alpha, mode = europed_analysis_2.find_critical(alpha_list, deltas, dict_gamma, crit_value)
            has_unstable, delta, mode = europed_analysis_2.find_critical(deltas, deltas, dict_gamma, crit_value)

            if mode == -1:
                continue

            print(alpha)
            print(color)

            ax1.scatter(alpha_exp, (alpha-alpha_exp)/alpha_exp, c=color, marker=marker)
            ax2.scatter(peped_exp, (peped-peped_exp)/peped_exp, c=color, marker=marker)
            ax3.scatter(delta_exp, (delta-delta_exp)/delta_exp, c=color, marker=marker)

            # Use the axes objects to plot
            if i == 0:
                list_a0.append((alpha_exp, (alpha-alpha_exp)/alpha_exp))
                list_p0.append((peped_exp, (peped-peped_exp)/peped_exp))
                list_d0.append((delta_exp, (delta-delta_exp)/delta_exp))
            if i == 1:
                list_a1_n20.append((alpha_exp, (alpha-alpha_exp)/alpha_exp))
                list_p1_n20.append((peped_exp, (peped-peped_exp)/peped_exp))
                list_d1_n20.append((delta_exp, (delta-delta_exp)/delta_exp))
            if i == 2:
                list_a1_n50.append((alpha_exp, (alpha-alpha_exp)/alpha_exp))
                list_p1_n50.append((peped_exp, (peped-peped_exp)/peped_exp))
                list_d1_n50.append((delta_exp, (delta-delta_exp)/delta_exp))

        except FileNotFoundError:
            pass
        except TypeError:
            pass
        except KeyError:
            pass


def plot_linear_interp(lists, ax, linestyle):
    list_x = []
    list_y = []
    for a in lists:
        i,j = a
        list_x.append(i)
        list_y.append(j)
    model1 = LinearRegression()
    list_x = np.array(list_x)
    list_x = list_x.reshape(-1, 1)
    model1.fit(list_x, list_y)
    list_x_to_plot = np.linspace(min(list_x),max(list_x),2).reshape(-1,1)
    list_y_to_plot = model1.predict(list_x_to_plot)
    ax.plot(list_x_to_plot, list_y_to_plot, linestyle=linestyle, color='black')


plot_linear_interp(list_a0, ax1, '--')
plot_linear_interp(list_a1_n20, ax1, ':')
plot_linear_interp(list_a1_n50, ax1, 'dashdot')

plot_linear_interp(list_p0, ax2, '--')
plot_linear_interp(list_p1_n20, ax2, ':')
plot_linear_interp(list_p1_n50, ax2, 'dashdot')

plot_linear_interp(list_d0, ax3, '--')
plot_linear_interp(list_d1_n20, ax3, ':')
plot_linear_interp(list_d1_n50, ax3, 'dashdot')


# Set labels and limits using the axes objects
ax1.set_xlabel(r'$\alpha_{\mathrm{exp}}$')
ax1.set_ylabel(r'$(\alpha_{\mathrm{crit}}-\alpha_{\mathrm{exp}})/\alpha_{\mathrm{exp}}$')
ax2.set_xlabel(r'${p_e^{\mathrm{ped}}}_{\mathrm{exp}}$')
ax2.set_ylabel(r'$({p_e^{\mathrm{ped}}}_{\mathrm{crit}}-{p_e^{\mathrm{ped}}}_{\mathrm{exp}})/{p_e^{\mathrm{ped}}}_{\mathrm{exp}}$')
ax3.set_xlabel(r'$\Delta_{\mathrm{exp}}$')
ax3.set_ylabel(r'$(\Delta_{\mathrm{crit}}-\Delta_{\mathrm{exp}})/\Delta_{\mathrm{exp}}$')


ax1.set_title(r'$\alpha$, $\eta=0$')
ax2.set_title(r'$p_e^{\mathrm{ped}}$, $\eta=0$')
ax3.set_title(r'$\Delta$, $\eta=0$')

# Display the plots
plt.show()
