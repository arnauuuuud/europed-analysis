#!/usr/local/depot/Python-3.7/bin/python
# /usr/local/depot/Python-3.5.1/bin/python

import pandas as pd
import matplotlib.pyplot as plt
from hoho import pedestal_values, global_functions, experimental_values, europed_analysis_2
import numpy as np
from matplotlib import cm
from matplotlib.colors import Normalize



europed_namess = [[f'tan_eta0_rs{rs}_neped2.57_betap{betap}' for betap in [0.55,0.7,0.85,1.0,1.15,1.3,1.45,1.6]] for rs in ['0.0',0.01,0.015,0.022,0.04]]

fig, axs = plt.subplots(1,2)
ax1 = axs[0]
ax2 = axs[1]

crit = 'alfven'
crit_value = 0.09
list_consid_mode = None
colors = ['blue', 'purple', 'red', 'orange', 'green']


for (europed_names, color) in zip(europed_namess, colors):
    for europed_name in europed_names:
        try:
            nesepneped = pedestal_values.nesep_neped(europed_name, crit=crit, crit_value=crit_value, list_consid_mode=list_consid_mode)


            betan_list = europed_analysis_2.get_x_parameter(europed_name, 'betan')
            alpha_list = europed_analysis_2.get_x_parameter(europed_name, 'alpha_helena_max')
            deltas = europed_analysis_2.get_x_parameter(europed_name, 'delta')
            dict_gamma = europed_analysis_2.get_filtered_dict(europed_name, crit, list_consid_mode)

            has_unstable, betan, mode = europed_analysis_2.find_critical(betan_list, deltas, dict_gamma, crit_value)
            has_unstable, alpha, mode = europed_analysis_2.find_critical(alpha_list, deltas, dict_gamma, crit_value)

            
            ax1.scatter(betan,alpha,c=color)
            ax2.scatter(betan,nesepneped,c=color)
        except TypeError:
            pass
        except AttributeError:
            pass

        except FileNotFoundError:
            pass


ax1.set_xlabel(global_functions.betan_label)
ax1.set_ylabel(r'$\alpha_{\mathrm{max}}$')
ax1.set_ylim(bottom=0)
ax1.set_xlim(left=0)
ax2.set_xlabel(global_functions.betan_label)
ax2.set_ylabel(global_functions.nesepneped_label)
ax2.set_ylim(bottom=0)
ax2.set_xlim(left=0)
plt.show()