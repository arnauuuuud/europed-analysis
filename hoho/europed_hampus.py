import matplotlib.pyplot as plt
# from pylib.misc import ReadFile, wait_for_night_or_weekend
# from pylib.decorators import plotfunction
from scipy import interpolate
import subprocess
import numpy as np
import time
import os
import h5py
import math

# ======================================================================== #
#                                                                          #
#                       EUROPED Data class                                 #
#                                                                          #
# ======================================================================== #

class EuropedHDF5:
    GAMMA_KEYS = {'alfven' : 'gamma', 'diamag' : 'gamma_diam'}
    CRIT_KEYS = {'alfven' : '1', 'diamag' : "2"} 
    PSI_KEYS = {
        **dict.fromkeys(("alpha", "q", "shear", "ballooning_stability"), "psi_map"),
        **dict.fromkeys(("te", "ne", "ti"), "psi")
    }
    scan_keys = [
    "castor/mishka/elite",
    "ne_parameters",
    "te_parameters",
    "ti_parameters",
    #################
    "betap",
    "betan",
    "betaped",
    "delta",
    "teped",
    "tiped",
    "delta_ne",
    "delta_te",
    "alpha_helena_max",
    "neped",
    "pped",
    "run",
    "p_alpha",
    "p_h",
    "fp_energy_fraction",
    #######################
    "psi_map",
    "alpha",
    "q",
    "shear",
    "ballooning_stability",
    ######################
    "psi",
    "ne",
    "te",
    "ti"
    ]

    def __init__(self, filepath):
        if '/' not in filepath:
            filepath = f"{os.environ['EUROPED_DIR']}hdf5/{filepath}"
        if '.h5' not in filepath:
            filepath += ".h5"

        self.gunziped = False
        if os.path.isfile(f"{filepath}.gz") and (not os.path.isfile(f"{filepath}")):
            os.system(f"gunzip {filepath}.gz")
            self.gunziped = True
        
        if os.path.isfile(filepath):
            pass
            #self.hdf5 = h5py.File(filepath)
        else:
            raise Exception(f"{filepath} does not exist.")
        self.filepath = filepath

    def __del__(self):
        if self.gunziped:
            os.system(f"gzip {self.filepath}")

    #
    # Getting functions
    #
    def get_scan_data(self, key):
        with h5py.File(self.filepath, 'r') as hdf5_file:
            equils = [int(hdf5_file['scan'][equil].name.split('/')[-1]) for equil in hdf5_file['scan'].keys()]
            equils.sort()

            data = []
            for i, equil in enumerate(equils):
                try:
                    value = hdf5_file[f'scan/{equil}'][key].value.squeeze()
                except KeyError:
                    value = None
                data.append(value)

        return np.array(data)

    def get_critical_data(self, key, crit = 'alfven'):
        with h5py.File(self.filepath, 'r') as hdf5_file:
            crit_key = self.CRIT_KEYS[crit]
            value = hdf5_file[f'critical/{crit_key}'][key].value.squeeze()
        return value

    def get_input(self, key):
        with h5py.File(self.filepath, 'r') as hdf5_file:
            value = hdf5_file['input'][key].value[0]
        return value

    def get_gamma_of_all_modes(self, crit = 'alfven'):
        gamma_key = self.GAMMA_KEYS[crit]

        stability_code = self.get_input('stability_code')
        ns = self.get_input('n').split(',')

        modes = {}
        for mode in ns:
            modes[mode] = self.get_scan_data(f"{stability_code}/{mode}/{gamma_key}")

        return modes
    
    #
    # Plotting functions
    #

    #@plotfunction
    def plot_scan_profiles(self, profile_key, ax = None, cmap = 'plasma', 
                           **plt_kwargs):
        psi_key = self.PSI_KEYS[profile_key]
        
        psis = self.get_scan_data(psi_key)
        profiles = self.get_scan_data(profile_key)

        nprofs = len(profiles)
        cmap = plt.get_cmap(cmap)
        for i, (psi, profile) in enumerate(zip(psis, profiles)):
            ax.plot(psi, profile, color = cmap(i/nprofs), **plt_kwargs)

    def interpolate_profile(self, profile_key, interp_id):
        with h5py.File(self.filepath, 'r') as hdf5_file:
            psi_key = self.PSI_KEYS[profile_key]

            lower_id = math.floor(interp_id)
            upper_id = math.ceil(interp_id)

            lower_profile = hdf5_file[f'scan/{lower_id}/{profile_key}'].value
            lower_profile = lower_profile.squeeze()
            upper_profile = hdf5_file[f'scan/{upper_id}/{profile_key}'].value
            upper_profile = upper_profile.squeeze()

            lower_psi = hdf5_file[f'scan/{lower_id}/{psi_key}'].value.squeeze()
            upper_psi = hdf5_file[f'scan/{upper_id}/{psi_key}'].value.squeeze()

            interpolator = interpolate.interp1d(upper_psi, upper_profile)
            upper_profile = interpolator(lower_psi)

            psi = (interp_id - lower_id) * upper_psi + \
                (upper_id - interp_id) * lower_psi
            profile = (interp_id - lower_id) * upper_profile + \
                    (upper_id - interp_id) * lower_profile
        return psi, profile

        


