#!/usr/local/depot/Python-3.7/bin/python
# /usr/local/depot/Python-3.5.1/bin/python

from hoho import useful_recurring_functions, europed_analysis, global_functions, startup, get_eigenfunction
import argparse
import matplotlib.pyplot as plt
import matplotlib.transforms as transforms
import math
import numpy as np
from hoho import useful_recurring_functions, find_pedestal_values_old
import matplotlib.tri as tri
from scipy.spatial import Delaunay
from pylib import castor

def argument_parser():
    """Defining comandline parser and returning the arguments"""
    parser = argparse.ArgumentParser(description = "Plots the values of the growth rate gamma and the critical contour on a 2D map neped,Teped (with the alven criterion)")
    parser.add_argument("castor_name", help = "name of the castor files")
    parser.add_argument("helena_name", help = "name of the castor files")
    parser.add_argument("ivar", help = "name of the helena mapping file")
    args = parser.parse_args()
    return args.castor_name, args.helena_name, args.ivar 
 
def main(castor_name, helena_name, ivar, phase = 0, levels = 30, ax = None, **plt_kwargs):
    """
    Contour plot of MISHKA/CASTOR data in poloidal cross section.
    
    Arguments
        data : dictionary
    Device is used to determine minor and major radius. 
    """

    fig,ax = plt.subplots(figsize=(4,8))
    a = castor.CastorData(castor_name,castor_name,helena_name)

    xx, yy, var = a.get_cont(ivar, 'JET', phase)
    ax.set_xlabel('R [m]')
    ax.set_ylabel('Z [m]')
    contour = ax.contourf(xx, yy, var, levels, cmap='seismic')
    ax.set_aspect('equal', 'box')
    #plt.colorbar(contour, ax = ax)
    plt.show()

if __name__ == '__main__':
    castor_name, helena_name, ivar = argument_parser()
    main(castor_name, helena_name, int(ivar))