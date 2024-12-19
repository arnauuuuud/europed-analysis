#!/usr/local/depot/Python-3.7/bin/python
# /usr/local/depot/Python-3.5.1/bin/python

from hoho import useful_recurring_functions, europed_analysis_2, global_functions, startup, pedestal_values
import argparse
import matplotlib.pyplot as plt
import numpy as np


def plot(ax, definition, color):
    # neped = [pedestal_values.pedestal_value_all_definition('ne', europed_name, crit='alfven', crit_value=0.05, q_ped_def=definition) for europed_name in europed_names]
    # neped = [europed_analysis_2.critical_value_europed_name(europed_name, 'alfven', 0.05, 'neped', definition) for europed_name in europed_names]
    # teped = [europed_analysis_2.critical_value_europed_name(europed_name, 'alfven', 0.05, 'teped', definition) for europed_name in europed_names]
    peped = [europed_analysis_2.critical_value_europed_name(europed_name, 'alfven', 0.05, 'peped', definition) for europed_name in europed_names]
    # teped = [pedestal_values.pedestal_value_all_definition('te', europed_name, crit='alfven', crit_value=0.05, q_ped_def=definition) for europed_name in europed_names]
    # print(neped)
    # print(teped)
    ax.scatter(range(len(peped)), peped, color = color, label=definition)




fix,axs = plt.subplots(2,2)

ax1 = axs[0][0]
ax2 = axs[0][1]
ax3 = axs[1][0]
ax4 = axs[1][1]

europed_names = [f'tan_eta0_rs{rs}_neped2.57_betap1.3' for rs in [0.0,0.01,0.02,0.022,0.03,0.04]]
plot(ax1,'positionTeped', 'cyan')
plot(ax1,'tepos-delta', 'red')
plot(ax1,'product', 'blue')
plot(ax1,'fixedposition', 'green')

europed_names = [f'tan_eta0_rs0.022_neped{neped}_betap1.3' for neped in [1.57,2.07,2.57,3.07,3.57,4.07]]
plot(ax2,'positionTeped', 'cyan')
plot(ax2,'tepos-delta', 'red')
plot(ax2,'product', 'blue')
plot(ax2,'fixedposition', 'green')

europed_names = [f'tan_eta0_rs0.022_neped2.57_betap{betap}' for betap in [0.55,0.7,0.85,1.0,1.15,1.3]]
plot(ax3,'positionTeped', 'cyan')
plot(ax3,'tepos-delta', 'red')
plot(ax3,'product', 'blue')
plot(ax3,'fixedposition', 'green')


ax1.set_xlim(left=0)
ax1.set_ylim(bottom=0)
ax2.set_xlim(left=0)
ax2.set_ylim(bottom=0)
ax3.set_xlim(left=0)
ax3.set_ylim(bottom=0)

plt.show()