class EuropedData():
    """
    Europed data class
    """
    CRITVALS = {'alfven' : 0.03, "diamag" : 0.25}

    def __init__(self, filepath):
        if '/' not in filepath:
            filepath = f"{os.environ['EUROPED_DIR']}output/{filepath}"
        self.filepath = filepath
        with ReadFile(self.filepath) as f:
            self.nrows = int(f.readline())
            
            # Initializing dictionaries and numpy arrays
            self.id = np.empty(self.nrows)
            self.nmax = {'alfven' : np.empty(self.nrows),
                        'diamag' : np.empty(self.nrows)}
            self.delta = np.empty(self.nrows)
            self.betaped = np.empty(self.nrows)
            self.pped = np.empty(self.nrows)
            self.teped = np.empty(self.nrows)
            self.betap = np.empty(self.nrows)
            self.betan = np.empty(self.nrows)
            self.Ph = np.empty(self.nrows)
            self.Palpha = np.empty(self.nrows)
            self.gammamax = {'alfven' : np.empty(self.nrows),
                            'diamag' : np.empty(self.nrows)}
            self.alpha = np.empty(self.nrows)
            self.shear = np.empty(self.nrows)
            self.run = np.empty(self.nrows)
            self.tepars = []
            self.nepars = []

            self.critical = {'alfven' : {},
                            'diamag' : {}}
            
            self.input = {}

            # Getting scan data
            line = f.readline()
            for i in range(self.nrows):
                spl = f.readline().split()
                self.id[i] = int(spl[0])
                self.nmax['alfven'][i] = int(spl[1])
                self.delta[i] = float(spl[2])
                self.betaped[i] = float(spl[3])
                self.pped[i] = float(spl[4])
                self.teped[i] = float(spl[5])
                self.betap[i] = float(spl[6])
                self.betan[i] = float(spl[7])
                self.Ph[i] = float(spl[8])
                self.Palpha[i] = float(spl[9])
                self.gammamax['alfven'][i] = float(spl[10])
                self.alpha[i] = float(spl[11])
                self.shear[i] = float(spl[12])
                self.run[i] = bool(spl[-1])

            for i in range(self.nrows):
                spl = f.readline().split()
                self.nmax['diamag'][i] = int(spl[1])
                self.gammamax['diamag'][i] = float(spl[10])
            
            # Getting critical data for Alfven criticality condition
            line = f.readline()
            if "no critical profile" not in line:
                self.critical['alfven']['teped'] = float(line.split()[-1])
                self.critical['alfven']['ttanh'] = float(f.readline().split()[-1])
                self.critical['alfven']['delta'] = float(f.readline().split()[-1])
                self.critical['alfven']['n'] = int(f.readline().split()[-1])
                self.critical['alfven']['alpha'] = float(f.readline().split()[-1])
                self.critical['alfven']['wfp'] = float(f.readline().split()[-1])
                self.critical['alfven']['wtot'] = float(f.readline().split()[-1])
                self.critical['alfven']['ph'] = float(f.readline().split()[-1])
                self.critical['alfven']['taue'] = float(f.readline().split()[-1])

                # Getting te and ne pars for Alfven criticality condition
                self.critical['alfven']['tepars'] = np.asarray(f.readline()[8:-3].split(), dtype = float)
                self.critical['alfven']['nepars'] = np.asarray(f.readline()[8:-3].split(), dtype = float)
            else:
                self.critical['alfven']['teped'] = 0
                self.critical['alfven']['ttanh'] = 0
                self.critical['alfven']['delta'] = 0
                self.critical['alfven']['n'] = 0
                self.critical['alfven']['alpha'] = 0
                self.critical['alfven']['wfp'] = 0
                self.critical['alfven']['wtot'] = 0
                self.critical['alfven']['ph'] = 0
                self.critical['alfven']['taue'] = 0
                self.critical['alfven']['tepars'] = np.zeros(9)
                self.critical['alfven']['nepars'] = np.zeros(9)
            
            # Getting critical data for diamagnetic criticality condition
            line = f.readline()
            if "no critical profile" not in line:
                self.critical['diamag']['teped'] = float(line.split()[-1])
                self.critical['diamag']['ttanh'] = float(f.readline().split()[-1])
                self.critical['diamag']['delta'] = float(f.readline().split()[-1])
                self.critical['diamag']['n'] = int(f.readline().split()[-1])
                self.critical['diamag']['alpha'] = float(f.readline().split()[-1])
                self.critical['diamag']['wfp'] = float(f.readline().split()[-1])
                self.critical['diamag']['wtot'] = float(f.readline().split()[-1])
                self.critical['diamag']['ph'] = float(f.readline().split()[-1])
                self.critical['diamag']['taue'] = float(f.readline().split()[-1])
                
                # Getting te and ne pars for Diamagnetic criticality condition
                self.critical['diamag']['tepars'] = np.asarray(f.readline()[8:-3].split(), dtype = float)
                self.critical['diamag']['nepars'] = np.asarray(f.readline()[8:-3].split(), dtype = float)
            else:
                self.critical['diamag']['teped'] = 0
                self.critical['diamag']['ttanh'] = 0
                self.critical['diamag']['delta'] = 0
                self.critical['diamag']['n'] = 0
                self.critical['diamag']['alpha'] = 0
                self.critical['diamag']['wfp'] = 0
                self.critical['diamag']['wtot'] = 0
                self.critical['diamag']['ph'] = 0
                self.critical['diamag']['taue'] = 0
                self.critical['diamag']['tepars'] = np.zeros(9)
                self.critical['diamag']['nepars'] = np.zeros(9)
            
            # Reading Z_eff
            self.zeff = float(f.readline().split()[-1])

            # Reading runid
            self.runid = f.readline().split()[-1]

            # Reading profiles
            for i in range(self.nrows):
                f.readline()
                f.readline()
                line = f.readline()
                spl = line.split(',')
                tepars = [float(expr.split()[-1]) for expr in spl[:-1]]
                self.tepars.append(tepars)
                line = f.readline()
                spl = line.split(',')
                nepars = [float(expr.split()[-1]) for expr in spl[:-1]]
                self.nepars.append(nepars)
                
            # Reading input
            line=f.readline()
            while line != "":
                spl = line.split('=')
                self.input[spl[0].strip()] = spl[-1].strip()
                line = f.readline()

    def get_critical_id(self, crit, critval = None):
        if critval is None:
            critval = self.CRITVALS[crit]
        index = np.where(self.gammamax[crit] > critval)[0][0]
        x = self.gammamax[crit][index - 1 : index + 1]
        y = self.id[index-1:index+1]
        interpolator = interpolate.interp1d(x, y)
        return interpolator(critval)

    #@plotfunction
    def plot_gamma(self, crit = 'alfven', ax = None, **plt_kwargs):
        ax.plot(self.alpha, self.gammamax[crit], **plt_kwargs)

    def create_mapping(self, equi = 'crit1'):
        """
        Takes europed data dictionary and runs HELENA to produce mapping file
        Arguments
            data : dict
                dictionary with europed data (returned from europed.read_data)
            equi : str/int
                indicator for which equilibrium.
                'crit1' : Alfven critical equilibrium
                'crit2' : Diamagnetic critical equilibrium
                integer : The equilibrium with the given index
        """
        helena_dir = os.environ['HELENA_DIR']
        namelist = f"{self.input['device_name']}{self.input['shotno']}.{self.runid}_{equi}"    
        terminal_command = f"{helena_dir}runhel.py -m {namelist}"

        os.system(terminal_command)

