#!/usr/local/depot/Python-3.7/bin/python
# /usr/local/depot/Python-3.5.1/bin/python

from hoho import useful_recurring_functions, europed_analysis, global_functions,startup, europed_hampus as europed
import argparse
import matplotlib.pyplot as plt

def argument_parser():
    """Defining comandline parser and returning the arguments"""
    parser = argparse.ArgumentParser(description = "Plots the profiles of a certain charactersitics for all width of a europed run")
    parser.add_argument("europed_name", help = "name of the Europed run")
    parser.add_argument("yaxises", type=useful_recurring_functions.parse_modes, help = "list of keys of the yaxis")

    parser.add_argument("-p",'--profiles', type=useful_recurring_functions.parse_modes, help = "list of profiles to consider")

    args = parser.parse_args()
    return args.europed_name, args.yaxises, args.profiles

def main(europed_name,yaxises,profiles_input):


    a = europed.EuropedHDF5(europed_name)
    deltas = a.get_scan_data("delta")

    n_ychar = len(yaxises)
    if n_ychar==1:
        fig,axs = plt.subplots(1,1, sharex=True)
    elif n_ychar==2:
        fig,axs = plt.subplots(1,2, sharex=True)
    elif n_ychar==3:
        fig,axs = plt.subplots(1,3, sharex=True)
    elif n_ychar==4:
        fig,axs = plt.subplots(2,2, sharex=True)

    for i_yaxis,yaxis in enumerate(yaxises):
        if n_ychar == 1:
            ax = axs
        elif n_ychar in [2,3]:
            ax = axs[i_yaxis]
        else:
            ax=axs[i_yaxis//2,i_yaxis%2]
        if yaxis == "pe":
            ne = a.get_scan_data("ne")
            te = a.get_scan_data("te")
            profiles = 1.6*ne*te
            psi_key = "psi"
        else:
            profiles = a.get_scan_data(yaxis)
            psi_key=a.PSI_KEYS[yaxis]
        psis =  a.get_scan_data(psi_key)
        
        nprofs = len(profiles)
        cmap="plasma"
        cmap = plt.get_cmap(cmap)

        for i, (psi, profile) in enumerate(zip(psis, profiles)):

            if (profiles_input is None) or str(i+1) in profiles_input:
                ax.plot(psi, profile, color = cmap(i/nprofs),label=str(round(deltas[i],3)))

        ax.set_xlabel(r"$\psi_N$")
        y_label = global_functions.get_profiles_label(yaxis)
        ax.set_ylabel(y_label)
        ax.set_ylim(bottom=0)

        if i_yaxis == 0:
            ax.legend(title="w",fontsize=6,ncol=2)

    del a
    fig.tight_layout()
    plt.show()

if __name__ == '__main__':
    europed_name,yaxises, profiles = argument_parser()
    main(europed_name,yaxises, profiles)