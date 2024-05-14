#!/usr/local/depot/Python-3.7/bin/python
# /usr/local/depot/Python-3.5.1/bin/python

from ppf import *
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.cm as cm
from matplotlib.colors import Normalize
from hoho import useful_recurring_functions, constant_function,read_kk3_2022
from thesis import constants
from hoho import useful_recurring_functions, find_pedestal_values
from scipy.interpolate import interp1d
import subprocess
import subprocess
import psutil
import re
import random
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


initial_kbm_const = 0.096
initial_fipm=0.75
initial_alpha_t2=1.4
initial_fipe=3
initial_fipw=0.6

max_kbm_const = 0.1
min_kbm_const = 0.092
max_step_kbm_const = 0.001

max_fipm = 4
min_fipm = 0
max_step_fipm = 0

max_alpha_t2 = 2.5
min_alpha_t2 = 1.1
max_step_alpha_t2 = 0.1

max_fipe = 4.5
min_fipe = 1.5
max_step_fipe = 0.5

max_fipw = 0.8
min_fipw = 0.3
max_step_fipw = 0.05

# maxs = np.array([max_kbm_const,max_fipm,max_fipe,max_fipw])
# mins = np.array([min_kbm_const,min_fipm,min_fipe,min_fipw])
# max_steps = np.array([max_step_kbm_const,max_step_fipm,max_step_fipe,max_step_fipw])
maxs = np.array([max_kbm_const,max_fipm,max_alpha_t2,max_fipe,max_fipw])
mins = np.array([min_kbm_const,min_fipm,min_alpha_t2,min_fipe,min_fipw])
max_steps = np.array([max_step_kbm_const,max_step_fipm,max_step_alpha_t2,max_step_fipe,max_step_fipw])

initial_filename='frog_30'


def is_batch_process_running(process_name):
    command = "llq -l | grep jwp9427.*batch"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if re.search(process_name, result.stdout):
        return True
    else:
        return False

def define_new_params(params):
    random_numbers = np.array([random.uniform(-1, 1) for _ in range(len(params))])
    steps = max_steps*random_numbers
    temp_params = params + steps
    temp_params_b = [min(p,q) for (p,q) in zip(maxs,temp_params)]
    final_params = [max(p,q) for (p,q) in zip(mins,temp_params_b)]
    return final_params

def create_new_input_file(params, name):
    new_params = define_new_params(params)
    kbm_const = new_params[0]
    fipm = new_params[1]
    alpha_t2 = new_params[2]
    fipe = new_params[3]
    fipw = new_params[4]
    # command = f"/home/jwp9427/work/python/goodtools/setinput.py {initial_filename} run_name={name} width_const={kbm_const} fast_ion_pressure_multip={fipm} fast_ion_pressure_exponent={fipe} fast_ion_pressure_width={fipw}"
    command = f"/home/jwp9427/work/python/goodtools/setinput.py {initial_filename} run_name={name} width_const={kbm_const} fast_ion_pressure_multip={fipm} alpha_t2={alpha_t2} fast_ion_pressure_exponent={fipe} fast_ion_pressure_width={fipw}"
    result = subprocess.run(command, shell=True)
    return new_params


def create_four_input_files(params, filenames):
    list__ = []
    for filename in filenames:
        list__.append(create_new_input_file(params, filename))
    return(list__)


def launch_and_wait(filenames):
    batch_script_names = ['','','','']

    for i,filename in enumerate(filenames):
        command = f"/home/jwp9427/work/europed/europed.py /home/jwp9427/work/europed/input/{filename} -b"

        result = subprocess.run(command, shell=True, capture_output=True, text=True)

        pattern_with_group = r"running batch file:(batch_run.*.script)"
        match = re.search(pattern_with_group, result.stdout)
        if match:
            batch_script_name = match.group(1)
        batch_script_names[i] = batch_script_name


    while (is_batch_process_running(batch_script_names[0]) or is_batch_process_running(batch_script_names[1]) or is_batch_process_running(batch_script_names[2]) or is_batch_process_running(batch_script_names[3])):
        print("Processes launched by europed.py are still running...", end='\r')
        time.sleep(300)  # Check every 300 second  
    return True


