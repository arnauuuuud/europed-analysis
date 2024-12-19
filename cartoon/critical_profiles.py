#!/usr/local/depot/Python-3.7/bin/python
# /usr/local/depot/Python-3.5.1/bin/python

from hoho import useful_recurring_functions, europed_analysis, global_functions,startup, pedestal_values
import argparse
import matplotlib.pyplot as plt
import numpy as np
from hoho import useful_recurring_functions, europed_hampus as europed

def argument_parser():
    """Defining comandline parser and returning the arguments"""
    parser = argparse.ArgumentParser(description = "Plots the profiles of a certain charactersitics for all width of a europed run")
    parser.add_argument("europed_names", type=useful_recurring_functions.parse_modes, help = "name of the Europed run")

    parser.add_argument("-d", "--diamag", action = 'store_const', const = 'diamag', dest = 'crit', default = 'alfven', help = "normalize growth rate to diamagnetic frequency instead of Alfven frequency")
    parser.add_argument("-v", "--critical_value", help= "critical value of the growth rate, default : 0.03 for alfven, 0.25 for diamagnetic")

    parser.add_argument('-x',"--exclud_mode", type=useful_recurring_functions.parse_modes, help = "list of modes to exclude, comma-separated (will plot all modes except for these ones)")


    args = parser.parse_args()
    return args.europed_names, args.crit, args.critical_value, args.exclud_mode

def main(europed_names, crit, crit_value, exclud_modes):
    crit_value = float(crit_value)
    fig, axs = plt.subplots(1,3)

    psis = np.linspace(0,1,100)

    for europed_name in europed_names:
        try:
            is_fw = europed_name.startswith('fw')
            te_profile, ne_profile = pedestal_values.create_profiles(europed_name, psis, crit=crit, crit_value=crit_value, exclud_mode = exclud_modes, fixed_width=is_fw)
            pe_profile = 1.6 * ne_profile * te_profile

            axs[0].plot(psis, ne_profile)
            axs[1].plot(psis, te_profile)
            axs[2].plot(psis, pe_profile)
        except TypeError:
            pass


    axs[0].set_xlabel(global_functions.psiN_label)
    axs[1].set_xlabel(global_functions.psiN_label)
    axs[2].set_xlabel(global_functions.psiN_label)
    axs[0].set_ylabel(global_functions.ne_label)
    axs[1].set_ylabel(global_functions.te_label)
    axs[2].set_ylabel(global_functions.pe_label)

    axs[0].set_xlim(left=0.85, right=1)
    axs[1].set_xlim(left=0.85, right=1)
    axs[2].set_xlim(left=0.85, right=1)

    axs[0].set_ylim(bottom=0)
    axs[1].set_ylim(bottom=0)
    axs[2].set_ylim(bottom=0)


    fig.tight_layout()
    plt.show()

if __name__ == '__main__':
    europed_names, crit, crit_value, exclud_modes = argument_parser()
    main(europed_names, crit, crit_value, exclud_modes)