import os
import subprocess
from hoho import useful_recurring_functions, europed_hampus as europed
import matplotlib.pyplot as plt
from matplotlib import ticker
from pylib.misc import ReadFile
import h5py
import gzip
import tempfile
import numpy as np
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
import glob
import re
import math
from hoho import useful_recurring_functions, global_functions, find_pedestal_values_old
import scipy.interpolate

def get_x_parameter(filename, x_parameter="alpha_helena_max"):
    foldername = f"{os.environ['EUROPED_DIR']}hdf5"
    os.chdir(foldername)

    original_filename = filename
    pattern = os.path.join(filename + '.h5.gz')
    try:
        filename = glob.glob(pattern)[0]
    except IndexError:
        print(f"File not found: {original_filename}")
        return 'File not found'

    if filename.endswith(".gz"):
        # Create a temporary file to decompress the .h5.gz file
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            with gzip.open(filename, 'rb') as gz_file:
                tmp_file.write(gz_file.read())
                tmp_file_name = tmp_file.name
        temp = True
        # print('Decompressed')
    else:
        tmp_file_name = filename
        temp = False


    with h5py.File(tmp_file_name, 'r') as hdf5_file:
        nrows = int(hdf5_file['input']['steps'][0])
        res = np.zeros((nrows))
        for i in range(nrows):
            res[i] = None
            try:
                if x_parameter == 'peped':
                    res[i] = find_pedestal_values_old.get_pressure(filename, i)
                else:
                    res[i] = float(hdf5_file['scan'][str(i)][x_parameter][0])
            except KeyError:
                print(f'Profile {i} does not exist in {original_filename}')
    if temp:
        os.remove(tmp_file_name)

    return res

def interpolate_points(x_values,y_values, num_points=1000):    
    # Linearly interpolate to get 100 points between the minimum and maximum x values
    try:
        # nan_indices = np.isnan(y_values)
        # y_values_valid = y_values[~nan_indices]
        # x_values_valid = x_values[~nan_indices]

        x_values_valid = x_values
        y_values_valid = y_values

        interpolated_x = np.linspace(x_values[0], x_values[-1], num_points)
        interpolated_y = np.interp(interpolated_x, x_values_valid, y_values_valid)
            
        return interpolated_y
    except ValueError:
        return np.zeros((num_points))

def give_envelop(tab,x_param):
    nan_indices = np.isnan(x_param)
    x_param = x_param[~nan_indices]
    tab = tab[~nan_indices]

    print(len(x_param))
    print(tab.shape)
    
    # nan_indices = np.array([np.all(np.isnan(tab_i)) for tab_i in tab])
    # x_param = x_param[~nan_indices]
    # tab = tab[~nan_indices]
    # tab = np.array(tab)
    new_tab = [interpolate_points(x_param,tab[:,i]) for i in range(len(tab[0]))]
    new_tab = np.array(new_tab).transpose()

    list_max = np.nanmax(new_tab, axis=1)
    x_param = interpolate_points(x_param,x_param)

    data_dict = {}
    for i in range(len(x_param)):
        if round(x_param[i],5) not in data_dict or list_max[i] > data_dict[round(x_param[i],5)]:
            data_dict[round(x_param[i],5)] = list_max[i]

    # Extract unique values of a and their corresponding maximum values of b
    unique_a = list(data_dict.keys())
    max_b_values = list(data_dict.values())
    sorted_pairs = sorted(zip(unique_a, max_b_values), key=lambda x: x[0])
    sorted_x, sorted_y = zip(*sorted_pairs)

    return(sorted_x, sorted_y)

