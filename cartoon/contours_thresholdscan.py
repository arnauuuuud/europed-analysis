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
    parser.add_argument("-c", "--crit")
    parser.add_argument("-Y", "--yaxis", help= "critical value of the growth rate, default : 0.03 for alfven, 0.25 for diamagnetic")
    parser.add_argument("-X", "--xaxis", help= "critical value of the growth rate, default : 0.03 for alfven, 0.25 for diamagnetic")
    parser.add_argument('-x',"--exclud_mode", type=useful_recurring_functions.parse_modes, help = "list of modes to exclude, comma-separated (will plot all modes except for these ones)")

    args = parser.parse_args()

    return args.list, args.crit, args.critical_value, args.yaxis, args.xaxis, args.exclud_mode


def main(list_input, crit, crit_value, ypar, xpar, exclud_mode):
    fig, ax = plt.subplots()

    crit_value = [float(v) for v in crit_value]

    cmap = cm.cool_r
    norm = Normalize(vmin=min(crit_value), vmax=max(crit_value))
    colors = [cmap(norm(value)) for value in crit_value]
    
  

    q_ped_def = 'tepos-delta'
    if ypar is None:
        ypar = 'peped'
    # crit = 'alfven'
    consid_mode_input = None

    print(crit)
    
    ymax = add_contours_to_plot.main(ax, colors, list_input, crit, crit_value, ypar, xpar, exclud_mode, nscan=False)




    xlabel, ylabel = global_functions.contour_labels(xpar, ypar)
    
    if exclud_mode == ['1','30','40','50']:
        text = fr'$n \leq {20}$ & $n \neq 1$'
    elif exclud_mode is None:
        max_n = 50
        text = fr'$n \leq {max_n}$'
    else:
        exclud_mode = [int(a) for a in exclud_mode]
        max_n = np.min(exclud_mode)-10
        text = fr'$n \leq {max_n}$'
    ax.text(0.05,0.05, text, transform=ax.transAxes)

    shot = 84794
    dda = 'T052'
    t0 = 45.619122
    time_range = [44.999969, 45.995216]
    x, xerr = experimental_values.get_values(xpar, shot, dda, t0, time_range)
    y, yerr = experimental_values.get_values(ypar, shot, dda, t0, time_range)
    ax.errorbar([x], [y], xerr=[xerr], yerr=[yerr], fmt='*', color='purple', zorder=10)
    ymax = max(ymax, (y+yerr)*1.05)

    shot = 87342
    dda = 'T037'
    t0 = 46.869762
    time_range = [45.312126, 48.428669]
    x, xerr = experimental_values.get_values(xpar, shot, dda, t0, time_range)
    y, yerr = experimental_values.get_values(ypar, shot, dda, t0, time_range)
    ax.errorbar([x], [y], xerr=[xerr], yerr=[yerr], fmt='*', color='orange', zorder=10)
    ymax = max(ymax, (y+yerr)*1.05)

    ax.set_ylabel(ylabel)
    ax.set_xlabel(xlabel)
    ax.set_ylim(bottom=0, top=ymax)
    ax.set_xlim(left=0)

    folder = '/home/jwp9427/work/figures/contours/'
    prefix = 'A' if crit == 'alfven' else 'D'
    run_name = f'{prefix}{list_input}_{crit_value}_{ypar}_{xpar}_{exclud_mode}'

    print(f'\n    {run_name} DONE\n')
    
    plt.savefig(f'{folder}{run_name}.png')
    plt.close()

if __name__ == '__main__':
    list_input, crit, crit_value, ypar, xpar, exclud_mode = argument_parser()
    main(list_input, crit, crit_value, ypar, xpar, exclud_mode)