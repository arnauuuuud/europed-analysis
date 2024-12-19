#!/usr/local/depot/Python-3.7/bin/python
# /usr/local/depot/Python-3.5.1/bin/python

from hoho import useful_recurring_functions, europed_analysis, global_functions, startup, find_pedestal_values_old
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


position_psin = 0.85

def parse_modes(mode_str):
    return mode_str.split(',')


def argument_parser():
    """Defining comandline parser and returning the arguments"""
    parser = argparse.ArgumentParser(description = "Plots the values of the growth rate gamma and the critical contour on a 2D map neped,Teped (with the alven criterion)")
    parser.add_argument("prefix", help = "prefix of the Europed run")
    parser.add_argument("variations", type=useful_recurring_functions.parse_modes, help = "name variations of the Europed runs")
    
    parser.add_argument("-s", "--suffix", help= "common suffix of the Europed runs if needed")
    
    parser.add_argument("-d", "--diamag", action = 'store_const', const = 'diamag', dest = 'crit', default = 'alfven', help = "normalize growth rate to diamagnetic frequency instead of Alfven frequency")
    parser.add_argument("-v", "--critical_value", help= "critical value of the growth rate, default : 0.03 for alfven, 0.25 for diamagnetic")

    parser.add_argument("-p", "--pressure", action = 'store_const', const = 'pe', dest = 'ypar', default = 'te', help= "pressure on yaxis instead of temperature")


    group = parser.add_mutually_exclusive_group()
    group.add_argument('-x',"--exclud_mode", type=useful_recurring_functions.parse_modes, help = "list of modes to exclude, comma-separated (will plot all modes except for these ones)")
    group.add_argument('-m',"--consid_mode", type=useful_recurring_functions.parse_modes, help = "list of modes to consider, comma-separated (will plot only these modes)")

    args = parser.parse_args()

    if args.exclud_mode and args.consid_mode:
        parser.error("Arguments --exclud_mode and --consid_mode are mutually exclusive. Use one or the other.")

    if args.critical_value:
        critical_value = float(args.critical_value)
    else:
        critical_value = None

    variations = args.variations
    if variations == ["full_list"]:
        variations = ['-0.0100','-0.0050','0.0000','0.0500','0.0100','0.0150','0.0200','0.0250','0.0300','0.0350','0.0400']

    return args.prefix, variations, args.suffix, args.crit, critical_value, args.ypar, args.exclud_mode, args.consid_mode


def get_helena_name(europed_name, profile):
    neped = float(europed_name[-4:])
    runid = dict_runid[neped]
    profile = get_adapted_profile_number(europed_name, profile)
    run_name = f'jet84794.{runid}_{str(profile)}'
    return run_name

def get_psin_sig(europed_name, profile):
    helena_name = get_helena_name(europed_name, profile)

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


def get_sig_pos(europed_name, profile):
    #profile = get_adapted_profile_number(europed_name, profile)
    te_pars, ne_pars = find_pedestal_values_old.find_profile_pars(europed_name, profile)
    pos = float(te_pars[3])
    delta = float(te_pars[4])


    psis,sigs = get_psin_sig(europed_name, profile)

    if not psis and not sigs:
        return None

    interpolator = interpolate.interp1d(psis[1:], sigs, bounds_error=False)
    sig_at_pedestal_pos = interpolator(position_psin)
    return sig_at_pedestal_pos


def get_eta_pos(europed_name, profile):
    sig = get_sig_pos(europed_name, profile)

    if not sig:
        return None
    eta = 1/sig
    return eta

def get_adapted_profile_number(filename, profile):
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
        delta_min=0.04
        for dataset_name, dataset in hdf5_file['scan'].items():    
            delta_min = min(delta_min,dataset['delta'][0])
        delta_profile = float(hdf5_file['scan'][str(profile)]['delta'][0])
        new_profile = int(round((delta_profile-delta_min)*1000,2))
    if temp:
        os.remove(tmp_file_name)

    return str(new_profile)

    

