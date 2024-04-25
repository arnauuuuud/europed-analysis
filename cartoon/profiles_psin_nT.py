#!/usr/local/depot/Python-3.7/bin/python
# /usr/local/depot/Python-3.5.1/bin/python

from hoho import europed_analysis, global_functions,startup
import argparse
import matplotlib.pyplot as plt
from hoho import europed_hampus as europed
import numpy as np

def parse_modes(mode_str):
    return mode_str.split(',')

def argument_parser():
    """Defining comandline parser and returning the arguments"""
    parser = argparse.ArgumentParser(description = "Plots the profiles of a certain charactersitics for all width of a europed run")
    parser.add_argument("europed_names", type=parse_modes, help = "name of the Europed run")
    parser.add_argument("-l",'--labels', type=parse_modes, help = "list of labels to consider")

    args = parser.parse_args()
    print(args.europed_names, args.labels)
    return args.europed_names, args.labels

def main(europed_names,labels):



    n_plot = len(europed_names)
    if n_plot==1:
        fig,axs = plt.subplots(1,1, sharex=True, sharey=True)
    elif n_plot==2:
        fig,axs = plt.subplots(1,2, sharex=True, sharey=True)
    elif n_plot==3:
        fig,axs = plt.subplots(1,3, sharex=True, sharey=True)
    elif n_plot==4:
        fig,axs = plt.subplots(2,2, sharex=True, sharey=True)
    elif n_plot==6:
        fig,axs = plt.subplots(2,3, sharex=True, sharey=True)

    for i_plots,europed_name in enumerate(europed_names):
        
        a = europed.EuropedHDF5(europed_name)
        
        if n_plot == 1:
            ax = axs
        elif n_plot in [2,3]:
            ax = axs[i_plots]
        elif n_plot == 4:
            ax=axs[i_plots//2,i_plots%2]
        elif n_plot == 6:
            ax=axs[i_plots//3,i_plots%3]

        ne = a.get_critical_data("ne")
        te = a.get_critical_data("te")
        psi =  a.get_critical_data("psi")
        

        if labels is not None:
            ax.text(0.05, 0.95, rf"{labels[i_plots]}", transform=ax.transAxes,verticalalignment='top', fontsize=10)

        ax2 = ax.twinx()

        line1, = ax.plot(psi, ne, color = 'C0',label=r'$n_e$')
        line2, = ax2.plot(psi, te, color = 'C1',label=r'$T_e$')

        ax.set_xlabel(r"$\psi_N$")

        ax.set_ylabel(global_functions.get_profiles_label('ne'))
        ax.set_ylim(bottom=0)

        ax2.set_ylabel(global_functions.get_profiles_label('te'))
        ax2.set_ylim(bottom=0, top=10/8)

        lines = [line1, line2]
        labels_temp = [line.get_label() for line in lines]
        ax.legend(lines, labels_temp)


        del a
    
    fig.tight_layout()
    plt.show()

if __name__ == '__main__':
    europed_name, labels = argument_parser()
    main(europed_name, labels)