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
    parser.add_argument("name_1", help = "name of the old run")
    parser.add_argument("name_2", help = "name of the new run")
    parser.add_argument("name_merged", help = "name of the merged run")
    parser.add_argument("n", type=parse_modes, help = "toroidal mode number")
    parser.add_argument("delta", type=parse_modes, help= "delta (pedestal width)")

    args = parser.parse_args()

    return args.name_1, args.name_2, args.name_merged, args.n, args.delta


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


def merge_files(file1_path, file2_path, output_file_path, n_tomerge, deltas):

    # foldername = f"{os.environ['EUROPED_DIR']}output"
    # os.chdir(foldername)
    # shutil.copy(file1_path, output_file_path)

    foldername = f"{os.environ['EUROPED_DIR']}hdf5"
    os.chdir(foldername)

    # Decompress the old and new files
    decompress_gz(file1_path)
    decompress_gz(file2_path)

    # Create a copy of the old file
    shutil.copy(file1_path +'.h5', output_file_path +'.h5')

    # Open the copied file in read-write mode
    with h5py.File(output_file_path + '.h5', 'a') as output_file, h5py.File(file1_path + '.h5', 'r') as file1, h5py.File(file2_path + '.h5', 'r') as file2:

        for n in n_tomerge:
            for delta in deltas:
                found1, found2 = False, False
                i1,i2 = 0,0
                while not found1:
                    if file1['scan'][str(i1)]['delta'][0] == np.float32(delta):
                        found1 = True
                    else:
                        i1 += 1
                while not found2:
                    if file2['scan'][str(i2)]['delta'][0] == np.float32(delta):
                        found2 = True
                    else:
                        i2 += 1
                
                i1 = str(i1)
                i2 = str(i2)

                stability_code = 'castor'
                try:
                    del output_file['scan'][i1][stability_code][str(n)]
                except KeyError:
                    print(f'No mode {n} in profile {i1} of original file')
                
                try:
                    new_group = file2['scan'][i2][stability_code][str(n)]

                    try:
                        output_file['scan'][i1][stability_code].create_group(str(n))
                    except KeyError:
                        output_file['scan'][i1].create_group(stability_code)
                        output_file['scan'][i1][stability_code].create_group(str(n))

                    for key in new_group.keys():
                        new_group.copy(key, output_file['scan'][i1][stability_code][str(n)])

                    print(f"Merging of n {n}, delta {delta}: took profile {i2} from {file2_path} and copied it in profile {i1} of {output_file_path}")
                except KeyError:
                    print(f'No mode {n} in profile {i1} of the new file')
         

    # Remove temporary .h5 files
    os.remove(file1_path +'.h5')
    os.remove(file2_path +'.h5')

    # Compress the output file to .gz
    compress_to_gz(output_file_path)
    os.remove(output_file_path +'.h5')

    print(f"\n\n{output_file_path} created")


if __name__ == '__main__':
    name_1, name_2, name_merged, n, delta = argument_parser()
    merge_files(name_1, name_2, name_merged, n, delta)