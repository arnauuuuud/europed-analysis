#!/usr/local/depot/Python-3.7/bin/python
# /usr/local/depot/Python-3.5.1/bin/python

from hoho import europed_analysis, global_functions, startup, useful_recurring_functions, h5_manipulation
import argparse
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.tri as tri
import h5py

def argument_parser():
    """Defining comandline parser and returning the arguments"""
    parser = argparse.ArgumentParser(description = "Plots the values of the growth rate gamma and the critical contour on a 2D map neped,Teped (with the alven criterion)")
    parser.add_argument("europed_name", help = "Europed run")
    parser.add_argument("delta", help = "name variations of the Europed runs")

    args = parser.parse_args()

    return args.europed_name, args.delta

def main(europed_name, delta):

    list_n = []
    list_gamma = []
    list_gamma_diam = []

    delta = float(delta)

    h5_manipulation.decompress_gz(europed_name)
    with h5py.File(f'{europed_name}.h5', 'a') as h5file:
        profile = h5_manipulation.find_profile_with_delta_file(h5file, delta)

        print(profile)
        for key in h5file['scan'][profile]['castor'].keys():
            n = h5file['scan'][profile]['castor'][key]['n'][0]
            try:
                gamma = h5file['scan'][profile]['castor'][key]['gamma'][0]
                gamma_diam = h5file['scan'][profile]['castor'][key]['gamma_diam'][0]
            except KeyError:
                continue
            list_n.append(n)
            list_gamma.append(gamma)
            list_gamma_diam.append(gamma_diam)
    h5_manipulation.removedoth5(europed_name)


    fig,ax = plt.subplots()
    ax.scatter(list_n,list_gamma)
    ax.set_xlim(left=0, right=50)
    ax.set_ylim(bottom=0)
    plt.show()

if __name__ == '__main__':
    europed_name, profile = argument_parser()
    main(europed_name, profile)