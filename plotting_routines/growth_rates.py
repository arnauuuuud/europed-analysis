#!/usr/local/depot/Python-3.7/bin/python
# /usr/local/depot/Python-3.5.1/bin/python

from hoho import useful_recurring_functions, europed_analysis, global_functions, startup
import argparse
import matplotlib.pyplot as plt
import matplotlib.transforms as transforms
import math
import numpy as np

def parse_modes(mode_str):
    return mode_str.split(',')


def argument_parser():
    """Defining comandline parser and returning the arguments"""
    parser = argparse.ArgumentParser(description = "Plots the growth rate of the individual toroidal modes versus alpha for the given europed run (the growth rate is normalized to the Alfven frequency) ")
    parser.add_argument("europed_runs", type=useful_recurring_functions.parse_modes, help = "names of the Europed run to plot the modes of")
    
    parser.add_argument("-A", "--firsname", help = "first part of the names, if you want to write before the prefixes")
    parser.add_argument("-B", "--middname", help = "between prefixes and variations")
    parser.add_argument("-Z", "--lastname", type=useful_recurring_functions.parse_modes, help = "variations")


    parser.add_argument("-d", "--diamag", action = 'store_const', const = 'diamag', dest = 'crit', default = 'alfven', help = "normalize growth rate to diamagnetic frequency instead of Alfven frequency")
    parser.add_argument("-o", "--omega", action = 'store_const', const = 'omega', dest = 'crit', default = 'alfven', help = "plot omega")

    parser.add_argument("-v", "--critical_value", help= "critical value of the growth rate, default : 0.03 for alfven, 0.25 for diamagnetic")

    group = parser.add_mutually_exclusive_group()
    group.add_argument("-T", "--teped", action = 'store_const', const = 'teped', dest = 'xpar', default = 'alpha_helena_max', help = "plot versus pedestal temperature instead of alpha")
    group.add_argument("-D", "--delta", action = 'store_const', const = 'delta', dest = 'xpar', help = "plot versus width instead of alpha")
    group.add_argument("-P", "--pped", action = 'store_const', const = 'pped', dest = 'xpar', help = "plot versus pedestal pressure instead of alpha")
    group.add_argument("-p", "--peped", action = 'store_const', const = 'peped', dest = 'xpar', help = "plot versus pedestal electron pressure instead of alpha")

    parser.add_argument("-l", "--labels", type=useful_recurring_functions.parse_modes, help= "labels to display for the different Europed run prefixes")

    group = parser.add_mutually_exclusive_group()
    group.add_argument('-x',"--exclud_mode", type=useful_recurring_functions.parse_modes, help = "list of modes to exclude, comma-separated (will plot all modes except for these ones)")
    group.add_argument('-m',"--consid_mode", type=useful_recurring_functions.parse_modes, help = "list of modes to consider, comma-separated (will plot only these modes)")

    parser.add_argument("-V", "--vertical_line", action = 'store_const', const = True, dest = 'plot_vline', default=False, help = "plot vertical line")
    parser.add_argument("-H", "--horizontal_line", action = 'store_const', const = True, dest = 'plot_hline', default=False, help = "plot horizontal line")

    parser.add_argument("-s", "--same_plot", action = 'store_const', const = True, dest = 'same_plot', default=False, help = "plot everything on the same plot")


    args = parser.parse_args()

    if args.exclud_mode and args.consid_mode:
        parser.error("Arguments --exclud_mode and --consid_mode are mutually exclusive. Use one or the other.")

    if args.critical_value:
        critical_value = float(args.critical_value)
    else:
        critical_value = None

    return args.europed_runs, args.firsname, args.middname, args.lastname, args.crit, critical_value, args.labels, args.xpar, args.exclud_mode, args.consid_mode, args.plot_vline, args.plot_hline, args.same_plot


