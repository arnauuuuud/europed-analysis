#!/usr/local/depot/Python-3.7/bin/python
# /usr/local/depot/Python-3.5.1/bin/python

from hoho import useful_recurring_functions, europed_analysis_2, global_functions, startup, pedestal_values, h5_manipulation, spitzer, experimental_values, for_fixedwidth
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

crit_value_ideal = 0.03
crit_value_resis = 0.1
list_n = [[],[50],[40,50],[30,40,50]]
marker_ideal = 'o'
marker_resistive = 's'
q_ped_def = 'tepos-delta'

# xy = 'alphapeped'
# xy = 'nepedteped'
xy = 'sepedwidth'


def plot(ax, europed_name, color, crit_value, marker = 'o', open_markers=False, xy='alphapeped'):
    print(europed_name)
    crit_x, crit_y = for_fixedwidth.give_critx_crity(europed_name, crit, crit_value, xy, q_ped_def)

    if not open_markers:
        ax.scatter(crit_x, crit_y, marker=marker, color=color, edgecolor='k', s=50)
    else:
        ax.scatter(crit_x, crit_y, marker=marker, color='white', edgecolor=color, s=50)

def plot_line(ax, europed_name, color, crit_value, list_n, xy='alphapeped'):
    x = []
    y = []
    for ex in list_n:
        crit_x, crit_y = for_fixedwidth.give_critx_crity(europed_name, crit, crit_value, xy, ex)
        x.append(float(crit_x))
        y.append(float(crit_y))
    print(x)
    print(y)

    x_filt = [xi for xi in x if not xi is None]
    y_filt = [yi for yi in y if not yi is None]

    print(x_filt)
    print(y_filt)
    ax.plot(x_filt, y_filt, color=color, linewidth=0.5, zorder=-1)


