#!/usr/local/depot/Python-3.7/bin/python
# /usr/local/depot/Python-3.5.1/bin/python

from hoho import h5_manipulation, useful_recurring_functions
import argparse
import os, h5py, shutil

def argument_parser():
    """Defining comandline parser and returning the arguments"""
    parser = argparse.ArgumentParser(description = "Supress profile from hdf5, will create a new file with the current version of the file and update the given file")
    parser.add_argument("original_name", help = "original name of the run")
    parser.add_argument("deltas", type=useful_recurring_functions.parse_delta, help= "list of deltas to suppress")
    parser.add_argument("--modes", "-n", type=useful_recurring_functions.parse_modes, help= "modes to be removed in the corresponding profiles")

    args = parser.parse_args()

    return args.original_name, args.deltas, args.modes


def copy_original_file(original_name):
    foldername = f"{os.environ['EUROPED_DIR']}hdf5"
    os.chdir(foldername)
    latest_version = h5_manipulation.get_latest_version(original_name)
    this_version = latest_version+1
    new_name = f'{original_name}_{this_version}_beforeremovingprofiles'
    h5_manipulation.decompress_gz(original_name)
    shutil.copy(original_name +'.h5', new_name +'.h5')
    h5_manipulation.compress_to_gz(new_name)
    print(f'Old version of {original_name} is now named {new_name}')


def update(original_name, modes, deltas):

    # Open the copied file in read-write mode
    with h5py.File(original_name + '.h5', 'a') as original_file:
        if not modes:
            suppressed_profile = []
            for delta in deltas:
                profile = h5_manipulation.find_profile_with_delta(original_file,delta)
                stability_code = 'castor'
                del original_file['scan'][profile]
                suppressed_profile.append(profile)
            print(f'List of suppressed profiles {suppressed_profile} in {original_name}')
                

        else:
            for delta in deltas:
                profile = h5_manipulation.find_profile_with_delta(original_file,delta)
                stability_code = 'castor'
                for mode in modes:
                    try:
                        del original_file['scan'][profile][stability_code][mode]
                        print(f"Mode {mode} in profile {profile}  deleted from {original_name}") 
                    except KeyError:
                        print(f"No mode {mode} in profile {profile}")           



if __name__ == '__main__':
    original_name, deltas, modes = argument_parser()
    copy_original_file(original_name)
    update(original_name, modes, deltas)
    h5_manipulation.compress_to_gz(original_name)