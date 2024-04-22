import re
import os
import math


foldername = f"{os.environ['EUROPED_DIR']}input"
os.chdir(foldername)

def grep(yourlist, yourstring):
    ide = [i for i, item in enumerate(yourlist) if re.search(yourstring, item)][0]
    return ide

def density_shifts_steps(model="m1",start=0.0,end=0.04,n_steps=10.0):
    step = (end-start)/n_steps
    densityshift = start

    f = open(model,"r")
    listlines = f.readlines()

    i_dshift = grep(listlines,"^density_shift=")
    i_runname = grep(listlines,"^run_name")

    for i in range(int(n_steps)+1):
        densityshift = round(start + float(i)*step,5)
        europed_run = model + "_ds"+ str(densityshift)
    
        temp = open(europed_run, "w")

        temp.writelines(listlines[:i_dshift])
        temp.write("density_shift=" + str(densityshift) + "\n")
        temp.writelines(listlines[i_dshift+1:i_runname])
        temp.write("run_name=" + europed_run + "\n")
        temp.writelines(listlines[i_runname+1:])

def density_shifts_list(model="m1",list_dshift = []):
    f = open(model,"r")
    listlines = f.readlines()

    i_dshift = grep(listlines,"^density_shift=")
    i_runname = grep(listlines,"^run_name")

    for density_shift in list_dshift:
        europed_run = model + "_ds"+ str(density_shift)
    
        temp = open(europed_run, "w")

        temp.writelines(listlines[:i_dshift])
        temp.write("density_shift=" + str(density_shift) + "\n")
        temp.writelines(listlines[i_dshift+1:i_runname])
        temp.write("run_name=" + europed_run + "\n")
        temp.writelines(listlines[i_runname+1:])



def general(parameter="density_shift",model="model1", list_values=[]):
    f = open(model,"r")
    listlines = f.readlines()

    i_param = grep(listlines,f"^{parameter}=")
    i_runname = grep(listlines,"^run_name")

    runname_first = min(i_param,i_runname) == i_runname

    for value in list_values:
        europed_run = model + f"_{parameter}_"+ str(value)
    
        temp = open(europed_run, "w")

        if runname_first:
            temp.writelines(listlines[:i_runname])
            temp.write("run_name=" + europed_run + "\n")
            temp.writelines(listlines[i_runname+1:i_param])
            temp.write(f"{parameter}=" + str(value) + "\n")
            temp.writelines(listlines[i_param+1:])
        else:
            temp.writelines(listlines[:i_param])
            temp.write(f"{parameter}=" + str(value) + "\n")
            temp.writelines(listlines[i_param+1:i_runname])
            temp.write("run_name=" + europed_run + "\n")
            temp.writelines(listlines[i_runname+1:])





