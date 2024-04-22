#!/usr/local/depot/Python-3.7/bin/python
# /usr/local/depot/Python-3.5.1/bin/python

from hoho import europed_analysis, global_functions, startup
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
from matplotlib.gridspec import GridSpec,GridSpecFromSubplotSpec


major_linewidth = constants.major_linewidth
fontsizelabel = constants.fontsizelabel
fontsizetick = constants.fontsizetick
fontsizetext = constants.fontsizetext
colorv = constants.colorv
colorh = constants.colorh


def main():
    etas = [0,1]
    prefix = 'eel_eta'
    middle = '_ds'
    variations = [-1,-0.5,0,0.5,1,2,3]
    crit = 'diamag'
    crit_value = 0.25
    ypar = 'te'
    ass = ['(a)','(b)','(c)']
    exclud_mode = None
    consid_mode = None

    fig,axs = plt.subplots(sharey=True,sharex=True,figsize=(12,5))
    gs1 = GridSpec(1, 1)
    gs1.update(left=0.87, right=0.89, bottom=0.21, top=0.97)
    gs2 = GridSpec(1, 2)
    gs2.update(left=0.1, right=0.85, bottom=0.21, top=0.97, wspace=0.09, hspace=0.03)


    for illl in range(1):
        ypar = 'te' if illl==0 else 'te'
        for ieta,eta in enumerate(etas):
            coloreta = constants.get_color_eta(eta)
            ax = plt.subplot(gs2[2*illl+ieta])
            z = []
            x = []
            y = []
            list_n = []
            list_ne = []

            for variation in variations:
                bool_first = True
                europed_run= prefix + str(eta) + middle + str(variation)


                print(europed_run)

                try:
                    gammas, modes = europed_analysis.get_gammas(europed_run, crit)
                    tab, consid_mode = europed_analysis.filter_tab_general(gammas, modes, consid_mode, exclud_mode)
                    tab_ne,tab_Te = europed_analysis.get_nT(europed_run)
                    relativeshifts = europed_analysis.get_relativeshift(europed_run)
                    print('\n\n\n')
                    print(relativeshifts)
                    print('\n\n\n')

                    for profile in range(len(tab[:,0])):
                        try:
                            argmax = np.nanargmax(tab[profile])
                            gamma = tab[profile, argmax]
                            ne = tab_ne[profile]
                            rshift = round(relativeshifts[profile]*100,3)
                            Te = tab_Te[profile]

                            list_n.append(modes[argmax])
                            z.append(gamma)
                            x.append(float(rshift))
                            y.append(Te)
                            list_ne.append(ne)

                        except ValueError:
                            print("ca marche pas du tout")

                except FileNotFoundError:
                    print(f"{europed_run:>40} FILE NOT FOUND")

            x = np.array(x)
            y = np.array(y)
            z = np.array(z)

            valid_indices = ~np.isnan(x) & ~np.isnan(y) & ~np.isnan(z)
            x = np.array(x)[valid_indices]
            y = np.array(y)[valid_indices]
            z = np.array(z)[valid_indices]
            list_ne = np.array(list_ne)[valid_indices]
            list_n = np.array(list_n)[valid_indices]


            x = np.array(x)

            unique_x = list(set(x))
            unique_x = sorted(unique_x)

            new_z = {}
            new_list_ne = []

            for (x1,y1,n,z1) in zip(x,y,list_n,z):
                if (x1,y1) not in new_z.keys():
                    new_z[(x1,y1)] = (z1,n)
                    new_list_ne.append(ne)
                else:

                    new_z[(x1,y1)] = (z1,n) if z1>new_z[(x1,y1)][0] else new_z[(x1,y1)]
            
            x = np.array([key[0] for key in new_z.keys()])
            y = np.array([key[1] for key in new_z.keys()])
            z = np.array([value[0] for value in new_z.values()])
            list_n = np.array([value[1] for value in new_z.values()])

            new_list_ne = np.array(new_list_ne)
            pressure = 1.6*new_list_ne*y

            ne_smooth = np.linspace(min(new_list_ne),max(new_list_ne),1000)
            x_smooth = np.linspace(min(x),max(x),1000)
            y_te_smooth = np.linspace(np.nanmin(y),np.nanmax(y),1000)
            
            
            X_smooth, Y_te_smooth = np.meshgrid(x_smooth, y_te_smooth)
            Ne_smooth,Y_te_smooth = np.meshgrid(ne_smooth, y_te_smooth)

            Y_pe_smooth = 1.6*Ne_smooth*Y_te_smooth

            if ypar == 'te':
                ylabel, gammalabel = global_functions.get_plot_labels_gamma_profiles('teped',crit)

                triang = tri.Triangulation(x,y)

                # Filter out triangles connecting x=-1 and x=1
                triangles_to_keep = []
                for triangle in triang.triangles:
                    x_values = x[triangle]
                    distances = np.array([np.abs(unique_x.index(x)-unique_x.index(y)) for x in x_values for y in x_values])
                    if np.all(distances <= 1):
                        triangles_to_keep.append(triangle)
                    else:
                        print(f'FILTERED TRIANGLE: {triangle} OF X VALUES {x_values}')

                # Create a new Triangulation object with filtered triangles
                filtered_triang = tri.Triangulation(x, y, triangles=np.array(triangles_to_keep))
                #ax.contour(X_smooth, Y_te_smooth, Y_pe_smooth, levels=[1,2,3],colors='k', linewidths = 1)

            elif ypar == 'pe':
                ylabel, gammalabel = global_functions.get_plot_labels_gamma_profiles('peped',crit)
                triang = tri.Triangulation(x,pressure)

                # Filter out triangles connecting x=-1 and x=1
                triangles_to_keep = []
                for triangle in triang.triangles:
                    x_values = x[triangle]
                    distances = np.array([np.abs(unique_x.index(x)-unique_x.index(y)) for x in x_values for y in x_values])
                    if np.all(distances <= 1):
                        triangles_to_keep.append(triangle)
                    else:
                        print(f'FILTERED TRIANGLE: {triangle} OF X VALUES {x_values}')

                # Create a new Triangulation object with filtered triangles
                filtered_triang = tri.Triangulation(x, pressure, triangles=np.array(triangles_to_keep))
                #ax.contour(X_smooth, Y_pe_smooth, Y_te_smooth, levels=[0.3,0.5,0.7],colors='k', linewidths = 1)        

            z = [min(zi,1) for zi in z]

            norm = mpl.colors.Normalize(vmin=0, vmax=1)
            contour = ax.tricontourf(filtered_triang, z, levels=20, cmap='inferno_r',norm=norm)

            cs = ax.tricontour(filtered_triang, z, levels=[crit_value],colors=colorh)

            ax.tricontourf(filtered_triang, z, levels=np.linspace(0.85*crit_value,1.15*crit_value, 2), colors=colorh,alpha=0.2)

            # ax.tricontour(filtered_triang, z, levels=[0.85*crit_value],colors=colorh, linestyles='dashed')
            # ax.tricontour(filtered_triang, z, levels=[1.15*crit_value],colors=colorh, linestyles='dashed')
            for i,(xi,yi) in enumerate(zip(x,y)):
                zi = z[i]
                if xi>=-1 and yi>0.2 and zi>= 0.85*crit_value and zi <= 1.15 * crit_value:
                    if xi == 3:
                        ha = 'right'
                    elif xi == -1:
                        ha='left'
                    else:
                        ha='center'
                
                    ax.text(xi,yi,str(list_n[i]),transform=ax.transData, va='center', ha=ha,color='w')
            ax.text(0.95, 0.05, ass[ieta], transform=ax.transAxes, fontsize=fontsizetick, va='bottom', ha='right', color = 'k')

            

            if illl==0:
                ax.set_ylim(bottom=0.15,top=0.65)
                # text = 'NO ' if eta == 0 else 'Resistive'
                # ax.text(0.05, 0.95, text, fontfamily='serif', transform=ax.transAxes, fontsize=fontsizetext, va='top', ha='left', color = 'w')
                ax.set_xlabel(r'$\Delta_{[\%]}$',fontsize=fontsizelabel)

            else:
                ax.set_ylim(bottom=0.5,top=2.2)
                ax.set_xlabel(r'$\Delta_{[\%]}$',fontsize=fontsizelabel)
    
    
    
            if (2*illl+ieta)%2==0:
                ax.set_ylabel(ylabel, fontsize=fontsizelabel)
            else:
                ax.tick_params(axis='y',labelleft=False,labelright=False)

    plt.tick_params(axis='both', which='major', labelsize=fontsizetick)
    ax = plt.subplot(gs1[0])
    plt.colorbar(contour, cax=ax,ticks=[0,0.25,0.5,0.75,1]).set_label(label=gammalabel,size=fontsizelabel)
    plt.savefig('/home/jwp9427/bouloulou/4_17')
    plt.close()

if __name__ == '__main__':
    main()