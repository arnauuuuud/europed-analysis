#!/usr/local/depot/Python-3.7/bin/python
# /usr/local/depot/Python-3.5.1/bin/python

from hoho import useful_recurring_functions,useful_recurring_functions,europed_analysis, global_functions, startup, read_helena_files, find_pedestal_values
import argparse
import matplotlib.pyplot as plt
import matplotlib.transforms as transforms
import math
import numpy as np
from hoho import find_pedestal_values
import matplotlib.tri as tri
from scipy.spatial import Delaunay
from thesis import constants
from scipy.interpolate import interp1d
import matplotlib as mpl
from mpl_toolkits.axes_grid1 import make_axes_locatable



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
    prefix = 'eel_eta'
    middle = '_ds'
    variations = [-1,-0.5,0,0.5,1,2,3]
    crit = 'diamag'
    crit_value = 0.25
    ypar = 'pe'
    exclud_mode = None
    consid_mode = None
    
    exclud_mode = None
    consid_mode = None

    colors_eta = [color_ideal,color_resis]

    fig, axs = plt.subplots(1,1,figsize=(6,5),sharex=True)
    # fig, axs = plt.subplots(1,2,figsize=(10,6),sharex=True)
    plt.subplots_adjust(wspace=0, hspace=0)

    for ieta,eta in enumerate(etas):
        color = colors_eta[ieta]
        z = []
        x = []
        y = []
        list_ne = []
        list_t = []
        

        for variation in variations:

            if eta == 1 and variation == 0:
                prefix = 'lololo_eta'
            else:
                prefix='eel_eta'

            bool_first = True
            europed_run= prefix + str(eta) + middle + str(variation)


            print(europed_run)

            try:
                gammas, modes = europed_analysis.get_gammas(europed_run, crit)
                tab, consid_mode = europed_analysis.filter_tab_general(gammas, modes, consid_mode, exclud_mode)
                tab_ne,tab_Te = europed_analysis.get_nT(europed_run)

                # deltas = europed_analysis.get_x_parameter(europed_run, 'delta')
                # filter_delta15 = np.where(deltas>=0.015)
                # tab = tab[filter_delta15] 
                # tab_ne = tab_ne[filter_delta15]
                # tab_Te = tab_Te[filter_delta15]
                # deltas = deltas[filter_delta15]

                print(len(tab[:,0]))
                for profile in range(len(tab[:,0])):
                    try:
                        

                        argmax = np.nanargmax(tab[profile])
                        gamma = tab[profile, argmax]
                        ne = tab_ne[profile]
                        dshift = float(variation)
                        Te = tab_Te[profile]

                        z.append(gamma)
                        x.append(dshift)
                        y.append(Te*ne*1.6)
                        list_ne.append(ne)

                        try:
                            #list_t.append(read_helena_files.get_eta_pos(europed_run, profile, pos))
                            #new_profile = read_helena_files.get_adapted_rs_number(europed_run,profile)
                            t = find_pedestal_values.get_temp_pos(europed_run,profile,pos)
                            list_t.append(t)
                        except ValueError:
                            print("oulalala")
                            list_t.append(None)
                        # except KeyError:
                        #     print("nononon")
                            #list_t.append(None)

                    except ValueError:
                        print("ca marche pas du tout")
                    
            except FileNotFoundError:
                print(f"{europed_run:>40} FILE NOT FOUND")
            



        x = np.array(x)
        y = np.array(y)
        z = np.array(z)
        list_ne = np.array(list_ne)
        list_t = np.array(list_t)

        valid_indices = ~np.isnan(x) & ~np.isnan(y) & ~np.isnan(z)
        x = np.array(x)[valid_indices]
        y = np.array(y)[valid_indices]
        z = np.array(z)[valid_indices]
        list_ne = np.array(list_ne)[valid_indices]
        list_t = np.array(list_t)[valid_indices]

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


        for (x1,y1,z1,t,ne) in zip(x,y,z,list_t,list_ne):
            if (x1,y1) not in new_z.keys():
                new_z[(x1,y1)] = (z1,t)
                new_list_ne.append(ne)
            else:
                new_z[(x1,y1)] = (z1,t) if z1 > new_z[(x1,y1)][0] else new_z[(x1,y1)]
        
        new_list_ne = np.array(new_list_ne)
        x = np.array([key[0] for key in new_z.keys()])
        y = np.array([key[1] for key in new_z.keys()])
        z = np.array([value[0] for value in new_z.values()])
        list_t = np.array([value[1] for value in new_z.values()])
        pressure = 1.6*new_list_ne*y
        list_eta_values = list_t**(-3/2)


        ypar = 'pe'
        ax = axs
        ylabel, gammalabel = global_functions.get_plot_labels_gamma_profiles('peped',crit)

        triang = tri.Triangulation(x,y)

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
        filtered_triang = tri.Triangulation(x, y, triangles=np.array(triangles_to_keep))
        
        z = [min(zi,1) for zi in z]
        cs = ax.tricontour(filtered_triang, z, levels=[crit_value],colors=color)
        ax.tricontourf(filtered_triang, z, levels=np.linspace(0.85*crit_value,1.15*crit_value, 2), colors=color,alpha=0.2)

        ax.set_xlabel(r'$\Delta_{[\%]}$',fontsize=fontsizelabel)
        ax.set_ylabel(ylabel, fontsize=fontsizelabel)
        ax.set_ylim(bottom=0,top=2.2)
        #ax.text(0.05, 0.95, '(a)', transform=ax.transAxes, fontsize=fontsizetick, va='top', ha='left', color= 'k')
        
        # ax.text(0.95, 0.95, 'Ideal', fontfamily='serif',transform=ax.transAxes, fontsize=fontsizetick, va='top', ha='right', color= color_ideal)
        # ax.text(0.01, 0.25, 'Resistive', fontfamily='serif',transform=ax.transAxes, fontsize=fontsizetick, va='center', ha='left', color= color_resis)

        # ypar = 'pe'
        # ax2 = ax.twinx()
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
        # cs = ax2.tricontour(filtered_triang, z, levels=[crit_value],colors=color,linestyles=':')
        # # ax2.tricontourf(filtered_triang, z, levels=np.linspace(0.85*crit_value,1.15*crit_value, 2), colors=color,alpha=0.2)

        # ax2.set_xlabel(r'$\Delta_{[\%]}$',fontsize=fontsizelabel)
        # ax2.set_ylabel(ylabel, fontsize=fontsizelabel)

        # interpolator = interp1d(y,pressure)
        # pe_max = interpolator(0.6)
        # ax2.set_ylim(bottom=0,top=pe_max)
        # #ax2.text(0.05, 0.95, '(a)', transform=ax2.transax2es, fontsize=fontsizetick, va='top', ha='left', color= 'k')
        
        # # ax2.text(0.95, 0.95, 'Ideal', fontfamily='serif',transform=ax2.transAxes, fontsize=fontsizetick, va='top', ha='right', color= color_ideal)
        # # ax2.text(0.05, 0.2, 'Resistive', fontfamily='serif',transform=ax2.transAxes, fontsize=fontsizetick, va='center', ha='left', color= color_resis)


        # # ax = axs[1]
        # # ylabel = r'${\left<\eta\right>^{0.98 \leq \psi_N \leq 1}}_{[\mathrm{a.u.}]}$'
        # # triang = tri.Triangulation(x,list_eta_values)

        # # # Filter out triangles connecting x=-1 and x=1
        # # triangles_to_keep = []
        # # for triangle in triang.triangles:
        # #     x_values = x[triangle]
        # #     distances = np.array([np.abs(unique_x.index(x)-unique_x.index(y)) for x in x_values for y in x_values])
        # #     if np.all(distances <= 1):
        # #         triangles_to_keep.append(triangle)
        # #     else:
        # #         pass
        # #         #print(f'FILTERED TRIANGLE: {triangle} OF X VALUES {x_values}')

        # # # Create a new Triangulation object with filtered triangles
        # # filtered_triang = tri.Triangulation(x, list_eta_values, triangles=np.array(triangles_to_keep))  

        # # z = [min(zi,1) for zi in z]
        # # cs = ax.tricontour(triang, z, levels=[crit_value],colors=color)
        # # ax.tricontourf(triang, z, levels=np.linspace(0.85*crit_value,1.15*crit_value, 2), colors=color,alpha=0.2)

        # # ax.set_xlabel(r'$\Delta_{[\%]}$',fontsize=fontsizelabel)
        # # ax.set_ylabel(ylabel, fontsize=fontsizelabel)
        # # ax.set_ylim(bottom=0,top=20)
        # # ax.text(0.95, 0.95, '(b)', transform=ax.transAxes, fontsize=fontsizetick, va='top', ha='right', color= 'k')


    
    plt.tick_params(axis='both', which='major', labelsize=fontsizetick)
    plt.savefig(f'/home/jwp9427/bouloulou/4_20')
    plt.close()

if __name__ == '__main__':
    main()