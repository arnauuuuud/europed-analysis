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

prefixes = ['sb_eta0.0_rs0.022_neped','sb_eta1.0_rs0.022_neped','sb_eta1.5_rs0.022_neped','sb_eta2.0_rs0.022_neped']
variations = ['1.07','1.57','2.07','2.57','3.07','3.57','4.07']

exclud_mode = [30,40,50]
crit = 'alfven'
crit_value = 0.05
ypar = 'pe'
consid_mode = None
suffix= None



def main(prefixes, variations, suffix, crit, crit_value, ypar, exclud_mode, consid_mode_input,plot_frac):


    colors = plot_canvas.colors
    linestyles = plot_canvas.linestyles

    # fig, axs = plt.subplots(2,2, figsize=(22*cm,13.4*cm), sharex='col', sharey='row', gridspec_kw={'height_ratios': [4, 1.5], 'width_ratios': [2,1], 'hspace': 0.08, 'wspace': 0.05})
    
    # ax = axs[0,0]

    fig = plt.figure(figsize=(20.8*cm,13.9*cm),dpi=300)#,dpi=300)
    
    # Define fixed size for the axes in inches
    horiz = [Size.Fixed(2.4*cm),Size.Fixed(12*cm),Size.Fixed(0.2*cm),Size.Fixed(6*cm)]
    vert = [Size.Fixed(2*cm),Size.Fixed(3.5*cm),Size.Fixed(0.2*cm),Size.Fixed(8*cm)]
    
    divider = Divider(fig, (0, 0, 1, 1), horiz, vert, aspect=True, anchor=(0,0))
    
    ax = fig.add_axes(divider.get_position(), axes_locator=divider.new_locator(nx=1, ny=3))
    ax2 = fig.add_axes(divider.get_position(), axes_locator=divider.new_locator(nx=1, ny=1))
    ax3 = fig.add_axes(divider.get_position(), axes_locator=divider.new_locator(nx=3, ny=3))


    # colors = [
    #     ['red','blue'],
    #     ['orange','green'],
    #     ['purple','yellow'],
    #     ['brown','brown']
    #     ]

    min_plot_n = [[0.8,1.4],[0.9,1.1],[0.95,1.05],[0.95,1.05]]

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

                        dshift = float(variation)
                        if plot_frac:
                            dshift = float(find_pedestal_values_old.get_frac(europed_run, profile=profile))


                        neped,teped = find_pedestal_values_old.pedestal_values(europed_run,profile)
                        list_n.append(consid_mode[argmax])
                        neped= round(neped,3)

                        z.append(gamma)
                        x.append(neped)
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


        triang = tri.Triangulation(x,pressure)



        # limit=30
        # triangles_to_keep = []
        # for triangle in triang.triangles:
        #     y_values = y[triangle]
        #     distances = np.array([np.abs(unique_y.index(x)-unique_y.index(y)) for x in y_values for y in y_values])
        #     if np.all(distances <= 20):
        #         triangles_to_keep.append(triangle)
        # # Create a new Triangulation object with filtered triangles
        filtered_triang = tri.Triangulation(x, pressure)#, triangles=np.array(triangles_to_keep))






        cs = ax.tricontour(filtered_triang, z, levels=[crit_value],colors=color_temp,linestyles=linestyle_temp,linewidths=3)
        ax.tricontourf(filtered_triang, z, levels=[0.85*crit_value,1.15*crit_value],colors=color_temp, alpha=0.2)

        plotplot = min_plot_n[i]

        for x_ind,y_ind,n_ind,z_ind in zip(x,pressure,list_n,z):
            if y_ind > 0 and y_ind < 4.5 and z_ind > plotplot[0]*crit_value and z_ind < plotplot[1]*crit_value and x_ind<3.9:
                if i == 0 and x_ind >2.5:
                    y_ind += 0.1
                
                ax.text(x_ind, y_ind, str(n_ind), fontsize=10, color=color_temp, fontweight='bold')

    ylabel = global_functions.peped_label
        #ax.set_ylim(bottom=0.8,top=2)
    
    #plt.clabel(cs, use_clabeltext =True, fmt='%1.1f',fontsize=8)
        
    # custom_legend2 = [
    #     plt.Line2D([0], [0], linewidth=2, color=colors[0], label=r'$\eta=0$', linestyle=linestyles[0]),
    #     #plt.Line2D([0], [0], linewidth=1, color=colors[0][1], label=r'$\eta=0$ - interpolation from temperature'),
    #     plt.Line2D([0], [0], linewidth=2, color=colors[1], label=r'$\eta=\eta_{Sp}$', linestyle=linestyles[1]),
    #   #  plt.Line2D([0], [0], linewidth=1, color=colors[2], label=r'$\eta=1.5\eta_{Sp}$', linestyle=linestyles[2]),
    #     plt.Line2D([0], [0], linewidth=2, color=colors[3], label=r'$\eta=2\eta_{Sp}$', linestyle=linestyles[3]),
    #     #plt.Line2D([0], [0], linewidth=1, color=colors[1][1], label=r'$\eta=1$ - interpolation from temperature'),
    #     ]

    # ax.text()
    # ax.legend(handles=custom_legend2, loc='upper right', fontsize=14) 

    ax.text(3.9, 4.1,'Ideal', ha='right', va='top', fontsize=20, color=colors[0])
    ax.text(2.2, 3.7, r'$\eta=\eta_{\mathrm{Sp}}$', ha='left', va='bottom', fontsize=20, color=colors[1])
    ax.text(2.2, 1.5, r'$\eta=2 \eta_{\mathrm{Sp}}$', ha='left', va='bottom', fontsize=20, color=colors[3])

    nelabel = global_functions.neped_label
    

    # ax.set_xlabel(nelabel)
    # if plot_frac:
    # ax.set_xlabel(nelabel)
    ax.set_ylabel(ylabel)
    ax.set_ylim(bottom=0, top=4.5)
    ax.set_xlim(left=1,right=4)
    ax.xaxis.set_tick_params(labelbottom=False)






    # ax2 = ax.twinx()
    # ax2 = axs[1,0]

    prefixes = ['sb_eta0.0_rs0.022_neped','sb_eta1.0_rs0.022_neped','sb_eta1.5_rs0.022_neped','sb_eta2.0_rs0.022_neped']
    variations = ['1.07','1.57','2.07','2.57','3.07','3.57','4.07']

    exclud_mode = [30,40,50]
    crit = 'alfven'
    crit_value = 0.05
    ypar = 'te'
    consid_mode = None
    suffix= None
    

    for i,prefix in enumerate(prefixes):

        if i == 0 or i ==2:
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
                        x.append(neped)
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

        pressure = 1.6*list_ne*y
        unique_x = list(set(x))
        unique_x = sorted(unique_x)
        unique_y = list(set(y))
        unique_y = sorted(unique_y)


        triang = tri.Triangulation(x,y)
        limit=30
        triangles_to_keep = []
        for triangle in triang.triangles:
            y_values = y[triangle]
            distances = np.array([np.abs(unique_y.index(x)-unique_y.index(y)) for x in y_values for y in y_values])
            if np.all(distances <= 50):
                triangles_to_keep.append(triangle)
        # Create a new Triangulation object with filtered triangles
        filtered_triang = tri.Triangulation(x, y)#, triangles=np.array(triangles_to_keep))
        # filtered_triang = tri.Triangulation(x, y)




        ylabel = global_functions.eta_ped_ohm_label    

        ax2.set_ylabel(ylabel)
        ax2.set_ylim(bottom=0,top=1.9)
        ax2.set_xlim(left=1,right=4)

        nelabel, shit = global_functions.get_plot_labels_gamma_profiles('neped',crit)
        

        ax2.set_xlabel(nelabel)

        cs = ax2.tricontour(filtered_triang, z, levels=[crit_value],colors=color_temp,linestyles=linestyle_temp,linewidths=3,zorder=-1000)
        # ax2.set_ylim(bottom=0, top=0.006)
        # ax.tricontourf(filtered_triang, z, levels=[0.85*crit_value,1.15*crit_value],colors=color_temp, alpha=0.2)



    # ax3 = axs[0,1]

    blue = 'darkgreen'
    green = 'darkgreen'
    pink = 'darkgreen'

    tab_density = [[2.50617, 0.118350, 3.20297, 0.373003, green],
            [2.55463, 0.142605, 2.78443, 0.316855, green],
            [2.40292, 0.101457, 3.35974, 0.330261, green],
            [2.78283, 0.130109, 3.03715, 0.322383, pink],
            [3.18955, 0.137792, 2.71660, 0.263086, pink],
            [2.89598, 0.151736, 2.96227, 0.364966, pink],
            [3.05267, 0.132252, 2.84640, 0.271229, pink]
    ]

    tab_density = np.array(tab_density)


    density = tab_density[:,0]
    density = [float(i) for i in density]
    density_error = tab_density[:,1]
    density_error = [float(i) for i in density_error]
    peped = tab_density[:,2]
    peped = [float(i) for i in peped]
    peped_error = tab_density[:,3]
    peped_error = [float(i) for i in peped_error]
    colors = tab_density[:,4]
    markers = ['s','s','s','*','*','*','*']



    for x,xerr,y,yerr,color,marker in zip(density,density_error,peped,peped_error,colors,markers):
        size=200
        if marker == '*':
            size=400
        ax3.scatter(x, y, color=color, marker=marker,s=size,linewidth=2, edgecolor=['black'],zorder=20)
        ax3.plot([x-xerr,x+xerr], [y,y], color=color)
        ax3.plot([x,x], [y-yerr,y+yerr], color=color)


    xlabel = global_functions.neped_label
    ylabel = global_functions.peped_label
    # ax.set_xlabel(xlabel, fontsize=50)
    # ax.set_ylabel(ylabel, fontsize=50)
    ax3.set_xlabel(xlabel, fontsize=20)
    ax3.set_ylabel(ylabel, fontsize=20)
    ax3.xaxis.set_tick_params(labelbottom=True)
    # ax3.yaxis.set_tick_params(labelleft=False)
    ax3.set_xlim(left=2.1,right=3.6)
    ax3.set_ylim(bottom=0, top=4.5)
    # ax3.xaxis.set_ticklabels([2.5,3,3.5])

    ax.text(0.05,0.05,r'$n_e^{\mathrm{pos}}-T_e^{\mathrm{pos}} = 2.2\%\psi_N$' + '\n' + r'$\beta_N = 3$' ,transform=ax.transAxes,ha='left',va='bottom')
    ax3.text(0.1,0.05,r'$0.4 \leq n_e^{\mathrm{sep}}/n_e^{\mathrm{ped}} \leq 0.7$' + '\n' + r'$1.6\leq \beta_N \leq 2$' ,transform=ax3.transAxes,ha='left',va='bottom')

    # axs[1,1].set_visible(False)
    # plt.subplots_adjust(top=0.999,
    #     bottom=0.16,
    #     left=0.105,
    #     right=0.98,
    #     hspace=0.2,
    #     wspace=0.2)
    # #fig.colorbar(contour, label=gammalabel)
    # fig.tight_layout()
    plt.savefig('/home/jwp9427/cococo/7')
    plt.close()
    # plt.show()

if __name__ == '__main__':
    main(prefixes, variations, suffix, crit, crit_value, ypar, exclud_mode, consid_mode, plot_frac=None)