#!/usr/local/depot/Python-3.7/bin/python3
import sys
import sys
sys.path.insert(0, '/home/jwp9427/work/python')
from hoho import useful_recurring_functions, europed_hampus as europed
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
        kwargs[arg.split('=')[0]] = arg.split('=')[1]

    return args.filename, kwargs

def main(inputfile, **kwargs):
    # Checking if name of run has been changed
    if 'run_name' in kwargs:
        if kwargs['run_name'] != inputfile:
            print("new run_name has been specified. creating new inputfile from template.")
            print(f"template = {inputfile}")
            print(f"new inputfile = {kwargs['run_name']}")
            os.system(f"cp /home/hnystrom/work/europed/input/{inputfile} /home/hnystrom/work/europed/input/{kwargs['run_name']}")
            inputfile = kwargs['run_name']
    
    # Setting parameters in inputfile
    written = europed.modify_inputfile(f"/home/hnystrom/work/europed/input/{inputfile}", **kwargs)

    # Writing information about the setting of the parameters
    if len(kwargs) > len(written):
        print("The following parameters do not exist in the inputfile:")
        for key in kwargs:
            if key not in written:
                print(f"{key}")
        print()
        
    print("The following parameters have been changed:")
    for key in written:
        print(f"{key:<16} = {kwargs[key]}")

if __name__ == '__main__':
    inputfile, kwargs = argument_parser()
    main(inputfile, **kwargs)


