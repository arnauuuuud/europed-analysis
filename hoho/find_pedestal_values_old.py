import os
from hoho import useful_recurring_functions, startup, europed_hampus as europed, europed_analysis, europed_analysis_2, h5_manipulation
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

def mtanh_offset(r, ppos, delta, h, s, offset):
    x = 2*(ppos-r)/delta
    res = h/2*(((1+s*x)*np.exp(x)-np.exp(-x))/(np.exp(x)+np.exp(-x)) + 1) + offset
    return res

mtanh_offset_vector = np.vectorize(mtanh_offset)


def find_critical_pars(europed_name, crit):
    foldername = f"{os.environ['EUROPED_DIR']}output"
    os.chdir(foldername)
    process_next_line = False
    critical_found = False

    with open(europed_name, 'r') as f:
        for line in f.readlines():

            if crit == 'alfven' and line.startswith("no critical profile found for gamma/gamma_A>0.030000 criterion"):
                raise useful_recurring_functions.CustomError(f"No critical profile found for criterion {crit} in {europed_name}")

            elif crit == 'diamag' and line.startswith("no critical profile found for gamma/omega*>0.250000 criterion"):
                raise useful_recurring_functions.CustomError(f"No critical profile found for criterion {crit} in {europed_name}")

            if  process_next_line:
                line_nepars = line
                process_next_line = False
                break

            if line.startswith('tepars'):
                line_tepars = line
                process_next_line = True

    te_pars = np.asarray(line_tepars[8:-3].split(), dtype = float)
    ne_pars = np.asarray(line_nepars[8:-3].split(), dtype = float)

    te_pars = tuple(te_pars)
    ne_pars = tuple(ne_pars)

    # print('CRITICAL')
    # print(te_pars)
    # print(ne_pars)

    # (a0, sep, a1, pos, delta, pedestal, alpha1, alpha2) = te_pars
    # teped = 2*a0 + sep + a0*(np.tanh(2*(1-pos)/delta)-1)
    # print(teped)

    # (a0, sep, a1, pos, delta, pedestal, alpha1, alpha2) = ne_pars
    # neped = 2*a0 + sep + a0*(np.tanh(2*(1-pos)/delta)-1)
    # print(neped)

    return(te_pars, ne_pars)
   
def find_profile_pars(filename, profile):
    h5_manipulation.decompress_gz(filename)
    with h5py.File(f'{filename}.h5', 'r') as hdf5_file:
        ne_pars = tuple(hdf5_file['scan'][str(profile)]['ne_parameters'])
        te_pars = tuple(hdf5_file['scan'][str(profile)]['te_parameters'])   
    h5_manipulation.removedoth5(filename)
    return(te_pars, ne_pars)

def ne_pars(filename, profile):
    h5_manipulation.decompress_gz(filename)
    h5_manipulation.decompress_gz(filename)
    with h5py.File(f'{filename}.h5', 'r') as hdf5_file:
        ne_pars = tuple(hdf5_file['scan'][str(profile)]['ne_parameters'])
    h5_manipulation.removedoth5(filename)
    return(ne_pars)

def te_pars(filename, profile):
    h5_manipulation.decompress_gz(filename)
    with h5py.File(f'{filename}.h5', 'r') as hdf5_file:
        te_pars = tuple(hdf5_file['scan'][str(profile)]['te_parameters'])
    h5_manipulation.removedoth5(filename)
    return(te_pars)


def create_profiles(europed_name, psis, crit=None, profile=None):

    if profile is None:
        te_pars, ne_pars = find_critical_pars(europed_name, crit)
    else:
        te_pars, ne_pars = find_profile_pars(europed_name, profile)

    # print(f'pos Te: {te_pars[3]}')
    # print(f'width Te: {te_pars[4]}')
    # print(f'pos ne: {ne_pars[3]}')
    # print(f'width ne: {ne_pars[4]}')

    te_profile = np.zeros(len(psis))
    ne_profile = np.zeros(len(psis))
    for i,psi in enumerate(psis):
        te_profile[i] = europed.eped_profile(te_pars, psi)
        ne_profile[i] = europed.eped_profile(ne_pars, psi)

    (a0, sep, a1, pos, delta, pedestal, alpha1, alpha2) = ne_pars
    neped = 2*a0 + sep + a0*(np.tanh(2*(1-pos)/delta)-1)
    return te_profile, ne_profile, neped



