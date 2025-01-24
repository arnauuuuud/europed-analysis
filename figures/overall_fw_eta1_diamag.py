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
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
from matplotlib.collections import LineCollection

matplotlib.rcParams['font.size'] = 14
matplotlib.rcParams['font.family'] = 'sans-serif'
# matplotlib.rcParams['font.sans-serif'] = [:]

cm = 1/2.54


# crit_value_list = [0.05,0.06,0.07,0.08,0.09]
# crit_value = 0.07
# exclude_modes = [30,40,50]

crit_value_list = []
crit_value = 0.09
exclude_modes = [50,40]

marker_ideal = 'o'
marker_resistive = 's'
q_ped_def = 'tepos-delta'
crit = 'diamag'


def main1(xy, ax, crit_value):
    # for europed_name in ['fwi_eta1_rs0.018_neped2.67_betap1.35_w0.063']:
    #     # for_fixedwidth.plot_line_threshold(ax, europed_name, 'blue', crit_value_list, crit, q_ped_def, xy=xy, exclude_modes=[])     
    #     for_fixedwidth.plot(ax, europed_name, 'blue', crit_value, crit, q_ped_def, 'o', True, xy=xy, exclude_modes=[])     
    # for europed_name in ['fwi_eta1_rs0.04_neped2.85_betap0.95_w0.07']:
    #     for_fixedwidth.plot_line_threshold(ax, europed_name, 'green', crit_value_list, crit, q_ped_def, xy=xy, exclude_modes=[])   
    #     for_fixedwidth.plot(ax, europed_name, 'green', crit_value, crit, q_ped_def, marker_resistive, True, xy=xy, exclude_modes=[])      

    for (exclude_modes,marker) in zip([[],[50],[50,40],[50,40,30]],['s','^','o','P']):
        for europed_name in ['fwi_eta1_rs0.018_neped2.67_betap1.35_w0.063']:
            color = global_functions.dict_HPLG_color_threshold[crit_value]
            for_fixedwidth.plot(ax, europed_name, color, crit_value, crit, q_ped_def, marker, False, xy=xy, exclude_modes=exclude_modes)     
        for europed_name in ['fwi_eta1_rs0.04_neped2.85_betap0.95_w0.07']:
            color = global_functions.dict_HPHG_color_threshold[crit_value]
            for_fixedwidth.plot(ax, europed_name, color, crit_value, crit, q_ped_def, marker, False, xy=xy, exclude_modes=exclude_modes)

    for_fixedwidth.add_labels(ax, xy)

    shotnos = [84794, 87342]
    colors = ['purple', 'orange']

    for_fixedwidth.plot_experimental_point(ax, xy, shotnos, colors)

    ax.set_xlim(left=0)
    ax.set_ylim(bottom=0)

def main2(xy, ax, exclude_modes, marker):
    for crit_value in [0.35,0.45,0.55,0.65,0.75]:
        for europed_name in ['fwi_eta1_rs0.018_neped2.67_betap1.35_w0.063']:
            color = global_functions.dict_HPLG_color_threshold_diamag[crit_value]
            for_fixedwidth.plot(ax, europed_name, color, crit_value, crit, q_ped_def, marker, False, xy=xy, exclude_modes=exclude_modes)     
        for europed_name in ['fwi_eta1_rs0.04_neped2.85_betap0.95_w0.07']:
            color = global_functions.dict_HPHG_color_threshold_diamag[crit_value]
            for_fixedwidth.plot(ax, europed_name, color, crit_value, crit, q_ped_def, marker, False, xy=xy, exclude_modes=exclude_modes)

    for_fixedwidth.add_labels(ax, xy)

    shotnos = [84794, 87342]
    colors = ['purple', 'orange']

    for_fixedwidth.plot_experimental_point(ax, xy, shotnos, colors)

    ax.set_xlim(left=0)
    ax.set_ylim(bottom=0)


