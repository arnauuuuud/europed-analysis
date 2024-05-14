#!/usr/local/depot/Python-3.7/bin/python
# /usr/local/depot/Python-3.5.1/bin/python

from hoho import useful_recurring_functions, europed_analysis, global_functions,startup
import argparse
import matplotlib.pyplot as plt
from hoho import useful_recurring_functions, europed_hampus as europed

def argument_parser():
    """Plot a characteristic for one given density shift at different neped"""
    parser = argparse.ArgumentParser(description = "Plot a characteristic for one given density shift at different neped")

    parser.add_argument("prefix", help = "Europed prefix")
    parser.add_argument("nepeds", type=useful_recurring_functions.parse_modes, help = "List of neped")
    parser.add_argument("suffix", help = "Suffix of the name, including density shift")

    parser.add_argument("-d", "--diamag", action = 'store_const', const = 'diamag', dest = 'crit', default = 'alfven', help = "normalize growth rate to diamagnetic frequency instead of Alfven frequency")
    parser.add_argument("-v", "--critical_value", help= "critical value of the growth rate, default : 0.03 for alfven, 0.25 for diamagnetic")

    group = parser.add_mutually_exclusive_group()
    group.add_argument("-T", "--teped", action = 'store_const', const = 'teped', dest = 'ypar', default = 'alpha_helena_max', help = "plot pedestal temperature instead of alpha")
    group.add_argument("-D", "--delta", action = 'store_const', const = 'delta', dest = 'ypar', help = "plot width instead of alpha")
    group.add_argument("-P", "--pped", action = 'store_const', const = 'pped', dest = 'ypar', help = "plot pedestal pressure instead of alpha")

    parser.add_argument("-n", "--shown", action = 'store_const', const = True, dest = 'shown', default = False, help = "show critical n for each point")

    args = parser.parse_args()

    critical_value = args.critical_value
    if critical_value:
        critical_value = float(args.critical_value)

    return args.prefix, args.nepeds, args.suffix, args.ypar, args.crit, critical_value, args.shown

def main(prefix, nepeds, suffix, y_parameter, crit, crit_value, sown):
    if crit_value is None:
        if crit == "alfven":
            crit_value=0.03
        elif crit == "diamag":
            crit_value=0.25

    fig, ax = plt.subplots()

    list_ycrit = []
    list_neped = []
    critical_modes = []

    for ineped,neped in enumerate(nepeds):        
        europed_run = prefix + neped + suffix
        list_neped.append(float(neped))
        try:
            x_param = europed_analysis.get_x_parameter(europed_run, y_parameter)
            gammas, modes = europed_analysis.get_gammas(europed_run, crit)
            has_unstable, y_crit, icritn = europed_analysis.find_critical(x_param, gammas, crit_value)
            list_ycrit.append(y_crit)
            critical_modes.append(modes[icritn])
        except FileNotFoundError:
            print(f"{europed_run:>40} FILE NOT FOUND")
            list_ycrit.append(None)
            critical_modes.append(None)
        except TypeError:
            list_ycrit.append(None)
            critical_modes.append(None)

    ax.plot(list_neped, list_ycrit, 'o-')
    if shown:    
        for i_critmode, critmode in enumerate(critical_modes):
            ax.annotate(critmode, (list_neped[i_critmode], list_ycrit[i_critmode]), textcoords="offset points", xytext=(0,5), ha='center') 

    ax.set_xlabel(r"$n_e^{\mathrm{ped}} [10^{19}e.m^{-3}]$")
    y_label = global_functions.get_critical_plot_label(y_parameter)
    ax.set_ylabel(y_label)
    ax.set_ylim(bottom=0)
    fig.tight_layout()
    plt.show()


if __name__ == '__main__':
    prefix, nepeds, suffix, ypar, crit, critical_value, shown = argument_parser()
    main(prefix, nepeds, suffix, ypar, crit, critical_value, shown)