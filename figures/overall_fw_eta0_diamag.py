#!/usr/local/depot/Python-3.7/bin/python
# /usr/local/depot/Python-3.5.1/bin/python

from hoho import useful_recurring_functions, europed_analysis_2, global_functions, startup, pedestal_values, h5_manipulation, spitzer, experimental_values,for_fixedwidth
from poster import plot_canvas
import argparse
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.tri as tri
import matplotlib as mpl
from ppf import ppfget,ppfuid
import matplotlib
from scipy.interpolate import interp1d
from mpl_toolkits.axes_grid1 import Divider, Size

matplotlib.rcParams['font.size'] = 14
matplotlib.rcParams['font.family'] = 'sans-serif'
# matplotlib.rcParams['font.sans-serif'] = [:]

cm = 1/2.54

crit_value = 0.25
marker_ideal = 'o'
marker_resistive = 's'
q_ped_def = 'tepos-delta'
crit = 'diamag'
exclude_modes = [1]

def plot(ax, europed_name, color, crit_value, marker = 'o', open_markers=False, xy='alphapeped'):
    print(europed_name)
    crit_x, crit_y = for_fixedwidth.give_critx_crity(europed_name, crit, crit_value, xy, q_ped_def, exclude_modes=exclude_modes)
    if not open_markers:
        ax.scatter(crit_x, crit_y, marker=marker, color=color, edgecolor='k', s=50)
    else:
        ax.scatter(crit_x, crit_y, marker=marker, color='white', edgecolor=color, s=50)


def main(xy, ax):
    for europed_name in ['fwi_eta0_rs0.018_neped2.67_betap1.35_w0.063']:
        plot(ax, europed_name, 'blue', crit_value, 'o', False, xy=xy) 
    for europed_name in ['fwi_eta0_rs0.04_neped2.85_betap0.95_w0.07']:
        plot(ax, europed_name, 'green', crit_value, 's', False, xy=xy)   

    # for europed_name in ['fwo_eta1_rs0.04_neped2.85_betap0.95_w0.07']:
    #     plot(ax, europed_name, 'gold', crit_value, marker_resistive, True, xy=xy)   

    for_fixedwidth.add_labels(ax, xy)

    shotnos = [84794, 87342]
    colors = ['purple', 'orange']

    for_fixedwidth.plot_experimental_point(ax, xy, shotnos, colors)

    ax.set_xlim(left=0)
    ax.set_ylim(bottom=0)


if __name__ == '__main__':
    fig, axs = plt.subplots(2,3)
    main('alphapeped',axs[0,0])
    main('nepedteped',axs[0,1])
    main('sepedwidthbis',axs[1,0])
    # main('deltadelta',axs[0,2])
    main('betapbetan',axs[1,1])
    main('relshrelsh',axs[1,2])
    axs[1,2].text(0.05,0.05, f'Threshold: {crit_value}', transform=axs[1,2].transAxes)
    plt.show()
    plt.close()