if __name__ == '__main__':

    # for xy in ['alphapeped','nepedteped','sepedwidthbis','betapbetan']:
        # for crit_value in [0.07,0.08,0.09,0.1,0.11]:
        #     fig, ax = plt.subplots()
        #     main1(xy,ax, crit_value)
        #     # main('nepedteped',axs[0,1])
        #     # main('sepedwidthbis',axs[1,0])
        #     # # main('deltadelta',axs[0,2])
        #     # main('betapbetan',axs[1,1])
        #     # main('relshrelsh',axs[1,2])
        #     ax.text(0.05,0.05, f'Threshold: {crit_value}', transform=ax.transAxes)

        #     custom_entries = []

        #     for (max_mode,marker) in zip([50,40,30,20],['s','^','o','P']):
        #         custom_entries.append(Line2D([0], [0], color='black', lw=0, marker=marker, label=fr'$n\leq{max_mode}$'))
                
        #     # Custom legend placement
        #     legend1 = ax.legend(handles=custom_entries, fontsize=8)
        #     ax.add_artist(legend1)

        #     dict1 = global_functions.dict_HPLG_color_threshold
        #     dict2 = global_functions.dict_HPHG_color_threshold
  
        #     list_label1 = []
        #     list_label2 = []
        #     list_pa1 = []
        #     list_pa2 = []

        #     for (value, color1, color2) in zip(dict1.keys(),dict1.values(),dict2.values()):
        #         list_label1.append('')
        #         list_label2.append(value)
        #         list_pa1.append(Patch(facecolor=color2))
        #         list_pa2.append(Patch(facecolor=color1))

        #     list_label = list_label1+list_label2
        #     list_pa = list_pa1+list_pa2
        #     fig.canvas.draw()
        #     legend_bbox = legend1.get_window_extent()

        #     # Convert pixels to figure coordinates
        #     bbox_in_axis_coords = legend_bbox.transformed(ax.transAxes.inverted())
        #     x0, y0, width, height = bbox_in_axis_coords.bounds

        #     ax.legend(handles=list_pa, labels=list_label, ncol=2, handletextpad=0.5, handlelength=1.0, columnspacing=-0.5, loc='upper left', fontsize=8, bbox_to_anchor=(x0 + width + 0.01, y0 + height + 0.01))
        #     if crit_value == 0.1:
        #         crit_value = '0.10'
        #     plt.savefig(f'/home/jwp9427/work/figures/2025-01-14_Gather_all/overall_fw_eta1_{xy}_threshold{crit_value}.png')

    for xy in ['alphapeped','nepedteped','sepedwidthbis','betapbetan']:
        for (exclude_modes,marker) in zip([[50,40,30,1]],['s']):
            fig, ax = plt.subplots()
            main2(xy,ax, exclude_modes, marker)
            if exclude_modes == [1,30,40,50]:
                text = fr'$n \leq {20}$ & $n \neq 1$'
            elif exclude_modes is None:
                max_n = 50
                text = fr'$n \leq {max_n}$'
            else:
                exclude_modes = [int(a) for a in exclude_modes]
                max_n = np.min(exclude_modes)-10
                text = fr'$n \leq {max_n}$'
            ax.text(0.05,0.05, text, transform=ax.transAxes)
            custom_entries = []

            for (max_mode,marker) in zip([20],['s']):
                custom_entries.append(Line2D([0], [0], color='black', lw=0, marker=marker, label=fr'$n\leq{max_mode}$'))
                
            # Custom legend placement
            legend1 = ax.legend(handles=custom_entries, fontsize=8, loc = 'upper left')
            ax.add_artist(legend1)

            dict1 = global_functions.dict_HPLG_color_threshold_diamag
            dict2 = global_functions.dict_HPHG_color_threshold_diamag
  
            list_label1 = []
            list_label2 = []
            list_pa1 = []
            list_pa2 = []

            for (value, color1, color2) in zip(dict1.keys(),dict1.values(),dict2.values()):
                list_label1.append('')
                list_label2.append(value)
                list_pa1.append(Patch(facecolor=color2))
                list_pa2.append(Patch(facecolor=color1))

            list_label = list_label1+list_label2
            list_pa = list_pa1+list_pa2
            fig.canvas.draw()
            legend_bbox = legend1.get_window_extent()

            # Convert pixels to figure coordinates
            bbox_in_axis_coords = legend_bbox.transformed(ax.transAxes.inverted())
            x0, y0, width, height = bbox_in_axis_coords.bounds

            ax.legend(handles=list_pa, labels=list_label, ncol=2, handletextpad=0.5, handlelength=1.0, columnspacing=-0.5, loc='upper left', fontsize=8, bbox_to_anchor=(x0 + width + 0.01, y0 + height + 0.01))
            if crit_value == 0.1:
                crit_value = '0.10'
            plt.savefig(f'/home/jwp9427/work/figures/2025-01-14_Gather_all/Doverall_fw_eta1_{xy}.png')