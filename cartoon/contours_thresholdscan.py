#!/usr/local/depot/Python-3.7/bin/python
# /usr/local/depot/Python-3.5.1/bin/python

from hoho import useful_recurring_functions, global_functions, startup, for_contour, experimental_values, add_contours_to_plot
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

# matplotlib.rcParams['font.size'] = 14
# matplotlib.rcParams['font.family'] = 'sans-serif'
# matplotlib.rcParams['font.sans-serif'] = [:]


def argument_parser():
    """Defining comandline parser and returning the arguments"""
    parser = argparse.ArgumentParser(description = "Plots the values of the growth rate gamma and the critical contour on a 2D map neped,Teped (with the alven criterion)")
    parser.add_argument("list", help = "prefix of the Europed run")
    
    parser.add_argument("-v", "--critical_value", type=useful_recurring_functions.parse_modes, help= "critical value of the growth rate, default : 0.03 for alfven, 0.25 for diamagnetic")
    parser.add_argument("-Y", "--yaxis", help= "critical value of the growth rate, default : 0.03 for alfven, 0.25 for diamagnetic")
    parser.add_argument("-X", "--xaxis", help= "critical value of the growth rate, default : 0.03 for alfven, 0.25 for diamagnetic")
    parser.add_argument('-x',"--exclud_mode", type=useful_recurring_functions.parse_modes, help = "list of modes to exclude, comma-separated (will plot all modes except for these ones)")

    args = parser.parse_args()

    return args.list, args.critical_value, args.yaxis, args.xaxis, args.exclud_mode


def main(list_input, crit_value, ypar, xpar, exclud_mode):
    fig, ax = plt.subplots()

    crit_value = [float(v) for v in crit_value]

    cmap = cm.plasma_r
    norm = Normalize(vmin=min(crit_value), vmax=max(crit_value))
    colors = [cmap(norm(value)) for value in crit_value]
    
  

    q_ped_def = 'tepos-delta'
    if ypar is None:
        ypar = 'peped'
    crit = 'alfven'
    consid_mode_input = None
    
    ymax = 0

    for color,cv in zip(colors, crit_value):
        print(color)
        ym = add_contours_to_plot.main(ax, color, list_input, cv, ypar, xpar, exclud_mode)
        ymax = max(ymax, ym)



    xlabel, ylabel = global_functions.contour_labels(xpar, ypar)
    
    ax.set_ylabel(ylabel)
    ax.set_xlabel(xlabel)
    ax.set_ylim(bottom=0, top=ymax)
    ax.set_xlim(left=0)

    folder = '/home/jwp9427/work/figures/contours/'
    run_name = f'{list_input}_{crit_value}_{ypar}_{xpar}_{exclud_mode}'
    plt.savefig(f'{folder}{run_name}.png')
    plt.close()

if __name__ == '__main__':
    list_input, crit_value, ypar, xpar, exclud_mode = argument_parser()
    main(list_input, crit_value, ypar, xpar, exclud_mode)