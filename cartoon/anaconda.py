#!/usr/local/depot/Python-3.7/bin/python
# /usr/local/depot/Python-3.5.1/bin/python

from hoho import europed_analysis, global_functions,startup, find_pedestal_values
import argparse
import matplotlib.pyplot as plt
import numpy as np

def parse_modes(mode_str):
    return mode_str.split(',')

def argument_parser():
    """Defining comandline parser and returning the arguments"""
    parser = argparse.ArgumentParser(description = "Plots the profile of the critical alpha versus density shift")
    parser.add_argument("prefixes", type=parse_modes, help = "list of prefixes to construct the Europed run names")
    parser.add_argument("variations", type=parse_modes, help = "name variations of the Europed runs (the Europed runs will have the name [prefix]+[variation]{+[suffix]})  If set to 'full_list', variations=['-0.0100','-0.0050','0.0000','0.050','0.0100','0.0050','0.0150','0.0200','0.0250','0.0350','0.0400']")
    
    parser.add_argument("-d", "--diamag", action = 'store_const', const = 'diamag', dest = 'crit', default = 'alfven', help = "normalize growth rate to diamagnetic frequency instead of Alfven frequency")
    parser.add_argument("-v", "--critical_value", help= "critical value of the growth rate, default : 0.03 for alfven, 0.25 for diamagnetic")
    parser.add_argument("-l", "--labels", type=parse_modes, help= "labels to display for the different Europed run prefixes")
    parser.add_argument("-L", "--legendtitle", help= "legend title")

    parser.add_argument("-n", "--shown", action = 'store_const', const = True, dest = 'shown', default = False, help = "show critical n for each point")

    group = parser.add_mutually_exclusive_group()
    group.add_argument("-f", "--frac", action = 'store_const', const = 'frac', dest = 'plot', default = 'dshift', help = "plot versus the fraction nesep/neped instead of versus density shift")
    group.add_argument("-s", "--nesep", action = 'store_const', const = 'nesep', dest = 'plot', help = "plot versus nesep instead of versus density shift")


    group = parser.add_mutually_exclusive_group()
    group.add_argument("-T", "--teped", action = 'store_const', const = 'teped', dest = 'ypar', default = 'alpha_helena_max', help = "plot critical pedestal temperature instead of alpha")
    group.add_argument("-D", "--delta", action = 'store_const', const = 'delta', dest = 'ypar', help = "plot critical width instead of aplha")
    group.add_argument("-P", "--pped", action = 'store_const', const = 'pped', dest = 'ypar', help = "plot critical pedestal pressure instead of alpha")
    group.add_argument("-p", "--peped", action = 'store_const', const = 'peped', dest = 'ypar', help = "plot critical pedestal electron pressure instead of alpha")


    group = parser.add_mutually_exclusive_group()
    group.add_argument('-x',"--exclude_mode", type=parse_modes, help = "list of modes to exclude, comma-separated (will consider all modes except for these ones)")
    group.add_argument('-m',"--modes", type=parse_modes, help = "list of modes to consider, comma-separated (will consider only these modes)")

    args = parser.parse_args()

    if args.exclude_mode and args.modes:
        parser.error("Arguments --exclude_mode and --modes are mutually exclusive. Use one or the other.")

    critical_value = args.critical_value
    if critical_value:
        critical_value = float(args.critical_value)

    prefixes = args.prefixes
    labels = args.labels
    legendtitle = args.legendtitle
    if prefixes == ["maxieta"]:
        prefixes = global_functions.alleta_prefixes_f1 + global_functions.bees_prefixes
        labels = global_functions.alleta_labels + global_functions.bees_labels
        legendtitle = "eta"


    variations = args.variations
    if variations == ["full_list"]:
        variations = global_functions.full_list


    return prefixes, variations, args.crit, critical_value, labels, legendtitle, args.shown, args.plot, args.ypar, args.exclude_mode, args.modes