def get_gammas(filename, crit="alfven"):
    foldername = f"{os.environ['EUROPED_DIR']}hdf5"
    os.chdir(foldername)

    original_filename = filename

    pattern = os.path.join(filename + '.h5.gz')
    filename = glob.glob(pattern)[0]

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
    with h5py.File(tmp_file_name, 'r') as hdf5_file:

        try:
            group_scan = hdf5_file['scan']
            n_profiles = int(hdf5_file['input']['steps'][0])
            list_modes = [int(i) for i in hdf5_file['input']['n'][0].decode('utf-8').split(',')]
            list_modes_output = []

            tab = np.zeros((n_profiles,len(list_modes)))

            temp = str(hdf5_file['input']['stability_code'][0])
            stability_code = re.findall(r"'(.*?)'", temp)[0]
            # print(f"{original_filename:<36}{stability_code}")

            for profile in range(n_profiles):
                try:
                    group_prof = group_scan[str(profile)][stability_code]      
                    for i_n, n in enumerate(list_modes):
                        try:
                            group_mode = group_prof[str(n)]

                            if crit == "alfven":
                                tab[profile,i_n] = group_mode['gamma'][0]
                            elif crit == "diamag":
                                tab[profile,i_n] = group_mode['gamma_diam'][0]
                            elif crit == "omega":
                                tab[profile,i_n] = group_mode['omega'][0]
                            list_modes_output.append(n)
                        except KeyError:
                            tab[profile,i_n] = None
                except KeyError:
                    print(f"{original_filename:>40} Profile {profile} crashed")
                    for i_n, n in enumerate(list_modes):
                        tab[profile,i_n] = None
        except KeyError:
            print(f"{original_filename:>40} Unable to open 'scan'")
            return None, None
    if temp == True:
        os.remove(tmp_file_name)


    list_modes = [int(x) for x in list_modes]
    sorted_indices = np.argsort(list_modes)
    tab = tab[:,sorted_indices]
    list_modes_output = sorted(set(list_modes))

    return tab,list_modes_output

def get_tpos(filename):
    h5file = europed.EuropedHDF5(filename)
    list_te = np.array(h5file.get_scan_data("te")[0])
    list_psi = np.array(h5file.get_scan_data("psi")[0])
    
    teped = h5file.get_scan_data("teped")[0]
    psi_inter = scipy.interpolate.interp1d(list_te, list_psi)
    psiped = psi_inter(teped)
    return psiped

def density_at_tpos(filename):
    h5file = europed.EuropedHDF5(filename)
    list_ne = np.array(h5file.get_scan_data("ne")[0])
    list_psi = np.array(h5file.get_scan_data("psi")[0])

    ne_inter = scipy.interpolate.interp1d(list_psi, list_ne)
    psiped = get_tpos(filename)
    neped = ne_inter(psiped)
    return neped

def temperature_at_tpos(filename):
    h5file = europed.EuropedHDF5(filename)
    teped = h5file.get_scan_data("teped")[0]
    return teped

def pressure_at_tpos(filename):
    neped = density_at_tpos(filename)
    teped = temperature_at_tpos(filename)
    return 1.6*neped*teped

def get_nT(filename):
    foldername = f"{os.environ['EUROPED_DIR']}hdf5"
    os.chdir(foldername)

    pattern = os.path.join(filename + '.h5.gz')
    filename = glob.glob(pattern)[0]

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
    with h5py.File(tmp_file_name, 'r') as hdf5_file:
        group_scan = hdf5_file['scan']
        n_profiles = int(hdf5_file['input']['steps'][0])

        list_ne = np.zeros((n_profiles))
        list_Te = np.zeros((n_profiles))


        for profile in range(n_profiles):
            try:
                group_prof = group_scan[str(profile)]
                try:
                    list_ne[profile] = group_prof['neped'][0]
                    list_Te[profile] = group_prof['teped'][0]
                except KeyError:
                    list_ne[profile] = None
                    list_Te[profile] = None

            except KeyError:
                print(filename)
                print(f"    Profile {profile} crashed")
                list_ne[profile] = None
                list_Te[profile] = None
                   
    if temp:
        os.remove(tmp_file_name)
    return list_ne,list_Te

def get_runid(europed_run):
    filepath = ""
    filepath = f"{os.environ['EUROPED_DIR']}output/{europed_run}"
    with ReadFile(filepath) as f:
        line = f.readline()
        while 'run id:' not in line:
            line=f.readline()
        lines = line.split(': ')
        runid = lines[1][:-1]
    return runid

