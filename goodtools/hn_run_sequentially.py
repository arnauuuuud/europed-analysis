#!/usr/local/depot/Python-3.7/bin/python
# /usr/local/depot/Python-3.5.1/bin/python

import subprocess
import time


#####################################################################
initial_rs=0.022
initial_neped=2.57
initial_betap=0.0

def create_input_file(root_file_name, eta, relative_shift, neped, betap):
    file_name = f'{root_file_name}_eta{eta}_rs{relative_shift}_neped{neped}'
    command = f"/home/jwp9427/work/python/goodtools/hn_setinput.py {root_file_name} run_name={file_name} eta={eta} density_shift={relative_shift} neped={neped} betap={betap}"
    result = subprocess.run(command, shell=True, capture_output=True)
    print(f'{file_name} was created')
    return file_name


def create_list_of_input_file(root_file_name, list_eta, list_rs=[initial_rs], list_neped=[initial_neped], list_betap=[initial_betap]):
    list_file_name = [create_input_file(root_file_name,eta,rs,neped,betap) for betap in list_betap for neped in list_neped for rs in list_rs for eta in list_eta]
    return(list_file_name)


def count_processes_running():
    command = "llq -l | grep hnystrom.*"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)   
    return len(result.stdout.splitlines())

def already_exists(filename):
    command = f"find /home/hnystrom/work/europed/output/ -name {filename}"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    len1 = len(result.stdout.splitlines())
    command = f"find /home/jwp9427/work/europed/output/ -name {filename}"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    len2 = len(result.stdout.splitlines())
    if len1 + len2 >= 1:
        return True
    else:
        return False


def launch_and_wait(filename):
    print(f'Launching run with filename: {filename}')
    command = f"/home/hnystrom/work/europed/europed.py /home/hnystrom/work/europed/input/{filename} -b"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    time.sleep(90)
    while count_processes_running()>22:
        print("Not enough computing time to launch new runs", end='\r')
        time.sleep(600)  # Check every 10 minutes  
    print("Available computing time")
    return True

def main():
    root_file_name='sb_middln'
    input_file_names = create_list_of_input_file(root_file_name, list_eta=[1.5], list_rs=[-0.01,0.0,0.01,0.02,0.03])
    for input_file_name in input_file_names:
        if not already_exists(input_file_name):
            launch_and_wait(input_file_name) 
    root_file_name='sb_lown'
    input_file_names = create_list_of_input_file(root_file_name, list_eta=[1.5], list_rs=[-0.01,0.0,0.01,0.02,0.03])
    for input_file_name in input_file_names:
        if not already_exists(input_file_name):
            launch_and_wait(input_file_name) 
    root_file_name='sb_middln'
    input_file_names = create_list_of_input_file(root_file_name, list_eta=[1.5], list_neped=[1.07,1.57,2.07,2.57,3.07,3.57])
    for input_file_name in input_file_names:
        if not already_exists(input_file_name):
            launch_and_wait(input_file_name) 
    root_file_name='sb_lown'
    input_file_names = create_list_of_input_file(root_file_name, list_eta=[1.5], list_neped=[1.07,1.57,2.07,2.57,3.07,3.57])
    for input_file_name in input_file_names:
        if not already_exists(input_file_name):
            launch_and_wait(input_file_name) 

if __name__ == "__main__":
    main()



