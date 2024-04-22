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
import matplotlib.transforms as transforms


major_linewidth = constants.major_linewidth
fontsizelabel = constants.fontsizelabel
fontsizetick = constants.fontsizetick
fontsizetext = constants.fontsizetext
colorv = constants.colorv
colorh = constants.colorh

main_delta = 0.034


min_value = 0
max_value = 1
label = r'$\eta / \eta_{\mathrm{Sp}}$'
cmap = constants.eta_cmap
ticks = [0.2,0.4,0.6,0.8]

    
def main():
    ds_list = [0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1]
    europed_runs = [f'eagle_eta{str(ds)}_ds0' for ds in ds_list]
    crit = 'diamag'
    crit_value = 0.25
    x_parameter = 'alpha_helena_max'
    plot_hline = True
    consid_mode_input_global = ['3','30']
    exclud_mode = None


    list_legends = {}

    fig = plt.figure(figsize=(12, 4))
    gs1 = GridSpec(1, 1)
    gs1.update(left=0.085, right=0.12, bottom=0.23, top=0.99)
    gs2 = GridSpec(1, 2)
    gs2.update(left=0.22, right=0.67, bottom=0.23, top=0.99, wspace=0.02)

    ax = plt.subplot(gs1[0])

    # fig,axs = plt.subplots(3,1,figsize=(4,8), gridspec_kw={'height_ratios': [1, 3, 3]})
    # #plt.subplots_adjust(wspace=0, hspace=0)

    # ax = axs[0]
    norm = mpl.colors.Normalize(vmin=min_value, vmax=max_value)
    cm = mpl.cm.ScalarMappable(norm=norm, cmap=cmap)
    cm.set_array([])

    # ax.set_ylabel(label,fontsize=fontsizelabel)
    # ax.yaxis.set_label_position("right")
    cbar = fig.colorbar(cm, cax=ax, ticks=ticks, orientation='vertical', extend='neither')
    #ax.text(0.5, -0.01, r'$n_e^{\mathrm{ped}} {10^{19}m^{-3}}$', ha='center', va='top', fontsize=fontsizetick, transform=ax.transAxes)   
    ax.tick_params(axis='y',which='both',direction='in',left=True,right=True,labelright=False,labelleft=True)
    ax.set_ylabel(label,fontsize=fontsizelabel)
    ax.yaxis.set_label_position('left')

    for icm, cm in enumerate(consid_mode_input_global):
        consid_mode_input = [cm]
        ax = plt.subplot(gs2[icm])
        
        for iplot,europed_run in enumerate(europed_runs):
            ds = ds_list[iplot]
            color = constants.get_color_eta(float(ds))

            x_param = europed_analysis.get_x_parameter(europed_run, x_parameter)
            gammas, modes = europed_analysis.get_gammas(europed_run, crit)
            tab, consid_mode = europed_analysis.filter_tab_general(gammas, modes, consid_mode_input, exclud_mode)

            sorted_indices = np.argsort(x_param)
            x_param = x_param[sorted_indices]
            tab = tab[sorted_indices]

            deltas = europed_analysis.get_x_parameter(europed_run, 'delta')
            deltas = deltas[sorted_indices]        

            for i, mode in enumerate(consid_mode):
                temp_x = x_param
                temp_y = tab[:,i]
                nan_indices = np.isnan(temp_y)
                x_filtered = temp_x[~nan_indices]
                y_filtered = temp_y[~nan_indices]
                delta_filtered = deltas[~nan_indices]
                
                overcrit = np.where(x_filtered>4.5)
                x_filtered = x_filtered[overcrit]
                y_filtered = y_filtered[overcrit]
                delta_filtered = delta_filtered[overcrit]

                ax.plot(x_filtered,y_filtered,"o-",color=color,mec='k',mew=0.5)


            # try:
            #     x_index1 = np.where(np.around(delta_filtered,5) == main_delta)[0]
            #     main_x = x_filtered[x_index1]
            #     trans = transforms.blended_transform_factory(ax.transData, ax.transAxes)
            #     ax.arrow(main_x,0,0,0.08, length_includes_head=True, width=0.01,head_width=0.1, head_length=0.03, color=constants.arrow_color, transform=trans)
            #     ax.arrow(main_x,1,0,-0.08, length_includes_head=True, width=0.01,head_width=0.1, head_length=0.03, color=constants.arrow_color,transform=trans)
            # except ValueError:
            #     pass   

        # if icm == 0:
        #     ax.text(0.95, 0.95,'(a)', transform=ax.transAxes, fontsize=fontsizetick, va='top', ha='right', color = 'black')
        # else:
        #     ax.text(0.95, 0.95,'(b)', transform=ax.transAxes, fontsize=fontsizetick, va='top', ha='right', color = 'black')

        ax.axhline(crit_value,color=colorh)
        ax.text(0.05, 0.95, rf'$n={cm}$', transform=ax.transAxes, fontsize=fontsizelabel, va='top', ha='left', color = constants.get_new_color_mode(int(cm)))


        x_label, y_label = global_functions.get_plot_labels_gamma_profiles(x_parameter, crit)

        ax.set_ylim(bottom=0,top=0.8)
        
        ax.set_xlim(left=4,right=7.2)
        ax.axhspan(crit_value*0.85,crit_value*1.15,color=colorh,alpha=0.3)
        
        ax.set_xlabel(x_label, fontsize=fontsizelabel)

        if icm == 0:
            ax.set_ylabel(y_label, fontsize = fontsizelabel)
            ax.set_yticks([0,0.3,0.6])
        
        
    ax.tick_params(axis='y',labelleft=False,labelright=False)
    #ax.text(0.5, -0.05, x_label, ha='center', va='top', fontsize=fontsizelabel, transform=ax.transAxes)   

    #ax.set_xlabel(x_label, fontsize = fontsizelabel)
    #plt.tick_params(axis='both', which='major', labelsize=fontsizetick)



    eta_list = [0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1]
    europed_runs = [f'eagle_eta{str(ds)}_ds0' for ds in ds_list]

    crit = 'diamag'
    crit_value = 0.25
    x_parameter = 'delta'
    plot_hline = True
    exclud_mode = None
    consid_mode_input_global = ['3','5','7','20','30','40']
    list_emptys = [[],[],[],[],[],[],[],[],[],[],[]]
    dict_results = dict(zip(consid_mode_input_global, list_emptys))
    exclud_mode = None

            
    # ax.text(0.95, 0.95,'(c)', transform=ax.transAxes, fontsize=fontsizetick, va='top', ha='right', color = 'black')
    # ax.set_yticks([0,0.4,0.8,1.2])
    # ax.set_xticks([])

    #plt.show()
    plt.savefig('/home/jwp9427/bouloulou/4_8')
    plt.close()
  
if __name__ == '__main__':
    main()