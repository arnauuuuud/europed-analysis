import os
import subprocess
from hoho import europed_hampus as europed
import matplotlib.pyplot as plt
from matplotlib import ticker
import h5py
import gzip
import tempfile
import numpy as np
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
import global_functions
import re

foldername = f"{os.environ['EUROPED_DIR']}hdf5"
os.chdir(foldername)

def maxparam_dshift(y_param="alpha", model = "model1", list_dshift=[round(0.004*i,5) for i in range(11)]):
    if y_param == "alpha":
        y_param = "alpha_helena_max"

    dshift_list = []
    criticalheight_list_diamag = []
    criticalheight_list_alfven = []

    for density_shift in list_dshift:
        europed_run = model + "_densityshift_"+ str(density_shift)
        dshift_list.append(density_shift)
        temp = europed.EuropedHDF5(europed_run)

        criticalheight_list_diamag.append(temp.get_critical_data(y_param,"diamag"))
        criticalheight_list_alfven.append(temp.get_critical_data(y_param,"alfven"))
    del temp

    fig, ax = plt.subplots()

    ax.plot(dshift_list,criticalheight_list_diamag,"x",label="Diamagnetic")
    ax.plot(dshift_list,criticalheight_list_alfven,"o",label="Alfven")
    ax.set_xlabel("Density shift [a.u.]")
    ax.set_ylabel(global_functions.get_critical_plot_label(y_param))
    ax.set_ylim(bottom=0)
    ax.set_xlim(left=0)
    ax.legend()
    plt.minorticks_on()
    plt.tick_params(axis="both",which="both",direction="in", bottom=True, top=True, left=True, right=True)

    plt.show()

def profile(param="ne",crit="alfven",europed_run=""):
    def get_critical_data(europed_run):
        temp = europed.EuropedHDF5(europed_run)
        if param in ["ne","te"]:
            res = temp.get_critical_data(param,crit)
        elif param == "pe":
            ne = temp.get_critical_data("ne",crit)
            te = temp.get_critical_data("te",crit)
            res = 1.6*ne*te
        psi = temp.get_critical_data("psi",crit)
        del temp
        return psi, res
    fig, ax = plt.subplots()

    if isinstance(europed_run, str):
        psi, res = get_critical_data(europed_run)
        ax.plot(psi,res)
    if isinstance(europed_run, list):
        for name in europed_run:
            psi, res = get_critical_data(name)
            label = re.search("0\.\d*", name).group()
            ax.plot(psi,res,label=label)
            ax.legend()

    ax.set_xlabel(r"$\psi_N$")
    ax.set_ylabel(global_functions.get_critical_profiles_label(param))
    plt.show()



### A refaire
def gamma_dshift_modes(start=0.0,end=0.04,n_steps=10, list_modes=[1,2,3,4,5,7,10,20,30,50], list_profiles=[2,3,4], crit="alfven"):
    model = "model1"
    step = (end-start)/n_steps

    dshift_list = []
    tab = np.zeros((int(n_steps)+1,len(list_profiles),len(list_modes)))

    for i_ds in range(int(n_steps)+1):
        densityshift = round(start + float(i_ds)*step,5)
        dshift_list.append(densityshift)
        europed_run = model + "_densityshift_"+ str(densityshift) + ".h5.gz"
        if europed_run.endswith(".gz"):
            # Create a temporary file to decompress the .h5.gz file
            with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
                with gzip.open(europed_run, 'rb') as gz_file:
                    tmp_file.write(gz_file.read())
                    tmp_file_name = tmp_file.name
            temp = True
        else:
            tmp_file_name = europed_run
            temp = False

        # Open the temporary file with h5py
        with h5py.File(tmp_file_name, 'r') as hdf5_file:

            for i_p, profile in enumerate(list_profiles):
                # Navigate to Group A
                group_a = hdf5_file['scan'][str(profile)]["mishka"]

                for i_n, n in enumerate(list_modes):
                    group_b = group_a[str(n)]

                    assert group_b['n'][0] == n
                    if crit == "alfven":
                        tab[i_ds,i_p,i_n] = group_b['gamma'][0]
                    elif crit == "diamag":
                        tab[i_ds,i_p,i_n] = group_b['gamma_diam'][0]
                    else:
                        print("wrong crit")
                        return
        if temp == True:
            os.remove(tmp_file_name)

    # PLOT
    list_markers =  [
    'o', '.', 'x', '+', 'v', '^', '<', '>', 's', 'd', '1', '2', '3', '4',
    '8', 'p', 'P', '*', 'h', 'H', '|', '_',
    ]
    list_colors = ["C0","C1","C2","C3","C4","C5","C6","C7","C8","C9"]
    linestyles = ['-', '--', '-.', ':', 'solid', 'dashed', 'dashdot', 'dotted',(0, (1, 1)), (0, (3, 1)), (0, (5, 1)), (0, (1, 2)), (0, (3, 2)),(0, (5, 2)), (0, (7, 2)), (0, (1, 1, 1, 1)), (0, (2, 2, 1, 2)),(0, (3, 1, 1, 1)), (0, (5, 1, 1, 1)), (0, (5, 2, 2, 2)), (0, (7, 2, 2, 2))]

    color_legend_elements = []
    marker_legend_elements = []

    fig, ax = plt.subplots()
    for i_p, profile in enumerate(list_profiles):
        
        color = list_colors[i_p]

        color_legend_elements.append(Line2D([0], [0], marker="o", color='w', label=str(profile), markerfacecolor=color, linewidth=0, markersize=10))
        for i_n, n in enumerate(list_modes):
            marker = list_markers[i_n]
            ax.plot(dshift_list,tab[:,i_p,i_n],color=color,marker=marker, linewidth=0, markersize=15)

    for i_n, n in enumerate(list_modes):
        marker = list_markers[i_n]
        marker_legend_elements.append(Line2D([0], [0], marker=marker, color="k", label=str(n), linewidth=0, markerfacecolor="w", markersize=10))

    ax.set_xlabel("Density shift [a.u.]")
    
    plt.minorticks_on()
    plt.tick_params(axis="both",which="both",direction="in", bottom=True, top=True, left=True, right=True)

    if crit == "alfven":
        ax.axhline(0.03, linestyle="--",color="k")
        ax.set_ylabel(r"Growth rate $\gamma/\omega_A$ ")
    elif crit == "diamag":
        ax.axhline(0.25, linestyle="--",color="k")
        ax.set_ylabel(r"Growth rate $\gamma/\omega*$ ")
    

    # Add the legends to the plot
    color_legend = ax.legend(handles=color_legend_elements, loc='lower left', title='Profiles')
    marker_legend = ax.legend(handles=marker_legend_elements, loc='lower right', title='Toroidal mode number')

    # Combine the legends into a single legend
    ax.add_artist(color_legend)

    # Set labels for the combined legend
    combined_legend = ax.get_legend()

    # Show the plot
    plt.show()