def main(prefix, variations, suffix, crit, crit_value, ypar, exclud_mode, consid_mode):
    if crit_value is None:
        if crit == "alfven":
            crit_value=0.03
        elif crit == "diamag":
            crit_value=0.25
    fig, ax = plt.subplots(figsize=(12,9))

    list_n = []
    z = []
    x = []
    y = []
    list_eta = []

    global_n = [1,2,3,4,5,7,10,20,30,40,50]
    for variation in variations:
        bool_first = True
        europed_run= prefix + variation
        if suffix :
            europed_run += suffix

        print(europed_run)

        try:
            gammas, modes = europed_analysis.get_gammas(europed_run, crit)
            tab, consid_mode = europed_analysis.filter_tab_general(gammas, modes, consid_mode, exclud_mode)
            tab_ne,tab_Te = europed_analysis.get_nT(europed_run)


            def remove_wrong_slopes(tab):
                temp_tab = tab
                for j in range(len(temp_tab[0])):
                    for i in range(len(temp_tab)-1):
                        if temp_tab[i,j]>temp_tab[i+1,j]: 
                            temp_tab[i,j] = None
                return temp_tab
            
            tab = remove_wrong_slopes(tab)

            for profile in range(len(tab[:,0])):
                try:
                    argmax = np.nanargmax(tab[profile])
                    gamma = tab[profile, argmax]
                    ne = tab_ne[profile]
                    Te = tab_Te[profile]
                    
                    eta_middle_ped = get_eta_pos(europed_run, profile)
                    

                    list_n.append(global_n[argmax])
                    z.append(gamma)
                    x.append(ne)
                    y.append(Te)
                    list_eta.append(eta_middle_ped)
                except ValueError:
                    print("ca marche pas du tout")
        except FileNotFoundError:
            print(f"{europed_run:>40} FILE NOT FOUND")

    valid_indices = ~np.isnan(x) & ~np.isnan(y) & ~np.isnan(z) & np.array([value is not None for value in list_eta])
    x = np.array(x)[valid_indices]
    y = np.array(y)[valid_indices]
    z = np.array(z)[valid_indices]
    list_n = np.array(list_n)[valid_indices]
    list_eta = np.array(list_eta)[valid_indices]

    # x_smooth = np.linspace(min(x),max(x),1000)
    # y_te_smooth = np.linspace(np.nanmin(y),np.nanmax(y),1000)
    
    # X_smooth, Y_te_smooth = np.meshgrid(x_smooth, y_te_smooth)
    # Y_pe_smooth = 1.6*X_smooth*Y_te_smooth

    pressure = 1.6*x*y
    unique_x = list(set(x))
    unique_x = sorted(unique_x)

    x = np.array(x)
    list_eta = np.array(list_eta)*10**6

    print('\n\n\n\n')
    print(len(x))
    print(len(list_eta))

    good_x = [x_indiv for x_indiv in x]
    good_eta = [eta for eta in list_eta]


    triang = tri.Triangulation(good_x,good_eta)

    #tri.Triangulation(x,list_eta)

    # Filter out triangles connecting x=-1 and x=1
    triangles_to_keep = []
    for triangle in triang.triangles:
        x_values = x[triangle]
        distances = np.array([np.abs(unique_x.index(x1)-unique_x.index(x2)) for x1 in x_values for x2 in x_values])
        if np.all(distances <= 1):
            triangles_to_keep.append(triangle)
        else:
            #print(f'FILTERED TRIANGLE: {triangle} OF X VALUES {x_values}')
            pass

    # Create a new Triangulation object with filtered triangles
    filtered_triang = tri.Triangulation(x, list_eta, triangles=np.array(triangles_to_keep))

    contour = ax.tricontourf(triang, z, levels=20, cmap='inferno_r')

    nelabel, gammalabel = global_functions.get_plot_labels_gamma_profiles('neped',crit)

    cs = ax.tricontour(triang, z, levels=[crit_value],colors='r')
    ax.tricontour(triang, z, levels=[0.85*crit_value,1.15*crit_value],colors='r', linestyles='dashed')

    plt.clabel(cs, use_clabeltext =True, fmt='%1.2f',fontsize=10)
    plt.ticklabel_format(axis='y', style='sci', scilimits=(0,0))
    

    ax.set_xlabel(nelabel, fontsize=20)
    ax.set_ylabel(rf'$\eta(\psi_N={position_psin})$ [a.u.]', fontsize=20)

    ax.set_ylim(bottom=0)

    

    fig.colorbar(contour, label=gammalabel)
    fig.tight_layout()
    plt.show()

if __name__ == '__main__':
    prefix, variations, suffix, crit, crit_value, ypar, exclud_mode, consid_mode = argument_parser()
    main(prefix, variations, suffix, crit, crit_value, ypar, exclud_mode, consid_mode)