def pedestal_values(europed_name, profile=None):
    te_pars, ne_pars = find_profile_pars(europed_name, profile)

    (a0, sep, a1, pos, delta, pedestal, alpha1, alpha2) = ne_pars
    neped = 2*a0 + sep + a0*(np.tanh(2*(1-pos)/delta)-1)
    (a0, sep, a1, pos, delta, pedestal, alpha1, alpha2) = te_pars
    teped = 2*a0 + sep + a0*(np.tanh(2*(1-pos)/delta)-1)

    return neped, teped

def get_te_pos(europed_name, profile=None):
    te_pars, ne_pars = find_profile_pars(europed_name, profile)
    (a0, sep, a1, pos, delta, pedestal, alpha1, alpha2) = te_pars
    teped = 2*a0 + sep + a0*(np.tanh(2*(1-pos)/delta)-1)
    return pos-delta/2

def create_critical_profiles(europed_name, psis, crit='alfven', crit_value=0.03, exclud_mode = None, list_consid_mode = None):

    deltas = europed_analysis_2.get_x_parameter(europed_name, 'delta')
    dict_gammas = europed_analysis_2.get_filtered_dict(europed_name, crit, list_consid_mode, exclud_mode)
    has_unstable, delta_crit, mode = europed_analysis_2.find_critical(deltas, deltas, dict_gammas, crit_value)

    try:
        delta_below = np.max([d for d in deltas if d < delta_crit])
    except ValueError:
        return None, None, None 
    delta_above = np.min([d for d in deltas if d > delta_crit])

    h5_manipulation.decompress_gz(europed_name)
    with h5py.File(europed_name + '.h5', 'r') as h5file:
        try:
            profile_below = h5_manipulation.find_profile_with_delta_file(h5file,delta_below)
            profile_above = h5_manipulation.find_profile_with_delta_file(h5file,delta_above)
        except useful_recurring_functions.CustomError:
            return None, None, None
    h5_manipulation.removedoth5(europed_name)


    te_below, ne_below, neped_below = create_profiles(europed_name, psis, profile=profile_below)
    te_above, ne_above, neped_above = create_profiles(europed_name, psis, profile=profile_above)

    interp_ne = interp2d(psis,[delta_below,delta_above],[ne_below, ne_above])
    interp_te = interp2d(psis,[delta_below,delta_above],[te_below, te_above])
    interp_neped = interp1d([delta_below,delta_above],[neped_below, neped_above])

    ne_profile_crit = interp_ne(psis,delta_crit)
    te_profile_crit = interp_te(psis,delta_crit)
    neped_crit = interp_neped(delta_crit)

    return te_profile_crit, ne_profile_crit, neped_crit#, te_below, ne_below, neped_below, te_above, ne_above, neped_above


def critical_pedestal_position(europed_name, crit='alfven', crit_value=0.05, exclud_mode = [30,40,50], list_consid_mode = None):

    deltas = europed_analysis_2.get_x_parameter(europed_name, 'delta')
    dict_gamma = europed_analysis_2.get_filtered_dict(europed_name, crit, list_consid_mode)
    has_unstable, y_crit, mode = europed_analysis_2.find_critical(x_param, deltas, dict_gamma, crit_value)

    try:
        delta_below = np.max([d for d in deltas if d < delta_crit])
    except ValueError:
        return None, None, None 
    delta_above = np.min([d for d in deltas if d > delta_crit])

    h5_manipulation.decompress_gz(europed_name)
    with h5py.File(europed_name + '.h5', 'r') as h5file:
        try:
            profile_below = h5_manipulation.find_profile_with_delta(h5file,delta_below)
            profile_above = h5_manipulation.find_profile_with_delta(h5file,delta_above)
        except useful_recurring_functions.CustomError:
            return None, None, None
    h5_manipulation.removedoth5(europed_name)


    pos1 = get_te_pos(europed_name, profile=profile_below)
    pos2 = get_te_pos(europed_name, profile=profile_above)

    pos = (pos1+pos2)*delta_above/(delta_crit-delta_below)
    return pos


