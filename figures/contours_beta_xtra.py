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

cm = 1/2.54

# europed_namess = [[f'tan_eta{eta}_rs{rs}_neped2.57_betap1.3' for rs in ['0.0','0.01','0.02','0.022','0.03','0.04']] for eta in [0, 1]]
# xpar = 'frac'

# europed_namess = [[f'tan_eta{eta}_rs0.022_neped{neped}_betap1.3' for neped in ['1.57','2.07','2.57','3.07','3.57','4.07']] for eta in [0,1]]
# xpar = 'neped'

europed_namess = [[f'tan_eta{eta}_rs0.022_neped2.57_betap{betap}' for betap in ['0.55','0.7','0.85','1.0','1.15','1.3','1.45']] for eta in [0, 1]]
xpar = 'betap'

# europed_namess = [[f'tb_eta{eta}_rs{rs}_neped3_betap0.85' for rs in ['0.01','0.02','0.03','0.04','0.08']] for eta in [0, 1]]
# xpar = 'frac'

# europed_namess = [[f'tb_eta{eta}_rs0.04_neped{neped}_betap0.85' for neped in [1.5,2,2.5,3,3.5,4]] for eta in [0, 1]]
# xpar = 'neped'

# europed_namess = [[f'tb_eta{eta}_rs0.04_neped3_betap{betap}' for betap in ['0.55','0.7','1.0','1.15','1.3']] for eta in [0, 1]]
# xpar = 'betap'

q_ped_def = 'tepos-delta'
ypar = 'alpha'
crit = 'alfven'
crit_value = 0.1
consid_mode = None
exclud_mode = None

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


def main(europed_namess, crit, crit_value, ypar, exclud_mode, consid_mode_input):
    colors = plot_canvas.colors
    linestyles = plot_canvas.linestyles

    fig, ax = plt.subplots()

    min_plot_n = [[0.9,1.1],[0.95,1.05],[0.95,1.05],[0.95,1.05]]

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

    shot = 84794
    dda = 'T052'
    t0 = 45.619122
    time_range = [44.999969, 45.995216]

    x, xerr = experimental_values.get_values(xpar, shot, dda, t0, time_range)
    y, yerr = experimental_values.get_values(ypar, shot, dda, t0, time_range)
    ax.errorbar([x], [y], xerr=[xerr], yerr=[yerr], fmt='*', color='purple', zorder=10)

    shot = 87342
    dda = 'T037'
    t0 = 46.869762
    time_range = [45.312126, 48.428669]
    x, xerr = experimental_values.get_values(xpar, shot, dda, t0, time_range)
    y, yerr = experimental_values.get_values(ypar, shot, dda, t0, time_range)
    ax.errorbar([x], [y], xerr=[xerr], yerr=[yerr], fmt='*', color='orange', zorder=10)


    # europed_name = 'tan_eta1_rs0.022_neped2.57_betap1.3'
    # ycrit_extra = europed_analysis_2.critical_value_europed_name(europed_name, crit, crit_value, ypar, q_ped_def)
    # xcrit_extra = europed_analysis_2.critical_value_europed_name(europed_name, crit, crit_value, xpar, q_ped_def)
    # ax.scatter(xcrit_extra, ycrit_extra, marker='D', color='yellow')

    # europed_name = 'tan_eta1_rs0.022_neped2.57_betap1.3'
    # ycrit_extra = europed_analysis_2.critical_value_europed_name(europed_name, crit, crit_valuqe, ypar, q_ped_def)
    # xcrit_extra = europed_analysis_2.critical_value_europed_name(europed_name, crit, crit_value, xpar, q_ped_def)
    # ax.scatter(xcrit_extra, ycrit_extra, marker='o', color='yellow')

    # europed_name = 'tan_eta0_rs0.035_neped2.85_betap0.95'
    # ycrit_extra = europed_analysis_2.critical_value_europed_name(europed_name, crit, crit_value, ypar, q_ped_def)
    # xcrit_extra = europed_analysis_2.critical_value_europed_name(europed_name, crit, crit_value, xpar, q_ped_def)
    # ax.scatter(xcrit_extra, ycrit_extra, marker='s', color='yellow')

    europed_name = 'tan_eta1_rs0.022_neped2.6_betap1.35'
    ycrit_extra = europed_analysis_2.critical_value_europed_name(europed_name, crit, crit_value, ypar, q_ped_def)
    xcrit_extra = europed_analysis_2.critical_value_europed_name(europed_name, crit, crit_value, xpar, q_ped_def)
    ax.scatter(xcrit_extra, ycrit_extra, marker='o', color='green')

    europed_name = 'tan_eta1_rs0.035_neped2.57_betap1.3'
    ycrit_extra = europed_analysis_2.critical_value_europed_name(europed_name, crit, crit_value, ypar, q_ped_def)
    xcrit_extra = europed_analysis_2.critical_value_europed_name(europed_name, crit, crit_value, xpar, q_ped_def)
    ax.scatter(xcrit_extra, ycrit_extra, marker='o', color='red')

    europed_name = 'tan_eta1_rs0.035_neped2.85_betap1.3'
    ycrit_extra = europed_analysis_2.critical_value_europed_name(europed_name, crit, crit_value, ypar, q_ped_def)
    xcrit_extra = europed_analysis_2.critical_value_europed_name(europed_name, crit, crit_value, xpar, q_ped_def)
    ax.scatter(xcrit_extra, ycrit_extra, marker='o', color='blue')

    europed_name = 'tan_eta1_rs0.04_neped2.8_betap0.95'
    ycrit_extra = europed_analysis_2.critical_value_europed_name(europed_name, crit, crit_value, ypar, q_ped_def)
    xcrit_extra = europed_analysis_2.critical_value_europed_name(europed_name, crit, crit_value, xpar, q_ped_def)
    ax.scatter(xcrit_extra, ycrit_extra, marker='o', color='brown')

    # europed_name = 'tan_2_eta1_rs0.04_neped2.8_betap0.95_kbm0.15'
    # ycrit_extra = europed_analysis_2.critical_value_europed_name(europed_name, crit, crit_value, ypar, q_ped_def)
    # xcrit_extra = europed_analysis_2.critical_value_europed_name(europed_name, crit, crit_value, xpar, q_ped_def)
    # ax.scatter(xcrit_extra, ycrit_extra, marker='o', color='purple')


    xlabel, ylabel = global_functions.contour_labels(xpar, ypar)
    
    ax.set_ylabel(ylabel)
    ax.set_xlabel(xlabel)
    ax.set_ylim(bottom=0)
    ax.set_xlim(left=0)

    plt.show()
    plt.close()

if __name__ == '__main__':
    main(europed_namess, crit, crit_value, ypar, exclud_mode, consid_mode)