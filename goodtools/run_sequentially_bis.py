#!/usr/local/depot/Python-3.7/bin/python
# /usr/local/depot/Python-3.5.1/bin/python

from ppf import *
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.cm as cm
from matplotlib.colors import Normalize
import sys
sys.path.insert(0, '/home/jwp9427/work/python')
from scipy.interpolate import interp1d
import subprocess
import subprocess
import psutil
import re
import random
import time


#####################################################################
root_file_name='sa'
initial_rs=0.022
initial_neped=2.57

def create_input_file(root_file_name, eta, relative_shift, neped):
    file_name = f'{root_file_name}_eta{eta}_rs{relative_shift}_neped{neped}'
    command = f"/home/jwp9427/work/python/goodtools/setinput_scans.py {root_file_name} run_name={file_name} eta={eta} density_shift={relative_shift} neped={neped}"
    result = subprocess.run(command, shell=True, capture_output=True)
    print(f'{file_name} was created')
    return file_name


def create_list_of_input_file(root_file_name, list_eta, list_rs=[initial_rs], list_neped=[initial_neped]):
    list_file_name = [create_input_file(root_file_name,eta,rs,neped) for eta in list_eta for rs in list_rs for neped in list_neped]
    return(list_file_name)


def count_processes_running():
    command = "llq -l | grep jwp9427.*"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)   
    return len(result.stdout.splitlines())


def launch_and_wait(filename):
    print(f'Launching run with filename: {filename}')
    command = f"/home/jwp9427/work/europed/europed.py /home/jwp9427/work/europed/scan_inputs/{filename} -b"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    time.sleep(90)
    while count_processes_running()>15:
        print("Not enough computing time to launch new runs", end='\r')
        time.sleep(300)  # Check every 300 second  
    print("Available computing time")
    return True

def main():
    input_file_names = create_list_of_input_file(root_file_name, list_eta=[0.0,0.5,1.0], list_rs=[-0.01,0.00,0.01,0.02,0.03,0.04])
    for input_file_name in input_file_names:
        launch_and_wait(input_file_name) 

if __name__ == "__main__":
    main()