def distance_functions(fa,fb):
    fa = np.array(fa)
    fb = np.array(fb)
    return(np.sum(np.abs(fa-fb)))



def get_reference_function():
    ppfuid(uid)
    ihdat,iwdat,temperature_fit,x,time,ier=ppfget(pulse=shot,dda=dda_global,dtyp=dtype_temp_fit)
    ihdat,iwdat,psi_fit,x,time,ier=ppfget(pulse=shot,dda=dda_global,dtyp=dtype_psi_fit)
    
    interp = interp1d(temperature_fit, psi_fit)
    psi_sep = np.interp([0.1], temperature_fit, psi_fit)[0]
    psi_sep = interp(0.1)

    psi_fit = np.array(psi_fit) + 1 - psi_sep

    psis = np.linspace(0.5,1.2,100)

    new_list = []
    interpolator = interp1d(psi_fit, temperature_fit, bounds_error=False)
    for p in psis:
        new_list.append(interpolator(p))
    return new_list


def initial_te():
    psis = np.linspace(0.5,1.2,100)
    # te,ne,dump2 = find_pedestal_values.create_profiles(initial_filename,psis,crit='diamag')

    try:
        te,ne,dump2 = find_pedestal_values.create_profiles(initial_filename,psis,crit='diamag')
        return te
    except find_pedestal_values.CustomError:
        print("ouloulou")
    


# def get_params(filename):


def main():
    best_kbm_const = initial_kbm_const
    best_fipm = initial_fipm
    best_alpha_t2 = initial_alpha_t2
    best_fipe = initial_fipe
    best_fipw = initial_fipw
    best_filename = initial_filename

    params = [best_kbm_const,best_fipm,best_alpha_t2,best_fipe,best_fipw]
    
    count_best_file = 1
    count_with_this_file = 1

    to_compare_with = get_reference_function()

    min_distance = distance_functions(to_compare_with, initial_te())

    for i in range(20):
        filenames = [f'{initial_filename}_v{chr(count_best_file + 96)}_t{c}' for c in range(count_with_this_file,count_with_this_file+4)]
        count_with_this_file += 4
        list_params = create_four_input_files(params, filenames)
        launch_and_wait(filenames)

        for i,filename in enumerate(filenames):
            psis = np.linspace(0.5,1.2,100)

            try:
                te,ne,dump2 = find_pedestal_values.create_profiles(filename,psis,crit='diamag')

            except find_pedestal_values.CustomError:
                continue

            distance = distance_functions(to_compare_with, te)

            if distance < min_distance:
                print('##########################')
                print(f'New best file: {filename}')
                print('##########################')


                best_filename = filename
                params = list_params[i]
                count_best_file += 1
                count_with_this_file = 1
                min_distance = distance











    # command = "/home/jwp9427/work/europed/europed.py /home/jwp9427/work/europed/input/test -b"

    # result = subprocess.run(command, shell=True, capture_output=True, text=True)
    # print('Europed was launched with initial file name')

    # pattern_with_group = r"running batch file:(batch_run.*.script)"
    # match = re.search(pattern_with_group, result.stdout)
    # if match:
    #     batch_script_name = match.group(1)
    #     print("Launched batch process:", batch_script_name)


    # while is_batch_process_running(batch_script_name):
    #     print("Processes launched by europed.py are still running...", end='\r')
    #     time.sleep(300)  # Check every 300 second    

    # # command = "qdel "+ batch_script_name
    # # subprocess.run(command, shell=True)
    # # print("Batch run was ended")
    
    # print("Processes launched by europed.py have completed.")





if __name__ == "__main__":
    main()



