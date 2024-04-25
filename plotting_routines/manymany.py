#!/usr/local/depot/Python-3.7/bin/python
# /usr/local/depot/Python-3.5.1/bin/python

from thesis import constants
import matplotlib.pyplot as plt
from hoho import europed_analysis, global_functions, startup, get_eigenfunction
import matplotlib.transforms as transforms
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from matplotlib.colors import Normalize
from matplotlib.colors import ListedColormap, BoundaryNorm
import math
import numpy as np
from pylib import castor
from matplotlib.gridspec import GridSpec,GridSpecFromSubplotSpec
import matplotlib.patches as patches

major_linewidth = constants.major_linewidth
fontsizelabel = constants.fontsizelabel
fontsizetick = constants.fontsizetick
fontsizetext = constants.fontsizetext
colorv = constants.colorv
colorh = constants.colorh


def main():
   
    fig = plt.figure(figsize=(10.8, 15.12))


    gs1 = GridSpec(1, 1)
    gs1.update(left=0.3, right=0.7, bottom=0.75, top=0.99)
    gs3 = GridSpec(2, 4,  width_ratios=[2,1.3,2,1.3])
    gs3.update(left=0.02, right=0.99, bottom=0.35, top=0.68, wspace=0.02, hspace = 0.04)
    gs2 = GridSpec(1, 2, width_ratios=[2,1.5])
    gs2.update(left=0.2, right=0.8, bottom=0.05, top=0.27, wspace=0.02)
    
    #gs.update(hspace=2,top=0.7,bottom=0.5)

    ax0 = plt.subplot(gs1[0])


    #gs.update(hspace=2,top=1,bottom=0) 
    ax1 = plt.subplot(gs2[0])
    ax2 = plt.subplot(gs2[1])


    europed_run = 'eagle_eta0.8_ds0'
    crit = "diamag"
    crit_value=0.25
    plot_hline = True
    plot_vline = True
    x_parameter = 'alpha_helena_max'
    consid_mode_input = [30]
    exclud_mode = None
    list_legends = {}

    colors = ['#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
    color34 = colors[0]
    color28 = colors[1]
    color22 = colors[2]
    color16 = colors[3]

    x_param = europed_analysis.get_x_parameter(europed_run, x_parameter)
    delta = europed_analysis.get_x_parameter(europed_run, 'delta')

    gammas, modes = europed_analysis.get_gammas(europed_run, crit)
    tab, consid_mode = europed_analysis.filter_tab_general(gammas, modes, consid_mode_input, exclud_mode)

    sorted_indices = np.argsort(x_param)
    x_param = x_param[sorted_indices]
    delta = delta[sorted_indices]
    tab = tab[sorted_indices]

    filter_delta15 = np.where(delta>=0.015)
    x_param = x_param[filter_delta15]
    tab = tab[filter_delta15]
    delta = delta[filter_delta15]


    consid_mode = sorted(consid_mode, key=lambda x: int(x))
    for i, mode in enumerate(consid_mode):
        color = constants.get_color_mode(int(mode))
        temp_x = x_param
        temp_y = tab[:,i]
        nan_indices = np.isnan(temp_y)
        x_filtered = temp_x[~nan_indices]
        delta_filtered = delta[~nan_indices]
        y_filtered = temp_y[~nan_indices]


        # if mode == 50:
        #     x_index = np.where(np.around(delta_filtered,3) == 0.03)[0]
        #     ax0.plot(x_filtered[x_index], y_filtered[x_index],'o',mec=color,fillstyle='none',markersize=20)

        x_index1 = np.where(np.around(delta_filtered,5) == 0.016)[0]
        ax0.plot(x_filtered[x_index1], y_filtered[x_index1],'o', fillstyle='none', markersize=20, markeredgewidth=5, mec=color16)
        x_index2 = np.where(np.around(delta_filtered,5) == 0.022)[0]
        ax0.plot(x_filtered[x_index2], y_filtered[x_index2],'o', fillstyle='none', markersize=20, markeredgewidth=5, mec=color22)
        x_index3 = np.where(np.around(delta_filtered,5) == 0.028)[0]
        ax0.plot(x_filtered[x_index3], y_filtered[x_index3],'o', fillstyle='none', markersize=20, markeredgewidth=5, mec=color28)
        x_index4 = np.where(np.around(delta_filtered,5) == 0.034)[0]
        ax0.plot(x_filtered[x_index4], y_filtered[x_index4],'o', fillstyle='none', markersize=20, markeredgewidth=5, mec=color34)
        ax0.text(0.95, 0.95, '(a)', transform=ax0.transAxes, fontsize=fontsizetick, va='top', ha='right', color= 'k')
 
        print(x_filtered[x_index1])
        print(x_filtered[x_index2])
        print(x_filtered[x_index3])
        print(x_filtered[x_index4])
        
        # elif mode == 7:
        #     x_index = np.where(np.around(delta_filtered,3) == 0.034)[0]
        #     ax.plot(x_filtered[x_index], y_filtered[x_index],'o',mec=color,fillstyle='none',markersize=20)
        list_legends[mode], = ax0.plot(x_filtered,y_filtered,"o-",label=mode, color=constants.get_new_color_mode(30), linewidth=major_linewidth, mec='k', mew=0.5)
        ax0.set_yticklabels([0.2,0.22,0.24,0.26,0.28])
            

    x_label, y_label = global_functions.get_plot_labels_gamma_profiles(x_parameter, crit)
    ax0.set_xlabel(x_label, fontsize = fontsizelabel)
    ax0.set_ylabel(y_label, fontsize = fontsizelabel)
    plt.tick_params(axis='both', which='major', labelsize=fontsizetick)
    ax0.set_ylim(bottom=0.2,top=0.3)
    ax0.set_xticks([0.016,0.022,0.028,0.034],[0.016,0.022,0.028,0.034])
    #ax0.set_xlim(left=2)


    castor_name1 = 'castor12arnaud_model_rs0_w0.034_ZA'
    castor_name2 = 'castor12arnaud_model_rs0_w0.028_ZB'
    castor_name3 = 'castor12arnaud_model_rs0_w0.022_ZE'
    castor_name4 = 'castor12arnaud_model_rs0_w0.016_ZD'

    castor_names = [castor_name1,castor_name1,castor_name3,castor_name4]

    helena_name1 = 'model_rs0_w0.034'
    helena_name2 = 'model_rs0_w0.028'
    helena_name3 = 'model_rs0_w0.022'
    helena_name4 = 'model_rs0_w0.016'

    helena_names = [helena_name1,helena_name2,helena_name3,helena_name4]

    ivar = 0
    phase=0
    levels = 30

    colors = ['#ff7f0e', '#2ca02c', '#d62728', '#9467bd']

    names = [r'$\alpha= 6.5$',r'$\alpha = 5.1$',r'$\alpha = 3.8$',r'$\alpha = 2.5$']

    first_label = ['(b)','(d)','(f)','(h)']
    second_label = ['(c)','(e)','(g)','(i)']


    for i in range(4):

        ax = plt.subplot(gs3[i//2,(i%2)*2])

        c_name = castor_names[i]
        h_name = helena_names[i]
        color = colors[i]
        name = names[i]

        x, vec = get_eigenfunction.get_eigenfunc(c_name, ivar)
        for func in vec:
            ax.plot(x,np.abs(func),'gray',linewidth=0.8)
        ax.set_ylim(bottom=0)
        ax.set_xlim(left=0.8,right=1)
        

        ax.tick_params(axis='both',labelright=False,labelleft=False,labeltop=False,labelbottom=False)
        # ax.set_yticklabels([])
        #ax.set_xticks([0.8,0.9,1],[0.8,0.9,1])
        
        # ax.set_ylabel(r'$|v_1|$',fontsize=fontsizelabel)
        if i//2 == 1:
            ax.set_xticks([0.8,0.9,1],[0.8,0.9,1])
            ax.tick_params(axis='x',labelbottom=True)
            ax.set_xlabel(r'$\psi_N$',fontsize=fontsizelabel)
        ax.text(0.05, 0.95, name, transform=ax.transAxes, fontsize=fontsizetick, va='top', ha='left', color= color)
        ax.text(0.9, 0.95, first_label[i], transform=ax.transAxes, fontsize=fontsizetick, va='top', ha='right', color= 'k')
        ax.text(1.65, 0.95, second_label[i], transform=ax.transAxes, fontsize=fontsizetick, va='top', ha='right', color= 'k')

        ax = plt.subplot(gs3[i//2,(i%2)*2+1])

        a = castor.CastorData(c_name,c_name,h_name)
        xx, yy, var = a.get_cont(ivar, 'JET', phase)
        contour = ax.contourf(xx, yy, var, levels, cmap='seismic')
        ax.set_aspect('equal')
        ax.set_axis_off()



    c_name = 'castor12arnaud_model_rs0_w0.016_ZDmieux'
    h_name = 'model_rs0_w0.016'
    color = '#9467bd'
    name = r'$1.6\%$'


    x, vec = get_eigenfunction.get_eigenfunc(c_name, ivar)
    for func in vec:
        ax1.plot(x,np.abs(func),'gray',linewidth=0.8)
    ax1.set_ylim(bottom=0)
    ax1.set_xlim(left=0.96,right=1)
    ax1.set_yticklabels([])

    ax1.set_ylabel(r'$|v_1|$',fontsize=fontsizelabel)
    ax1.set_xlabel(r'$\psi_N$',fontsize=fontsizelabel)
    ax1.text(0.05, 0.95, name, transform=ax1.transAxes, fontsize=fontsizetick, va='top', ha='left', color= color)
    ax1.text(0.95, 0.95, '(j)', transform=ax1.transAxes, fontsize=fontsizetick, va='top', ha='right', color= 'k')
    ax1.text(1.75, 0.95, '(k)', transform=ax1.transAxes, fontsize=fontsizetick, va='top', ha='right', color= 'k')
    ax1.set_xticks([0.96,0.97,0.98,0.99,1],[0.96,0.97,0.98,0.99,1])  
       
    a = castor.CastorData(c_name,c_name,h_name)
    xx, yy, var = a.get_cont(ivar, 'JET', phase)
    contour = ax2.contourf(xx, yy, var, levels, cmap='seismic')
    ax2.set_aspect('equal', 'box')
    ax2.set_axis_off()

    fig.tight_layout()

    plt.savefig('/home/jwp9427/bouloulou/4_13')
    plt.close()



if __name__ == '__main__':
    main()