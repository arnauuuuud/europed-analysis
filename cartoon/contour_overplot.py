#!/usr/local/depot/Python-3.7/bin/python
# /usr/local/depot/Python-3.5.1/bin/python

from hoho import useful_recurring_functions, europed_analysis, global_functions, startup
import argparse
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.tri as tri

def argument_parser():
    """Defining comandline parser and returning the arguments"""
    parser = argparse.ArgumentParser(description = "Plots the values of the growth rate gamma and the critical contour on a 2D map neped,Teped (with the alven criterion)")
    parser.add_argument("prefix", type=useful_recurring_functions.parse_modes, help = "prefix of the Europed run")
    parser.add_argument("variations", type=useful_recurring_functions.parse_modes, help = "name variations of the Europed runs")
    
    parser.add_argument("-s", "--suffix", help= "common suffix of the Europed runs if needed")
    
    parser.add_argument("-d", "--diamag", action = 'store_const', const = 'diamag', dest = 'crit', default = 'alfven', help = "normalize growth rate to diamagnetic frequency instead of Alfven frequency")
    parser.add_argument("-v", "--critical_value", help= "critical value of the growth rate, default : 0.03 for alfven, 0.25 for diamagnetic")

    parser.add_argument("-p", "--pressure", action = 'store_const', const = 'pe', dest = 'ypar', default = 'te', help= "pressure on yaxis instead of temperature")


    group = parser.add_mutually_exclusive_group()
    group.add_argument('-x',"--exclud_mode", type=useful_recurring_functions.parse_modes, help = "list of modes to exclude, comma-separated (will plot all modes except for these ones)")
    group.add_argument('-m',"--consid_mode", type=useful_recurring_functions.parse_modes, help = "list of modes to consider, comma-separated (will plot only these modes)")

    args = parser.parse_args()

    if args.exclud_mode and args.consid_mode:
        parser.error("Arguments --exclud_mode and --consid_mode are mutually exclusive. Use one or the other.")

    if args.critical_value:
        critical_value = float(args.critical_value)
    else:
        critical_value = None

    variations = args.variations
    if variations == ["full_list"]:
        variations = ['-0.0100','-0.0050','0.0000','0.0500','0.0100','0.0150','0.0200','0.0250','0.0300','0.0350','0.0400']

    return args.prefix, variations, args.suffix, args.crit, critical_value, args.ypar, args.exclud_mode, args.consid_mode

