#!/usr/local/depot/Python-3.7/bin/python3
import sys
from hoho import europed_hampus as europed
import os
import argparse

def argument_parser():
    # Defining commandline parser
    parser = argparse.ArgumentParser(description = "Modifies the given Europed inputfile with the supplied parameter-value pairs")
    parser.add_argument("filename", help = "name of the Europed inputfile")
    
    parser.add_argument("parameter", nargs='*', help = 'parameter and its value, should be on the form "parameter=value" with no spaces')
    
    args = parser.parse_args()

    # Doing manual parsing and returning values
    kwargs = {}
    for arg in args.parameter:
        kwargs[arg.split('=')[0]] = '0'

    return args.filename, kwargs

def main(inputfile, **kwargs):
    h5_file = europed.EuropedHDF5(inputfile)  
    for key in kwargs:
        print(f'{key} = {h5_file.get_input(key)}')  

if __name__ == '__main__':
    inputfile, kwargs = argument_parser()
    main(inputfile, **kwargs)


