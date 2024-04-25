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
    parser = argparse.ArgumentParser(description = "Merge two results of runs together")
    parser.add_argument("name_1", help = "name of the first file to be merged (the basis)")
    parser.add_argument("name_2", help = "name of the second file to be merged (the addition)")
    parser.add_argument("name_new", help = "name of the new run")
    parser.add_argument("profile", type=parse_modes, help= "profile(s) to be added from the second file to the first one")

    args = parser.parse_args()

    return args.name_1, args.name_2, args.name_new, args.profile


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


def merge_files(file1_path, file2_path, output_file_path, profiles):

    foldername = f"{os.environ['EUROPED_DIR']}hdf5"
    os.chdir(foldername)

    # Decompress the old and new files
    decompress_gz(file1_path)
    decompress_gz(file2_path)

    # Create a copy of the old file
    shutil.copy(file1_path +'.h5', output_file_path +'.h5')

    # Open the copied file in read-write mode
    with h5py.File(output_file_path + '.h5', 'a') as output_file, h5py.File(file1_path + '.h5', 'r') as file1, h5py.File(file2_path + '.h5', 'r') as file2:

        steps = int(file1['input']['steps'][0])
        new_steps = str(steps+len(profiles))
        new_steps_encoded = new_steps.encode('utf-8')
        del output_file['input']['steps']
        output_file['input'].create_dataset('steps', data = [new_steps_encoded])
        print(f'Number of steps in {output_file_path}: {new_steps}')
        
        for i,profile in enumerate(profiles):
            
            new_group = file2['scan'][profile]
            name_new_profile = str(steps+i)
            output_file['scan'].create_group(name_new_profile)
            for key in new_group.keys():
                new_group.copy(key, output_file['scan'][name_new_profile])

            print(f"Took profile {profile} and copied it under name '{name_new_profile}' in file {output_file_path}")

         

    # Remove temporary .h5 files
    os.remove(file1_path +'.h5')
    os.remove(file2_path +'.h5')

    # Compress the output file to .gz
    compress_to_gz(output_file_path)
    os.remove(output_file_path +'.h5')

    print(f"\n\n{output_file_path} created")


if __name__ == '__main__':
    name_1, name_2, name_merged, profile = argument_parser()
    merge_files(name_1, name_2, name_merged, profile)