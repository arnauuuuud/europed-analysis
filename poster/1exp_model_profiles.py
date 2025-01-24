#!/usr/local/depot/Python-3.7/bin/python
# /usr/local/depot/Python-3.5.1/bin/python

from hoho import useful_recurring_functions, europed_analysis, global_functions, startup, find_pedestal_values_old, h5_manipulation, spitzer
from poster import plot_canvas
from mpl_toolkits.axes_grid1 import Divider, Size
from ppf import *
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.cm as cm
from matplotlib.colors import Normalize
from thesis import constants
import matplotlib.colors as mcolors
from scipy.interpolate import interp1d
major_linewidth = constants.major_linewidth
fontsizelabel = constants.fontsizelabel
fontsizetick = constants.fontsizetick
fontsizetext = constants.fontsizetext

#####################################################################
# TEMPERATURE
phys_quantity = 'TEMPERATURE'
dda_global = 'T052'
dtype_temp = 'TE'
dtype_density = 'NE'
dtype_psi = 'PSIE'
dtype_psi_fit = 'PSIF'
dtype_temp_fit = 'TEF5'
dtype_density_fit = 'NEF3'

uid = 'lfrassin'
n = len(dtype_temp)
shot = 84794
time_inputs = [45.51]

cmap = plt.cm.inferno_r
europed_names = ['sb_eta0.0_rs0.022_neped2.57']
new_cmap = cmap(np.linspace(0.2, 0.8, 256))
new_cmap = mcolors.ListedColormap(new_cmap)
color0 = new_cmap(0)

#####################################################################
def main():
    
    for europed_name in europed_names:
        print('')
        print(shot)


        ppfuid(uid)
        cm = 1/2.54

        fig = plt.figure(figsize=(12.6*cm,11.9*cm),dpi=300)
        # Define fixed size for the axes in inches
        horiz = [Size.Fixed(1.3*cm),Size.Fixed(11*cm)]
        vert = [Size.Fixed(1.6*cm),Size.Fixed(10*cm)]
        divider = Divider(fig, (0, 0, 1, 1), horiz, vert, aspect=True, anchor=(0,0))

        ax = fig.add_axes(divider.get_position(), axes_locator=divider.new_locator(nx=1, ny=1))


        list_psin = []
        list_temperature = []

        ihdat,iwdat,temperature,x,time,ier=ppfget(pulse=shot,dda=dda_global,dtyp=dtype_temp)
        ihdat,iwdat,density,x,time,ier=ppfget(pulse=shot,dda=dda_global,dtyp=dtype_density)
        ihdat,iwdat,psi,x,time,ier=ppfget(pulse=shot,dda=dda_global,dtyp=dtype_psi)
        ihdat,iwdat,temperature_fit,x,time,ier=ppfget(pulse=shot,dda=dda_global,dtyp=dtype_temp_fit)
        ihdat,iwdat,density_fit,x,time,ier=ppfget(pulse=shot,dda=dda_global,dtyp=dtype_density_fit)
        ihdat,iwdat,psi_fit,x,time,ier=ppfget(pulse=shot,dda=dda_global,dtyp=dtype_psi_fit)
        
        interp = interp1d(temperature_fit, psi_fit)
        psi_sep = np.interp([0.1], temperature_fit, psi_fit)[0]
        psi_sep = interp(0.1)



        psi = np.array(psi) + 1 - psi_sep
        psi_fit = np.array(psi_fit) + 1 - psi_sep


        temperature = np.array(temperature)
        density = np.array(density)
        pressure = density*temperature*1.6

        temperature_fit = np.array(temperature_fit)
        density_fit = np.array(density_fit)
        pressure_fit = density_fit*temperature_fit*1.6


 
        ax.scatter(psi,pressure,color='white',edgecolors='red')
        # ax.plot(psi_fit,pressure_fit,'red')


        psis = np.linspace(0,1.2,100)
        te,ne,dump2 = find_pedestal_values_old.create_critical_profiles(europed_name,psis,crit='alfven',crit_value=0.05)

        pe = 1.6*ne*te

        ax.plot(psis,pe,color=color0,linewidth=3)

        ax.set_xlim(left=0.8,right=1)
        ax.set_ylim(bottom=0, top=6)


        y_label = global_functions.get_profiles_label('pe')
        x_label = global_functions.psiN_label

        ax.text(0.93, 4.6, 'Europed', transform=ax.transData, ha='left', va='bottom', color='orange',fontsize=20)
        ax.text(0.87, 0.5, 'Experimental\nvalues', transform=ax.transData, ha='left', va='bottom', color='red',fontsize=20)

        # custom_legend2 = [
        #     plt.Line2D([0], [0], linewidth=0, label=r'data point', marker='o', markerfacecolor='white', markeredgecolor='red'),
        #     plt.Line2D([0], [0], linewidth=2, label=r'fit', color='red'),
        #     ]
        # ax.legend(handles=custom_legend2, loc='lower left', fontsize=20,title='Experimental values') 


        ax.set_xlabel(x_label,fontsize=20)
        ax.set_ylabel(y_label,fontsize=20)

        plt.savefig('/home/jwp9427/cococo/1')
        plt.close()

if __name__ == '__main__':
    main()

