#!/usr/local/depot/Python-3.7/bin/python
# /usr/local/depot/Python-3.5.1/bin/python

from hoho import startup
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
    parser.add_argument("europed_name", type=parse_modes, help = "name of the europed name")
    parser.add_argument("id", help = "id of the profile")


    args = parser.parse_args()
    return args.europed_name, args.id



def extract_psi_and_j(filename):
    foldername = f"{os.environ['HELENA_DIR']}output"
    os.chdir(foldername)

    s_values = []
    p_values = []

    ready = False
    reading = False


    with open(filename, 'r') as file:
        lines = file.readlines()
        for line in lines:


            if 'S' in line and 'P [Pa]' in line:
                print(line, end=' ')
                ready = True
                pass

            elif ready and not reading and '*' in line:
                reading=True
                pass

            elif reading and '*' not in line:
                print(line, end=' ')
                elements = line.split()
                if len(elements)>=2:
                    s = float(elements[0])
                    p = float(elements[1])
                    s_values.append(s)
                    p_values.append(p)

            elif reading and '*' in line:
                break

    return s_values,p_values


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