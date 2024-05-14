from hoho import useful_recurring_functions, europed_analysis, global_functions, startup, find_pedestal_values
import argparse
import matplotlib.pyplot as plt
import matplotlib.transforms as transforms
import math
import numpy as np
import matplotlib.tri as tri
from scipy.spatial import Delaunay
from scipy import interpolate
import os
from pylib.misc import ReadFile
import glob
import h5py
import gzip
import tempfile


dict_runid = {
    1.04:2106,
    1.29:2107,
    1.55:2108,
    1.80:2109,
    2.06:2110,
    2.31:2111,
    2.57:2112,
    2.83:2113,
    3.35:2114,
    3.86:2115,
    5.14:2116
}



def get_helena_name(europed_name, delta):
    neped = float(europed_name[-4:])
    runid = dict_runid[neped]
    # rs = get_adapted_rs_number(europed_name, rs)
    neped = '1.80' if neped == 1.8 else neped
    run_name = f'neped{neped}_delta{round(delta,5)}'
    return run_name

def get_psin_sig(europed_name, delta):
    helena_name = get_helena_name(europed_name, delta)

    psis = []
    sigs = []

    filepath = ""
    filepath = f"{os.environ['HELENA_DIR']}output/{helena_name}"
    
    try:
        with ReadFile(filepath) as f:
            line = ''
            while '* I   PSI     S      <J>     ERROR   LENGTH    BUSSAC   VOL    VOLP   AREA *' not in line:
                line = f.readline()
            dump = f.readline()
            line = f.readline()

            while '********************' not in line:
                
                line_strip = line.split()
                psi = line_strip[2]
                psis.append(float(psi))
                line = f.readline()

            while '*   S,       Q,      Fcirc,     NU_e,     NU_i,   SIG(Spitz),SIG(neo) *' not in line:
                line = f.readline()
            dump = f.readline()
            line = f.readline()

            while len(line)>10:
                line_split = line.split()
                sig = line_split[5]
                sigs.append(float(sig))
                line = f.readline()

            return psis, sigs 
    except FileNotFoundError:
        print(f'{helena_name:>20}: FILE NOT FOUND')
        return None,None


def get_sig_pos(europed_name, profile, delta, pos):
    #rs = get_adapted_rs_number(europed_name, rs)
    te_pars, ne_pars = find_pedestal_values.find_profile_pars(europed_name, profile)
    #pos_temp = float(te_pars[3])
    delta = float(te_pars[4])


    psis,sigs = get_psin_sig(europed_name, delta)

    if not psis and not sigs:
        return None

    interpolator = interpolate.interp1d(psis[1:], sigs, bounds_error=False)
    print(pos)
    sig_at_pedestal_pos = interpolator(pos)
    return sig_at_pedestal_pos


def get_eta_pos(europed_name, profile, delta, pos):
    # sig = []
    # for pos in range(0.8,1,100):
    #     sig.append(get_sig_pos(europed_name, profile, delta, pos))

    # if not sig:
    #     return None
    # sig = np.nanmean(sig)
    print(pos)
    sig = get_sig_pos(europed_name,profile,delta,pos)
    eta = 1/sig
    return eta

def get_adapted_rs_number(filename, profile):
    foldername = f"{os.environ['EUROPED_DIR']}hdf5"
    os.chdir(foldername)
    


    pattern = os.path.join(filename + '.h5.*')
    filename = glob.glob(pattern)[0]
    print('\n\n\n')
    print(filename)
    print(profile)

    if filename.endswith(".gz"):
        # Create a temporary file to decompress the .h5.gz file
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            with gzip.open(filename, 'rb') as gz_file:
                tmp_file.write(gz_file.read())
                tmp_file_name = tmp_file.name
        temp = True
    else:
        tmp_file_name = filename
        temp = False

    # Open the temporary file with h5py
    print(tmp_file_name)
    with h5py.File(tmp_file_name, 'r') as hdf5_file:
        delta_min=0.04
        for dataset_name, dataset in hdf5_file['scan'].items():    
            delta_min = min(delta_min,dataset['delta'][0])
        delta_min = 0.015
        print(delta_min)
        print(profile)
        delta_profile = float(hdf5_file['scan'][str(int(profile))]['delta'][0])
        new_profile = int(round((delta_profile-delta_min)*1000,2))
        print(new_profile)
    if temp:
        os.remove(tmp_file_name)

    return str(new_profile)