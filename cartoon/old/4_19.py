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

ylim_min_te,ylim_max_te = 0.15,0.65
ylim_min_pe,ylim_max_pe = 0.5,2.2

color_ideal = 'c'
color_resis = 'm'


def main():
    etas = [0,1]
    #variations = [1.04, 1.29, 1.55, '1.80', 2.06, 2.31, 2.57, 2.83, 3.35, 3.86, 5.14]
    variations = [1.04, 1.29, '1.80', 2.06, 2.31, 2.57, 2.83, 3.35, 3.86, 5.14]
    crit = 'diamag'
    crit_value = 0.25
    ypar = 'pe'
    exclud_mode = None
    consid_mode = None
    ass = ['(a)','(b)','(c)']

    fig,axs = plt.subplots(sharey=True,sharex=True,figsize=(12,5))
    gs1 = GridSpec(1, 1)
    gs1.update(left=0.87, right=0.89, bottom=0.21, top=0.97)
    gs2 = GridSpec(1, 2)
    gs2.update(left=0.1, right=0.85, bottom=0.21, top=0.97, wspace=0.03, hspace=0.03)

    plt.subplots_adjust(wspace=0, hspace=0)

    for iplot in range(1):
        ypar = 'pe' if iplot==0 else 'te'

        for ieta,eta in enumerate(etas):
            coloreta = constants.get_color_eta(eta)
            prefix = 'kudu_' if eta==0 else 'kyky_'
            ax = plt.subplot(gs2[iplot,ieta])
            z = []
            x = []
            y = []
            list_n = []
            list_ne = []
            dict_znne = {}

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

                            tab_ne = np.array(tab_ne)
                            ne = tab_ne[profile]
                            dshift = float(variation)
                            Te = tab_Te[profile]

                            list_n.append(modes[argmax])
                            z.append(gamma)
                            x.append(float(ne))
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
            list_n = np.array(list_n)[valid_indices]
            list_ne = np.array(list_ne)[valid_indices]

            x = np.array(x)

            unique_x = list(set(x))
            unique_x = sorted(unique_x)

            new_z = {}
            new_list_ne = []

            for (x1,y1,n,z1) in zip(x,y,list_n,z):
                if (x1,y1) not in new_z.keys():
                    new_z[(x1,y1)] = (z1,n)
                else:
                    new_z[(x1,y1)] = (z1,n) if z1>new_z[(x1,y1)][0] else new_z[(x1,y1)]
            
            x = np.array([key[0] for key in new_z.keys()])
            y = np.array([key[1] for key in new_z.keys()])
            z = np.array([value[0] for value in new_z.values()])
            list_n = np.array([value[1] for value in new_z.values()])
            pressure = 1.6*x*y

            new_list_ne = np.array(x)
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
                ax.contour(X_smooth, Y_te_smooth, Y_pe_smooth, levels=[1,2,3],colors='w', linewidths = 1)
                ylim_min,ylim_max = ylim_min_te+0.02,ylim_max_te

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
                # ax.contour(X_smooth, Y_pe_smooth, Y_te_smooth, levels=[0.1,0.3,0.5,0.7],colors='w', linewidths = 1)        
                ylim_min,ylim_max = ylim_min_pe+0.05,ylim_max_pe        

            z = [min(zi,1) for zi in z]

            norm = mpl.colors.Normalize(vmin=0, vmax=1)
            contour = ax.tricontourf(filtered_triang, z, levels=20, cmap='inferno_r',norm=norm)

            cs = ax.tricontour(filtered_triang, z, levels=[crit_value],colors=colorh)
            # color = color_ideal if ieta == 0 else color_resis
            # cs = ax.tricontour(filtered_triang, z, levels=[crit_value],colors=color)

            ax.tricontourf(filtered_triang, z, levels=np.linspace(0.85*crit_value,1.15*crit_value, 2), colors=colorh,alpha=0.2)
            # ax.tricontourf(filtered_triang, z, levels=np.linspace(0.85*crit_value,1.15*crit_value, 2), colors=color,alpha=0.2)

            temp_y = y if ypar == 'te' else pressure
            for i,(xi,yi) in enumerate(zip(x,temp_y)):
                if xi>4:
                    ha = 'right'
                elif xi<1:
                    ha = 'left'
                else:
                    ha = 'center'
                #ha = 'right' if xi > 4 else 'center'
                zi = z[i]
                if yi>ylim_min and yi<ylim_max and zi>= 0.85*crit_value and zi <= 1.15 * crit_value:
                    ax.text(xi,yi,str(list_n[i]),transform=ax.transData, va='center', ha=ha, color='w')

            # ax.tricontour(filtered_triang, z, levels=[0.85*crit_value],colors=colorh, linestyles='dashed')
            # ax.tricontour(filtered_triang, z, levels=[1.15*crit_value],colors=colorh, linestyles='dashed')

            #ax.set_xlim(left=1)
            #ax.text(0.05, 0.95,r'$\eta/\eta_{\mathrm{Sp}}=$'+str(eta), transform=ax.transAxes, fontsize=fontsizetext, va='top', ha='left', color = constants.get_color_eta(float(eta)),backgroundcolor='white')
            # ax.text(0.95, 0.05, ass[ieta], transform=ax.transAxes, fontsize=fontsizetick, va='bottom', ha='right', color = 'k')

            if 0==0:
                ax.set_ylim(bottom=0.15,top=0.65)
                # text = 'Ideal' 695, text, fontfamily='serif', transform=ax.transAxes, fontsize=fontsizetext, va='top', ha='right', color = 'w')
                ax.set_xlabel(r'$\Delta_{[\%]}$',fontsize=fontsizelabel)

            if iplot==1:
                # ax.tick_params(axis='x',labeltop=False,labelbottom=False)
                ax.set_ylim(bottom=ylim_min_te,top=ylim_max_te)
                ax.set_xlabel(r'${n_e^{\mathrm{ped}}}_{[10^{19} \mathrm{m}^{-3}]}$',fontsize=fontsizelabel)

                #ax.text(0.05, 0.95,r'$\eta/\eta_{\mathrm{Sp}}=$'+str(eta), transform=ax.transAxes, fontsize=fontsizetext, va='top', ha='left', color = constants.get_color_eta(float(eta)),backgroundcolor='white')
            else:
                ax.set_ylim(bottom=ylim_min_pe,top=ylim_max_pe)
                ax.set_xlabel(r'${n_e^{\mathrm{ped}}}_{[10^{19} \mathrm{m}^{-3}]}$',fontsize=fontsizelabel)
    
    
            if ieta ==0:
                ax.set_ylabel(ylabel, fontsize=fontsizelabel)
            else:
                ax.tick_params(axis='y',labelleft=False,labelright=False)
    
    plt.tick_params(axis='both', which='major', labelsize=fontsizetick)
    
    
    ax = plt.subplot(gs1[0])

    plt.colorbar(contour, cax=ax,ticks=[0,0.25,0.5,0.75,1]).set_label(label=gammalabel,size=fontsizelabel)
    #plt.show()
    plt.savefig('/home/jwp9427/bouloulou/4_19')
    plt.close()

if __name__ == '__main__':
    main()