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
import os, subprocess, glob, tempfile, gzip, h5py, re, shutil
import glob

def parse_modes(mode_str):
    return mode_str.split(',')

def decompress_gz(input_path):
    with gzip.open(input_path + '.h5.gz', 'rb') as f_in, open(input_path + '.h5', 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)

def compress_to_gz(input_path):
    with open(input_path + '.h5', 'rb') as f_in, gzip.open(input_path + '.h5.gz', 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)

def argument_parser():
    """Defining comandline parser and returning the arguments"""
    parser = argparse.ArgumentParser(description = "Give structure of the hds")
    parser.add_argument("europed_name", help = "name of the old run")
    parser.add_argument("list_groups", type=parse_modes, help = "list of group or datasets going down from the root of the file")
    parser.add_argument("new_value", help = "new value in the group")


    args = parser.parse_args()
    return args.europed_name, args.list_groups, args.new_value

def main(europed_name, list_groups, new_value):
    pattern = os.path.join(europed_name + '*')
    europed_run = glob.glob(pattern)[0]
    print(europed_name)

    foldername = f"{os.environ['EUROPED_DIR']}hdf5"
    os.chdir(foldername)

    # decompress_gz(europed_name)

    with gzip.open(europed_name + '.h5.gz', 'rb') as gz_file:
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            shutil.copyfileobj(gz_file, tmp_file)

    # Open the temporary file with h5py
    with h5py.File(tmp_file.name, 'r+') as hdf5_file:
        # Access and modify the dataset
        print("Old value")
        print(hdf5_file['input']['steps'][0])
        del hdf5_file['input']['steps']
        hdf5_file['input'].create_dataset('steps', data = [new_value.encode('utf-8')])
        print("New value")
        print(hdf5_file['input']['steps'][0])

    # Remove the original gzip file
    os.remove(europed_name + '.h5.gz')

    # Compress the modified data and save it back to the original gzip file
    with gzip.open(europed_name + '.h5.gz', 'wb') as gz_file:
        with open(tmp_file.name, 'rb') as tmp_file_content:
            shutil.copyfileobj(tmp_file_content, gz_file)

    # Remove the temporary file
    os.remove(tmp_file.name)






    # os.remove(europed_name + '.h5.gz')
    # compress_to_gz(europed_name)
    # os.remove(europed_name + '.h5')



if __name__ == '__main__':
    europed_name, list_groups, new_value = argument_parser()
    main(europed_name, list_groups, new_value)