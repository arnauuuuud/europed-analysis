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
    
    parser.add_argument("-v", "--critical_value", help= "critical value of the growth rate, default : 0.03 for alfven, 0.25 for diamagnetic")
    parser.add_argument("-Y", "--yaxis", help= "critical value of the growth rate, default : 0.03 for alfven, 0.25 for diamagnetic")
    parser.add_argument("-X", "--xaxis", help= "critical value of the growth rate, default : 0.03 for alfven, 0.25 for diamagnetic")
    parser.add_argument('-x',"--exclud_mode", type=useful_recurring_functions.parse_list_modes, help = "list of modes to exclude, comma-separated (will plot all modes except for these ones)")

    args = parser.parse_args()

    return args.list, args.critical_value, args.yaxis, args.xaxis, args.exclud_mode


def main(list_input, crit_value, ypar, xpar, exclud_mode):
    fig, ax = plt.subplots()

    print(exclud_mode)
    exclud_modes_good = []
    for b in exclud_mode:
        temp = []
        for a in b:
            if a == '':
                temp = None
            else:
                temp.append(float(a))
        exclud_modes_good.append(temp)
    print(exclud_modes_good)

    cmap = cm.plasma_r

    len_exclude_modes = []
    for b in exclud_modes_good:
        if b is None:
            len_exclude_modes.append(0)
        else:
            len_exclude_modes.append(len(b))
    norm = Normalize(vmin=min(len_exclude_modes), vmax=max(len_exclude_modes))
    colors = [cmap(norm(value)) for value in len_exclude_modes]
    
  

    q_ped_def = 'tepos-delta'
    if ypar is None:
        ypar = 'peped'
    crit = 'alfven'
    consid_mode_input = None
    
    ymax = 0

    for color,em in zip(colors, exclud_modes_good):
        print(color)
        ym = add_contours_to_plot.main(ax, color, list_input, crit_value, ypar, xpar, em)
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