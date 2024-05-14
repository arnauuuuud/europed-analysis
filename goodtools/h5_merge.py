#!/usr/local/depot/Python-3.7/bin/python
# /usr/local/depot/Python-3.5.1/bin/python

from hoho import europed_analysis, h5_manipulation, useful_recurring_functions
import argparse
import numpy as np
import os, h5py, shutil


class useful_recurring_functions.CustomError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


def argument_parser():
    """Defining comandline parser and returning the arguments"""
    parser = argparse.ArgumentParser(description = "Merge two results of runs together")
    parser.add_argument("original_name", help = "name of the original run")
    parser.add_argument("extension_name", help = "name of the extenstion run")

    group = parser.add_mutually_exclusive_group()
    group.add_argument('-r',"--replace", action = 'store_const', const = 'replace', default='ignore', dest = 'option', help = "")

    parser.add_argument("--modes", "-n", type=useful_recurring_functions.parse_modes, help= "list of modes (comma-separated)")
    parser.add_argument("--deltas", "-d", type=useful_recurring_functions.parse_delta, help= "list of deltas (comma-separated), or delta_min and delta_max (dash-separated - steps 0.002)")

    args = parser.parse_args()

    return args.original_name, args.extension_name, args.option, args.modes, args.deltas


def new_name_for_original_file(original_name, extension_name, option):
    latest_version = h5_manipulation.get_latest_version(original_name)
    this_version = latest_version+1
    new_name = None
    if option == 'ignore':
        new_name = f"{original_name}_{this_version}_beforemerging(i)with_{extension_name}"
    elif option == "replace":
        new_name = f"{original_name}_{this_version}_beforemerging(r)with_{extension_name}"
    elif option == 'smart':
        new_name = f"{original_name}_{this_version}_beforemerging(m)with_{extension_name}"
    return new_name

def copy_original_file(original_name, extension_name, option):
    foldername = f"{os.environ['EUROPED_DIR']}hdf5"
    os.chdir(foldername)
    new_name = new_name_for_original_file(original_name, extension_name, option)
    if os.path.exists(foldername+new_name):
        raise useful_recurring_functions.useful_recurring_functions.CustomError('the new name for the original file already exists')
    h5_manipulation.decompress_gz(original_name)
    shutil.copy(original_name +'.h5', new_name +'.h5')
    h5_manipulation.compress_to_gz(new_name)


def merge_single_profile(original_file, extension_file, modes, delta):

    profile_original = h5_manipulation.find_profile_with_delta(original_file,delta)
    profile_extension = h5_manipulation.find_profile_with_delta(extension_file,delta)

    if modes is None:
        modes = ['1','2','3','4','5','7','10','20','30','40','50']
    
    try:
        for n in modes:
            del original_file['scan'][profile_original]['castor'][str(n)]
            new_group = extension_file['scan'][profile_extension]['castor'][str(n)]
            original_file['scan'][profile_original]['castor'].create_group(str(n))
            for key in new_group.keys():
                new_group.copy(key, original_file['scan'][profile_original]['castor'][str(n)])
    except KeyError:
        print(f'Profile with given delta {delta} does not have stability calculation')


def merge(original_name, extension_name, option, modes, deltas_to_put):

    with h5py.File(f'{original_name}.h5', 'a') as original_file, h5py.File(f'{extension_name}.h5', 'r') as extension_file:
        original_steps = int(original_file['input']['steps'][0])
        count_new_profile = 1

        try:
            deltas_original = original_file['input']['delta']
        except KeyError:
            deltas_original = europed_analysis.get_x_parameter(original_name, 'delta')
        new_delta_in_original = []

        for key in extension_file['scan'].keys():
            profile = key
            new_group = extension_file['scan'][profile]
            delta_extension = round(float(new_group['delta'][0]),5)

            # if delta is not in the list of interesting deltas, pass
            if all(abs(delta_extension-delta)>0.0001 for delta in deltas_to_put):
                continue

            # if delta is already in the original file
            if any(abs(delta_extension-delta)<=0.0001 for delta in deltas_original):
                if option == 'replace':
                    merge_single_profile(original_file, extension_file, modes, delta_extension)

            # if delta should be added to the original file
            else:
                name_new_profile = str(original_steps + count_new_profile)
                
                count_new_profile += 1
                original_file['scan'].create_group(name_new_profile)
                for key in new_group.keys():
                    new_group.copy(key, original_file['scan'][name_new_profile])
                new_delta_in_original.append(delta_extension)

                print(f"Took profile {profile}, delta {round(float(new_group['delta'][0]),5)} and copied it under name '{name_new_profile}' in file {original_name}")
        
        new_steps = str(original_steps+count_new_profile)
        new_steps_encoded = new_steps.encode('utf-8')
        del original_file['input']['steps']
        original_file['input'].create_dataset('steps', data = [new_steps_encoded])
        try:
            del original_file['input']['delta']
        except KeyError:
            pass
        updated_delta = np.concatenate((deltas_original,new_delta_in_original))
        original_file['input'].create_dataset('delta', data = updated_delta)
        print(f'Updated number of steps in {original_name}: {new_steps}')
        print(f'Updated range of deltas in {original_name}: {updated_delta}')
         

def merge_files(original_name, extension_name, option, modes, deltas):
    copy_original_file(original_name, extension_name, option)
    h5_manipulation.decompress_gz(extension_name)
    merge(original_name, extension_name, option, modes, deltas)
    h5_manipulation.compress_to_gz(extension_name)
    h5_manipulation.compress_to_gz(original_name)




if __name__ == '__main__':
    original_name, extension_name, option, modes, deltas = argument_parser()
    merge_files(original_name, extension_name, option, modes, deltas)