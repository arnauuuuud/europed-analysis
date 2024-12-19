#!/usr/local/depot/Python-3.7/bin/python
# /usr/local/depot/Python-3.5.1/bin/python

from hoho import useful_recurring_functions, startup
import argparse
import matplotlib.pyplot as plt
from pylib.misc import ReadFile
import os
import numpy as np
from matplotlib.ticker import ScalarFormatter

def argument_parser():
    """Defining comandline parser and returning the arguments"""
    parser = argparse.ArgumentParser(description = "Plot the current profileof a HELENA file")
    parser.add_argument("europed_name", type=useful_recurring_functions.parse_modes, help = "name of the europed name")
    parser.add_argument("id", help = "id of the profile")
    args = parser.parse_args()
    return args.europed_name, args.id

def extract_from_lines(lines, eta):
    s_values = []
    p_values = []
    ready = False
    reading = False

    if eta == 'NEO':
        inline = 'SIG(neo)'
        index_neo = 6
    if eta == 'SPITZER':
        inline = 'SIG(Spitz)'
        index_neo = 5

    for line in lines:
        if 'S' in line and inline in line:
            ready = True
            pass
        elif ready and not reading and '*' in line:
            reading=True
            pass

        elif reading and len(line.split('  ')) > 0 and not '*' in line:
            elements = line.split()
            if len(elements)>=2:
                s = float(elements[0])
                p = float(elements[index_neo])
                s_values.append(s)
                p_values.append(p)
        elif reading and '*' in line or len(line.split('  ')) == 0:
            break
    return np.array(s_values),np.array(p_values)

def extract_s_and_eta(filename, eta):
    foldername = f"{os.environ['HELENA_DIR']}output"
    os.chdir(foldername)
    with open(filename, 'r') as file:
        lines = file.readlines()
        s_values, p_values = extract_from_lines(lines, eta)
    return s_values, p_values



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

def plot(filename, ax):
    psi_values, j_values = extract_s_and_eta(filename,'SPITZER')
    ax.plot(psi_values,1/j_values, label=r'$\eta_{Sp}$')
    # ax.plot(psi_values,2/j_values, label=r'$2 \eta_{Sp}$')
    psi_values, j_values = extract_s_and_eta(filename,'NEO')
    ax.plot(psi_values,1/j_values, label=r'$\eta_{Neo}$')
    ax.set_xlabel(r'$s$')
    ax.set_ylabel(r'$\eta$ [a.u.]')
    # ax.set_ylim(bottom=0)
    ax.set_xlim(left=0)
    plt.yscale('log')

def plot_frac(filename, ax):
    psi_values, j_values_Sp = extract_s_and_eta(filename,'SPITZER')
    psi_values, j_values_Neo = extract_s_and_eta(filename,'NEO')
    ax.plot(psi_values,j_values_Sp/j_values_Neo)
    ax.set_xlabel(r'$s$')
    ax.set_ylabel(r'$\eta_{neo}/\eta_{Sp}$')
    ax.set_ylim(bottom=0)
    ax.set_xlim(left=0)
    ax.axhline(2,color='k')
    ax.axhline(1,color='k')

def main(europed_name, profile):
    fig, ax = plt.subplots()

    for name in europed_name:
        runid = get_helena_filename(name)
        helena_name = f'jet84794.{runid}_{profile}'
        print(helena_name)
        
        plot_frac(helena_name, ax)
    plt.gca().yaxis.set_major_formatter(ScalarFormatter(useMathText=True))
    plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))

    plt.legend()
    plt.show()

if __name__ == '__main__':
    europed_name, profile = argument_parser()
    main(europed_name, profile)