def main(xy, ax):
    # for europed_name in [f'fwo_eta0_rs{rs}_neped2.65_betap1.3_w0.065' for rs in [0.023,0.028,0.033]]:
    #     plot(ax, europed_name, 'green', crit_value_ideal, marker=marker_ideal, xy=xy)
    # for europed_name in [f'fwo_eta0_rs0.033_neped{neped}_betap1.3_w0.065' for neped in [2.75,2.85]]:
    #     plot(ax, europed_name, 'red', crit_value_ideal, marker=marker_ideal, xy=xy)
    # for europed_name in [f'fwo_eta0_rs0.033_neped2.85_betap{betap}_w0.065' for betap in [1.1,0.95]]:
    #     plot(ax, europed_name, 'blue', crit_value_ideal, marker=marker_ideal, xy=xy)
    # for europed_name in [f'fwo_eta0_rs0.033_neped2.85_betap0.95_w{w}' for w in [0.07,0.075]]:
    #     plot(ax, europed_name, 'purple', crit_value_ideal, marker=marker_ideal, xy=xy)

    # for europed_name in [f'fwo_eta1_rs{rs}_neped2.65_betap1.3_w0.065' for rs in [0.023]]:
    #     plot(ax, europed_name, 'green', crit_value_resis, marker_resistive, True, xy=xy)
    # for europed_name in [f'fwo_eta1_rs0.033_neped{neped}_betap1.3_w0.065' for neped in [2.75,2.85]]:
    #     plot(ax, europed_name, 'red', crit_value_resis, marker_resistive, True, xy=xy)
    # for europed_name in [f'fwo_eta1_rs0.033_neped2.85_betap{betap}_w0.065' for betap in [1.1,0.95]]:
    #     plot(ax, europed_name, 'blue', crit_value_resis, marker_resistive, True, xy=xy)
    # for europed_name in [f'fwo_eta1_rs0.033_neped2.85_betap0.95_w{w}' for w in [0.07,0.075]]:
    #     plot(ax, europed_name, 'purple', crit_value_resis, marker_resistive, True, xy=xy)
    # for europed_name in [f'fwo_eta1_rs0.033_neped2.85_betap0.95_w{w}' for w in [0.065,0.07,0.075]]:
    #     plot(ax, europed_name, 'purple', crit_value_resis, marker_resistive, True, xy=xy)
    # for europed_name in [f'fwo_eta1_rs0.038_neped2.85_betap0.95_w{w}' for w in [0.075]]:
    #     plot(ax, europed_name, 'red', crit_value_resis, marker_resistive, True, xy=xy)
    
    for europed_name in ['tan_eta1_rs0.022_neped2.57_betap1.3']:
        plot(ax, europed_name, 'green', crit_value_resis, 'p', True, xy=xy)    
        plot_line(ax, europed_name, 'green', crit_value_resis, list_n, xy=xy)    
    # for europed_name in ['fwo_30-50_eta1_rs0.02_neped2.65_betap1.35_w0.06']:
    #     plot(ax, europed_name, 'blue', crit_value_resis, 'p', True, xy=xy)    
    # for europed_name in ['fwo_30-50_eta1_rs0.02_neped2.65_betap1.35_w0.061']:
    #     plot(ax, europed_name, 'red', crit_value_resis, 'p', True, xy=xy)    
    # for europed_name in ['fwo_30-50_eta1_rs0.02_neped2.65_betap1.35_w0.062']:
    #     plot(ax, europed_name, 'purple', crit_value_resis, 'p', True, xy=xy)    
    # for europed_name in ['fwo_30-50_eta1_rs0.02_neped2.65_betap1.35_w0.063']:
    #     plot(ax, europed_name, 'brown', crit_value_resis, 'p', True, xy=xy)    
    # for europed_name in ['fwo_30-50_eta1_rs0.022_neped2.65_betap1.35_w0.063']:
    #     plot(ax, europed_name, 'purple', crit_value_resis, 'o', True, xy=xy)    
    # for europed_name in ['fwo_30-50_eta1_rs0.023_neped2.65_betap1.35_w0.063']:
    #     plot(ax, europed_name, 'red', crit_value_resis, 'o', True, xy=xy)    
    # for europed_name in ['fwo_30-50_eta1_rs0.024_neped2.65_betap1.35_w0.063']:
    #     plot(ax, europed_name, 'blue', crit_value_resis, 'o', True, xy=xy)    
    # for europed_name in ['fwo_30-50_eta1_rs0.025_neped2.65_betap1.35_w0.063']:
    #     plot(ax, europed_name, 'green', crit_value_resis, 'o', True, xy=xy)  
    # for europed_name in ['fwo_30-50_eta1_rs0.022_neped2.65_betap1.335_w0.06']:
    #     plot(ax, europed_name, 'purple', crit_value_resis, 's', True, xy=xy)    
    # for europed_name in ['fwo_30-50_eta1_rs0.022_neped2.65_betap1.34_w0.06']:
    #     plot(ax, europed_name, 'purple', crit_value_resis, 'D', True, xy=xy)
    # for europed_name in ['fwo_eta1_rs0.043_neped2.85_betap0.95_w0.075','fwo_eta1_rs0.04_neped2.85_betap0.95_w0.07','fwo_eta1_rs0.037_neped2.85_betap0.95_w0.065']:
    #     plot(ax, europed_name, 'yellow', crit_value_resis, marker_resistive, True, xy=xy)

    

    for_fixedwidth.add_labels(ax, xy)

    shotnos = [84794, 87342]
    colors = ['purple', 'orange']

    for_fixedwidth.plot_experimental_point(ax, xy, shotnos, colors)

    ax.set_xlim(left=0)
    ax.set_ylim(bottom=0)


if __name__ == '__main__':
    fig, axs = plt.subplots(2,3)
    main('alphapeped',axs[0,0])
    # main('nepedteped',axs[0,1])
    # main('sepedwidthbis',axs[1,0])
    # main('deltadelta',axs[1,1])
    # main('betapbetan',axs[0,2])
    # main('relshrelsh',axs[1,2])
    axs[1,2].text(0.05,0.05, f'Threshold: {crit_value_resis}', transform=axs[1,2].transAxes)
    plt.show()
    plt.close()