#!/usr/local/depot/Python-3.7/bin/python
# /usr/local/depot/Python-3.5.1/bin/python

from hoho import europed_analysis, global_functions, startup, useful_recurring_functions
import argparse
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.tri as tri

def argument_parser():
    """Defining comandline parser and returning the arguments"""
    parser = argparse.ArgumentParser(description = "Plots the values of the growth rate gamma and the critical contour on a 2D map neped,Teped (with the alven criterion)")
    parser.add_argument("prefix", help = "prefix of the Europed run")
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

def main(prefix, variations, suffix, crit, crit_value, ypar, exclud_mode, consid_mode):

    if crit_value is None:
        if crit == "alfven":
            crit_value=0.03
        elif crit == "diamag":
            crit_value=0.25

    fig, ax = plt.subplots(figsize=(12,9))

    list_n = []
    z = []
    x = []
    y = []

    global_n = [1,2,3,4,5,7,10,20,30,40,50]
    for variation in variations:
        bool_first = True
        europed_run= prefix + variation
        if suffix :
            europed_run += suffix

        print(europed_run)

        try:
            gammas, modes = europed_analysis.get_gammas(europed_run, crit)
            tab, consid_mode = europed_analysis.filter_tab_general(gammas, modes, consid_mode, exclud_mode)
            tab_ne,tab_Te = europed_analysis.get_nT(europed_run)


            def remove_wrong_slopes(tab):
                temp_tab = tab
                for j in range(len(temp_tab[0])):
                    for i in range(len(temp_tab)-1):
                        if temp_tab[i,j]>temp_tab[i+1,j]: 
                            temp_tab[i,j] = None
                return temp_tab
            
            tab = remove_wrong_slopes(tab)

            for profile in range(len(tab[:,0])):
                try:
                    argmax = np.nanargmax(tab[profile])
                    gamma = tab[profile, argmax]
                    ne = tab_ne[profile]
                    Te = tab_Te[profile]

                    list_n.append(global_n[argmax])
                    z.append(gamma)
                    x.append(ne)
                    y.append(Te)
                except ValueError:
                    print("ca marche pas du tout")
        except FileNotFoundError:
            print(f"{europed_run:>40} FILE NOT FOUND")

    valid_indices = ~np.isnan(x) & ~np.isnan(y) & ~np.isnan(z)
    x = np.array(x)[valid_indices]
    y = np.array(y)[valid_indices]
    z = np.array(z)[valid_indices]
    list_n = np.array(list_n)[valid_indices]

    x_smooth = np.linspace(min(x),max(x),1000)
    y_te_smooth = np.linspace(np.nanmin(y),np.nanmax(y),1000)
    
    X_smooth, Y_te_smooth = np.meshgrid(x_smooth, y_te_smooth)
    Y_pe_smooth = 1.6*X_smooth*Y_te_smooth

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



    if ypar == 'pe':
        bottom = 0.8
        top = 2
    elif ypar == 'te':
        bottom = 0
        top = 1


    # ax.triplot(filtered_triang, linestyle='dotted',color='blue')
    
    # if ypar == 'te':
    #     ax.plot(x, y, 'bo')  # Plot the data points
    # elif ypar == 'pe':
    #     ax.plot(x, pressure, 'bo')
    contour = ax.tricontourf(filtered_triang, z, levels=20, cmap='inferno_r')

    cs = ax.tricontour(filtered_triang, z, levels=[crit_value],colors='r')
    ax.tricontour(filtered_triang, z, levels=[0.85*crit_value],colors='r', linestyles='dashed')
    ax.tricontour(filtered_triang, z, levels=[1.15*crit_value],colors='r', linestyles='dashed')
    # plt.clabel(cs, use_clabeltext =True, fmt='%1.2f',fontsize=10)
    #ax.set_ylim(bottom=0)

    #plt.clabel(cs, use_clabeltext =True, fmt='%1.2f',fontsize=10)

    if ypar == 'te':
        cs = ax.contour(X_smooth, Y_te_smooth, Y_pe_smooth, levels=[0.5,1,1.5, 2],colors='k', linewidths = 1)
        #cs = ax.tricontour(filtered_triang, pressure, levels=[0.5,1,1.5, 2, 2.5, 3, 3.5],colors='k', linewidths = 1)
        ylabel, gammalabel = global_functions.get_plot_labels_gamma_profiles('teped',crit)
        #ax.set_ylim(top=0.5)
    elif ypar == 'pe':
        cs = ax.contour(X_smooth, Y_pe_smooth, Y_te_smooth, levels=[0.1,0.2,0.3,0.5,0.7,0.9],colors='k', linewidths = 1)
        #cs = ax.tricontour(filtered_triang, y, levels=[0.1, 0.2, 0.3, 0.4 ,0.5],colors='k', linestye="dotted", linewidths = 1)
        ylabel, gammalabel = global_functions.get_plot_labels_gamma_profiles('peped',crit)
        
    
    plt.clabel(cs, use_clabeltext =True, fmt='%1.1f',fontsize=8)
        

    if ypar == 'te':
        for x_ind,y_ind,n_ind in zip(x,y,list_n):
            if y_ind > bottom and y_ind < top:
                ax.text(x_ind, y_ind, str(n_ind), fontsize=8, color='b')
    if ypar == 'pe':
        for x_ind,y_ind,n_ind in zip(x,pressure,list_n):
            if y_ind > bottom and y_ind < top:
                ax.text(x_ind, y_ind, str(n_ind), fontsize=8, color='b')

    ax.set_ylim(bottom=bottom,top=top)


    nelabel, shit = global_functions.get_plot_labels_gamma_profiles('neped',crit)
    

    ax.set_xlabel(nelabel)
    ax.set_ylabel(ylabel)

    

    fig.colorbar(contour, label=gammalabel)
    fig.tight_layout()
    plt.show()

if __name__ == '__main__':
    prefix, variations, suffix, crit, crit_value, ypar, exclud_mode, consid_mode = argument_parser()
    main(prefix, variations, suffix, crit, crit_value, ypar, exclud_mode, consid_mode)