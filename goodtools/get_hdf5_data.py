#!/usr/local/depot/Python-3.7/bin/python
# /usr/local/depot/Python-3.5.1/bin/python

from hoho import startup, information_hdf5
import argparse
import os
import re
import math
from hoho import europed_hampus as europed
import h5py
import gzip
import tempfile
import glob

def parse_modes(mode_str):
    return mode_str.split(',')

def argument_parser():
    """Defining comandline parser and returning the arguments"""
    parser = argparse.ArgumentParser(description = "Give structure of the hds")
    parser.add_argument("europed_name", help = "name of the old run")
    parser.add_argument("list_groups", type=parse_modes, help = "list of group or datasets going down from the root of the file")

    args = parser.parse_args()
    return args.europed_name, args.list_groups

def main(europed_name, list_groups):
    pattern = os.path.join(europed_name + '.h5.gz')
    europed_run = glob.glob(pattern)[0]

    if europed_run.endswith(".gz"):
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            with gzip.open(europed_run, 'rb') as gz_file:
                tmp_file.write(gz_file.read())
                tmp_file_name = tmp_file.name
        temp = True
    else:
        tmp_file_name = europed_run
        temp = False

    with h5py.File(tmp_file_name, 'r') as hdf5_file:
        temp = hdf5_file
        for group in list_groups:
            print(group, end='/')
            temp = temp[group]
        print()
        print(temp[0])



    os.remove(tmp_file_name)



if __name__ == '__main__':
    europed_name, list_groups = argument_parser()
    main(europed_name, list_groups)