#!/usr/local/depot/Python-3.7/bin/python
# /usr/local/depot/Python-3.5.1/bin/python

from hoho import useful_recurring_functions, global_functions, startup, for_contour, experimental_values, europed_analysis_2
from poster import plot_canvas
import argparse
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.tri as tri
import matplotlib as mpl
import matplotlib
from mpl_toolkits.axes_grid1 import Divider, Size

# matplotlib.rcParams['font.size'] = 14
# matplotlib.rcParams['font.family'] = 'sans-serif'
# matplotlib.rcParams['font.sans-serif'] = [:]

europed_names = [f'tan_eta{eta}_rs0.022_neped2.57_betap1.3' for eta in [0, 1]]

q_ped_def = 'tepos-delta'
ypar = 'alpha'
crit = 'alfven'
crit_value = 0.08
list_consid_modes = [[3],[10],[20],[30],[40],[50]]
list_eta =  [0, 1]

fig, ax = plt.subplots()

for list_consid_mode in list_consid_modes:
    y_crits = []
    for (eta,europed_name) in zip(list_eta, europed_names):
        y_crit = europed_analysis_2.critical_value_europed_name(europed_name, crit, crit_value, ypar, q_ped_def, list_consid_mode=list_consid_mode)
        y_crits.append(y_crit)
    ax.plot(list_eta, y_crits, label=list_consid_mode[0])

plt.legend()
plt.show()
plt.close()

