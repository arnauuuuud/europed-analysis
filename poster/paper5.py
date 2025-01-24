#!/usr/local/depot/Python-3.7/bin/python
# /usr/local/depot/Python-3.5.1/bin/python

from hoho import useful_recurring_functions, europed_analysis, global_functions, startup, find_pedestal_values_old, h5_manipulation, spitzer
from poster import plot_canvas
import argparse
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.tri as tri
import matplotlib as mpl
import matplotlib
from mpl_toolkits.axes_grid1 import Divider, Size

matplotlib.rcParams['font.size'] = 14
matplotlib.rcParams['font.family'] = 'sans-serif'
# matplotlib.rcParams['font.sans-serif'] = [:]

cm = 1/2.54

prefixes = ['sb_eta0.0_rs','sb_eta1.0_rs','sb_eta1.5_rs','sb_eta2.0_rs']
variations = ['-0.01','0.0','0.01','0.02','0.022','0.03']
suffix = '_neped2.57' 
exclud_mode = [30,40,50]
crit = 'alfven'
crit_value = 0.05
plot_frac = True
ypar = 'pe'
consid_mode = None


colors = plot_canvas.colors
linestyles = plot_canvas.linestyles




def main(prefixes, variations, suffix, crit, crit_value, ypar, exclud_mode, consid_mode_input,plot_frac):



    colors = plot_canvas.colors
    linestyles = plot_canvas.linestyles

    # fig, axs = plt.subplots(2,2, figsize=(21*cm,11*cm), sharex='col', sharey='row', gridspec_kw={'height_ratios': [4, 1.5], 'width_ratios': [2,1], 'hspace': 0.08, 'wspace': 0.05})
    # fig, axs = plt.subplots(1,2, figsize=(21*cm,11*cm), sharex='col', sharey='row', gridspec_kw={'width_ratios': [2,1], 'hspace': 0.08, 'wspace': 0.08})

    fig = plt.figure(figsize=(15*cm,13.9*cm),dpi=300)#,dpi=300)
    
    # Define fixed size for the axes in inches
    horiz = [Size.Fixed(2.4*cm),Size.Fixed(12*cm)]#,Size.Fixed(0.2*cm),Size.Fixed(6*cm)]
    vert = [Size.Fixed(2*cm),Size.Fixed(3.5*cm),Size.Fixed(0.2*cm),Size.Fixed(8*cm)]
    
    divider = Divider(fig, (0, 0, 1, 1), horiz, vert, aspect=True, anchor=(0,0))
    
    ax = fig.add_axes(divider.get_position(), axes_locator=divider.new_locator(nx=1, ny=3))
    ax2 = fig.add_axes(divider.get_position(), axes_locator=divider.new_locator(nx=1, ny=1))
    # ax3 = fig.add_axes(divider.get_position(), axes_locator=divider.new_locator(nx=3, ny=3))
    

    list_ne_full = []
    list_betan_full = []

    # ax = axs[0,0]
    # ax = axs[0]

    # colors = [
    #     ['red','blue'],
    #     ['orange','green'],
    #     ['purple','yellow'],
    #     ['brown','brown']
    #     ]
    min_plot_n = [[0.8,1.3],[0.9,1.1],[0.95,1.05],[0.95,1.05]]


    for i,prefix in enumerate(prefixes):

        if i == 2:
            continue

        color_temp = colors[i]
        linestyle_temp = linestyles[i]
        z = []
        x = []
        list_n = []
        list_ne = []
        y = []
        list_dshift = []
        for variation in variations:
            bool_first = True
            europed_run= prefix + variation
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
                        
                        dshift = float(find_pedestal_values_old.get_frac(europed_run, profile=profile))


                        neped,teped = find_pedestal_values_old.pedestal_values(europed_run,profile)

                        neped= round(neped,3)
                        list_ne_full.append(neped)
                        betap = h5_manipulation.get_data(europed_run,['scan',str(profile),'betan'])
                        list_betan_full.append(betap)


                        z.append(gamma)
                        x.append(dshift)
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
        y = pressure
        unique_x = list(set(x))
        unique_x = sorted(unique_x)
        unique_y = list(set(y))
        unique_y = sorted(unique_y)

        
        triang = tri.Triangulation(x,pressure)

        if i>0:
            limit=4
        else:
            limit=2
        triangles_to_keep = []
        for triangle in triang.triangles:
            y_values = y[triangle]
            distances = np.array([np.abs(unique_y.index(x)-unique_y.index(y)) for x in y_values for y in y_values])
            if np.all(distances <= 5):
                triangles_to_keep.append(triangle)
        # Create a new Triangulation object with filtered triangles
        filtered_triang = tri.Triangulation(x, y, triangles=np.array(triangles_to_keep))

        cs = ax.tricontour(filtered_triang, z, levels=[crit_value],colors=color_temp,linestyles=linestyle_temp,linewidths=3)
        ax.tricontourf(filtered_triang, z, levels=[0.85*crit_value,1.15*crit_value],colors=color_temp, alpha=0.2)

        plotplot = min_plot_n[i]

        for x_ind,y_ind,n_ind,z_ind in zip(x,pressure,list_n,z):
            if y_ind > 0 and y_ind < 5.5 and z_ind > plotplot[0]*crit_value and z_ind < plotplot[1]*crit_value and x_ind<3.9:
                if i == 3 and x_ind <0.13:
                    y_ind -= 0.5 
                if i == 0 and x_ind <0.13:
                    y_ind += 0.05
                
                ax.text(x_ind, y_ind, str(n_ind), fontsize=10, color=color_temp, fontweight='bold')


    ylabel = global_functions.peped_label
    #     #ax.set_ylim(bottom=0.8,top=2)
    


    ax.text(0.3, 4.6,'Ideal', ha='left', va='bottom', fontsize=20, color=colors[0])
    ax.text(0.65, 3.8, r'$\eta=\eta_{\mathrm{Sp}}$', ha='left', va='center', fontsize=20, color=colors[1])
    ax.text(0.45, 1, r'$\eta=2 \eta_{\mathrm{Sp}}$', ha='left', va='bottom', fontsize=20, color=colors[3])

    nelabel = global_functions.nesepneped_label
    

    # ax.set_xlabel(nelabel)

    ax.set_ylabel(ylabel)
    ax.set_ylim(bottom=0, top=5.9)
    ax.set_xlim(left=0,right=0.8)
    ax.xaxis.set_tick_params(labelbottom=False)
    ax.yaxis.set_ticklabels([0,1,2,3,4,5],[0,1,2,3,4,5])



    # ax2 = ax.twinx()
    # ax2 = axs[1,0]

    prefixes = ['sb_eta0.0_rs','sb_eta1.0_rs','sb_eta1.5_rs','sb_eta2.0_rs']
    variations = ['-0.02','-0.01','0.0','0.01','0.02','0.022','0.03']
    variations = ['-0.01','0.0','0.01','0.02','0.022','0.03']
    suffix = '_neped2.57' 

    exclud_mode = [30,40,50]
    crit = 'alfven'
    crit_value = 0.05
    ypar = 'te'
    consid_mode = None
    

    for i,prefix in enumerate(prefixes):
        if i == 0 or i == 2:
            continue


        color_temp = colors[i]
        linestyle_temp = linestyles[i]
        z = []
        x = []
        list_ne = []
        y = []
        list_dshift = []
        for variation in variations:
            bool_first = True
            europed_run= prefix + variation
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

                        dshift = float(variation)
                        if plot_frac:
                            dshift = float(find_pedestal_values_old.get_frac(europed_run, profile=profile))


                        neped,teped = find_pedestal_values_old.pedestal_values(europed_run,profile)

                        zeff = h5_manipulation.get_data(europed_run,['input','zeff'])

                        neped=round(neped,3) 

                        resistivity = spitzer.resistivity(neped*1e19, teped*1e3, zeff)*1e7

                        z.append(gamma)
                        x.append(dshift)
                        y.append(resistivity)
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
        #     if np.all(distances <= 50):
        #         triangles_to_keep.append(triangle)
        # # Create a new Triangulation object with filtered triangles
        # filtered_triang = tri.Triangulation(x, y)#, triangles=np.array(triangles_to_keep))
        filtered_triang = tri.Triangulation(x, y)






        cs = ax2.tricontour(filtered_triang, z, levels=[crit_value],colors=color_temp,linestyles=linestyle_temp,linewidths=3,zorder=-1000)

    ylabel = global_functions.eta_ped_ohm_label    

    ax2.set_ylabel(ylabel)
    ax2.set_ylim(bottom=0,top=0.9)
    ax2.set_xlim(left=0,right=0.8)

    nelabel = global_functions.nesepneped_label
    

    ax2.set_xlabel(nelabel)



    # axs[1,1].set_visible(False)
    # plt.subplots_adjust(top=0.999,
    #     bottom=0.16,
    #     left=0.08,
    #     right=0.995,
    #     hspace=0.2,
    #     wspace=0.2)

    # #fig.colorbar(contour, label=gammalabel)
    # # fig.tight_layout()
    # plt.savefig('/home/jwp9427/cococo/8_nesep')
    # plt.close()

    print(f'{min(list_ne_full)} <= neped <= {max(list_ne_full)}')
    print(f'{min(list_betan_full)} <= betan <= {max(list_betan_full)}')

    ax.text(0.05,0.05,r'$n_e^{\mathrm{ped}} = 2.57 \cdot 10^{19} \mathrm{m}^{-3}$' + '\n' + r'$\beta_N = 3$',transform=ax.transAxes,ha='left',va='bottom')
    # ax3.text(0.1,0.05,r'$2.5 \leq {n_e^{\mathrm{ped}}}_{[10^{19}\mathrm{m}^{-3}]} \leq 3.2$' + '\n' + r'$1.7\leq \beta_N \leq 2.3$' ,transform=ax3.transAxes,ha='left',va='bottom')

    ax2.text(0.95,0.05,'(b)', transform=ax2.transAxes, ha='right', va='bottom')
    ax.text(0.95,0.05,'(a)', transform=ax.transAxes, ha='right', va='bottom')

    plt.savefig('/home/jwp9427/cococo/paper5')
    plt.close()

if __name__ == '__main__':
    main(prefixes, variations, suffix, crit, crit_value, ypar, exclud_mode, consid_mode, plot_frac)