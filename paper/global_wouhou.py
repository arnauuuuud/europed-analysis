#!/usr/local/depot/Python-3.7/bin/python
# /usr/local/depot/Python-3.5.1/bin/python

from hoho import useful_recurring_functions, europed_analysis_2, global_functions, startup, pedestal_values, h5_manipulation, spitzer, experimental_values, for_fixedwidth
from paper import plot_canvas
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


colorHPLG = plot_canvas.colorHPLG
colorHPHG = plot_canvas.colorHPHG
color_eta0 = plot_canvas.color_eta0
color_n50 = plot_canvas.color_n50
color_n20 = plot_canvas.color_n20

crit_value_ideal = 0.09
crit_value_resis = 0.09
crit_value_resis_n20 = 0.09
crit_value_list_resis = [0.9*crit_value_resis,crit_value_resis,1.1*crit_value_resis]
crit_value_list_resis_n20 = [0.9*crit_value_resis_n20,crit_value_resis_n20,1.1*crit_value_resis_n20]
crit_value_list_ideal = [0.9*crit_value_ideal,crit_value_ideal,1.1*crit_value_ideal]
marker_ideal = 'o'
marker_resistive = 'p'
q_ped_def = 'tepos-delta'
crit = 'alfven'

folder_to_save = '/home/jwp9427/work/figures/2025-03-05_paper/'

# xy = 'alphapeped'
# xy = 'nepedteped'
xy = 'sepedwidth'


def plot(ax, europed_name, color, crit_value, marker = 'o', open_markers=False, xy='alphapeped', list_consid_mode=[1,2,3,4,5,7,10,20,30,40,50]):
    print(europed_name)
    try:
        crit_x, crit_y = for_fixedwidth.give_critx_crity(europed_name, crit, crit_value, xy, q_ped_def, list_consid_mode=list_consid_mode)

        if not open_markers:
            ax.scatter(crit_x, crit_y, marker=marker, color=color, edgecolor='k', s=100)
        else:
            ax.scatter(crit_x, crit_y, marker=marker, color='white', edgecolor=color, s=100)
        return crit_x, crit_y
    except KeyError:
        return None, None

def plot_line(ax, europed_name, color, crit_value_list, xy='alphapeped', list_consid_mode=[1,2,3,4,5,7,10,20,30,40,50]):
    x = []
    y = []
    for cv in crit_value_list:
        try:
            crit_x, crit_y = for_fixedwidth.give_critx_crity(europed_name, crit, cv, xy, q_ped_def, list_consid_mode=list_consid_mode)
            x.append(float(crit_x))
            y.append(float(crit_y))
        except (KeyError, TypeError) as e:
            pass
    print(x)
    print(y)

    x_filt = [xi for xi in x if not xi is None]
    y_filt = [yi for yi in y if not yi is None]

    print(x_filt)
    print(y_filt)
    ax.plot(x_filt, y_filt, color=color, linewidth=0.5, zorder=-1)


