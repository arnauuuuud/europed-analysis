#!/usr/local/depot/Python-3.7/bin/python
# /usr/local/depot/Python-3.5.1/bin/python
import argparse
from hoho import useful_recurring_functions
import fcntl

launchedlistfile = '/home/jwp9427/Desktop/launched'

def lock_file(file):
    fcntl.flock(file, fcntl.LOCK_EX)

def unlock_file(file):
    fcntl.flock(file, fcntl.LOCK_UN)

#####################################################################
def argument_parser():
    """Defining comandline parser and returning the arguments"""
    parser = argparse.ArgumentParser(description = "Append file to the waiting list")
    parser.add_argument("list_name", type=useful_recurring_functions.parse_modes, help = "file name list to append to the waiting list")
    
    args = parser.parse_args()
    return args.list_name
    
    
def remove_exact_line(filename, exact_line):
    # Read the file contents
    with open(filename, 'r+') as file:
        lock_file(file)
        lines = file.readlines()
        lines = [line for line in lines if line.strip() != exact_line]
        file.seek(0)
        file.truncate()
        lines_unique = list(set(lines))
        file.writelines(lines_unique)
        unlock_file(file)


def main(filename_list):
    for filename in filename_list:
        remove_exact_line(launchedlistfile,filename)

if __name__ == "__main__":
    list_name = argument_parser()
    main(list_name)