def main(prefixes, variations, suffix, crit, crit_value, ypar, exclud_mode, consid_mode_input):

    if crit_value is None:
        if crit == "alfven":
            crit_value=0.03
        elif crit == "diamag":
            crit_value=0.25

    fig, ax = plt.subplots(figsize=(9,7))

    colors = [
        ['red','blue'],
        ['orange','green'],
        ['purple','yellow'],
        ['pink','brown']
        ]

    for i,prefix in enumerate(prefixes):
        color_temp = colors[i]
        z = []
        x = []
        y = []
        for variation in variations:
            europed_run= prefix + variation
            if suffix :
                europed_run += suffix

            print(europed_run)

            try:
                gammas, modes = europed_analysis.get_gammas(europed_run, crit)
                tab, consid_mode = europed_analysis.filter_tab_general(gammas, modes, consid_mode_input, exclud_mode)


                for profile in range(len(tab[:,0])):
                    try:
                        argmax = np.nanargmax(tab[profile])
                        gamma = tab[profile, argmax]
                        neped,teped = find_pedestal_values_old.pedestal_values(europed_run,profile)

                        z.append(gamma)
                        x.append(neped)
                        y.append(teped)
                    except ValueError:
                        print("ca marche pas du tout")
            except (IndexError,FileNotFoundError):
                print(f"{europed_run:>40} FILE NOT FOUND")

        valid_indices = ~np.isnan(x) & ~np.isnan(y) & ~np.isnan(z)
        x = np.array(x)[valid_indices]
        y = np.array(y)[valid_indices]
        z = np.array(z)[valid_indices]

        pressure = 1.6*x*y
        unique_x = list(set(x))
        unique_x = sorted(unique_x)


        if ypar == 'te':
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

        elif ypar == 'pe':
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


        cs = ax.tricontour(filtered_triang, z, levels=[crit_value],colors=color_temp[0])
        ax.tricontour(filtered_triang, z, levels=[0.85*crit_value],colors=color_temp[0], linestyles='dashed')
        ax.tricontour(filtered_triang, z, levels=[1.15*crit_value],colors=color_temp[0], linestyles='dashed')

        del filtered_triang
        del z
        del triang
        del x 
        del y
        del tab
        del gammas 
        del modes
        del pressure
        del tab_ne
        del tab_Te


        # ax.triplot(filtered_triang, linestyle='dotted',color='blue')
        
        # if ypar == 'te':
        #     ax.plot(x, y, 'bo')  # Plot the data points
        # elif ypar == 'pe':
        #     ax.plot(x, pressure, 'bo')
        # contour = ax.tricontourf(filtered_triang, z, levels=20, cmap='inferno_r')

        #ax.plot(x, pressure, 'bo')

        # # contour_te = plt.tricontour(filtered_triang_te, z, levels=[crit_value],linewidths=0)
        # contour_path = contour_te.collections[0].get_paths()[0]
        # vertices = contour_path.vertices
        # # ax.plot(vertices[:, 0], 1.6*vertices[:,0]*vertices[:, 1], color=color_temp[1], linewidth=2)

        # contour_te = plt.tricontour(filtered_triang_te, z, levels=[0.85*crit_value],linewidths=0)
        # contour_path = contour_te.collections[0].get_paths()[0]
        # vertices = contour_path.vertices
        # # ax.plot(vertices[:, 0], 1.6*vertices[:,0]*vertices[:, 1], color=color_temp[1], linestyle='dashed', linewidth=2)

        # contour_te = plt.tricontour(filtered_triang_te, z, levels=[1.15*crit_value],linewidths=0)
        # contour_path = contour_te.collections[0].get_paths()[0]
        # vertices = contour_path.vertices
        # ax.plot(vertices[:, 0], 1.6*vertices[:,0]*vertices[:, 1], color=color_temp[1], linestyle='dashed', linewidth=2)

        # cs = ax.tricontour(filtered_triang, z, levels=[crit_value],colors=color_temp[0])
        #ax.tricontour(filtered_triang, z, levels=[0.85*crit_value,1.15*crit_value],colors=color_temp[0], linestyles='dashed')
        # plt.clabel(cs, use_clabeltext =True, fmt='%1.2f',fontsize=10)
        #ax.set_ylim(bottom=0)

        #plt.clabel(cs, use_clabeltext =True, fmt='%1.2f',fontsize=10)

    if ypar == 'te':
    #     cs = ax.contour(X_smooth, Y_te_smooth, Y_pe_smooth, levels=[0.5,1,1.5, 2],colors='k', linewidths = 1)
    #     #cs = ax.tricontour(filtered_triang, pressure, levels=[0.5,1,1.5, 2, 2.5, 3, 3.5],colors='k', linewidths = 1)
        ylabel, gammalabel = global_functions.get_plot_labels_gamma_profiles('teped',crit)
    #     #ax.set_ylim(top=0.5)
    elif ypar == 'pe':
    #     cs = ax.contour(X_smooth, Y_pe_smooth, Y_te_smooth, levels=[0.1,0.2,0.3,0.5,0.7,0.9],colors='k', linewidths = 1)
    #     #cs = ax.tricontour(filtered_triang, y, levels=[0.1, 0.2, 0.3, 0.4 ,0.5],colors='k', linestye="dotted", linewidths = 1)
        ylabel, gammalabel = global_functions.get_plot_labels_gamma_profiles('peped',crit)
        ax.set_ylim(bottom=0.8,top=2)
    
    #plt.clabel(cs, use_clabeltext =True, fmt='%1.1f',fontsize=8)
        
    custom_legend2 = [
        plt.Line2D([0], [0], linewidth=1, color=colors[0][0], label=r'$\eta=0$'),
        #plt.Line2D([0], [0], linewidth=1, color=colors[0][1], label=r'$\eta=0$ - interpolation from temperature'),
        plt.Line2D([0], [0], linewidth=1, color=colors[1][0], label=r'$\eta=\eta_{Sp}$'),
        plt.Line2D([0], [0], linewidth=1, color=colors[2][0], label=r'$\eta=1.5\eta_{Sp}$'),
        plt.Line2D([0], [0], linewidth=1, color=colors[3][0], label=r'$\eta=2.0\eta_{Sp}$'),
        #plt.Line2D([0], [0], linewidth=1, color=colors[1][1], label=r'$\eta=1$ - interpolation from temperature'),
        ]
    ax.legend(handles=custom_legend2, loc='lower right', fontsize=14) 



    # nelabel, shit = global_functions.get_plot_labels_gamma_profiles('neped',crit)
    

    ax.set_xlabel(r'$n_e^{ped}$', fontsize=20)
    ax.set_ylabel(ylabel, fontsize=20)

    ax.set_ylim(bottom=0,top=2)


    #fig.colorbar(contour, label=gammalabel)
    fig.tight_layout()
    plt.show()

if __name__ == '__main__':
    prefix, variations, suffix, crit, crit_value, ypar, exclud_mode, consid_mode = argument_parser()
    main(prefix, variations, suffix, crit, crit_value, ypar, exclud_mode, consid_mode)