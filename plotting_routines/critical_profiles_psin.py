#!/usr/local/depot/Python-3.7/bin/python
# /usr/local/depot/Python-3.5.1/bin/python

from hoho import useful_recurring_functions, europed_analysis, global_functions,startup
import argparse
import matplotlib.pyplot as plt
from hoho import useful_recurring_functions, europed_hampus as europed
import numpy as np

def parse_modes(mode_str):
    return mode_str.split(',')

def argument_parser():
    """Defining comandline parser and returning the arguments"""
    parser = argparse.ArgumentParser(description = "Plots the profiles of a certain charactersitics for all width of a europed run")
    parser.add_argument("europed_names", type=useful_recurring_functions.parse_modes, help = "name of the Europed run")
    parser.add_argument("yaxises", type=useful_recurring_functions.parse_modes, help = "list of keys of the yaxis")

    parser.add_argument("-d", "--diamag", action = 'store_const', const = 'diamag', dest = 'crit', default = 'alfven', help = "normalize growth rate to diamagnetic frequency instead of Alfven frequency")

    args = parser.parse_args()
    return args.europed_names, args.yaxises, args.crit

def main(europed_names,yaxises,crit):

    n_ychar = len(yaxises)
    if n_ychar==1:
        fig,axs = plt.subplots(1,1)
    elif n_ychar==2:
        fig,axs = plt.subplots(1,2)
    elif n_ychar==3:
        fig,axs = plt.subplots(1,3)
    elif n_ychar==4:
        fig,axs = plt.subplots(2,2)

    for europed_name in europed_names:

        a = europed.EuropedHDF5(europed_name)
        psi = a.get_critical_data("psi", crit)

        for i_yaxis,yaxis in enumerate(yaxises):
            if n_ychar == 1:
                ax = axs
            elif n_ychar in [2,3]:
                ax = axs[i_yaxis]
            else:
                ax=axs[i_yaxis//2,i_yaxis%2]

            profile = a.get_critical_data(yaxis, crit)

            if i_yaxis == 0:
                ax.plot(psi, profile, label=europed_name)
                ax.legend(fontsize=8)
            else:
                ax.plot(psi, profile)
            ax.set_xlabel(r"$\psi_N$")
            y_label = global_functions.get_profiles_label(yaxis)
            ax.set_ylabel(y_label)
            ax.set_ylim(bottom=0)

    del a
    
    fig.tight_layout()
    plt.show()

if __name__ == '__main__':
    europed_names,yaxises,crit = argument_parser()
    main(europed_names,yaxises, crit)