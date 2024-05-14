#!/usr/local/depot/Python-3.7/bin/python
# /usr/local/depot/Python-3.5.1/bin/python

from hoho import useful_recurring_functions, europed_analysis, global_functions, startup
import argparse
import matplotlib.pyplot as plt
import numpy as np

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

    z = []
    x = []
    y_te = []
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
            ne = tab_ne[0]
            x.append(ne)
            y_te_temp = []
            z_temp = []

            for profile in range(len(tab[:,0])):
                try:
                    argmax = np.nanargmax(tab[profile])
                    gamma = tab[profile, argmax]
                    
                    Te = tab_Te[profile]

                    z_temp.append(gamma)
                    
                    y_te_temp.append(Te)
                except ValueError:
                    y_te_temp.append(None)
                    z_temp.append(None)
                    print("ca marche pas du tout")

            y_te.append(y_te_temp)
            z.append(z_temp)
        except FileNotFoundError:
            print(f"{europed_run:>40} FILE NOT FOUND")

    # valid_indices = ~np.isnan(x) & ~np.isnan(y_te) & ~np.isnan(z)
    # x = np.array(x)[valid_indices]
    # y_te = np.array(y_te)[valid_indices]
    # z = np.array(z)[valid_indices]


    x = np.array(x)
    #y_te = np.array([te or np.nan for te in y_te])

    max_length = max([len(y_sub) for y_sub in y_te])

    for i,te_sub in enumerate(y_te):
        dumb = [np.nan]*(max_length-len(te_sub)) if max_length > len(te_sub) else []
        y_te[i] += dumb
        z[i] += dumb

    # x_smooth = np.linspace(min(x),max(x),1000)
    # y_te_smooth = np.linspace(np.nanmin(y_te),np.nanmax(y_te),1000)
    
    # X_smooth, Y_te_smooth = np.meshgrid(x_smooth, y_te_smooth)
    # Y_pe_smooth = 1.6*X_smooth*Y_te_smooth

    print(len(x))
    print(len(y_te[0]))
    print(len(y_te[1]))
    print(len(y_te[2]))
    print(len(y_te[3]))
    print(len(y_te[4]))

    x = np.expand_dims(x, axis=1)

    tableX = np.tile(x, (1,len(y_te[0])))
    tableX = np.array(tableX)

    
    # tableY_te = np.reshape(y_te, (len(y_te)//len,len(x)), order='F')

    # tableZ = np.reshape(z, (len(y_te)//len(x),len(x)), order='F')

    tableY_te = np.array(y_te)

    
    # tableY_pe = 1.6*tableX*tableY_te
    tableZ = np.array(z)

    print(tableX.shape)
    print(tableY_te.shape)
    print(tableZ.shape)


    if ypar == 'te':
        contour = ax.contourf(tableX,tableY_te,tableZ, levels=20, cmap='inferno_r')
        ax.plot(tableX, tableY_te, 'bo')  # Plot the data points
        ax.contour(tableX,tableY_te,tableZ, levels=[crit_value],colors='r')
        ax.contour(tableX,tableY_te,tableZ, levels=[0.85*crit_value,1.15*crit_value],colors='r', linestyles='dashed')
        # cs = ax.contour(X_smooth, Y_te_smooth, Y_pe_smooth, levels=[0.5,1,1.5, 2],colors='k', linewidths = 1)
        ylabel, gammalabel = global_functions.get_plot_labels_gamma_profiles('teped',crit)



    elif ypar == 'pe':
        contour = ax.contourf(tableX,tableY_pe,tableZ, levels=20, cmap='inferno_r')
        ax.plot(tableX, tableY_pe, 'bo')  # Plot the data points
        ax.contour(tableX,tableY_pe,tableZ, levels=[crit_value],colors='r')
        ax.contour(tableX,tableY_pe,tableZ, levels=[0.85*crit_value,1.15*crit_value],colors='r', linestyles='dashed')
        cs = ax.contour(X_smooth, Y_pe_smooth, Y_te_smooth, levels=[0.1, 0.2, 0.3, 0.4 ,0.5],colors='k', linewidths = 1)
        ylabel, gammalabel = global_functions.get_plot_labels_gamma_profiles('peped',crit)
        #ax.set_ylim(bottom=0.6,top=2)

    #plt.clabel(cs, use_clabeltext =True, fmt='%1.1f',fontsize=8)



    nelabel, shit = global_functions.get_plot_labels_gamma_profiles('neped',crit)
    

    ax.set_xlabel(nelabel)
    ax.set_ylabel(ylabel)
    

    #fig.colorbar(contour, label=gammalabel)
    fig.tight_layout()
    plt.show()

if __name__ == '__main__':
    prefix, variations, suffix, crit, crit_value, ypar, exclud_mode, consid_mode = argument_parser()
    main(prefix, variations, suffix, crit, crit_value, ypar, exclud_mode, consid_mode)