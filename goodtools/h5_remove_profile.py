#!/usr/local/depot/Python-3.7/bin/python
# /usr/local/depot/Python-3.5.1/bin/python

from hoho import europed_analysis, global_functions, startup
import argparse
import matplotlib.pyplot as plt
import matplotlib.transforms as transforms
import math
import numpy as np
import matplotlib.tri as tri
import os, subprocess, glob, tempfile, gzip, h5py, re, shutil
import h5py
import gzip
import shutil
import os

def parse_modes(mode_str):
    return mode_str.split(',')

def argument_parser():
    """Defining comandline parser and returning the arguments"""
    parser = argparse.ArgumentParser(description = "Supress profile from hdf5")
    parser.add_argument("old_name", help = "old name of the run")
    parser.add_argument("new_name", help = "new name of the run")
    parser.add_argument("profile", type=parse_modes, help= "list of profiles to suppress")

    parser.add_argument("--modes", "-n", type=parse_modes, help= "modes to be removed in the corresponding profiles")

    args = parser.parse_args()

    return args.old_name, args.new_name, args.profile, args.modes


def copy_hdf5(source_file, destination_file):
    command = f'cp {source_file} {destination_file}'
    subprocess.run(command, shell=True)
    print(f'File "{source_file}" copied to "{destination_file}".')


def decompress_gz(input_path):
    with gzip.open(input_path + '.h5.gz', 'rb') as f_in, open(input_path + '.h5', 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)

def compress_to_gz(input_path):
    with open(input_path + '.h5', 'rb') as f_in, gzip.open(input_path + '.h5.gz', 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)


def merge_files(old_name, new_name, profiles, modes):

    foldername = f"{os.environ['EUROPED_DIR']}output"
    os.chdir(foldername)
    #shutil.copy(old_name, new_name)

    foldername = f"{os.environ['EUROPED_DIR']}hdf5"
    os.chdir(foldername)

    # Decompress the old file
    decompress_gz(old_name)

    # Create a copy of the old file
    shutil.copy(old_name +'.h5', new_name +'.h5')

    # Open the copied file in read-write mode
    with h5py.File(new_name + '.h5', 'a') as output_file:
        if not modes:
            for profile in profiles:
                stability_code = 'castor'
                del output_file['scan'][profile]
                print(f"Profile {profile}  deleted from {new_name}")

        else:
            for profile in profiles:
                stability_code = 'castor'
                for mode in modes:
                    try:
                        del output_file['scan'][profile][stability_code][mode]
                        print(f"Mode {mode} in profile {profile}  deleted from {new_name}") 
                    except KeyError:
                        print(f"No mode {mode} in profile {profile}")           

    # Remove temporary .h5 files
    os.remove(old_name +'.h5')

    # Compress the output file to .gz
    compress_to_gz(new_name)
    os.remove(new_name +'.h5')

    print(f"\n\n{new_name} created")


if __name__ == '__main__':
    old_name, new_name, profile, modes = argument_parser()
    merge_files(old_name, new_name, profile, modes)