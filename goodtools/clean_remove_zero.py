#!/usr/local/depot/Python-3.7/bin/python
# /usr/local/depot/Python-3.5.1/bin/python
import argparse
from hoho import useful_recurring_functions, h5_manipulation
import numpy as np
import os
import h5py
import shutil

#####################################################################
def argument_parser():
    """Defining comandline parser and returning the arguments"""
    parser = argparse.ArgumentParser(description = "Append file to the waiting list")
    parser.add_argument("list_name", type=useful_recurring_functions.parse_modes, help = "file name list to append to the waiting list")
    
    args = parser.parse_args()
    return args.list_name
    

def copy_original_file(original_name):
    foldername = f"{os.environ['EUROPED_DIR']}hdf5"
    os.chdir(foldername)
    latest_version = h5_manipulation.get_latest_version(original_name)
    this_version = latest_version+1
    new_name = f'{original_name}_{this_version}_beforecleaningprocess'
    h5_manipulation.decompress_gz(original_name)
    shutil.copy(original_name +'.h5', new_name +'.h5')
    h5_manipulation.compress_to_gz(new_name)
    print(f'Old version of {original_name} is now named {new_name}')

def create_list_delta(europed_name):
    delta_max = h5_manipulation.get_data(europed_name, ['input','delta_max'])
    delta_min = h5_manipulation.get_data(europed_name, ['input','delta_min'])
    steps = h5_manipulation.get_data(europed_name, ['input','steps'])
    deltas = np.linspace(delta_min, delta_max, steps)
    return deltas


def remove_for_given_n(europed_name, n, threshold=1e-4):
    steps = h5_manipulation.get_data_decrompressed(europed_name, ['input','steps'])
    for profile in range(steps):
        try:
            gamma = h5_manipulation.get_data_decrompressed(europed_name, ['scan', str(profile), 'castor', str(n), 'gamma'])
        except KeyError:
            continue    
        if gamma<threshold:
            pop_profile_n(europed_name, profile, n)


    # for delta in deltas:
    #     try:
    #         profile = h5_manipulation.find_profile_with_delta(europed_name, delta)
    #     except useful_recurring_functions.CustomError:
    #         continue
    #     try:
    #         gamma = h5_manipulation.get_data(europed_name, ['input', str(profile), 'castor', str(n), 'gamma'])
    #     except KeyError:
    #         continue
    #     if gamma < threshold:
    #         pop_profile_n(europed_name, profile, n)


def pop_profile_n(europed_name, profile, n):
    with h5py.File(europed_name + '.h5', 'a') as original_file:
        del original_file['scan'][str(profile)]['castor'][n]
        print(f'Profile {profile} n {n} removed from {europed_name}')



def main(filename_list):
    for filename in filename_list:
        # deltas = create_list_delta(filename)
        copy_original_file(filename)
        for n in [1, 2, 3, 4, 5, 7, 10, 20, 30, 40, 50]:
            remove_for_given_n(filename, str(n))
        h5_manipulation.compress_to_gz(filename)



if __name__ == "__main__":
    list_name = argument_parser()
    main(list_name)





