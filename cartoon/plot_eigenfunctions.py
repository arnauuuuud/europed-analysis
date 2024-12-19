#!/usr/local/depot/Python-3.7/bin/python
# /usr/local/depot/Python-3.5.1/bin/python

from hoho import useful_recurring_functions, europed_analysis, global_functions, startup, get_eigenfunction
import argparse
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter


def argument_parser():
    """Defining comandline parser and returning the arguments"""
    parser = argparse.ArgumentParser(description = "Plots the values of the growth rate gamma and the critical contour on a 2D map neped,Teped (with the alven criterion)")
    parser.add_argument("castor_names", type=useful_recurring_functions.parse_modes, help = "name of the castor files")
    parser.add_argument("ivar", help = "name of the helena mapping file")
    args = parser.parse_args()
    return args.castor_names, args.ivar

def moving_average(data, window_size):
    weights = np.repeat(1.0, window_size) / window_size
    return np.convolve(data, weights, 'valid')


def main(castor_names,ivar):

    sample_points = np.linspace(0.3, 1, len(castor_names))
    colors = plt.cm.inferno_r(sample_points)

    for i,castor_name in enumerate(castor_names):
        x, vec = get_eigenfunction.get_eigenfunc(castor_name, ivar)
        vec = np.array(vec)
        x = np.array(x)
        print(len(x))
        # if len(castor_names) == 1:
        #     for func in vec:
        #         plt.plot(x,np.abs(func),'k')
        # else:
        #     y = np.abs(np.max(vec,axis=0))/np.abs(np.max(vec))
        #     y = np.abs(np.max(vec,axis=0))/np.abs(np.max(vec))
        #     y_smooth = moving_average(y,50)
        #     plt.plot(x[49:],y_smooth, label=castor_name, color=colors[i])   
        for func in vec:
            plt.plot(x,np.abs(func)/np.max(vec),'k')
        # y = np.abs(np.max(vec,axis=0))/np.abs(np.max(vec))
        # y = np.abs(np.max(vec,axis=0))/np.abs(np.max(vec))
        # y_smooth = moving_average(y,50)
        # plt.plot(x[49:],y_smooth, label=castor_name, color=colors[i])

    plt.legend()
    plt.show()

if __name__ == '__main__':
    castor_names, ivar = argument_parser()
    main(castor_names, int(ivar))
