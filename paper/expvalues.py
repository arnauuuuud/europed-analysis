#!/usr/local/depot/Python-3.7/bin/python
# /usr/local/depot/Python-3.5.1/bin/python

import pandas as pd
import matplotlib.pyplot as plt
from hoho import pedestal_values, global_functions, experimental_values
import numpy as np
from matplotlib import cm
from matplotlib.colors import Normalize
from sklearn.linear_model import LinearRegression




list_shot = [87342, 84794, 84791, 84792, 84793, 84795, 84796, 84797, 84798, 87335, 87336, 87337, 87338, 87339, 87340, 87341, 87342, 87344, 87346, 87348, 87349, 87350]
list_dda = [global_functions.dict_shot_dda[s] for s in list_shot]

markers_exp ={
    'blue': 'o',
    'green': 's',
    'magenta': '^'
}


folder_to_save = '/home/jwp9427/work/figures/2025-03-05_paper/'

def plot(xpar, ypar):
    fig, ax = plt.subplots()
    colors = []
    markers = []
    dict_shot = {
        'blue':[],
        'green':[],
        'magenta':[],
    }
    for shot, dda in zip(list_shot, list_dda):
        x_here, x_here_err = experimental_values.get_values(xpar, shot, dda)
        y_here, y_here_err = experimental_values.get_values(ypar, shot, dda)
        color = experimental_values.get_color(shot, dda)
        ax.errorbar([x_here],[y_here],xerr=[x_here_err],yerr=[y_here_err],c=color, marker=markers_exp[color], linewidth=0.5)
        dict_shot[color].append((x_here,y_here))

    for color in list(dict_shot.keys()):
        ll = dict_shot[color]
        lx = np.array([l[0] for l in ll])
        ly = [l[1] for l in ll]
        model1 = LinearRegression()
        lx = lx.reshape(-1, 1)
        model1.fit(lx, ly)
        lx_to_plot = np.linspace(min(lx),max(lx),2).reshape(-1,1)
        ly_to_plot = model1.predict(lx_to_plot)

        ax.plot(lx_to_plot, ly_to_plot, c=color, linewidth=2, linestyle='--')

    xlabel = global_functions.get_label(xpar)
    ylabel = global_functions.get_label(ypar)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_ylim(bottom=0)
    ax.set_xlim(left=0)
    plt.savefig(f'{folder_to_save}exp_values_{xpar}_{ypar}.png')
    plt.show()

# plot('betan','alpha')
plot('betan','peped_1delta')
plot('frac','alpha')
plot('frac','peped_fixedpos')
plot('neped','alpha')
plot('neped','peped_fixedpos')