#!/usr/local/depot/Python-3.7/bin/python
# /usr/local/depot/Python-3.5.1/bin/python

from hoho import useful_recurring_functions, global_functions, startup, for_contour, experimental_values, add_contours_to_plot, critical_helena_profile 
from poster import plot_canvas
import argparse
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import Normalize
import numpy as np
import matplotlib.tri as tri
import matplotlib as mpl
import matplotlib
from mpl_toolkits.axes_grid1 import Divider, Size
import traceback

fig, ax = plt.subplots()

psi_exp,q_exp,qerr = experimental_values.get_qprofile(84794, 'T052')
# list_europed_name = ['fwo_30-50_eta1_rs0.022_neped2.65_betap1.35_w0.063_q0-1.1_alpha_b','fwo_30-50_eta1_rs0.022_neped2.65_betap1.35_w0.063_q0-1.1_alpha_c','fwo_30-50_eta1_rs0.022_neped2.65_betap1.35_w0.063_q0-1.1_alpha_e']
ax.plot(psi_exp, q_exp, label='HPLG')

psi_exp,q_exp,qerr = experimental_values.get_qprofile(87342, 'T037')
# list_europed_name = ['fwo_30-50_eta1_rs0.04_neped2.85_betap0.95_w0.07_helsave','fwo_30-50_eta1_rs0.04_neped2.85_betap0.95_w0.07_q0-1.4','fwo_30-50_eta1_rs0.04_neped2.85_betap0.95_w0.07_q0-1.6', 'fwo_30-50_eta1_rs0.04_neped2.85_betap0.95_w0.07_q0-1.2']
list_europed_name = []


ax.plot(psi_exp, q_exp, label='HPHG')
for europed_name in list_europed_name:
    try:
        psi = critical_helena_profile.get_profile_eliteinp('Psi',europed_name, device_name='jet', shot_number=84794, crit_value=0.1)
        psi = psi/psi[-1]
        q = critical_helena_profile.get_profile_eliteinp('q',europed_name, device_name='jet', shot_number=84794, crit_value=0.1)
        ax.plot(psi, q, label=europed_name)
    except Exception as e:
        print(e)
        traceback.print_exc()


plt.legend()
plt.show()
