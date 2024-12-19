#!/usr/local/depot/Python-3.7/bin/python
# /usr/local/depot/Python-3.5.1/bin/python

import subprocess
import time

#####################################################################
initial_rs=0.022
initial_neped=2.57

def create_input_file(root_file_name, eta, relative_shift, neped):
    file_name = f'{root_file_name}_eta{eta}_rs{relative_shift}_neped{neped}'
    command = f"/home/jwp9427/work/python/goodtools/setinput.py {root_file_name} run_name={file_name} eta={eta} density_shift={relative_shift} neped={neped}"
    result = subprocess.run(command, shell=True, capture_output=True)
    print(f'{file_name} was created')
    return file_name


def create_list_of_input_file(root_file_name, list_eta, list_rs=[initial_rs], list_neped=[initial_neped]):
    list_file_name = [create_input_file(root_file_name,eta,rs,neped) for neped in list_neped for rs in list_rs for eta in list_eta]
    return(list_file_name)


def count_processes_running():
    command = "llq -l | grep jwp9427.*"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)   
    return len(result.stdout.splitlines())


def launch_and_wait(filename):
    print(f'Launching run with filename: {filename}')
    command = f"/home/jwp9427/work/europed/europed.py /home/jwp9427/work/europed/input/{filename} -b"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    time.sleep(90)
    while count_processes_running()>22:
        print("Not enough computing time to launch new runs", end='\r')
        time.sleep(300)  # Check every 300 second  
    print("Available computing time")
    return True

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

def main():
    root_file_name='sb_n234'
    input_file_names = create_list_of_input_file(root_file_name, list_eta=[2.0])
    for input_file_name in input_file_names:
        if not already_exists(input_file_name):
            launch_and_wait(input_file_name) 

if __name__ == "__main__":
    main()



