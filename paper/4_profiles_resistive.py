#!/usr/local/depot/Python-3.7/bin/python
# /usr/local/depot/Python-3.5.1/bin/python

from hoho import pedestal_values, experimental_values, global_functions
from paper import plot_canvas
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

crit = 'alfven'
crit_value = 0.1
fixed_width = False
frac_uncertainty = 0.1
exclud_mode = []
color_exp = plot_canvas.colorHPLG
color_europed_eta0 = plot_canvas.color_eta0
color_europed_eta1 = plot_canvas.color_eta1
linestyle_n20 = plot_canvas.linestyle_n20
linestyle_n50 = plot_canvas.linestyle_n50
shot = 84794
dda = 'T052'
markersize = 20
alpha = 0.5

fig, axs = plt.subplots(1, 3)


psis = np.linspace(0,1.1,500)


europed_name = 'tan_eta0_rs0.022_neped2.57_betap1.3'
te,ne = pedestal_values.create_profiles(europed_name,psis,crit=crit,crit_value=crit_value, fixed_width=fixed_width, exclud_mode = exclud_mode)
pe = 1.6*ne*te
axs[0].plot(psis, ne, color=color_europed_eta0)
axs[1].plot(psis, te, color=color_europed_eta0)
axs[2].plot(psis, pe, color=color_europed_eta0)

te_m,ne_m = pedestal_values.create_profiles(europed_name,psis,crit=crit,crit_value=crit_value*(1-frac_uncertainty), fixed_width=fixed_width, exclud_mode = exclud_mode)
pe_m = 1.6*ne_m*te_m
te_p,ne_p = pedestal_values.create_profiles(europed_name,psis,crit=crit,crit_value=crit_value*(1+frac_uncertainty), fixed_width=fixed_width, exclud_mode = exclud_mode)
pe_p = 1.6*ne_p*te_p
axs[2].fill_between(psis, pe_m, pe_p, color=color_europed_eta0, alpha=0.2)


europed_name = 'tan_eta1_rs0.022_neped2.57_betap1.3'
te,ne = pedestal_values.create_profiles(europed_name,psis,crit=crit,crit_value=crit_value, fixed_width=fixed_width, exclud_mode = exclud_mode)
pe = 1.6*ne*te
axs[0].plot(psis, ne, color=color_europed_eta1, linestyle=linestyle_n50)
axs[1].plot(psis, te, color=color_europed_eta1, linestyle=linestyle_n50)
axs[2].plot(psis, pe, color=color_europed_eta1, linestyle=linestyle_n50)

te_m,ne_m = pedestal_values.create_profiles(europed_name,psis,crit=crit,crit_value=crit_value*(1-frac_uncertainty), fixed_width=fixed_width, exclud_mode = exclud_mode)
pe_m = 1.6*ne_m*te_m
te_p,ne_p = pedestal_values.create_profiles(europed_name,psis,crit=crit,crit_value=crit_value*(1+frac_uncertainty), fixed_width=fixed_width, exclud_mode = exclud_mode)
pe_p = 1.6*ne_p*te_p
axs[2].fill_between(psis, pe_m, pe_p, color=color_europed_eta1, alpha=0.2)

europed_name = 'tan_eta1_rs0.022_neped2.57_betap1.3'
exclud_mode = [30,40,50]
te,ne = pedestal_values.create_profiles(europed_name,psis,crit=crit,crit_value=crit_value, fixed_width=fixed_width, exclud_mode = exclud_mode)
pe = 1.6*ne*te
axs[0].plot(psis, ne, color=color_europed_eta1, linestyle=linestyle_n20)
axs[1].plot(psis, te, color=color_europed_eta1, linestyle=linestyle_n20)
axs[2].plot(psis, pe, color=color_europed_eta1, linestyle=linestyle_n20)



psi, pe_exp = experimental_values.get_pe_points(shot, dda)
psi, ne_exp = experimental_values.get_ne_points(shot, dda)
psi, te_exp = experimental_values.get_te_points(shot, dda)

axs[0].scatter(psi, ne_exp, s=markersize, alpha=alpha, color=color_exp)
axs[1].scatter(psi, te_exp, s=markersize, alpha=alpha, color=color_exp)
axs[2].scatter(psi, pe_exp, s=markersize, alpha=alpha, color=color_exp)



axs[0].set_xlabel(r'$\psi_N$')
axs[1].set_xlabel(r'$\psi_N$')
axs[2].set_xlabel(r'$\psi_N$')
axs[0].set_ylabel(global_functions.ne_label)
axs[1].set_ylabel(global_functions.te_label)
axs[2].set_ylabel(global_functions.pe_label)

axs[0].axvline(1, linestyle=':', color='black')
axs[1].axvline(1, linestyle=':', color='black')
axs[2].axvline(1, linestyle=':', color='black')

axs[1].text(1,1.5, r'$T_e^{\mathrm{sep}} = 100 \mathrm{eV}$', horizontalalignment='center', verticalalignment='center', backgroundcolor='white', fontsize=10, rotation=90)

axs[0].set_xlim(left=0.8, right=1.05)
axs[1].set_xlim(left=0.8, right=1.05)
axs[2].set_xlim(left=0.8, right=1.05)
axs[0].set_ylim(bottom=0, top=3)
axs[1].set_ylim(bottom=0, top=2)
axs[2].set_ylim(bottom=0, top=8)



plt.show()