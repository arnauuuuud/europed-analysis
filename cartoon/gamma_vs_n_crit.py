#!/usr/local/depot/Python-3.7/bin/python
# /usr/local/depot/Python-3.5.1/bin/python

from hoho import europed_analysis, global_functions, startup, useful_recurring_functions, h5_manipulation, europed_analysis_2
import argparse
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.tri as tri
import h5py

def argument_parser():
    """Defining comandline parser and returning the arguments"""
    parser = argparse.ArgumentParser(description = "Plots the values of the growth rate gamma and the critical contour on a 2D map neped,Teped (with the alven criterion)")
    parser.add_argument("europed_name", help = "Europed run")
    parser.add_argument("crit", help = "name variations of the Europed runs")
    parser.add_argument("crit_value", help = "name variations of the Europed runs")

    args = parser.parse_args()

    return args.europed_name, args.crit, args.crit_value

def main(europed_name, crit, crit_value):

    crit_value = float(crit_value)
    x_param = 'alpha_helena_max'

    dict_gamma = europed_analysis_2.get_gammas(europed_name, crit=crit)
    list_n = europed_analysis_2.list_n_from_dict(dict_gamma)
    res = []

    for n in list_n:
        cv = europed_analysis_2.critical_value_europed_name(europed_name, crit, crit_value, x_param, list_consid_mode=[n])
        res.append(cv)


    fig,ax = plt.subplots()
    ax.scatter(list_n,res)
    # ax.set_xlim(left=0, right=51)
    ax.set_xscale('log')

    ax.set_ylim(bottom=0)
    plt.show()

if __name__ == '__main__':
    europed_name, crit, crit_value = argument_parser()
    main(europed_name, crit, crit_value)