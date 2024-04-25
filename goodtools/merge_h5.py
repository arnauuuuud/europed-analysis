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

def parse_modes(mode_str):
    return mode_str.split(',')

def argument_parser():
    """Defining comandline parser and returning the arguments"""
    parser = argparse.ArgumentParser(description = "Merge two results of runs together")
    parser.add_argument("name_1", help = "name of the old run")
    parser.add_argument("name_2", help = "name of the new run")
    parser.add_argument("name_merged", help = "name of the merged run")

    args = parser.parse_args()

    return args.name_1, args.name_2, args.name_merged


def copy_hdf5(source_file, destination_file):
    command = f'cp {source_file} {destination_file}'
    subprocess.run(command, shell=True)
    print(f'File "{source_file}" copied to "{destination_file}".')


import h5py
import gzip
import shutil
import os

def decompress_gz(input_path):
    with gzip.open(input_path + '.h5.gz', 'rb') as f_in, open(input_path + '.h5', 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)

def compress_to_gz(input_path):
    with open(input_path + '.h5', 'rb') as f_in, gzip.open(input_path + '.h5.gz', 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)


def merge_files(file1_path, file2_path, output_file_path):

    foldername = f"{os.environ['EUROPED_DIR']}output"
    os.chdir(foldername)
    shutil.copy(file1_path, output_file_path)

    foldername = f"{os.environ['EUROPED_DIR']}hdf5"
    os.chdir(foldername)

    # Decompress the old and new files
    decompress_gz(file1_path)
    decompress_gz(file2_path)

    # Create a copy of the old file
    shutil.copy(file1_path +'.h5', output_file_path +'.h5')

    # Open the copied file in read-write mode
    with h5py.File(output_file_path + '.h5', 'a') as output_file, h5py.File(file1_path + '.h5', 'r') as file1, h5py.File(file2_path + '.h5', 'r') as file2:

        list_n_1 = file1['input']['n'][0].decode('utf-8').split(',')
        list_n_2 = file2['input']['n'][0].decode('utf-8').split(',')
        list_n_merged = list(set(list_n_1 + list_n_2))
        list_n_merged = sorted(list_n_merged, key = lambda x: int(x))
        string_n_merged = str([int(i) for i in list_n_merged])[1:-1].replace(" ", "")
        string_n_merged_encoded = string_n_merged.encode('utf-8')

        del output_file['input']['n']
        output_file['input'].create_dataset('n', data = [string_n_merged_encoded])
        print(f'New list n :{string_n_merged_encoded}')

        for profile in file2['scan']:
            for stability_code in ['castor']:
                try:
                    for n in file2['scan'][profile][stability_code]:
                        # Check if the corresponding group exists in the file1
                        if profile in file1['scan'] and stability_code in file1['scan'][profile]:
                            test = True
                            try:
                                # Delete the existing 'n' group in the output file
                                del output_file['scan'][profile][stability_code][str(n)]
                            except:
                                test = False

                            # Copy the 'n' group from the new file to the old file
                            new_group = file2['scan'][profile][stability_code][str(n)]
                            output_file['scan'][profile][stability_code].create_group(str(n))
                            for key in new_group.keys():
                                new_group.copy(key, output_file['scan'][profile][stability_code][str(n)])

                            if test:
                                print(f'   {n} in profile {profile} replaced')
                            else:
                                print(f'   {n} in profile {profile} added')
                except KeyError:
                    pass

    # Remove temporary .h5 files
    os.remove(file1_path +'.h5')
    os.remove(file2_path +'.h5')

    # Compress the output file to .gz
    compress_to_gz(output_file_path)
    os.remove(output_file_path +'.h5')

    print(f"{output_file_path} created")


if __name__ == '__main__':
    name_1, name_2, name_merged = argument_parser()
    merge_files(name_1, name_2, name_merged)