def filter_tab_general(gammas, modes, consid_modes, exclud_modes = None):
    if consid_modes is not None:
        consid_modes = [int(mode) for mode in modes if mode in consid_modes]
        tab = filter_tab(gammas, modes, consid_modes)
    elif exclud_modes is not None:
        exclud_modes = [int(mode) for mode in exclud_modes]
        consid_modes = [mode for mode in modes if mode not in exclud_modes] 
        tab = filter_tab(gammas, modes, consid_modes)
    else:
        consid_modes = modes
        tab=gammas
    return tab, consid_modes

def filter_tab(tab, a, b):
    # Filter elements of a that are part of b
    filtered_a = [elem for elem in a if elem in b]
    
    # Use boolean indexing to select columns
    selected_columns = np.isin(a, filtered_a)
    
    # Return the filtered tab
    return tab[:, selected_columns]

def first_valid_element(array):
    for i,element in enumerate(array):
        if element is not None and not np.isnan(element):
            return i,element
    return 0,None  # or another value to indicate no valid element was found

def find_first_point_break_condition(tab,crit_value):
    true_indices=np.where(tab>crit_value)
    if np.any(true_indices):
        min_col_value_index = np.nanargmin(true_indices[0])
        row_index = true_indices[0][min_col_value_index]
        return row_index, True, min_col_value_index
    else:
        return None, False, None

def remove_wrong_slopes(tab):
    temp_tab = tab
    for j in range(len(temp_tab[0])):
        for i in range(len(temp_tab)-1):
            if temp_tab[i,j]>temp_tab[i+1,j]: 
                temp_tab[i,j] = None
    return temp_tab

def find_critical(x_param, gamma_tab, list_n, crit_value, filter_wrong_slope=False):

    sorted_indices = np.argsort(x_param)
    x_param = x_param[sorted_indices]
    gamma_tab = gamma_tab[sorted_indices]

    if filter_wrong_slope:
        gamma_tab_filtered = remove_wrong_slopes(gamma_tab)
    else:
        gamma_tab_filtered = gamma_tab

    row, has_unstable, col_crit = find_first_point_break_condition(gamma_tab_filtered,crit_value)

    x_crit=None
    if has_unstable: # or x_param[row] == min(x_param):
        if row==0:
            x_crit = np.copy(x_param[row]) 
            return True, x_crit, -1, -1
        else:
            xlow = [np.copy(x_param)[row-1]]*len(gamma_tab[0])
            ylow = np.copy(gamma_tab[row-1,:])
    
            for j_temp,y_temp in enumerate(ylow):
                minus_i = 1
                while minus_i <= row and np.isnan(y_temp):
                    minus_i += 1
                    y_temp = np.copy(gamma_tab[row-minus_i][j_temp])
                ylow[j_temp] = y_temp
                xlow[j_temp] = np.copy(x_param)[row-minus_i]

            xsup = [np.copy(x_param)[row]]*len(gamma_tab[0])
            ysup = np.copy(gamma_tab[row,:])

            filt = np.where(ysup>crit_value)
            ylow = np.array(ylow[filt])
            ysup = np.array(ysup[filt])
            xsup = np.array(xsup)[filt]
            xlow = np.array(xlow)[filt]
            try:
                list_n = np.array(list_n)[filt]
            except IndexError:
                pass
            try:
                x_crit = np.nanmin(xlow + (xsup-xlow) * (crit_value-ylow)/(ysup-ylow))
                col_crit = np.nanargmin(xlow + (xsup-xlow) * (crit_value-ylow)/(ysup-ylow))
            except (RuntimeWarning, ValueError):
                x_crit = None
                col_crit = None

    list_i = []
    for j in range(len(gamma_tab[0])):
        i, element = first_valid_element(gamma_tab[:,j])
        if element is not None and element > crit_value:
            list_i.append(i)

    if len(list_i)>0 and (x_crit is None or x_param[min(list_i)]<x_crit):
        return True, x_param[min(list_i)], -1, -1 
    try:
        return has_unstable, x_crit, col_crit, list_n[col_crit]
    except (TypeError, IndexError):
        return has_unstable, x_crit, -1, -1