def create_pressure_profile(europed_name, psis, crit=None, profile=None):
    te_profile, ne_profile, neped = create_profiles(europed_name, psis, profile=profile)
    pe_profile = 1.6*(ne_profile)*(te_profile)
    return pe_profile

def fit_mtanh_pressure(psis, pe_profile):
    params, covariance = curve_fit(mtanh_offset, psis, pe_profile, maxfev=1000000, p0=[0.95, 0.06, 5, 1, 0.01])
    return params

def fit_mtanh_density(psis, ne_profile):
    params, covariance = curve_fit(mtanh_offset, psis, ne_profile)
    return params

def fit_mtanh(psis, ne_profile):
    params, covariance = curve_fit(mtanh_offset, psis, ne_profile, p0=[0.95, 0.05, 4.5, 1, 0.01])
    return params

def plot_pressure(europed_name, profile=None):
    fig, ax = plt.subplots()
    psis = np.linspace(0.92,1,500)
    te_profile, ne_profile, dummy = create_profiles(europed_name, psis, profile=profile)
    
    # plt.scatter(psi_interesting,[ne_interesting])
    # plt.plot(psis, ne_profile, label='ne')
    # plt.plot(psis, te_profile*10, label='10 te')
    # plt.plot(psis, ne_profile-ne_last)
    # plt.plot(psis, te_profile-te_last)

    # plt.show()

    # pe_profile = 1.6*(ne_profile-ne_last)*(te_profile-te_last)
    # pe_profile0 = pe_profile + 1.6*te_last*ne_last
    # pe_profile1 = pe_profile + 1.6*te_last*ne_interesting

    # plt.plot(psis, pe_profile0)
    # plt.plot(psis, pe_profile1)


    pe_profile = create_pressure_profile(europed_name, psis, profile=profile)

    # plt.plot(psis, pe_profile, label='pe')
    # plt.legend()
    # plt.show()


    params = fit_mtanh_pressure(psis, pe_profile)
    ppos, delta, h, s, offset = params
    list_res = []
    for psi in psis:
        list_res.append(mtanh_offset(psi, ppos, delta, h, s, offset))

    # plt.plot(psis, pe_profile, label = 'set to 0')
    ax.plot(psis, pe_profile, label='pe')
    ax.plot(psis,list_res, label='fit')
    plt.legend()
    ax.axhline(h+offset, color='black', linestyle="dashed")
    ax.set_ylim(bottom=0)
    plt.show()

def get_pedestal_pressure(europed_name, profile=None):
    # psis = np.linspace(0.85,1,20)
    # te_profile, ne_profile, dummy = create_profiles(europed_name, psis, profile=profile)
    # pe_profile = create_pressure_profile(te_profile, ne_profile)
    # params = fit_mtanh(psis, pe_profile)
    # ppos, delta, h, s, offset = params
    psis = np.linspace(0.85,1,20)
    pe_profile = create_pressure_profile(europed_name, psis, profile=profile)
    te_pos = get_te_pos(europed_name, profile=profile)
    interpolator = scipy.interpolate.interp1d(psis, pe_profile)
    pe_ped = interpolator(te_pos)
    return(pe_ped)

def get_pedestal_pressure2(europed_name, profile=None):
    neped, teped = pedestal_values(europed_name, profile)
    peped = 1.6 * neped * teped
    return(peped)

def get_pedestal_density(europed_name, profile=None):
    psis = np.linspace(0.85,1,20)
    te_profile, ne_profile, dummy = create_profiles(europed_name, psis, profile=profile)
    te_pos = get_te_pos(europed_name, profile=profile)
    interpolator = scipy.interpolate.interp1d(psis, ne_profile)
    ne_ped = interpolator(te_pos)
    return(ne_ped)

