#!/usr/local/depot/Python-3.7/bin/python
# /usr/local/depot/Python-3.5.1/bin/python

from hoho import startup
import argparse
import matplotlib.pyplot as plt
import matplotlib.transforms as transforms
import math
import numpy as np
import matplotlib.tri as tri
import os


def argument_parser():
    """Defining comandline parser and returning the arguments"""
    parser = argparse.ArgumentParser(description = "Plot the current profileof a HELENA file")
    parser.add_argument("helena_name", help = "name of the HELENA output file to plot the current profile of")

    args = parser.parse_args()
    return args.helena_name



def extract_psi_and_j(filename):
    foldername = f"{os.environ['HELENA_DIR']}output"
    os.chdir(foldername)

    psi_values = []
    j_values = []

    ready1 = False
    ready2 = False

    s = False

    with open(filename, 'r') as file:
        lines = file.readlines()
        for line in lines:

            if 'PSI' in line and '<J>' in line:
                print(line, end=' ')
                ready1 = True
                pass

            if 'S' in line and 'AVERAGE JPHI' in line:
                print(line, end=' ')
                ready1 = True
                s = True
                pass

            if ready1 and '*****' in line:
                print(line, end=' ')
                ready2 = True
                ready1 = False
                pass
            
            elif ready2 and '*****' in line:
                print(line, end=' ')
                ready2 = False
                break

            elif ready2 and '*****' not in line and not s:
                print(line, end=' ')
                elements = line.split()
                psi = float(elements[1])
                j = float(elements[3])
                psi_values.append(psi)
                j_values.append(j)

            elif ready2 and '*****' not in line and s:
                print(line, end=' ')
                elements = line.split()
                if len(elements)>=2:
                    psi = float(elements[0])**2
                    j = float(elements[1])
                    psi_values.append(psi)
                    j_values.append(j)

    return psi_values,j_values


def main(filename):

    fig, ax = plt.subplots()

    psi_values, j_values = extract_psi_and_j(filename)

    ax.plot(psi_values,j_values)
    ax.set_xlabel(r'$\psi_N$')
    ax.set_ylabel(r'$\left< J \right>$ [a.u.]')

    plt.show()


if __name__ == '__main__':
    helena_name = argument_parser()
    main(helena_name)