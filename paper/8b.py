#!/usr/local/depot/Python-3.7/bin/python
# /usr/local/depot/Python-3.5.1/bin/python

from hoho import useful_recurring_functions, global_functions, startup, for_contour, experimental_values
from paper import plot_canvas
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

colorHPLG = plot_canvas.colorHPLG
color_eta0 = plot_canvas.color_eta0
color_n20 = plot_canvas.color_n20
color_n30 = plot_canvas.color_n30
color_n40 = plot_canvas.color_n40
color_n50 = plot_canvas.color_n50
colors = [color_n20,color_n30,color_n40,color_n50]
folder_to_save = '/home/jwp9427/work/figures/2025-03-05_paper/'

europed_namess = [[f'tan_eta{eta}_rs{rs}_neped2.57_betap1.3' for rs in ['0.0','0.01','0.02','0.022','0.03','0.04']] for eta in [1, 1, 1, 1]]
xpar = 'frac'

# europed_namess = [[f'tan_eta{eta}_rs0.022_neped{neped}_betap1.3' for neped in ['1.57','2.07','2.57','3.07','3.57','4.07']] for eta in [0,1,1]]
# xpar = 'neped'

# europed_namess = [[f'tan_eta{eta}_rs0.022_neped2.57_betap{betap}' for betap in ['0.55','0.7','0.85','1.0','1.15','1.3','1.45']] for eta in [0, 1]]
# xpar = 'betap'

# europed_namess = [[f'tb_eta{eta}_rs{rs}_neped3_betap0.85' for rs in ['0.01','0.02','0.03','0.04','0.08']] for eta in [0, 1]]
# xpar = 'frac'

# europed_namess = [[f'tb_eta{eta}_rs0.04_neped{neped}_betap0.85' for neped in [1.5,2,2.5,3,3.5,4]] for eta in [0, 1]]
# xpar = 'neped'

# europed_namess = [[f'tb_eta{eta}_rs0.04_neped3_betap{betap}' for betap in ['0.55','0.7','1.0','1.15','1.3']] for eta in [0, 1]]
# xpar = 'betap'

q_ped_def = 'positionTeped'
ypar = 'alpha'
crit = 'alfven'
crit_value = 0.08
frac_uncertainty = 0.1
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



def main(ax, europed_namess, crit, crit_value, ypar, exclud_mode, consid_mode_input):

    linestyle_temp = '-'

    min_plot_n = [[0.9,1.1],[0.95,1.05],[0.95,1.05],[0.95,1.05]]

    for i,europed_names in enumerate(europed_namess):
        if i == 0:
            consid_mode_input = [1,2,3,4,5,7,10,20]
        if i == 1:
            consid_mode_input = [1,2,3,4,5,7,10,20,30]
        if i == 2:
            consid_mode_input = [1,2,3,4,5,7,10,20,30,40]
        if i == 3:
            consid_mode_input = [1,2,3,4,5,7,10,20,30,40,50]
        try:
            x, y, z, list_n, triang = for_contour.give_triangles_to_plot(europed_names, xpar, ypar, crit, consid_mode_input, exclud_mode, q_ped_def)
        except RuntimeError:
            continue
        color_temp = colors[i]

        cs = ax.tricontour(triang, z, levels=[crit_value],colors=[color_temp],linestyles=linestyle_temp,linewidths=3)

        # ax.scatter(x,y)
        # ax.triplot(triang)
        # plotplot = min_plot_n[i]

        # for x_ind,y_ind,n_ind,z_ind in zip(x,y,list_n,z):
        #     if y_ind > 0 and y_ind < 4.5 and z_ind > plotplot[0]*crit_value and z_ind < plotplot[1]*crit_value and x_ind<3.9:
        #         if i == 0 and x_ind >2.5:
        #             y_ind += 0.1
                
        #         ax.text(x_ind, y_ind, str(n_ind), fontsize=10, color=color_temp, fontweight='bold')


    # x, xerr = experimental_values.get_values(xpar, shot, dda, t0, time_range)
    # y, yerr = experimental_values.get_values(ypar, shot, dda, t0, time_range)
    # ax.errorbar([x], [y], xerr=[xerr], yerr=[yerr], fmt='*', color=colorHPLG, zorder=10)

    
    


if __name__ == '__main__':
    fig, ax = plt.subplots(figsize=(6,5))

    ypar = 'peped'
    main(ax,europed_namess, crit, crit_value, ypar, exclud_mode, consid_mode)
    xlabel, ylabel = global_functions.contour_labels(xpar, ypar)
    ax.set_ylabel(ylabel)
    ax.set_xlabel(xlabel)
    ax.set_ylim(bottom=0)
    ax.set_xlim(left=0)



    plt.savefig(folder_to_save+'8b.png')
    plt.show()
    plt.close()