def get_pedestal_temperature(europed_name, profile=None):
    psis = np.linspace(0.85,1,20)
    te_profile, ne_profile, dummy = create_profiles(europed_name, psis, profile=profile)
    te_pos = get_te_pos(europed_name, profile=profile)
    interpolator = scipy.interpolate.interp1d(psis, te_profile)
    te_ped = interpolator(te_pos)
    return(te_ped)

def plot_density(europed_name, profile=None):
    fig, ax = plt.subplots()
    psis = np.linspace(0.85,1.2,500)
    te_profile, ne_profile, neped = create_profiles(europed_name, psis, profile)

    params = fit_mtanh_density(psis, ne_profile)
    ppos, delta, h, s, offset = params
    list_res = []
    for psi in psis:
        list_res.append(mtanh_offset(psi, ppos, delta, h, s, offset))

    ax.plot(psis, ne_profile, label='ne')
    ax.plot(psis,list_res, label='fit')
    plt.legend()
    ax.axhline(h+offset, color='black', linestyle="dashed")
    ax.axhline(neped, color='black', linestyle="dotted")
    ax.set_ylim(bottom=0)
    plt.show()


def get_density(europed_name, profile=None):
    psis = np.linspace(0.85,1,10)
    te_profile, ne_profile, neped = create_profiles(europed_name, psis, profile)
    return(neped)

def get_frac(europed_name, crit=None, profile=None):
    psis = np.linspace(0.85,1,10)
    try:
        te_profile, ne_profile, neped = create_profiles(europed_name, psis, crit, profile)
    except  useful_recurring_functions.CustomError:
        print(f"NO CRITICAL PROFILE WAS FOUND FOR {europed_name} - IMPOSSIBLE TO TAKE nesep/neped FOR THE CRITICAL PROFILES")
        return None

    nesep = ne_profile[-1]
    frac = nesep/neped
    return(frac)


def nesep_neped(europed_name, profile=None):
    te_pars, ne_pars = find_profile_pars(europed_name, profile)
    (a0, sep, a1, pos, delta, pedestal, alpha1, alpha2) = ne_pars
    neped = 2*a0 + sep + a0*(np.tanh(2*(1-pos)/delta)-1)
    nesep = sep
    frac = nesep/neped
    return(frac)

def get_critical_frac(europed_name, crit='alfven', crit_value=0.03, exclud_mode = None, list_consid_mode = None):
    psis = np.linspace(0.85,1,10)
    te_profile, ne_profile, neped = create_critical_profiles(europed_name, psis, crit, crit_value, exclud_mode, list_consid_mode)
    if ne_profile is None or neped is None:
        return(np.nan)
    nesep = ne_profile[-1]
    frac = nesep/neped
    return(frac)

def get_nesep(europed_name, crit, profile=None):
    psis = np.linspace(0.85,1,10)
    try:
        te_profile, ne_profile, neped = create_profiles(europed_name, psis, crit, profile)
    except  useful_recurring_functions.CustomError:
        print(f"NO CRITICAL PROFILE WAS FOUND FOR {europed_name} - IMPOSSIBLE TO TAKE nesep FOR THE CRITICAL PROFILES")
        return None
    nesep = ne_profile[-1]
    return(nesep)


def get_temp_middle_ped(europed_name, crit='alfven', profile=None):
    if profile is None:
        te_pars, ne_pars = find_critical_pars(europed_name, crit)
    else:
        te_pars, ne_pars = find_profile_pars(europed_name, profile)

    pos = te_pars[3]
    temp_at_middle_ped = europed.eped_profile(te_pars, 0.99)

    return temp_at_middle_ped
  

def get_temp_pos(europed_name, profile=None, pos=0.99):

    te_pars, ne_pars = find_profile_pars(europed_name, profile)

    #pos = te_pars[3]
    temp = []

    for pos in np.linspace(0.98,1,1000):
        temp.append(europed.eped_profile(te_pars, pos))
    temp_at_middle_ped = europed.eped_profile(te_pars, pos)
    good_temp = np.mean(temp)

    return good_temp