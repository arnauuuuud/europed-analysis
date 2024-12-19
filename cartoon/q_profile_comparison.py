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

fig, ax = plt.subplots()

psi,q,qerr = experimental_values.get_qprofile(84794, 'T052')
ax.plot(psi, q, color='k', label='Exp')

list_europed_name = ['fwo_30-50_eta1_rs0.022_neped2.65_betap1.35_w0.063_q0-1.1', 'fwo_30-50_eta1_rs0.022_neped2.65_betap1.35_w0.063_q0-1.2']

for europed_name in list_europed_name:
    psi = critical_helena_profile.get_profile_eliteinp('Psi',europed_name, device_name='jet', shot_number=84794, crit_value=0.1)
    psi = psi/psi[-1]
    q = critical_helena_profile.get_profile_eliteinp('q',europed_name, device_name='jet', shot_number=84794, crit_value=0.1)
    ax.plot(psi, q, label=europed_name)


plt.legend()
plt.show()
