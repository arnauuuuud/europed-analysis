#!/usr/local/depot/Python-3.7/bin/python
# /usr/local/depot/Python-3.5.1/bin/python

from thesis import constants
import matplotlib.pyplot as plt
from hoho import useful_recurring_functions, europed_analysis_2, global_functions, startup
import matplotlib.transforms as transforms
from matplotlib.colors import Normalize
import math
import numpy as np
import matplotlib.patches as patches
from paper import plot_canvas

major_linewidth = constants.major_linewidth
fontsizelabel = constants.fontsizelabel
fontsizetick = constants.fontsizetick
colorv = constants.colorv
colorv2 = 'orange'
colorh = 'black'


color_eta0 = plot_canvas.color_eta0
color_n20 = plot_canvas.color_n20
color_n50 = plot_canvas.color_n50


def main():
   

    fig,ax = plt.subplots()


    
    crit = "alfven"
    crit_value=0.08
    frac_uncertainty = 0.1
    plot_hline = True
    plot_vline = True
    x_parameter = 'alpha_helena_max'
    consid_mode_input = None
    exclud_mode = None
    list_legends = {}
    fixed_width=False
    wrongslope = False
    list_consid_mode = [1,2,3,4,5,7,10,20,30,40,50]
    q_ped_def = 'tepos-delta'

    folder_to_save = '/home/jwp9427/work/figures/2025-03-05_paper/'
    europed_run = 'global_v4_84794_eta0_betan3.07_neped2.55_nesepneped0.33'

    x_param = europed_analysis_2.get_x_parameter(europed_run, x_parameter, q_ped_def)
    if not fixed_width:
        deltas = europed_analysis_2.get_x_parameter(europed_run, 'delta')
    else:
        deltas = europed_analysis_2.get_x_parameter(europed_run, 'betaped')


    x_label, y_label = global_functions.get_plot_labels_gamma_profiles(x_parameter, crit)
    ax.set_xlabel(x_label, fontsize = fontsizelabel)
    ax.set_ylabel(y_label, fontsize = fontsizelabel)
    plt.tick_params(axis='both', which='major', labelsize=fontsizetick)

    dict_gamma = europed_analysis_2.get_gammas(europed_run, crit, fixed_width)
    dict_gamma = europed_analysis_2.filter_dict(dict_gamma, list_consid_mode)
    if wrongslope:
        dict_gamma = europed_analysis_2.remove_wrong_slope(dict_gamma)
    dict_gamma_r = europed_analysis_2.reverse_nested_dict(dict_gamma)
    x_envelope, y_envelope = europed_analysis_2.give_envelop(dict_gamma, deltas, x_parameter=x_param)
    ax.plot(x_envelope,y_envelope, color=color_eta0, linewidth=major_linewidth) 

    x_crit = europed_analysis_2.critical_value_europed_name(europed_run, crit, crit_value, x_parameter)
    x_crit_minus = europed_analysis_2.critical_value_europed_name(europed_run, crit, crit_value*0.9, x_parameter)
    x_crit_plus = europed_analysis_2.critical_value_europed_name(europed_run, crit, crit_value*1.1, x_parameter)

    x_limits = plt.xlim()
    y_limits = plt.ylim()
    
    ax.axvspan(x_crit_minus,x_crit_plus,color=colorv2,alpha=0.1)
    # ax.vlines(x_crit,color=color_eta0, ymin=crit_value, ymax=y_limits[1], linewidth=major_linewidth)
    # ax.vlines(x_crit_minus,color=color_eta0, ymin=crit_value*(1-frac_uncertainty), ymax=y_limits[1], linestyle="--", linewidth=major_linewidth, alpha=1)
    # ax.vlines(x_crit_plus,color=color_eta0, ymin=crit_value*(1+frac_uncertainty), ymax=y_limits[1], linestyle="--", linewidth=major_linewidth, alpha=1)

    europed_run = 'global_v4_84794_eta1_betan3.07_neped2.55_nesepneped0.33'

    x_param = europed_analysis_2.get_x_parameter(europed_run, x_parameter, q_ped_def)
    if not fixed_width:
        deltas = europed_analysis_2.get_x_parameter(europed_run, 'delta')
    else:
        deltas = europed_analysis_2.get_x_parameter(europed_run, 'betaped')


    x_label, y_label = global_functions.get_plot_labels_gamma_profiles(x_parameter, crit)
    ax.set_xlabel(x_label, fontsize = fontsizelabel)
    ax.set_ylabel(y_label, fontsize = fontsizelabel)
    plt.tick_params(axis='both', which='major', labelsize=fontsizetick)

    dict_gamma = europed_analysis_2.get_gammas(europed_run, crit, fixed_width)
    dict_gamma = europed_analysis_2.filter_dict(dict_gamma, list_consid_mode)
    if wrongslope:
        dict_gamma = europed_analysis_2.remove_wrong_slope(dict_gamma)
    dict_gamma_r = europed_analysis_2.reverse_nested_dict(dict_gamma)
    x_envelope, y_envelope = europed_analysis_2.give_envelop(dict_gamma, deltas, x_parameter=x_param)
    ax.plot(x_envelope,y_envelope, color=color_n50, linewidth=major_linewidth) 

    x_crit = europed_analysis_2.critical_value_europed_name(europed_run, crit, crit_value, x_parameter, list_consid_mode=list_consid_mode)
    x_crit_minus = europed_analysis_2.critical_value_europed_name(europed_run, crit, crit_value*(1-frac_uncertainty), x_parameter, list_consid_mode=list_consid_mode)
    x_crit_plus = europed_analysis_2.critical_value_europed_name(europed_run, crit, crit_value*(1+frac_uncertainty), x_parameter, list_consid_mode=list_consid_mode)
    
    trans = transforms.blended_transform_factory(ax.transData, ax.transAxes)
    # ax.text(x_crit, 1, r"$\alpha_0$", color=colorv, horizontalalignment='center', verticalalignment='bottom',transform=trans, fontsize=fontsizetick)
    # ax.text(x_crit_plus, 1, r"$\alpha_{s}$", color=colorv, horizontalalignment='center', verticalalignment='bottom',transform=trans, fontsize=fontsizetick)
    # ax.text(x_crit_minus, 1, r"$\alpha_{i}$", color=colorv, horizontalalignment='center', verticalalignment='bottom',transform=trans, fontsize=fontsizetick)


    x_label, y_label = global_functions.get_plot_labels_gamma_profiles(x_parameter, crit)

    # ax.tick_params(axis='y', which='both', left=True, right=True, labelleft=False, labelright=True)


    # ax.set_xlim(left=0)
    # ax.set_ylim(bottom=0)


    ax.set_xlabel(x_label, fontsize = fontsizelabel)
    ax.set_ylabel(y_label, fontsize = fontsizelabel)
    plt.tick_params(axis='both', which='major', labelsize=fontsizetick)

    ax.yaxis.set_label_position("left") 
    ax.axhspan(crit_value*0.9,crit_value*1.1,color=colorh,alpha=0.1)
    ax.axvspan(x_crit_minus,x_crit_plus,color=color_n50,alpha=0.1)

    ax.axhline(crit_value, color=colorh)

    # ax.hlines(crit_value, color=colorh, xmax=x_crit, xmin=4, linewidth=major_linewidth)
    # ax.hlines(crit_value*0.9, linestyle="--", color=colorh, xmax=x_crit_minus, xmin=4, linewidth=major_linewidth, alpha=1)
    # ax.hlines(crit_value*1.1, linestyle="--", color=colorh, xmax=x_crit_plus, xmin=4, linewidth=major_linewidth, alpha=1)
    
    # ax.vlines(x_crit,color=color_n50, ymin=crit_value, ymax=y_limits[1], linewidth=major_linewidth)
    # ax.vlines(x_crit_minus,color=color_n50, ymin=crit_value*0.9, ymax=y_limits[1], linestyle="--", linewidth=major_linewidth, alpha=1)
    # ax.vlines(x_crit_plus,color=color_n50, ymin=crit_value*1.1, ymax=y_limits[1], linestyle="--", linewidth=major_linewidth, alpha=1)

    europed_run = 'global_v4_84794_eta1_betan3.07_neped2.55_nesepneped0.33'
    list_consid_mode = [1, 2, 3, 4, 5, 7, 10, 20]

    x_param = europed_analysis_2.get_x_parameter(europed_run, x_parameter, q_ped_def)
    if not fixed_width:
        deltas = europed_analysis_2.get_x_parameter(europed_run, 'delta')
    else:
        deltas = europed_analysis_2.get_x_parameter(europed_run, 'betaped')


    x_label, y_label = global_functions.get_plot_labels_gamma_profiles(x_parameter, crit)
    ax.set_xlabel(x_label, fontsize = fontsizelabel)
    ax.set_ylabel(y_label, fontsize = fontsizelabel)
    plt.tick_params(axis='both', which='major', labelsize=fontsizetick)

    dict_gamma = europed_analysis_2.get_gammas(europed_run, crit, fixed_width)
    dict_gamma = europed_analysis_2.filter_dict(dict_gamma, list_consid_mode)
    if wrongslope:
        dict_gamma = europed_analysis_2.remove_wrong_slope(dict_gamma)
    dict_gamma_r = europed_analysis_2.reverse_nested_dict(dict_gamma)
    x_envelope, y_envelope = europed_analysis_2.give_envelop(dict_gamma, deltas, x_parameter=x_param)
    ax.plot(x_envelope,y_envelope, color=color_n20, linewidth=major_linewidth) 

    x_crit = europed_analysis_2.critical_value_europed_name(europed_run, crit, crit_value, x_parameter, list_consid_mode=list_consid_mode)
    x_crit_minus = europed_analysis_2.critical_value_europed_name(europed_run, crit, crit_value*(1-frac_uncertainty), x_parameter, list_consid_mode=list_consid_mode)
    x_crit_plus = europed_analysis_2.critical_value_europed_name(europed_run, crit, crit_value*(1+frac_uncertainty), x_parameter, list_consid_mode=list_consid_mode)
    
    trans = transforms.blended_transform_factory(ax.transData, ax.transAxes)
    # ax.text(x_crit, 1, r"$\alpha_0$", color=colorv, horizontalalignment='center', verticalalignment='bottom',transform=trans, fontsize=fontsizetick)
    # ax.text(x_crit_plus, 1, r"$\alpha_{s}$", color=colorv, horizontalalignment='center', verticalalignment='bottom',transform=trans, fontsize=fontsizetick)
    # ax.text(x_crit_minus, 1, r"$\alpha_{i}$", color=colorv, horizontalalignment='center', verticalalignment='bottom',transform=trans, fontsize=fontsizetick)


    x_label, y_label = global_functions.get_plot_labels_gamma_profiles(x_parameter, crit)

    # ax.tick_params(axis='y', which='both', left=True, right=True, labelleft=False, labelright=True)


    # ax.set_xlim(left=0)
    # ax.set_ylim(bottom=0)


    ax.set_xlabel(x_label, fontsize = fontsizelabel)
    ax.set_ylabel(y_label, fontsize = fontsizelabel)
    plt.tick_params(axis='both', which='major', labelsize=fontsizetick)

    ax.yaxis.set_label_position("left") 
    ax.axhspan(crit_value*0.9,crit_value*1.1,color=colorh,alpha=0.1)
    ax.axvspan(x_crit_minus,x_crit_plus,color=color_n20,alpha=0.1)

    ax.axhline(crit_value, color=colorh)

    # ax.hlines(crit_value, color=colorh, xmax=x_crit, xmin=4, linewidth=major_linewidth)
    # ax.hlines(crit_value*0.9, linestyle="--", color=colorh, xmax=x_crit_minus, xmin=4, linewidth=major_linewidth, alpha=1)
    # ax.hlines(crit_value*1.1, linestyle="--", color=colorh, xmax=x_crit_plus, xmin=4, linewidth=major_linewidth, alpha=1)
    
    # ax.vlines(x_crit,color=color_n20, ymin=crit_value, ymax=y_limits[1], linewidth=major_linewidth)
    # ax.vlines(x_crit_minus,color=color_n20, ymin=crit_value*0.9, ymax=y_limits[1], linestyle="--", linewidth=major_linewidth, alpha=1)
    # ax.vlines(x_crit_plus,color=color_n20, ymin=crit_value*1.1, ymax=y_limits[1], linestyle="--", linewidth=major_linewidth, alpha=1)

    # ax.set_ylim(bottom=0.1, top=0.4)
    # ax.set_xlim(left=5.2, right=6.2)


    # ax1 = axs[0]
    # ax2 = axs[1]

    # # Draw a rectangle in the first subplot
    # rect = patches.Rectangle((5.2, 0.1), 1, 0.3, linewidth=1, edgecolor='gray', facecolor='none')
    # ax1.add_patch(rect)

    # xyA = (5.2, 0.1)  # (x, y) on ax1
    # xyB = (0, 0)

    # connection_line = patches.ConnectionPatch(xyA=xyA, xyB=xyB, coordsA="data", coordsB="axes fraction", axesA=ax1, axesB=ax2, color="gray", linestyle="-")
    # ax1.add_patch(connection_line)

    # xyA = (5.2, 0.4)  # (x, y) on ax1
    # xyB = (0, 1)
    # connection_line = patches.ConnectionPatch(xyA=xyA, xyB=xyB, coordsA="data", coordsB="axes fraction", axesA=ax1, axesB=ax2, color="gray", linestyle="-")
    # ax1.add_artist(connection_line)


    ax.set_xlim(left=2,right=6)
    ax.set_ylim(bottom=0, top=0.14)

    plt.subplots_adjust(wspace=0, hspace=0)
    plt.savefig(folder_to_save+'5.png') 
    plt.show()
    plt.close()

if __name__ == '__main__':
    main()