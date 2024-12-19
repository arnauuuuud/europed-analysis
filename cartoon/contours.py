#!/usr/local/depot/Python-3.7/bin/python
# /usr/local/depot/Python-3.5.1/bin/python

from hoho import useful_recurring_functions, global_functions, startup, for_contour, experimental_values
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


def argument_parser():
    """Defining comandline parser and returning the arguments"""
    parser = argparse.ArgumentParser(description = "Plots the values of the growth rate gamma and the critical contour on a 2D map neped,Teped (with the alven criterion)")
    parser.add_argument("list", help = "prefix of the Europed run")
    
    parser.add_argument("-v", "--critical_value", help= "critical value of the growth rate, default : 0.03 for alfven, 0.25 for diamagnetic")
    parser.add_argument("-Y", "--yaxis", help= "critical value of the growth rate, default : 0.03 for alfven, 0.25 for diamagnetic")
    parser.add_argument("-X", "--xaxis", help= "critical value of the growth rate, default : 0.03 for alfven, 0.25 for diamagnetic")
    parser.add_argument('-x',"--exclud_mode", type=useful_recurring_functions.parse_modes, help = "list of modes to exclude, comma-separated (will plot all modes except for these ones)")

    args = parser.parse_args()

    return args.list, args.critical_value, args.yaxis, args.xaxis, args.exclud_mode


def main(list_input, crit_value, ypar, xpar, exclud_mode):
    cm = 1/2.54

    if list_input == 'tanrs':
        europed_namess = [[f'tan_eta{eta}_rs{rs}_neped2.57_betap1.3' for rs in ['0.0','0.01','0.02','0.022','0.03','0.04']] for eta in [0, 1]]
        if xpar is None:
            xpar = 'frac'

    elif list_input == 'tanneped':
        europed_namess = [[f'tan_eta{eta}_rs0.022_neped{neped}_betap1.3' for neped in ['1.57','2.07','2.57','3.07','3.57','4.07']] for eta in [0,1]]
        if xpar is None:
            xpar = 'neped'

    elif list_input == 'tanbeta':
        europed_namess = [[f'tan_eta{eta}_rs0.022_neped2.57_betap{betap}' for betap in ['0.55','0.7','0.85','1.0','1.15','1.3','1.45']] for eta in [0, 1]]
        if xpar is None:
            xpar = 'betap'

    elif list_input == 'tbrs':
        europed_namess = [[f'tb_eta{eta}_rs{rs}_neped3_betap0.85' for rs in ['0.01','0.02','0.03','0.04','0.08']] for eta in [0, 1]]
        if xpar is None:
            xpar = 'frac'

    elif list_input == 'tbneped':
        europed_namess = [[f'tb_eta{eta}_rs0.04_neped{neped}_betap0.85' for neped in [1.5,2,2.5,3,3.5,4]] for eta in [0, 1]]
        if xpar is None:
            xpar = 'neped'

    elif list_input == 'tbbeta':
        europed_namess = [[f'tb_eta{eta}_rs0.04_neped3_betap{betap}' for betap in ['0.55','0.7','1.0','1.15','1.3']] for eta in [0, 1]]
        if xpar is None:
            xpar = 'betap'


    q_ped_def = 'tepos-delta'
    if ypar is None:
        ypar = 'peped'
    crit = 'alfven'
    consid_mode_input = None
    
    crit_value = 0.1 if crit_value is None else float(crit_value)

    if europed_namess[0][0].startswith('tan'):
        shot = 84794
        dda = 'T052'
        t0 = 45.619122
        time_range = [44.999969, 45.995216]
    elif europed_namess[0][0].startswith('tb'):
        shot = 87342
        dda = 'T037'
        t0 = 46.869762
        time_range = [45.312126, 48.428669]

    colors = plot_canvas.colors
    linestyles = plot_canvas.linestyles


    
    colors = plot_canvas.colors
    linestyles = plot_canvas.linestyles

    fig, ax = plt.subplots()

    min_plot_n = [[0.9,1.1],[0.95,1.05],[0.95,1.05],[0.95,1.05]]

    ymax = []
    for i,europed_names in enumerate(europed_namess):
        
        x, y, z, list_n, triang = for_contour.give_triangles_to_plot(europed_names, xpar, ypar, crit, consid_mode_input, exclud_mode, q_ped_def)
        color_temp = colors[i]
        linestyle_temp = linestyles[i]
        cs = ax.tricontour(triang, z, levels=[crit_value],colors=color_temp,linestyles=linestyle_temp,linewidths=3)
        ax.tricontourf(triang, z, levels=[0.85*crit_value,1.15*crit_value],colors=color_temp, alpha=0.2)

        # ax.scatter(x,y)
        # ax.triplot(triang)
        # plotplot = min_plot_n[i]

        # for x_ind,y_ind,n_ind,z_ind in zip(x,y,list_n,z):
        #     if y_ind > 0 and y_ind < 4.5 and z_ind > plotplot[0]*crit_value and z_ind < plotplot[1]*crit_value and x_ind<3.9:
        #         if i == 0 and x_ind >2.5:
        #             y_ind += 0.1
                
        #         ax.text(x_ind, y_ind, str(n_ind), fontsize=10, color=color_temp, fontweight='bold')

        ymax.append(np.nanmax([yi for (yi,zi) in zip(y,z) if zi < 1.2*crit_value]))

    ymax = max(ymax)

    x, xerr = experimental_values.get_values(xpar, shot, dda, t0, time_range)
    y, yerr = experimental_values.get_values(ypar, shot, dda, t0, time_range)
    ax.errorbar([x], [y], xerr=[xerr], yerr=[yerr], fmt='*', color='black', zorder=10)




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