def main(europed_runs, firsname, middname, lastname, crit, crit_value, labels, x_parameter, exclud_mode, consid_mode_input, plot_vline, plot_hline, same_plot):
    
    if firsname is None:
        firsname = ''            
    if middname is None:
        middname = ''
    if lastname is None:
        lastname = ['']

    if consid_mode_input:
        consid_mode_input = sorted(consid_mode_input, key=lambda x: int(x))


    # if labels is None and lastname != ['']:
    #     labels = [europed_run + '/' + str(round(float(ln)*1,5)) + '%' for ln in lastname for europed_run in europed_runs]

    if labels is None:
        labels = europed_runs

    europed_runs = [firsname + europed_run + middname + ln for ln in lastname for europed_run in europed_runs]

    list_legends = {}


    if crit_value is None:
        if crit == "alfven":
            crit_value=0.03
        elif crit == "diamag":
            crit_value=0.25

    if not same_plot:
        nplot= len(europed_runs) 

        num_rows,num_cols = global_functions.subplots_dict[nplot]
        fig,axs = plt.subplots(num_rows,num_cols, sharex=True, sharey=True, squeeze=True)
        plt.subplots_adjust(wspace=0, hspace=0)

        for iplot,europed_run in enumerate(europed_runs):
            print(europed_run)
            ax = global_functions.get_axis_subplot(nplot, axs, iplot)

            if labels is not None:
                ax.text(0.05, 0.95, rf"{labels[iplot]}", transform=ax.transAxes,verticalalignment='top', fontsize=10)
            try:
                x_param = europed_analysis.get_x_parameter(europed_run, x_parameter)
                gammas, modes = europed_analysis.get_gammas(europed_run, crit)
                tab, consid_mode = europed_analysis.filter_tab_general(gammas, modes, consid_mode_input, exclud_mode)

                sorted_indices = np.argsort(x_param)
                x_param = x_param[sorted_indices]
                tab = tab[sorted_indices]

                def remove_wrong_slopes(tab):
                    temp_tab = tab
                    for j in range(len(temp_tab[0])):
                        for i in range(len(temp_tab)-1):
                            if temp_tab[i,j]>temp_tab[i+1,j]: 
                                for poupou in range(i+1):
                                    temp_tab[poupou,j] = None
                    return temp_tab
                
                #tab = remove_wrong_slopes(tab)
                consid_mode = sorted(consid_mode, key=lambda x: int(x))
                for i, mode in enumerate(consid_mode):
                    

                    temp_x = x_param
                    temp_y = tab[:,i]
                    nan_indices = np.isnan(temp_y)
                    x_filtered = temp_x[~nan_indices]
                    y_filtered = temp_y[~nan_indices]
                    list_legends[mode], = ax.plot(x_filtered,y_filtered,"o-",label=mode, color=global_functions.dict_mode_color[int(mode)])
                    
                if plot_vline:
                    has_unstable, x_crit, col, n = europed_analysis.find_critical(x_param, tab, consid_mode, crit_value)
                    print(n)
                    if has_unstable and x_crit:
                        ax.axvline(x_crit, color="r")

                        xmin,xmax,ymin,ymax = ax.axis()
                        ratio = (x_crit-xmin)/(xmax-xmin)

                        trans = transforms.blended_transform_factory(ax.transData, ax.transAxes)
                        x_crit_order = math.floor(math.log10(x_crit))
                        x_crit_round = np.around(np.around(x_crit*10**-x_crit_order,1)*10**x_crit_order,6)

                        ax.text(x_crit, 1.0, str(x_crit_round), color="r", horizontalalignment='center', verticalalignment='bottom',transform=trans)
            except RuntimeError:
                print(f"{europed_run:>40} RUNTIME ERROR : NO FIT FOUND")
            if plot_hline:
                ax.axhline(crit_value, linestyle="--",color="k")

            
                



        fig.legend(handles=list_legends.values(), title='n', fontsize=8)

        #fig.legend(title="n", fontsize=8, loc='upper right')

        x_label, y_label = global_functions.get_plot_labels_gamma_profiles(x_parameter, crit)

        ax_temp = axs.flatten() if isinstance(axs, np.ndarray) else np.array([ax])
        all_x_limits = np.array([axis.get_xlim() for axis in ax_temp])
        all_y_limits = np.array([axis.get_ylim() for axis in ax_temp])
        yaxis_top = np.max(all_y_limits)
        xaxis_right = np.max(all_x_limits)

        ax0 = global_functions.get_axis_subplot(nplot, axs, 0)
        ax0.set_xlim(left=0,right=xaxis_right)
        ax0.set_ylim(bottom=0,top=yaxis_top)

        if num_rows == 1 and num_cols == 1:
            axs.set_xlabel(x_label)
            axs.set_ylabel(y_label)

        elif num_rows == 1:
            axs[0].set_ylabel(y_label)
            for j in range(num_cols):
                axs[j].set_xlabel(x_label)

        else:
            for j in range(0, num_cols):
                axs[num_rows-1, j].set_xlabel(x_label)
            for i in range(0, num_rows):
                axs[i, 0].set_ylabel(y_label)




    else:
        fig, ax = plt.subplots()

        linestyles = ['solid','dashed','dotted','dashdot']
        markers = ['o','^','s','*']

        for iplot,europed_run in enumerate(europed_runs):
            try:
                x_param = europed_analysis.get_x_parameter(europed_run, x_parameter)
                gammas, modes = europed_analysis.get_gammas(europed_run, crit)
                tab, consid_mode = europed_analysis.filter_tab_general(gammas, modes, consid_mode_input, exclud_mode)

                for i, mode in enumerate(consid_mode):
                    ax.plot(x_param,tab[:,i],"o-", color=global_functions.dict_mode_color[int(mode)], linestyle = linestyles[iplot], marker = markers[iplot], label=labels[iplot] + ' - ' + str(mode))
                
                if plot_vline:
                    has_unstable, x_crit, col = europed_analysis.find_critical(x_param, tab, crit_value)
                    if has_unstable:
                        ax.axvline(x_crit, color="r")

                        xmin,xmax,ymin,ymax = ax.axis()
                        ratio = (x_crit-xmin)/(xmax-xmin)

                        trans = transforms.blended_transform_factory(ax.transData, ax.transAxes)
                        x_crit_order = math.floor(math.log10(x_crit))
                        x_crit_round = np.around(np.around(x_crit*10**-x_crit_order,1)*10**x_crit_order,6)

                        ax.text(x_crit, 1.0, str(x_crit_round), color="r", horizontalalignment='center', verticalalignment='bottom',transform=trans)
            except RuntimeError:
                print(f"{europed_run:>40} RUNTIME ERROR : NO FIT FOUND")
            if plot_hline:
                ax.axhline(crit_value, linestyle="--",color="k")

        ax.legend()
        x_label, y_label = global_functions.get_plot_labels_gamma_profiles(x_parameter, crit)
        ax.set_xlabel(x_label)

        if crit != 'omega':
            ax.set_ylim(bottom=0)
        ax.set_xlim(left=0)
    fig.tight_layout()
    plt.show()

if __name__ == '__main__':
    europed_runs, firsname, middname, lastname, crit, crit_value, labels, x_parameter, exclud_mode, consid_mode, plot_vline, plot_hline, same_plot = argument_parser()
    main(europed_runs, firsname, middname, lastname, crit, crit_value, labels, x_parameter, exclud_mode, consid_mode, plot_vline, plot_hline, same_plot)