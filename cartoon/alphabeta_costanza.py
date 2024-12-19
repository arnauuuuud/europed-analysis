#!/usr/local/depot/Python-3.7/bin/python
# /usr/local/depot/Python-3.5.1/bin/python

import pandas as pd
import matplotlib.pyplot as plt
from hoho import pedestal_values, global_functions, experimental_values
import numpy as np
from matplotlib import cm
from matplotlib.colors import Normalize




list_shot = [87342, 84794, 84791, 84792, 84793, 84795, 84796, 84797, 84798, 87335, 87336, 87337, 87338, 87339, 87340, 87341, 87342, 87344, 87346, 87348, 87349, 87350]
list_dda = [global_functions.dict_shot_dda[s] for s in list_shot]

x = []
y = []
colors = []

fig, ax = plt.subplots()


norm = Normalize(vmin=0, vmax=1)  # Normalize the data between -100 and 100
cmap = cm.inferno_r  # Use the 'viridis' colormap
# Create a scatter plot with colors mapped to 'z'
colors = []
markers = []

for shot, dda in zip(list_shot, list_dda):
    alpha, a_err = experimental_values.get_alpha(shot, dda)
    power, p_err = experimental_values.get_power(shot, dda)
    gasrate, g_err = experimental_values.get_gasrate(shot, dda)

    y.append(alpha)
    x.append(power)
    nesepneped = experimental_values.get_nesepneped(shot, dda)
    color = cmap(norm(nesepneped[0]))
    colors.append(color)

    if gasrate <= 0.5e22:
        marker = 's'
        color = 'blue'
    elif gasrate <= 1.5e22:
        marker = 'o'
        color = 'green'
    else:
        marker = '^'
        color = 'magenta'
    # colors.append(color)
    markers.append(marker)
    power = power*1e-6
    ax.scatter(power,alpha,c=color, marker=marker)


ax.set_xlabel(r'$P_{\mathrm{[MW]}}$')
ax.set_ylabel(r'$\alpha_{\mathrm{max}}$')
ax.set_ylim(bottom=0)
ax.set_xlim(left=0)
plt.show()