def main(prefixes, variations, crit, crit_value, labels, legendtitle, shown, plot, y_parameter, excluded_modes, considered_modes_input):

    if crit_value is None:
        if crit == "alfven":
            crit_value=0.03
        elif crit == "diamag":
            crit_value=0.25

    fig, ax = plt.subplots()

    for iprefix,prefix in enumerate(prefixes):
        list_ycrit = []
        critical_modes = []
        list_y_temp = []
        list_dshifts = []

        for dshift in variations:
            europed_run = prefix+dshift
            try:
                x_param = europed_analysis.get_x_parameter(europed_run, y_parameter)
                gammas, modes = europed_analysis.get_gammas(europed_run, crit)

                tab, considered_modes = europed_analysis.filter_tab_general(gammas, modes, considered_modes_input, excluded_modes)

                has_unstable, y_crit, i_mode = europed_analysis.find_critical(x_param, tab, crit_value)
                list_ycrit.append(y_crit)
                critical_modes.append(considered_modes[i_mode])
                list_dshifts.append(dshift)

                if plot == 'frac':
                    frac = find_pedestal_values.get_frac(europed_run, crit)
                    list_y_temp.append(frac)
                elif plot == 'nesep':
                    nesep = find_pedestal_values.get_nesep(europed_run, crit)
                    list_y_temp.append(nesep)

                print("WENT GOOD : " + europed_run)

            except FileNotFoundError:
                print(f"{europed_run:>40} FILE NOT FOUND")
                list_dshifts.append(None)
                list_ycrit.append(None)
                critical_modes.append(None)
                list_y_temp.append(None)
            except RuntimeError:
                print(f"{europed_run:>40} RUNTIME ERROR : NO FIT FOUND")
                list_dshifts.append(None)
                list_ycrit.append(None)
                critical_modes.append(None)
                list_y_temp.append(None)
            except IndexError:
                print(f"{europed_run:>40} KEY ERROR : NO FIT FOUND")
                # list_ycrit.append(None)
                # critical_modes.append(None)
                # list_y_temp.append(None)
            except TypeError:
                list_dshifts.append(None)
                list_ycrit.append(None)
                critical_modes.append(None)
                print("icicici")


        y_label = global_functions.get_critical_plot_label(y_parameter)

        if plot in ['frac','nesep']:
            list_x = [frac for frac, ycrit in zip(list_y_temp, list_ycrit) if frac is not None and y_crit is not None]
            list_y = [ycrit for frac, ycrit in zip(list_y_temp, list_ycrit) if frac is not None and y_crit is not None]
            critical_modes = [str(critmode) for critmode,y_crit, frac in zip(critical_modes,list_ycrit, list_y_temp) if y_crit is not None and frac is not None]
        elif plot == 'dshift':
            list_x = [float(dshift) for dshift,y_crit in zip(list_dshifts,list_ycrit) if y_crit is not None]
            list_y = [y_crit for y_crit in list_ycrit if y_crit is not None]   
            critical_modes = [str(critmode) for critmode,y_crit in zip(critical_modes,list_ycrit) if y_crit is not None]

        if legendtitle == "eta":
            dict_color = global_functions.dict_eta_color
        elif legendtitle == "neped":
            dict_color = global_functions.dict_neped_color

        if labels:
            label = labels[iprefix]
            if 'm2' in prefix:
                marker = 'D'
                fillstyle = 'none'
                otherlabel = " - MISHKA"
            elif 'f1' in prefix:
                marker = 'D'
                fillstyle = 'full'
                otherlabel = r" - CASTOR $n_e^{sep}/n_e^{\mathrm{ped}} = 0.15$"
            elif 'bee' in prefix:
                marker = 's'
                fillstyle = 'full'
                otherlabel = r" - CASTOR $n_e^{sep}/n_e^{\mathrm{ped}} = 0.10$"

            ax.plot(list_x, list_y, marker=marker, label=label+otherlabel, color=dict_color[label], fillstyle=fillstyle, linewidth=0)  
  
            if shown:    
                for i_critmode, critmode in enumerate(critical_modes):
                    ax.annotate(critmode, (list_x[i_critmode], list_y[i_critmode]), color=dict_color[label], textcoords="offset points", xytext=(0,5), ha='center') 
        else:
            ax.plot(list_x, list_y, 'o-')

    # Manually create a legend with custom labels
    labelstobeshown = [label for label in global_functions.bees_labels if label in labels]

    custom_legend = [plt.Line2D([0], [0], marker='o', color=dict_color[label], linewidth=0, label=label)  for label in labelstobeshown]
    legend1 = plt.legend(handles=custom_legend, fontsize=8, title = r'$\eta$', loc='lower left') 

    woo = plt.gca()

    # Add the first legend back to the axes
    woo.add_artist(legend1)

    # Manually create a legend with custom labels
    custom_legend2 = [
        plt.Line2D([0], [0], marker='D', fillstyle = 'none', linewidth=0, color='k', label=r'MISHKA $n_e^{sep}/n_e^{\mathrm{ped}} = 0.15$'),
        plt.Line2D([0], [0], marker='D', fillstyle = 'full', linewidth=0, color='k', label=r'CASTOR $n_e^{sep}/n_e^{\mathrm{ped}} = 0.15$'),
        plt.Line2D([0], [0], marker='s', fillstyle = 'full', linewidth=0, color='k', label=r'CASTOR $n_e^{sep}/n_e^{\mathrm{ped}} = 0.10$'),
        ]
    ax.legend(handles=custom_legend2, loc='lower right', fontsize=8)   

    #legend1 = plt.legend(loc='upper left')

    # Add the first legend to the axes
    #ax = plt.gca().add_artist(legend1) 


    # if labels is not None:
    #     if legendtitle == "neped":
    #         ax.legend(title=r"$n_e^{\mathrm{ped}} [10^{19}e.s^{-1}]$", fontsize=8)
    #     elif legendtitle == "eta":
    #         ax.legend(title=r"$\eta$", fontsize=8)
    #     else:
    #         ax.legend(title=legendtitle, fontsize=8)
    ax.set_ylabel(y_label)

    if plot == 'frac':
        ax.set_xlabel(r"$n_e^{sep}/n_e^{\mathrm{ped}}$")
    elif plot == 'nesep':
        ax.set_xlabel(r"$n_e^{sep}$")
    elif plot == 'dshift':
        ax.set_xlabel("Density shift")
    ax.set_ylim(bottom=0)
    fig.tight_layout()
    plt.show()

if __name__ == '__main__':
    prefixes, variations, crit, crit_value, labels, legendtitle, shown, plot, y_parameter, excluded_modes, modes = argument_parser()
    main(prefixes, variations, crit, crit_value, labels, legendtitle, shown, plot, y_parameter, excluded_modes, modes)