#!/usr/local/depot/Python-3.7/bin/python
# /usr/local/depot/Python-3.5.1/bin/python

from paper import constants
import matplotlib.pyplot as plt
from hoho import europed_analysis, global_functions, startup
import matplotlib.transforms as transforms
from matplotlib.colors import Normalize
import math
import numpy as np
import matplotlib.patches as patches
from matplotlib.gridspec import GridSpec,GridSpecFromSubplotSpec
import matplotlib as mpl

major_linewidth = constants.major_linewidth
fontsizelabel = constants.fontsizelabel
fontsizetick = constants.fontsizetick
fontsizetext = constants.fontsizetext
colorv = constants.colorv
colorh = constants.colorh

min_value = -1
max_value = 3
ticks=[-1,0,1,2,3]
label = r'$\Delta_{[\%]}$'
cmap = constants.rs_cmap

    
def main():
    eta_list = [0,1]
    rs_list = [-1,-0.5,0,0.5,1,2,3]
    crit = 'diamag'
    crit_value = 0.25
    x_parameter = 'alpha_helena_max'
    plot_hline = True
    consid_mode_input = [1,10,40]
    exclud_mode = None


    list_legends = {}



    fig,axs = plt.subplots(sharey=True,sharex=True,figsize=(12,8))
    gs1 = GridSpec(1, 1)
    gs1.update(left=0.085, right=0.12, bottom=0.23, top=0.97)
    gs2 = GridSpec(2, 3)
    gs2.update(left=0.22, right=0.99, bottom=0.23, top=0.97, wspace=0.02)

    ax = plt.subplot(gs1[0])

    norm = mpl.colors.Normalize(vmin=min_value, vmax=max_value)
    cm = mpl.cm.ScalarMappable(norm=norm, cmap=cmap)
    cm.set_array([])
    cbar = fig.colorbar(cm, cax=ax, orientation='vertical', ticks=ticks, extend='neither')

    ax.tick_params(axis='y',which='both',direction='in',left=True,right=True,labelright=False,labelleft=True)
    ax.set_ylabel(label,fontsize=fontsizelabel)
    ax.yaxis.set_label_position('left')

    consid_modes = [[1],[10],[40]]

    ass = ['(a)','(b)','(c)']

    for icm,temp_cm in enumerate(consid_modes):
        

        for ieta,eta in enumerate(eta_list):
            ax = plt.subplot(gs2[ieta,icm])
            for rs in rs_list:
            
            
                europed_run = f'eel_eta{str(eta)}_ds{str(rs)}'

                color = constants.get_color_ds(float(rs))

                x_param = europed_analysis.get_x_parameter(europed_run, x_parameter)
                gammas, modes = europed_analysis.get_gammas(europed_run, crit)
                tab, consid_mode = europed_analysis.filter_tab_general(gammas, modes, temp_cm, exclud_mode)

                sorted_indices = np.argsort(x_param)
                x_param = x_param[sorted_indices]
                tab = tab[sorted_indices]
                

                deltas = europed_analysis.get_x_parameter(europed_run, 'delta')
                delta_sorted = deltas[sorted_indices]
                filter_delta15 = np.where(delta_sorted>=0.015)
                x_param = x_param[filter_delta15]
                tab = tab[filter_delta15] 

                temp_x = x_param
                temp_y = tab[:,0]
                nan_indices = np.isnan(temp_y)
                x_filtered = temp_x[~nan_indices]
                y_filtered = temp_y[~nan_indices]
                ax.plot(x_filtered,y_filtered,"o-",color=color,mec='k',mew=0.5)
                mode = temp_cm[0]
            ax.text(0.05, 0.95, rf'$n={mode}$', transform=ax.transAxes, fontsize=fontsizelabel, va='top', ha='left', color = constants.get_new_color_mode(mode))
            #ax.text(0.95, 0.05,ass[icm], transform=ax.transAxes, fontsize=fontsizetick, va='bottom', ha='right')

            ax.axhline(crit_value,color=colorh)
            ax.axhspan(0.85*crit_value,1.15*crit_value,color=colorh,alpha=0.2)


            x_label, y_label = global_functions.get_plot_labels_gamma_profiles(x_parameter, crit)

            if ieta == 1:
                ax.set_xlabel(x_label, fontsize = fontsizelabel)
            ax.set_ylim(bottom=0,top=0.65)
            ax.set_xlim(left=2,right=7)

            if icm==0:
                ax.set_ylabel(y_label, fontsize = fontsizelabel)

            else:
                ax.tick_params(axis='y',labelleft=False,labelright=False)
            plt.tick_params(axis='both', which='major', labelsize=fontsizetick)

    plt.savefig('/home/jwp9427/bouloulou/4_15')
    plt.close()


if __name__ == '__main__':
    main()