def main(xy, axs):  
    ax = axs[2]
    list_x = []  
    list_y = []  
    for europed_name in ['global_v4_84794_eta1_betan3.07_neped2.55_nesepneped0.33']:
        color = 'blue'
        x,y = plot(ax, europed_name, color, crit_value_resis, 'p', False, xy=xy)    
        # plot_line(ax, europed_name, color, crit_value_list_resis , xy=xy)  
        list_x.append(x)
        list_y.append(y)
    for europed_name in ['global_v4_84794_eta1_betan2.12_neped2.55_nesepneped0.33']:
        color = 'purple'
        x,y = plot(ax, europed_name, color, crit_value_resis, 'p', False, xy=xy)    
        # plot_line(ax, europed_name, color, crit_value_list_resis , xy=xy)    
        list_x.append(x)
        list_y.append(y) 
    for europed_name in ['global_v4_84794_eta1_betan2.12_neped2.72_nesepneped0.33']:
        color = 'gray'
        x,y = plot(ax, europed_name, color, crit_value_resis, 'p', False, xy=xy)    
    #     plot_line(ax, europed_name, color, crit_value_list_resis , xy=xy)    
        list_x.append(x)
        list_y.append(y) 
    for europed_name in ['global_v4_87342_eta1_betan2.12_neped2.72_nesepneped0.57']:
        color = 'magenta'
        x,y = plot(ax, europed_name, color, crit_value_resis, 'p', False, xy=xy)    
        # plot_line(ax, europed_name, color, crit_value_list_resis , xy=xy)     
        list_x.append(x)
        list_y.append(y) 
    ax.plot(list_x, list_y, color_n50)


    for_fixedwidth.add_labels(ax, xy)

    shotnos = [84794, 87342]
    colors = [colorHPLG, colorHPHG]

    for_fixedwidth.plot_experimental_point(ax, xy, shotnos, colors)

    ax.set_xlim(left=0)
    ax.set_ylim(bottom=0)



    ax = axs[1]
    list_x = []  
    list_y = []  
    list_consid_mode = [1,2,3,4,5,7,10,20]
    for europed_name in ['global_v4_84794_eta1_betan3.07_neped2.55_nesepneped0.33']:
        color = 'blue'
        x,y = plot(ax, europed_name, color, crit_value_resis_n20, 'p', False, xy=xy, list_consid_mode=list_consid_mode)
        # plot_line(ax, europed_name, color, crit_value_list_resis_n20 , xy=xy, list_consid_mode=list_consid_mode)  
        list_x.append(x)
        list_y.append(y)
    for europed_name in ['global_v4_84794_eta1_betan2.12_neped2.55_nesepneped0.33']:
        color = 'purple'
        x,y = plot(ax, europed_name, color, crit_value_resis_n20, 'p', False, xy=xy, list_consid_mode=list_consid_mode)    
        # plot_line(ax, europed_name, color, crit_value_list_resis_n20 , xy=xy, list_consid_mode=list_consid_mode)    
        list_x.append(x)
        list_y.append(y)  
    for europed_name in ['global_v4_84794_eta1_betan2.12_neped2.72_nesepneped0.33']:
        color = 'gray'
        x,y = plot(ax, europed_name, color, crit_value_resis_n20, 'p', False, xy=xy, list_consid_mode=list_consid_mode)    
    #     plot_line(ax, europed_name, color, crit_value_list_resis_n20 , xy=xy) 
        list_x.append(x)
        list_y.append(y)    
    for europed_name in ['global_v4_87342_eta1_betan2.12_neped2.72_nesepneped0.57']:
        color = 'magenta'
        x,y = plot(ax, europed_name, color, crit_value_resis_n20, 'p', False, xy=xy, list_consid_mode=list_consid_mode)    
        # plot_line(ax, europed_name, color, crit_value_list_resis_n20 , xy=xy, list_consid_mode=list_consid_mode)     
        list_x.append(x)
        list_y.append(y) 
    ax.plot(list_x, list_y, color_n20)


    for_fixedwidth.add_labels(ax, xy)

    shotnos = [84794, 87342]
    colors = [colorHPLG, colorHPHG]

    for_fixedwidth.plot_experimental_point(ax, xy, shotnos, colors)

    ax.set_xlim(left=0)
    ax.set_ylim(bottom=0)

    ax = axs[0]
    list_x = []
    list_y = []
    
    for europed_name in ['global_v4_84794_eta0_betan3.07_neped2.55_nesepneped0.33']:
        color = 'blue'
        x,y = plot(ax, europed_name, color, crit_value_ideal, 'p', False, xy=xy)    
        # plot_line(ax, europed_name, color, crit_value_list_ideal , xy=xy)   
        list_x.append(x)
        list_y.append(y) 
    for europed_name in ['global_v4_84794_eta0_betan2.12_neped2.55_nesepneped0.33']:
        color = 'purple'
        x,y = plot(ax, europed_name, color, crit_value_ideal, 'p', False, xy=xy)    
        # plot_line(ax, europed_name, color, crit_value_list_ideal , xy=xy)   
        list_x.append(x)
        list_y.append(y)   
    for europed_name in ['global_v4_84794_eta0_betan2.12_neped2.72_nesepneped0.33']:
        color = 'gray'
        x,y = plot(ax, europed_name, color, crit_value_ideal, 'p', False, xy=xy)    
        # plot_line(ax, europed_name, color, crit_value_list_ideal , xy=xy)    
        list_x.append(x)
        list_y.append(y)  
    for europed_name in ['global_v4_87342_eta0_betan2.12_neped2.72_nesepneped0.57']:
        color = 'magenta'
        x,y = plot(ax, europed_name, color, crit_value_ideal, 'p', False, xy=xy)    
        # plot_line(ax, europed_name, color, crit_value_list_ideal , xy=xy)     
        list_x.append(x)
        list_y.append(y) 
    ax.plot(list_x, list_y, color_eta0)

    

    for_fixedwidth.add_labels(ax, xy)

    shotnos = [84794, 87342]
    colors = [colorHPLG, colorHPHG]

    for_fixedwidth.plot_experimental_point(ax, xy, shotnos, colors)

    ax.set_xlim(left=0)
    ax.set_ylim(bottom=0)


if __name__ == '__main__':
    fig, axs = plt.subplots(1,3, sharex=True, sharey=True, figsize=(10,4))
    main('alphapeped',axs)

    axs[0].set_xlim(2.1,4.9)
    axs[0].set_ylim(2.3,3.9)
    # main('nepedteped',axs[0,1])
    # main('sepedwidthbis',axs[1,0])
    # main('deltadelta',axs[1,1])
    # main('betapbetan',axs[0,2])
    # main('relshrelsh',axs[1,2])
    # axs[1,2].text(0.05,0.05, f'Threshold: {crit_value_resis}', transform=axs[1,2].transAxes)
    plt.savefig(f'{folder_to_save}parambyparam')
    plt.show()