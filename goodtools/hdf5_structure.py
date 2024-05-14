#!/usr/local/depot/Python-3.7/bin/python
# /usr/local/depot/Python-3.5.1/bin/python

from hoho import useful_recurring_functions, startup, information_hdf5
import argparse
import matplotlib.pyplot as plt
import matplotlib.transforms as transforms
import math
import numpy as np
import matplotlib.tri as tri

def parse_modes(mode_str):
    return mode_str.split(',')

def argument_parser():
    """Defining comandline parser and returning the arguments"""
    parser = argparse.ArgumentParser(description = "Give structure of the hds")
    parser.add_argument("europed_name", help = "name of the old run")

    args = parser.parse_args()
    return args.europed_name

if __name__ == '__main__':
    europed_name = argument_parser()
    information_hdf5.get_structure(europed_name)