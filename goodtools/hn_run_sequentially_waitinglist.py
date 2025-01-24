#!/usr/local/depot/Python-3.7/bin/python
# /usr/local/depot/Python-3.5.1/bin/python

import subprocess
import time
import fcntl

waitinglistfile = '/home/jwp9427/Desktop/waitinglist'
launchedlist_file = '/home/jwp9427/Desktop/launched'

def lock_file(file):
    fcntl.flock(file, fcntl.LOCK_EX)

def unlock_file(file):
    fcntl.flock(file, fcntl.LOCK_UN)

#####################################################################
def read_and_delete_first_line(file_path):
    with open(file_path, 'r') as file:
        lock_file(file)
        lines = file.readlines()
        unlock_file(file)
    if not lines:
        return None  # File is empty
    first_line = lines[0]
    with open(file_path, 'w') as file:
        lock_file(file)
        file.writelines(lines[1:])
        unlock_file(file)
    return first_line


def append(file_path,line):
    with open(file_path, 'a') as file:
        lock_file(file)
        file.write(line)
        unlock_file(file)


def count_processes_running():
    command = "llq -l | grep hnystrom.*"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)   
    return len(result.stdout.splitlines())


def launch_and_wait(filename):
    print(f'Launching run with filename: {filename}')
    command = f"cp /home/jwp9427/work/europed/input/{filename} /home/hnystrom/work/europed/input/{filename}"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)  
    command = f"/home/hnystrom/work/europed/europed.py /home/hnystrom/work/europed/input/{filename} -b"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    time.sleep(90)
    while count_processes_running()>22:
        print("Not enough computing time to launch new runs", end='\r')
        time.sleep(300)  # Check every 300 second  
    print("Available computing time                                       ")
    return True

def main():
    while True:
        filename = read_and_delete_first_line(waitinglistfile)
        while filename is not None:
            append(launchedlist_file,filename)
            print(filename.strip())
            launch_and_wait(filename.strip())
            filename = read_and_delete_first_line(waitinglistfile)
        time.sleep(3600)
        
if __name__ == "__main__":
    main()



