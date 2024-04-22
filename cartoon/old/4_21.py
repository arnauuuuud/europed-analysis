#!/usr/local/depot/Python-3.7/bin/python
# /usr/local/depot/Python-3.5.1/bin/python

from hoho import europed_analysis, global_functions, startup, read_helena_files, find_pedestal_values
import argparse
import matplotlib.pyplot as plt
import matplotlib.transforms as transforms
import math
import numpy as np
from hoho import find_pedestal_values
import matplotlib.tri as tri
from scipy.spatial import Delaunay
from paper import constants
import matplotlib as mpl
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib.gridspec import GridSpec,GridSpecFromSubplotSpec



major_linewidth = constants.major_linewidth
fontsizelabel = constants.fontsizelabel
fontsizetick = constants.fontsizetick
fontsizetext = constants.fontsizetext
colorv = constants.colorv
colorh = constants.colorh

color_ideal = 'c'
color_resis = 'm'

pos = 0.98


def main():
    etas = [0,1]
    #variations = [1.04, 1.29, 1.55, '1.80', 2.06, 2.31, 2.57, 2.83, 3.35, 3.86, 5.14]
    variations = [1.04, 1.29, '1.80', 2.06, 2.31, 2.57, 2.83, 3.35, 3.86, 5.14]
    crit = 'diamag'
    crit_value = 0.25
    
    exclud_mode = None
    consid_mode = None

    colors_eta = ['c','m']

    fig,axs = plt.subplots(sharey=True,sharex=True,figsize=(12,5))
    gs1 = GridSpec(1, 1)
    gs1.update(left=0.87, right=0.89, bottom=0.21, top=0.97)
    gs2 = GridSpec(1, 2)
    gs2.update(left=0.1, right=0.85, bottom=0.21, top=0.97, wspace=0.03, hspace=0.03)

    plt.subplots_adjust(wspace=0, hspace=0)

    for ieta,eta in enumerate(etas):
        color = colors_eta[ieta]
        prefix = 'kudu_' if eta==0 else 'kyky_'
        z = []
        x = []
        y = []
        list_ne = []
        list_n = []
        list_t = []
        

        for variation in variations:
            bool_first = True
            europed_run= prefix + str(variation)


            print(europed_run)

            try:
                gammas, modes = europed_analysis.get_gammas(europed_run, crit)
                tab, consid_mode = europed_analysis.filter_tab_general(gammas, modes, consid_mode, exclud_mode)
                tab_ne,tab_Te = europed_analysis.get_nT(europed_run)

                for profile in range(len(tab[:,0])):
                    try:
                        argmax = np.nanargmax(tab[profile])
                        gamma = tab[profile, argmax]
                        ne = tab_ne[profile]
                        dshift = float(variation)
                        Te = tab_Te[profile]

                        list_n.append(modes[argmax])
                        z.append(gamma)
                        x.append(ne)
                        y.append(Te)
                        
                        try:
                            #list_t.append(read_helena_files.get_eta_pos(europed_run, profile, pos))
                            t = find_pedestal_values.get_temp_pos(europed_run,profile,pos)
                            list_t.append(t)
                        except ValueError:
                            print("oulalala")
                            list_t.append(None)

                    except ValueError:
                        print("ca marche pas du tout")
                    
            except FileNotFoundError:
                print(f"{europed_run:>40} FILE NOT FOUND")
            



        x = np.array(x)
        y = np.array(y)
        z = np.array(z)
        list_t = np.array(list_t)

        valid_indices = ~np.isnan(x) & ~np.isnan(y) & ~np.isnan(z)
        x = np.array(x)[valid_indices]
        y = np.array(y)[valid_indices]
        z = np.array(z)[valid_indices]
        list_t = np.array(list_t)[valid_indices]
        list_n = np.array(list_n)[valid_indices]

        unique_x = list(set(x))
        unique_x = sorted(unique_x)

        new_z = {}
        new_list_ne = []

        # for (x1,y1,z1) in zip(x,y,z):
        #     if (x1,y1) not in new_z.keys():
        #         new_z[(x1,y1)] = z1
        #     else:
        #         new_z[(x1,y1)] = max(z1,new_z[(x1,y1)])
        
        # x = np.array([key[0] for key in new_z.keys()])
        # y = np.array([key[1] for key in new_z.keys()])
        # z = np.array([value for value in new_z.values()])


        for (x1,y1,z1,t,n) in zip(x,y,z,list_t,list_n):
            if (x1,y1) not in new_z.keys():
                new_z[(x1,y1)] = (z1,t,n)
            else:
                new_z[(x1,y1)] = (z1,t,n) if z1 > new_z[(x1,y1)][0] else new_z[(x1,y1)]
        
        x = np.array([key[0] for key in new_z.keys()])
        y = np.array([key[1] for key in new_z.keys()])
        z = np.array([value[0] for value in new_z.values()])
        list_t = np.array([value[1] for value in new_z.values()])
        list_n = np.array([value[2] for value in new_z.values()])
        pressure = 1.6*x*y
        list_eta_values = list_t**(-3/2)


        # ypar = 'te'
        # ax = axs[0]
        # ylabel, gammalabel = global_functions.get_plot_labels_gamma_profiles('teped',crit)

        # triang = tri.Triangulation(x,y)

        # # Filter out triangles connecting x=-1 and x=1
        # triangles_to_keep = []
        # for triangle in triang.triangles:
        #     x_values = x[triangle]
        #     distances = np.array([np.abs(unique_x.index(x)-unique_x.index(y)) for x in x_values for y in x_values])
        #     if np.all(distances <= 1):
        #         triangles_to_keep.append(triangle)
        #     else:
        #         pass
        #         #print(f'FILTERED TRIANGLE: {triangle} OF X VALUES {x_values}')

        # # Create a new Triangulation object with filtered triangles
        # filtered_triang = tri.Triangulation(x, y, triangles=np.array(triangles_to_keep))
        
        # z = [min(zi,1) for zi in z]
        # cs = ax.tricontour(filtered_triang, z, levels=[crit_value],colors=color)
        # ax.tricontourf(filtered_triang, z, levels=np.linspace(0.85*crit_value,1.15*crit_value, 2), colors=color,alpha=0.2)

        # #ax.set_xlabel(r'${n_e^{\mathrm{ped}}}_{[10^{19} \mathrm{m}^{-3}]}$',fontsize=fontsizelabel)
        # # ax.tick_params(axis='x',labelbottom=False,labeltop=False)
        # ax.set_ylabel(ylabel, fontsize=fontsizelabel)
        # ax.set_ylim(bottom=0,top=0.75)

        # ax.text(1.2, 0.4, 'Resistive', rotation=-90, fontfamily='serif',transform=ax.transData, fontsize=fontsizelabel, va='center', ha='center', color= color_resis)
        # #ax.text(2.5, 0.35, 'Resistive unstable', rotation=-40, fontfamily='serif',transform=ax.transData, fontsize=fontsizelabel, va='center', ha='center', color= 'k')
        # ax.text(3.2, 0.5, 'Ideal', fontfamily='serif',transform=ax.transData, fontsize=fontsizelabel, va='center', ha='center', color= color_ideal)
        # #ax.text(0.95, 0.95, '(a)', transform=ax.transAxes, fontsize=fontsizetick, va='top', ha='right', color= 'k')
        # ax.set_xlabel(r'${n_e^{\mathrm{ped}}}_{[10^{19} \mathrm{m}^{-3}]}$',fontsize=fontsizelabel)



        # ypar = 'pe'
        # ax = plt.subplot(gs2[0])
        # ylabel, gammalabel = global_functions.get_plot_labels_gamma_profiles('peped',crit)
        # triang = tri.Triangulation(x,pressure)

        # # Filter out triangles connecting x=-1 and x=1
        # triangles_to_keep = []
        # for triangle in triang.triangles:
        #     x_values = x[triangle]
        #     distances = np.array([np.abs(unique_x.index(x)-unique_x.index(y)) for x in x_values for y in x_values])
        #     if np.all(distances <= 1):
        #         triangles_to_keep.append(triangle)
        #     else:
        #         pass
        #         #print(f'FILTERED TRIANGLE: {triangle} OF X VALUES {x_values}')

        # # Create a new Triangulation object with filtered triangles
        # filtered_triang = tri.Triangulation(x, pressure, triangles=np.array(triangles_to_keep))  

        # z = [min(zi,1) for zi in z]
        # cs = ax.tricontour(filtered_triang, z, levels=[crit_value],colors=color)
        # ax.tricontourf(filtered_triang, z, levels=np.linspace(0.85*crit_value,1.15*crit_value, 2), colors=color,alpha=0.2)

        # #ax.set_xlabel(r'${n_e^{\mathrm{ped}}}_{[10^{19} \mathrm{m}^{-3}]}$',fontsize=fontsizelabel)
        # # ax.tick_params(axis='x',labelbottom=False,labeltop=False)
        # ax.set_ylabel(ylabel, fontsize=fontsizelabel)
        # ax.set_ylim(bottom=0,top=2)

        # # ylim_min = 0
        # # ylim_max = 2
        # # temp_y = y if ypar == 'te' else pressure
        # # for i,(xi,yi) in enumerate(zip(x,temp_y)):
        # #     if xi>4:
        # #         ha = 'right'
        # #     elif xi<1:
        # #         ha = 'left'
        # #     else:
        # #         ha = 'center'
        # #     #ha = 'right' if xi > 4 else 'center'
        # #     zi = z[i]
        # #     if yi>ylim_min and yi<ylim_max and zi>= 0.85*crit_value and zi <= 1.15 * crit_value:
        # #         ax.text(xi,yi,str(list_n[i]),transform=ax.transData, va='center', ha=ha, color='k')

        # #ax.text(0.95, 0.95, '(b)', transform=ax.transAxes, fontsize=fontsizetick, va='top', ha='right', color= 'k')
        # ax.set_xlabel(r'${n_e^{\mathrm{ped}}}_{[10^{19} \mathrm{m}^{-3}]}$',fontsize=fontsizelabel)

        

        ypar = 'pe'
        ax = plt.subplot(gs2[1])
        ylabel = r'${\left<\eta\right>_{0.98 \leq \psi_N \leq 1}}$ $_{[\mathrm{a.u.}]}$'
        triang = tri.Triangulation(x,list_eta_values)

        # Filter out triangles connecting x=-1 and x=1
        triangles_to_keep = []
        for triangle in triang.triangles:
            x_values = x[triangle]
            distances = np.array([np.abs(unique_x.index(x)-unique_x.index(y)) for x in x_values for y in x_values])
            if np.all(distances <= 1):
                triangles_to_keep.append(triangle)
            else:
                pass
                #print(f'FILTERED TRIANGLE: {triangle} OF X VALUES {x_values}')

        # Create a new Triangulation object with filtered triangles
        filtered_triang = tri.Triangulation(x, list_eta_values, triangles=np.array(triangles_to_keep))  

        z = [min(zi,1) for zi in z]
        cs = ax.tricontour(triang, z, levels=[crit_value],colors=color)
        ax.tricontourf(triang, z, levels=np.linspace(0.85*crit_value,1.15*crit_value, 2), colors=color,alpha=0.2)
        temp_y = y if ypar == 'te' else pressure
        
        ax.set_xlabel(r'${n_e^{\mathrm{ped}}}_{[10^{19} \mathrm{m}^{-3}]}$',fontsize=fontsizelabel)
        ax.set_ylabel(ylabel, fontsize=fontsizelabel)
        ax.set_ylim(bottom=0,top=18)
        # ax.text(0.95, 0.95, '(c)', transform=ax.transAxes, fontsize=fontsizetick, va='top', ha='right', color= 'k')


    
    plt.tick_params(axis='both', which='major', labelsize=fontsizetick)
    plt.savefig(f'/home/jwp9427/bouloulou/4_21')
    plt.close()

if __name__ == '__main__':
    main()