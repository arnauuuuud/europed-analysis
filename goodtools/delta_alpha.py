#!/usr/local/depot/Python-3.7/bin/python
# /usr/local/depot/Python-3.5.1/bin/python

from hoho import europed_analysis, global_functions, startup
import argparse
import matplotlib.pyplot as plt
import matplotlib.transforms as transforms
import math
import numpy as np
import matplotlib.tri as tri
import os, subprocess, glob, tempfile, gzip, h5py, re, shutil
import h5py
import gzip
import shutil
import os

def parse_modes(mode_str):
    return mode_str.split(',')

def argument_parser():
    """Defining comandline parser and returning the arguments"""
    parser = argparse.ArgumentParser(description = "Merge two results of runs together")
    parser.add_argument("name", help = "name of the old run")

    args = parser.parse_args()

    return args.name

def main(europed_run):
    deltas = europed_analysis.get_x_parameter(europed_run, 'delta')
    alphas = europed_analysis.get_x_parameter(europed_run, 'alpha_helena_max')

    alphas = np.array(alphas)

    index = np.argmin(np.abs(alphas-6))
    print(alphas[index-1:index+2])
    print(deltas[index-1:index+2])

 


if __name__ == '__main__':
    name = argument_parser()
    main(name)