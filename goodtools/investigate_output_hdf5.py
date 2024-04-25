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
    parser.add_argument("europed_name", help = "name of the Europed run")

    args = parser.parse_args()
    return args.europed_name

def main(europed_name):

    a = europed.EuropedHDF5(europed_name)
    print(a.get_scan_data("neped")[0])
    print(europed_analysis.density_at_tpos(europed_name))
    print(a.get_scan_data("teped")[0])
    print(a.get_scan_data("pped")[0])
    print(1.6*a.get_scan_data("neped")[0]*a.get_scan_data("teped")[0])
    print(europed_analysis.pressure_at_tpos(europed_name))
    print(a.get_scan_data("betaped")[0])



if __name__ == '__main__':
    europed_name = argument_parser()
    main(europed_name)