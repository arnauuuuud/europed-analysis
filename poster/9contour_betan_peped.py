#!/usr/local/depot/Python-3.7/bin/python
# /usr/local/depot/Python-3.5.1/bin/python

from hoho import useful_recurring_functions, europed_analysis, global_functions, startup, find_pedestal_values_old, h5_manipulation
from poster import plot_canvas
import argparse
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.tri as tri
import matplotlib as mpl
from mpl_toolkits.axes_grid1 import Divider, Size



prefixes = ['sb_eta0.0_rs0.022_neped2.57_betap','sb_eta1.0_rs0.022_neped2.57_betap','sb_eta1.5_rs0.022_neped2.57_betap','sb_eta2.0_rs0.022_neped2.57_betap']
variations = ['0.55','0.7','0.85','1.0','1.15','000']

exclud_mode = [30,40,50]
crit = 'alfven'
crit_value = 0.05
ypar = 'te'
consid_mode = None
suffix= None

list_ne_full = []
list_frac_full = []

colors = plot_canvas.colors
linestyles = plot_canvas.linestyles

def main(prefixes, variations, suffix, crit, crit_value, ypar, exclud_mode, consid_mode_input,plot_frac):


    cm = 1/2.54
    min_plot_n = [[0.8,1.3],[0.9,1.1],[0.95,1.05],[0.95,1.05]]
    fig = plt.figure(figsize=(14*cm,10*cm),dpi=300)#,dpi=300)
    
    # Define fixed size for the axes in inches
    horiz = [Size.Fixed(2.4*cm),Size.Fixed(11*cm)]
    vert = [Size.Fixed(1.9*cm),Size.Fixed(8*cm)]
    
    divider = Divider(fig, (0, 0, 1, 1), horiz, vert, aspect=True, anchor=(0,0))
    
    ax = fig.add_axes(divider.get_position(), axes_locator=divider.new_locator(nx=1, ny=1))

    # colors = [
    #     ['red','blue'],
    #     ['orange','green'],
    #     ['purple','yellow'],
    #     ['brown','brown']
    #     ]

    for i,prefix in enumerate(prefixes):

        if i == 2:
            continue

        color_temp = colors[i]
        linestyle_temp = linestyles[i]
        z = []
        x = []
        list_ne = []
        list_n = []
        y = []
        list_dshift = []
        for variation in variations:
            bool_first = True
            europed_run= prefix + variation
            if variation == '000':
                europed_run = prefix[:-6]
            if suffix :
                europed_run += suffix

            print(europed_run)

            try:
                try:
                    gammas, modes = europed_analysis.get_gammas(europed_run, crit)
                except IndexError:
                    continue
                tab, consid_mode = europed_analysis.filter_tab_general(gammas, modes, consid_mode_input, exclud_mode)

                     
                #tab = remove_wrong_slopes(tab)

                for profile in range(len(tab[:,0])):
                    try:
                        argmax = np.nanargmax(tab[profile])
                        gamma = tab[profile, argmax]
                        list_n.append(consid_mode[argmax])

                        dshift = float(variation)
            
                        neped,teped = find_pedestal_values_old.pedestal_values(europed_run,profile)
                        betap = h5_manipulation.get_data(europed_run,['scan',str(profile),'betan'])
                        print(betap)
                        dshift = float(find_pedestal_values_old.get_frac(europed_run, profile=profile))

                        list_ne_full.append(neped)
                        list_frac_full.append(dshift)
                        print(f'nesep/neped: {dshift}')
                        print(f'neped: {neped}')
                        # betap = round(betap,1)

                        z.append(gamma)
                        x.append(betap)
                        y.append(teped)
                        list_ne.append(neped)
                    except ValueError:
                        print("ca marche pas du tout")
            except (IndexError,FileNotFoundError):
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

        pressure = 1.6*list_ne*y
        unique_x = list(set(x))
        unique_x = sorted(unique_x)
        unique_y = list(set(y))
        unique_y = sorted(unique_y)


        triang = tri.Triangulation(x,y)



        # limit=30
        # triangles_to_keep = []
        # for triangle in triang.triangles:
        #     y_values = y[triangle]
        #     distances = np.array([np.abs(unique_y.index(x)-unique_y.index(y)) for x in y_values for y in y_values])
        #     if np.all(distances <= 4):
        #         triangles_to_keep.append(triangle)
        # # # Create a new Triangulation object with filtered triangles
        filtered_triang = tri.Triangulation(x, pressure)#, triangles=np.array(triangles_to_keep))
        # filtered_triang = tri.Triangulation(x, y)#, triangles=np.array(triangles_to_keep))






        cs = ax.tricontour(filtered_triang, z, levels=[crit_value],colors=color_temp,linestyles=linestyle_temp,linewidths=3)
        ax.tricontourf(filtered_triang, z, levels=[0.85*crit_value,1.15*crit_value],colors=color_temp, alpha=0.2)

        plotplot = min_plot_n[i]


        for x_ind,y_ind,n_ind,z_ind in zip(x,pressure,list_n,z):
            if y_ind > 0 and y_ind < 4.4 and z_ind > plotplot[0]*crit_value and z_ind < plotplot[1]*crit_value and x_ind<2.9:
                # if i == 3 and x_ind <0.13:
                #     y_ind -= 0.5 
                # if i == 0 and x_ind <0.13:
                #     y_ind += 0.05
                
                ax.text(x_ind, y_ind, str(n_ind), fontsize=10, color=color_temp, fontweight='bold')

    ylabel, gammalabel = global_functions.get_plot_labels_gamma_profiles('peped',crit)
        #ax.set_ylim(bottom=0.8,top=2)
    
    #plt.clabel(cs, use_clabeltext =True, fmt='%1.1f',fontsize=8)

    # ax.scatter([3],[4.11], color='red', marker='+',s=500)
    # ax.scatter([1.9],[3.3], color='yellow', marker='+',s=500)
        
    # custom_legend2 = [
    #     plt.Line2D([0], [0], linewidth=2, color=colors[0], label=r'$\eta=0$', linestyle=linestyles[0]),
    #     #plt.Line2D([0], [0], linewidth=1, color=colors[0][1], label=r'$\eta=0$ - interpolation from temperature'),
    #     plt.Line2D([0], [0], linewidth=2, color=colors[1], label=r'$\eta=\eta_{Sp}$', linestyle=linestyles[1]),
    #   #  plt.Line2D([0], [0], linewidth=1, color=colors[2], label=r'$\eta=1.5\eta_{Sp}$', linestyle=linestyles[2]),
    #     plt.Line2D([0], [0], linewidth=2, color=colors[3], label=r'$\eta=2\eta_{Sp}$', linestyle=linestyles[3]),
    #     #plt.Line2D([0], [0], linewidth=1, color=colors[1][1], label=r'$\eta=1$ - interpolation from temperature'),
    #     ]
    # ax.legend(handles=custom_legend2, loc='lower left', fontsize=14) 
  

    ax.set_xlabel(r'$\beta_N$')
    ax.set_ylabel(ylabel)
    ax.set_ylim(bottom=0, top=4.4)
    ax.set_xlim(left=1,right=3)

    ax.text(1.3, 3.6,'Ideal', ha='left', va='top',fontsize=20, color=colors[0])
    ax.text(2.5, 3.5, r'$\eta=\eta_{\mathrm{Sp}}$', ha='left', va='bottom', fontsize=20, color=colors[1])
    ax.text(2, 1.8, r'$\eta=2 \eta_{\mathrm{Sp}}$', ha='left', va='bottom', fontsize=20, color=colors[3])
    
    ax.xaxis.set_ticklabels([1,1.5,2,2.5,3])

    #fig.colorbar(contour, label=gammalabel)
    # fig.tight_layout()
    # plt.savefig('/home/jwp9427/cococo/9_betan')
    # plt.close()

    ax.text(0.05,0.05,r'$n_e^{\mathrm{ped}} = 2.57 \cdot 10^{19} \mathrm{m}^{-3}$' + '\n' + r'$n_e^{\mathrm{pos}}-T_e^{\mathrm{pos}} = 2.2\%\psi_N$',transform=ax.transAxes,ha='left',va='bottom')


    print(f'{min(list_ne_full)} <= neped <= {max(list_ne_full)}')
    print(f'{min(list_frac_full)} <= frac <= {max(list_frac_full)}')

    plt.savefig('/home/jwp9427/cococo/9')
    plt.close()

if __name__ == '__main__':
    main(prefixes, variations, suffix, crit, crit_value, ypar, exclud_mode, consid_mode, plot_frac=None)