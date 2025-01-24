import os
from hoho import useful_recurring_functions, startup, europed_hampus as europed, europed_analysis, europed_analysis_2, h5_manipulation, hdf5_data, find_pedestal_values_old, pedestal_values
import matplotlib.pyplot as plt
import h5py
import gzip
import tempfile
import numpy as np
import scipy
import glob
from scipy.optimize import curve_fit
from scipy.interpolate import interp1d,interp2d

startup.reload(h5_manipulation)
startup.reload(europed_analysis_2)

   
def get_standard_profile(europed_name, profile):
    h5_manipulation.decompress_gz(europed_name)
    with h5py.File(f'{europed_name}.h5', 'r') as hdf5_file:
        alpha = np.array(hdf5_file['scan'][str(profile)]['alpha'])
        psi = np.array(hdf5_file['scan'][str(profile)]['psi_map'])
    h5_manipulation.removedoth5(europed_name)
    return(psi, alpha)

def get_critical_profile(europed_name, crit='alfven', crit_value=0.03, exclud_mode = None, list_consid_mode = None, fixed_width=False):
    p1, p2, ratio = pedestal_values.critical_profile_number(europed_name, crit, crit_value, exclud_mode, list_consid_mode, fixed_width)
    psi1,a1 = get_standard_profile(europed_name, p1)
    psi2,a2 = get_standard_profile(europed_name, p2)
    interpolator = interp1d(psi2,a2)
    a2_on_psi1 = interpolator(psi1)
    a_ratio = (1-ratio)*a1 + ratio*a2_on_psi1
    return(psi1, a_ratio)

def get_profile(europed_name, profile=None, crit=None, crit_value=0.03, exclud_mode = None, list_consid_mode = None, fixed_width=False):
    if crit is None and not profile is None:
        psi, alpha = get_standard_profile(europed_name, profile)
    elif not crit is None and profile is None:
        psi, alpha = get_critical_profile(europed_name, crit, crit_value, exclud_mode, list_consid_mode, fixed_width)
    return psi, alpha


def average_given_value(europed_name, psi_min, psi_max, profile=None, crit=None, crit_value=0.03, exclud_mode = None, list_consid_mode = None, fixed_width=False):
    psi, alpha = get_profile(europed_name, profile, crit, crit_value, exclud_mode, list_consid_mode, fixed_width)
    indexes_between = (psi>=psi_min) & (psi<=psi_max)
    alpha_less = alpha[indexes_between]
    return np.mean(alpha_less)

def average_fixed_value(europed_name, profile=None, crit=None, crit_value=0.03, exclud_mode = None, list_consid_mode = None, fixed_width=False):
    psi_min = 0.8
    psi_max = 1

    alpha_average = average_given_value(europed_name, psi_min, psi_max, profile, crit, crit_value, exclud_mode, list_consid_mode, fixed_width)
    return alpha_average

def average_fixed_value2(europed_name, profile=None, crit=None, crit_value=0.03, exclud_mode = None, list_consid_mode = None, fixed_width=False):
    psi_min = 0.9
    psi_max = 1

    alpha_average = average_given_value(europed_name, psi_min, psi_max, profile, crit, crit_value, exclud_mode, list_consid_mode, fixed_width)
    return alpha_average


def average_pedestal_width(europed_name, profile=None, crit=None, crit_value=0.03, exclud_mode = None, list_consid_mode = None, fixed_width=False):
    pepos, width = pedestal_values.pepos_and_delta(europed_name, profile, crit, crit_value, exclud_mode, list_consid_mode)
    psi_min = pepos - width/2
    psi_max = pepos + width/2

    alpha_average = average_given_value(europed_name, psi_min, psi_max, profile, crit, crit_value, exclud_mode, list_consid_mode, fixed_width)
    return alpha_average
