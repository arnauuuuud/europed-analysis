import os
import subprocess
from hoho import europed_hampus as europed

foldername = f"{os.environ['EUROPED_DIR']}"
os.chdir(foldername)

def density_shift(start=0.0,end=0.04,n_steps=10.0):
    model = "model1_zoom_resistivity_new"
    step = (end-start)/n_steps

    for i in range(int(n_steps)+1):
        densityshift = round(start + float(i)*step,5)
        filename = model + "_densityshift_"+ str(densityshift)
        print(filename)
        europed.batch_submit(filename)


def list_files(basis="model1_zoom_resistivity_densityshift_", listvariation=[]):
    for variation in listvariation:
        filename = "input/" +basis+str(variation)
        os.system(f"europed.py {filename} -b")
