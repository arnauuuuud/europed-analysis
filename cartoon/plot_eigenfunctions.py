#!/usr/local/depot/Python-3.7/bin/python
# /usr/local/depot/Python-3.5.1/bin/python

from hoho import europed_analysis, global_functions, startup, get_eigenfunction
import argparse
import matplotlib.pyplot as plt
import matplotlib.transforms as transforms
import math
import numpy as np
from hoho import find_pedestal_values
import matplotlib.tri as tri
from scipy.spatial import Delaunay
from pylib import castor

def argument_parser():
    """Defining comandline parser and returning the arguments"""
    parser = argparse.ArgumentParser(description = "Plots the values of the growth rate gamma and the critical contour on a 2D map neped,Teped (with the alven criterion)")
    parser.add_argument("castor_name", help = "name of the castor files")
    parser.add_argument("ivar", help = "name of the helena mapping file")
    args = parser.parse_args()
    return args.castor_name, args.ivar

def main(castor_name,ivar):
    x, vec = get_eigenfunction.get_eigenfunc(castor_name, ivar)
    for func in vec:
        plt.plot(x,np.abs(func),'k')
    plt.show()

if __name__ == '__main__':
    castor_name, ivar = argument_parser()
    main(castor_name, int(ivar))
