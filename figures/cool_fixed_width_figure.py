#!/usr/local/depot/Python-3.7/bin/python
# /usr/local/depot/Python-3.5.1/bin/python

from hoho import useful_recurring_functions, europed_analysis_2, global_functions, startup, pedestal_values, h5_manipulation, spitzer, experimental_values
import hlib.matplotlib as cooltool
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
crit_value_resis = 0.095
marker_ideal = 'o'
marker_resistive = 's'
q_ped_def = 'product'

# xy = 'alphapeped'
# xy = 'nepedteped'
xy = 'sepedwidth'


dict_indices_textbox = {
    
}


def plot(ax, europed_name, color, crit_value, marker = 'o', open_markers=False, xy='alphapeped'):
    print(europed_name)
    try:
        fixed_width = europed_name.startswith('fw')

        crit_x_def = None
        crit_y_def = None

        if xy == 'alphapeped':
            xs = europed_analysis_2.get_x_parameter(europed_name, 'alpha_helena_max')
            ys = europed_analysis_2.get_x_parameter(europed_name, 'peped',q_ped_def)

        elif xy == 'nepedteped':
            xs = europed_analysis_2.get_x_parameter(europed_name, 'neped',q_ped_def)
            ys = europed_analysis_2.get_x_parameter(europed_name, 'teped', q_ped_def)

        elif xy == 'sepedwidth':
            xs = europed_analysis_2.get_x_parameter(europed_name, 'nesep_neped',q_ped_def)
            ys = europed_analysis_2.get_x_parameter(europed_name, 'delta', q_ped_def)

        elif xy == 'sepedwidthbis':
            xs = europed_analysis_2.get_x_parameter(europed_name, 'nesep_neped',q_ped_def)
            crit_y_def = pedestal_values.get_fit_width(europed_name, q='pe', crit='alfven', crit_value=crit_value, fixed_width=fixed_width)

        elif xy == 'deltadelta':
            crit_x_def = pedestal_values.get_fit_width(europed_name, q='ne', crit='alfven', crit_value=crit_value, fixed_width=fixed_width)
            crit_y_def = pedestal_values.get_fit_width(europed_name, q='te', crit='alfven', crit_value=crit_value, fixed_width=fixed_width)

        elif xy == 'betapbetan':
            xs = europed_analysis_2.get_x_parameter(europed_name, 'betap',q_ped_def)
            ys = europed_analysis_2.get_x_parameter(europed_name, 'betan',q_ped_def)

        elif xy == 'relshrelsh':
            crit_x_def = pedestal_values.get_fit_rs(europed_name, crit='alfven', crit_value=crit_value, fixed_width=fixed_width)
            crit_y_def = pedestal_values.get_rs(europed_name, crit='alfven', crit_value=crit_value, fixed_width=fixed_width)

        
        deltas = europed_analysis_2.get_x_parameter(europed_name, 'betaped')  if fixed_width else europed_analysis_2.get_x_parameter(europed_name, 'delta') 
        marker = '+' if not fixed_width else marker

        dict_gamma = europed_analysis_2.get_gammas(europed_name, crit='alfven', fixed_width=fixed_width)
        if crit_x_def is None:
            bo, crit_x, bi = europed_analysis_2.find_critical(xs, deltas, dict_gamma, crit_value)
        else:
            crit_x = crit_x_def

        if crit_y_def is None:
            bo, crit_y, bi = europed_analysis_2.find_critical(ys, deltas, dict_gamma, crit_value)
        else:
            crit_y = crit_y_def

        if not open_markers:
            ax.scatter(crit_x, crit_y, marker=marker, color=color, edgecolor='k', s=50)
        else:
            ax.scatter(crit_x, crit_y, marker=marker, color='white', edgecolor=color, s=50)

    except ValueError:
        pass


    # bo, crit_peped, bi = europed_analysis_2.find_critical(pepeds2, deltas, dict_gamma, crit_value)
    # ax.scatter(crit_alpha, crit_peped, marker=marker, color='white', edgecolor=color, s=50)


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
    
    for europed_name in ['fwo_eta1_rs0.02_neped2.65_betap1.3_w0.065']:
        plot(ax, europed_name, 'green', crit_value_resis, 'p', True, xy=xy)    
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
    # for europed_name in ['fwo_30-50_eta1_rs0.02_neped2.65_betap1.335_w0.06']:
    #     plot(ax, europed_name, 'purple', crit_value_resis, '*', True, xy=xy) 
    # for europed_name in ['fwo_30-50_eta1_rs0.021_neped2.65_betap1.335_w0.06']:
    #     plot(ax, europed_name, 'green', crit_value_resis, '*', True, xy=xy)  
    # for europed_name in ['fwo_30-50_eta1_rs0.022_neped2.65_betap1.335_w0.06']:
    #     plot(ax, europed_name, 'brown', crit_value_resis, '*', True, xy=xy)    
    # for europed_name in ['fwo_30-50_eta1_rs0.02_neped2.65_betap1.34_w0.06']:
    #     plot(ax, europed_name, 'purple', crit_value_resis, 'D', True, xy=xy)  
    # for europed_name in ['fwo_30-50_eta1_rs0.021_neped2.65_betap1.34_w0.06']:
    #     plot(ax, europed_name, 'green', crit_value_resis, 'D', True, xy=xy)  
    # for europed_name in ['fwo_30-50_eta1_rs0.022_neped2.65_betap1.34_w0.06']:
    #     plot(ax, europed_name, 'brown', crit_value_resis, 'D', True, xy=xy)  
    # for europed_name in ['fwo_50_eta1_rs0.02_neped2.65_betap1.37_w0.06']:
    #     plot(ax, europed_name, 'purple', crit_value_resis, 's', True, xy=xy)  
    # for europed_name in ['fwo_50_eta1_rs0.02_neped2.65_betap1.36_w0.06']:
    #     plot(ax, europed_name, 'red', crit_value_resis, 's', True, xy=xy)
    # for europed_name in ['fwo_eta1_rs0.043_neped2.85_betap0.95_w0.075','fwo_eta1_rs0.04_neped2.85_betap0.95_w0.07','fwo_eta1_rs0.037_neped2.85_betap0.95_w0.065']:
    #     plot(ax, europed_name, 'yellow', crit_value_resis, marker_resistive, True, xy=xy)

    
    if xy == 'alphapeped':
        xlabel = global_functions.alpha_label        
        ylabel = global_functions.peped_label

    elif xy == 'nepedteped':
        xlabel = global_functions.neped_label
        ylabel = global_functions.teped_label

    elif xy == 'sepedwidth':
        xlabel = global_functions.nesepneped_label
        ylabel = global_functions.delta_label

    elif xy == 'sepedwidthbis':
        xlabel = global_functions.nesepneped_label
        ylabel = global_functions.delta_pe_label

    elif xy == 'deltadelta':
        xlabel = global_functions.delta_ne_label
        ylabel = global_functions.delta_te_label

    elif xy == 'betapbetan':
        xlabel = global_functions.betap_label
        ylabel = global_functions.betan_label

    elif xy == 'relshrelsh':
        ylabel = global_functions.rs_label
        xlabel = global_functions.rs2_label

    ax.set_ylabel(ylabel)
    ax.set_xlabel(xlabel)


    ppfuid('lfrassin')

    shotnos = [84794, 87342]
    ddas = ['T052', 'T037']
    t0s = [45.51,46.869762]
    time_ranges = [[44.999969, 45.995216],[45.312126, 48.428669]]
    colors = ['yellow', 'orange']

    if xy == 'alphapeped':
        for (shotno, dda, color) in zip(shotnos, ddas, colors):
            alpha, alpha_error = experimental_values.get_alpha(shotno, dda)
            peped, peped_error = experimental_values.get_peped(shotno, dda)
            ax.errorbar([alpha], [peped], xerr=[alpha_error], yerr=[peped_error], fmt='*', color=color, zorder=-1)

    elif xy == 'nepedteped':
        for (shotno, dda, color) in zip(shotnos, ddas, colors):
            teped, teped_error = experimental_values.get_teped(shotno, dda)
            neped, neped_error = experimental_values.get_neped(shotno, dda)
            ax.errorbar([neped], [teped], xerr=[neped_error], yerr=[teped_error], fmt='*', color=color, zorder=-1)

    elif xy == 'sepedwidth':
        for (shotno, dda, color) in zip(shotnos, ddas, colors):
            nesepneped, nesepneped_error = experimental_values.get_nesepneped(shotno, dda)
            wp, wp_error = experimental_values.get_width_pe(shotno, dda)
            ax.errorbar([nesepneped], [wp], xerr=[nesepneped_error], yerr=[wp_error], fmt='*', color=color, zorder=-1)
    
    elif xy == 'sepedwidthbis':
        for (shotno, dda, color) in zip(shotnos, ddas, colors):
            nesepneped, nesepneped_error = experimental_values.get_nesepneped(shotno, dda)
            wp, wp_error = experimental_values.get_width_pe(shotno, dda)
            wp_fit = experimental_values.get_my_fit_width(shotno, dda, 'pe')
            wp_fit_error = wp_fit / wp * wp_error
            ax.errorbar([nesepneped], [wp_fit], xerr=[nesepneped_error], yerr=[wp_fit_error], fmt='*', color=color, zorder=-1)    

    elif xy == 'deltadelta':
        for (shotno, dda, color) in zip(shotnos, ddas, colors):
            wn, wn_error = experimental_values.get_width_ne(shotno, dda)
            wt, wt_error = experimental_values.get_width_te(shotno, dda)

            wn_fit = experimental_values.get_my_fit_width(shotno, dda, 'ne')
            wn_fit_error = wn_fit/wn *wn_error
            wt_fit = experimental_values.get_my_fit_width(shotno, dda, 'te')
            wt_fit_error = wt_fit/wt *wt_error

            ax.errorbar([wn_fit], [wt_fit], xerr=[wn_fit_error], yerr=[wt_fit_error], fmt='*', color=color, zorder=-1)

    elif xy == 'betapbetan':
        for (shotno, to, time_range, color) in zip(shotnos, t0s, time_ranges, colors):
            betap, betap_error = experimental_values.get_betap(shotno, to, time_range)
            betan, betan_error = experimental_values.get_betan(shotno, to, time_range)

            ax.errorbar([betap], [betan], xerr=[betap_error], yerr=[betan_error], fmt='*', color=color, zorder=-1)

    elif xy == 'relshrelsh':
        for (shotno, dda, color) in zip(shotnos, ddas, colors):
            nepostepos, nepostepos_error = experimental_values.get_nepostepos(shotno, dda)
            nepostepos_myfit, nepostepos_myfit_error = experimental_values.get_nepostepos_myfit(shotno, dda)

            ax.errorbar([nepostepos], [nepostepos_myfit], xerr=[nepostepos_error], yerr=[nepostepos_myfit_error], fmt='*', color=color, zorder=-1)

    ax.set_xlim(left=0)
    ax.set_ylim(bottom=0)


if __name__ == '__main__':
    fig, axs = plt.subplots(2,3)
    main('alphapeped',axs[0,0])
    main('nepedteped',axs[0,1])
    main('sepedwidthbis',axs[1,0])
    # main('deltadelta',axs[1,1])
    main('betapbetan',axs[0,2])
    # main('relshrelsh',axs[1,2])
    axs[1,2].text(0.05,0.05, f'Threshold: {crit_value_resis}', transform=axs[1,2].transAxes)
    plt.show()
    plt.close()