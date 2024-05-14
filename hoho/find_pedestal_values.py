import os
from hoho import useful_recurring_functions, europed_hampus as europed
import matplotlib.pyplot as plt
import h5py
import gzip
import tempfile
import numpy as np
import glob
from scipy.optimize import curve_fit

def mtanh_offset(r, ppos, delta, h, s, offset):
    x = 2*(ppos-r)/delta
    res = h/2*(((1+s*x)*np.exp(x)-np.exp(-x))/(np.exp(x)+np.exp(-x)) + 1) + offset
    return res


def find_critical_pars(europed_name, crit):
    foldername = f"{os.environ['EUROPED_DIR']}output"
    os.chdir(foldername)
    process_next_line = False
    critical_found = False

    with open(europed_name, 'r') as f:
        for line in f.readlines():

            if crit == 'alfven' and line.startswith("no critical profile found for gamma/gamma_A>0.030000 criterion"):
                raise useful_recurring_functions.useful_recurring_functions.CustomError(f"No critical profile found for criterion {crit} in {europed_name}")

            elif crit == 'diamag' and line.startswith("no critical profile found for gamma/omega*>0.250000 criterion"):
                raise useful_recurring_functions.useful_recurring_functions.CustomError(f"No critical profile found for criterion {crit} in {europed_name}")

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

    return(te_pars, ne_pars)


   



def find_profile_pars(filename, profile):
    foldername = f"{os.environ['EUROPED_DIR']}hdf5"
    os.chdir(foldername)

    pattern = os.path.join(filename + '*')
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
        ne_pars = tuple(hdf5_file['scan'][str(profile)]['ne_parameters'])
        te_pars = tuple(hdf5_file['scan'][str(profile)]['te_parameters'])                   
    if temp:
        os.remove(tmp_file_name)

    return(te_pars, ne_pars)


def create_profiles(europed_name, psis, crit=None, profile=None):

    if profile is None:
        te_pars, ne_pars = find_critical_pars(europed_name, crit)
    else:
        te_pars, ne_pars = find_profile_pars(europed_name, profile)

    te_profile = np.zeros(len(psis))
    ne_profile = np.zeros(len(psis))
    for i,psi in enumerate(psis):
        te_profile[i] = europed.eped_profile(te_pars, psi)
        ne_profile[i] = europed.eped_profile(ne_pars, psi)

    (a0, sep, a1, pos, delta, pedestal, alpha1, alpha2) = ne_pars

    neped = 2*a0 + sep + a0*(np.tanh(2*(1-pos)/delta)-1)

    # te_last = te_profile[-1]
    # ne_last = ne_profile[-1]

    # i_095 = np.where(np.abs(psis-0.9)<0.005)[0][-1]
    # psi_interesting = psis[i_095]
    # ne_interesting = ne_profile[i_095]


    # return te_profile, ne_profile, te_last, ne_last, ne_interesting, psi_interesting
    return te_profile, ne_profile, neped

def create_pressure_profile(te_profile, ne_profile):
    pe_profile = 1.6*(ne_profile)*(te_profile)
    #pe_profile +=  1.6*te_last*ne_interesting

    return pe_profile

def fit_mtanh_pressure(psis, pe_profile):
    weights = np.ones_like(pe_profile)

    weights[-200:] = 6
    initial_guess = [0.97, 0.03, 2, 0.3,0]

    params, covariance = curve_fit(mtanh_offset, psis, pe_profile, sigma=1/weights, maxfev=3000, p0=initial_guess)
    return params

def fit_mtanh_density(psis, ne_profile):
    params, covariance = curve_fit(mtanh_offset, psis, ne_profile)
    return params

def fit_mtanh(psis, ne_profile):
    params, covariance = curve_fit(mtanh_offset, psis, ne_profile)
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


    pe_profile = create_pressure_profile(te_profile, ne_profile)

    # plt.plot(psis, pe_profile, label='pe')
    # plt.legend()
    # plt.show()


    params = fit_mtanh_pressure(psis, pe_profile)
    ppos, delta, h, s, offset = params
    print(params)
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

def get_pressure(europed_name, profile=None):
    psis = np.linspace(0.92,1,500)
    te_profile, ne_profile, dummy = create_profiles(europed_name, psis, profile)
    pe_profile = create_pressure_profile(te_profile, ne_profile)

    params = fit_mtanh_pressure(psis, pe_profile)
    ppos, delta, h, s, offset = params
    return(h + offset)

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

def get_frac(europed_name, crit, profile=None):
    psis = np.linspace(0.85,1,10)
    try:
        te_profile, ne_profile, neped = create_profiles(europed_name, psis, crit, profile)
    except  useful_recurring_functions.CustomError:
        print(f"NO CRITICAL PROFILE WAS FOUND FOR {europed_name} - IMPOSSIBLE TO TAKE nesep/neped FOR THE CRITICAL PROFILES")
        return None
    te_profile, ne_profile, neped = create_profiles(europed_name, psis, crit, profile)
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