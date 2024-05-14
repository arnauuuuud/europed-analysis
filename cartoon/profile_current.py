#!/usr/local/depot/Python-3.7/bin/python
# /usr/local/depot/Python-3.5.1/bin/python

from hoho import useful_recurring_functions, startup
import argparse
import matplotlib.pyplot as plt
import matplotlib.transforms as transforms
import math
from pylib.misc import ReadFile
import numpy as np
import matplotlib.tri as tri
import os

def parse_modes(mode_str):
    return mode_str.split(',')



def argument_parser():
    """Defining comandline parser and returning the arguments"""
    parser = argparse.ArgumentParser(description = "Plot the current profileof a HELENA file")
    parser.add_argument("europed_name", type=useful_recurring_functions.parse_modes, help = "name of the europed name")
    parser.add_argument("id", help = "id of the profile")


    args = parser.parse_args()
    return args.europed_name, args.id



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
                # print(line, end=' ')
                ready1 = True
                pass

            if 'S' in line and 'AVERAGE JPHI' in line:
                # print(line, end=' ')
                ready1 = True
                s = True
                pass

            if ready1 and '*****' in line:
                # print(line, end=' ')
                ready2 = True
                ready1 = False
                pass
            
            elif ready2 and '*****' in line:
                # print(line, end=' ')
                ready2 = False
                break

            elif ready2 and '*****' not in line and not s:
                # print(line, end=' ')
                elements = line.split()
                psi = float(elements[1])
                j = float(elements[3])
                psi_values.append(psi)
                j_values.append(j)

            elif ready2 and '*****' not in line and s:
                # print(line, end=' ')
                elements = line.split()
                if len(elements)>=2:
                    psi = float(elements[0])**2
                    j = float(elements[1])
                    psi_values.append(psi)
                    j_values.append(j)

    return psi_values,j_values


def plot(filename, ax, name):

    

    psi_values, j_values = extract_psi_and_j(filename)

    ax.plot(psi_values,j_values, label=name)
    ax.set_xlabel(r'$\psi_N$')
    ax.set_ylabel(r'$\left< J \right>$ [a.u.]')

    

def get_helena_filename(europed_name):
    filepath = europed_name
    if '/' not in filepath:
        filepath = f"{os.environ['EUROPED_DIR']}output/{filepath}"
    with ReadFile(filepath) as f:
        for line in f.readlines():
            if line.startswith('run id:'):
                runid = line.split(': ')[1]
                if runid.endswith('\n'):
                    runid = runid[:-1]
                return runid
            else:
                continue


def main(europed_name, profile):
    fig, ax = plt.subplots()

    for name in europed_name:

        runid = get_helena_filename(name)
        helena_name = f'jet84794.{runid}_{profile}.out'
        print(helena_name)
        
        plot(helena_name, ax, name)
    plt.legend()
    plt.show()

if __name__ == '__main__':
    europed_name, profile = argument_parser()
    main(europed_name, profile)