def eped_profile(pars, psi):
    """
    Takes profile parameters from europed to return profile value at psi
    Arguments:
        pars : iterable
            iterable of length 8 containing the profile parameters
        psi : float/iterable
            if iterable returns numpy array with profile values at psi
            else returns profile value at psi
    """
    def core_profile(a1, pedestal, alpha1, alpha2, x):
        if psi > pedestal:
            return 0.0
        else:
            return a1*(1-(x/pedestal)**alpha1)**alpha2

    def pedestal_profile(sep, a0, pos, delta, x):
        return sep+a0*(np.tanh(2*(1-pos)/delta)-np.tanh(2*(x-pos)/delta))
    
    (a0, sep, a1, pos, delta, pedestal, alpha1, alpha2) = pars
    
    if isinstance(psi, float) or isinstance(psi, int):
        ped = pedestal_profile(sep, a0, pos, delta, psi)
        if (psi > pedestal):
            return ped
        else:
            core = core_profile(a1, pedestal, alpha1, alpha2, psi)
            return ped + core
    else:
        prof = np.empty(len(psi))
        for i in range(len(psi)):
            prof[i] = eped_profile(pars, psi[i])
        return prof

def modify_inputfile(filepath, outputfile = None, **kwargs) -> list:
    """
    Modifies the inputfile given by filepath according to **kwargs.
    The modified file will overwrite the inputfile unless another 
    file name is given as output. 
    """
    if '/' not in filepath:
        filepath = os.environ['EUROPED_DIR'] + 'input/' + filepath

    with open(filepath, 'r') as f:
        lines = f.readlines()
    
    written = []
    with open(filepath, 'w') as f:
        for line in lines:
            for kwarg in kwargs:
                if kwarg == line.split('=')[0].strip():
                    line = f"{kwarg}={kwargs[kwarg]}\n"
                    written.append(kwarg)
            f.write(line)
    return written

