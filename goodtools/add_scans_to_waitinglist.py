#!/usr/local/depot/Python-3.7/bin/python
# /usr/local/depot/Python-3.5.1/bin/python
import argparse
from hoho import useful_recurring_functions
import fcntl
import subprocess


waitinglistfile = '/home/jwp9427/Desktop/waitinglist'

def lock_file(file):
    fcntl.flock(file, fcntl.LOCK_EX)

def unlock_file(file):
    fcntl.flock(file, fcntl.LOCK_UN)

#####################################################################
def argument_parser():
    """Defining comandline parser and returning the arguments"""
    parser = argparse.ArgumentParser(description = "Append file to the waiting list")
    parser.add_argument("list_prefix", type=useful_recurring_functions.parse_modes, help = "file name list to append to the waiting list")
    parser.add_argument("list_eta", type=useful_recurring_functions.parse_modes, help = "file name list to append to the waiting list")
    parser.add_argument("list_rs", type=useful_recurring_functions.parse_modes, help = "file name list to append to the waiting list")
    parser.add_argument("list_neped", type=useful_recurring_functions.parse_modes, help = "file name list to append to the waiting list")
    parser.add_argument("list_betap", type=useful_recurring_functions.parse_modes, help = "file name list to append to the waiting list")
    
    args = parser.parse_args()
    return args.list_prefix, args.list_eta, args.list_rs, args.list_neped, args.list_betap
    

def create_input_file(root_file_name, eta, relative_shift, neped, betap):
    file_name = f'{root_file_name}_eta{eta}_rs{relative_shift}_neped{neped}_betap{betap}'
    command = f"/home/jwp9427/work/python/goodtools/setinput.py {root_file_name} run_name={file_name} eta={eta} density_shift={relative_shift} neped={neped} betap={betap}"
    result = subprocess.run(command, shell=True, capture_output=True)
    print(f'{file_name} was created')
    return file_name

def append(file_path,line):
    with open(file_path, 'a') as file:
        lock_file(file)
        file.write(line)
        unlock_file(file)

def main(list_prefix, list_eta, list_rs, list_neped, list_betap):
    for prefix in list_prefix:
        for eta in list_eta:
            for rs in list_rs:
                for neped in list_neped:
                    for betap in list_betap:
                        create_input_file(prefix,eta,rs,neped,betap)

    filename_list = [f'{prefix}_eta{eta}_rs{rs}_neped{neped}_betap{betap}' for prefix in list_prefix for eta in list_eta for rs in list_rs for neped in list_neped for betap in list_betap]
    for filename in filename_list:
        append(waitinglistfile,filename+'\n')

if __name__ == "__main__":
    list_prefix, list_eta, list_rs, list_neped, list_betap = argument_parser()
    main(list_prefix, list_eta, list_rs, list_neped, list_betap)



