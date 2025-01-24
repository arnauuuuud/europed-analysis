#!/usr/local/depot/Python-3.7/bin/python
# /usr/local/depot/Python-3.5.1/bin/python
import argparse
from hoho import useful_recurring_functions
import fcntl


waitinglistfile = '/home/jwp9427/Desktop/waitinglist'

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
    
    
def append(file_path, exact_line):
    with open(file_path, 'r+') as file:
        lock_file(file)
        lines = file.readlines()
        lines_output = []
        done = False
        for line in lines:
            if line.strip() == 'pause' and not done:
                lines_output.append(f'{exact_line}\n')
                lines_output.append('pause\n')
                done = True
            else:
                lines_output.append(line)

        file.seek(0)
        file.truncate()
        file.writelines(lines_output)
        unlock_file(file)

def main(filename_list):
    for filename in filename_list:
        append(waitinglistfile,filename)

if __name__ == "__main__":
    list_name = argument_parser()
    main(list_name)