def get_parameters_from_inputfile(filepath, *args):
    """
    Takes an europed inputfile given by filepath and searches for the 
    strings given by *args. Returns a dictionary where *args are the 
    keys and the read values are the values.
    """
    if '/' not in filepath:
        filepath = os.environ['EUROPED_DIR'] + 'input/' + filepath
    
    parameters = {}
    with open(filepath) as f:
        for line in f:
            for arg in args:
                if arg == line.split('=')[0].strip():
                    parameters[arg] = line.split('=')[-1].strip()
    return parameters

def get_settings_from_hrts(shot, dda, uid, seq = 0):
    hrts_data = hrts.HRTSfitData(shot, dda, uid)
    

def parameter_in_inputfile(filepath, parameter):
    """
    Takes an europed inputfile given by filepath and searches for the 
    strings given by *args. Returns a dictionary where *args are the 
    keys and the read values are the values.
    """
    if '/' not in filepath:
        filepath = os.environ['EUROPED_DIR'] + 'input/' + filepath
    
    with open(filepath) as f:
        for line in f:
            if parameter == line.split('=')[0].strip():
                return True
    return False

def batch_submit(inputfile):
    os.system(f"{os.environ['EUROPED_DIR']}europed.py input/{inputfile} -b")

def submit_list(inputfiles, maxjobs = 5, only_night_and_weekend = False):
    cwd = os.getcwd()
    os.chdir(os.environ['EUROPED_DIR'])
    runs = []
    for inputfile in inputfiles:
        if only_night_and_weekend:
            wait_for_night_or_weekend()

        (_, output) = subprocess.getstatusoutput(f"europed.py input/{inputfile} -b")
        
        output=output.split('\n')
        for line in output:
            if "running batch file:" in line:
                script_name = line.split(':')[-1].strip()
        time.sleep(3)

        (err, output) = subprocess.getstatusoutput("llq -l")
        while err:
            (err, output) = subprocess.getstatusoutput("llq -l")
            time.sleep(300)

        output = output.split('\n')
        for line in output: 
            if script_name in line:
                runs.append(line.split()[0])
                break
        
        while len(runs) == maxjobs:
            (err, output) = subprocess.getstatusoutput("llq -l")
            while err:
                (err, output) = subprocess.getstatusoutput("llq -l")
                time.sleep(300)
            for run in runs:
                if (output.find(run) == -1):
                    runs.remove(run)
            time.sleep(180)
    os.chdir(cwd)
