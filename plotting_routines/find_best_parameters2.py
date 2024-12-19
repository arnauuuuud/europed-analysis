#!/usr/local/depot/Python-3.7/bin/python
# /usr/local/depot/Python-3.5.1/bin/python

from ppf import *
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.cm as cm
from matplotlib.colors import Normalize
from hoho import useful_recurring_functions, constant_function,read_kk3_2022
from thesis import constants
from hoho import useful_recurring_functions, find_pedestal_values_old
from scipy.interpolate import interp1d
import subprocess
import subprocess
import psutil
import re
import time
major_linewidth = constants.major_linewidth
fontsizelabel = constants.fontsizelabel
fontsizetick = constants.fontsizetick
fontsizetext = constants.fontsizetext

#####################################################################
# TEMPERATURE
phys_quantity = 'TEMPERATURE'
dda_global = 'T052'
dtype_temp = 'TE'
dtype_density = 'NE'
dtype_psi = 'PSIE'
dtype_psi_fit = 'PSIF'
dtype_temp_fit = 'TEF5'
dtype_density_fit = 'NEF3'

uid = 'lfrassin'
n = len(dtype_temp)
shot = 84794
time_inputs = [45.51]

europed_names = ['kbm_v2_0076','kbm_v2_0086','kbm_v2_0096','kbm_v2_0106','kbm_v2_0116']

def is_process_running(process_name):
    command = "llq -l | grep jwp9427.*batch"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if re.search(process_name, result.stdout):
        return True
    else:
        return False



def main():
    
    command = "/home/jwp9427/work/europed/europed.py /home/jwp9427/work/europed/input/test -b"

    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    print('Europed was launched with initial file name')

    pattern_with_group = r"running batch file:(batch_run.*.script)"
    match = re.search(pattern_with_group, result.stdout)
    if match:
        batch_script_name = match.group(1)
        print("Launched batch process:", batch_script_name)


    while is_process_running(batch_script_name):
        print("Processes launched by europed.py are still running...", end='\r')
        time.sleep(300)  # Check every 300 second    

    # command = "qdel "+ batch_script_name
    # subprocess.run(command, shell=True)
    # print("Batch run was ended")
    
    print("Processes launched by europed.py have completed.")

if __name__ == "__main__":
    main()



