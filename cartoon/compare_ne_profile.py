#!/usr/local/depot/Python-3.7/bin/python
# /usr/local/depot/Python-3.5.1/bin/python

from hoho import useful_recurring_functions, europed_analysis, global_functions, startup, find_pedestal_values_old
import matplotlib.pyplot as plt
import numpy as np
from scipy import interpolate
from netCDF4 import Dataset # Import netCDF library
from matplotlib.ticker import ScalarFormatter
from ppf import ppfuid, ppfget
from scipy.interpolate import interp1d

TRANSPDat = Dataset("/common/transp_shared/Data/result/JET/84794/D05/D05.CDF") # Define the netCDF file path

fig,ax=plt.subplots()

psi = np.array(TRANSPDat.variables["PLFLX"])
time = np.array(TRANSPDat.variables["TIME"])
ne = np.array(TRANSPDat.variables["NE"])
te = np.array(TRANSPDat.variables["TE"])
for i in range(len(psi)):
    psi[i] = psi[i]/psi[i,-1]



ne_tab = np.zeros((1,50))
te_tab = np.zeros((1,50))
x_profile = np.zeros((1,50))



time_points = np.linspace(5.51, 8, 1)

interp_func_ne = interpolate.interp1d(time, ne, kind='linear', axis=0)
interp_func_te = interpolate.interp1d(time, te, kind='linear', axis=0)
interp_func2 = interpolate.interp1d(time, psi, kind='linear', axis=0)
for i,timepoimt in enumerate(time_points):
    
    ne_tab[i] = interp_func_ne(timepoimt)
    te_tab[i] = interp_func_te(timepoimt)
   
    x_profile[i] = interp_func2(timepoimt)

x_profile = np.mean(x_profile,axis=0)**2
ne = np.mean(ne_tab,axis=0)*1e6
te = np.mean(te_tab,axis=0)

# plt.plot(x_profile, ne, label='NE')
ax.plot(x_profile, ne, linewidth=3, linestyle='--', label='TRANSP')


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
ppfuid(uid)
ihdat,iwdat,temperature_fit,x,time,ier=ppfget(pulse=shot,dda=dda_global,dtyp=dtype_temp_fit)
ihdat,iwdat,density_fit,x,time,ier=ppfget(pulse=shot,dda=dda_global,dtyp=dtype_density_fit)
ihdat,iwdat,psi_fit,x,time,ier=ppfget(pulse=shot,dda=dda_global,dtyp=dtype_psi_fit)

temperature_fit = temperature_fit * 1e3
density_fit = density_fit * 1e19

interp = interp1d(temperature_fit, psi_fit)
psi_sep = np.interp([0.1], temperature_fit, psi_fit)[0]
psi_sep = interp(100)
psi_fit = np.array(psi_fit) + 1 - psi_sep
ax.plot(psi_fit,density_fit,linewidth=3, linestyle='-', label='PPF FIT')


europed_name = 'tan_eta0_rs0.022_neped2.57_betap1.3w'
psis = np.linspace(0,1,100)
te,ne,dump2 = find_pedestal_values_old.create_profiles(europed_name,psis,crit='alfven')
te = te*1e3
ne = ne*1e19
ax.plot(psis,ne, linewidth=3, linestyle=':', label='Critical Ruroped')


ax.set_ylim(bottom=0)
ax.set_xlim(left=0, right=1)
ax.set_xlabel(r'$\psi_N$')
ax.set_ylabel(r'$T_e$ [keV]')
ax.set_ylabel(r'$n_e$ [m^-3]')

plt.gca().yaxis.set_major_formatter(ScalarFormatter(useMathText=True))
plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
plt.legend()
plt.show()

# plt.plot(time, fi)

# plt.show()
# plt.plot(time, q0)

# plt.show()

# # plt.plot(x, q)
# # plt.show()

# # print(x.shape)
# # print(fi.shape)
# # plt.plot(x, ion_temp)
# # plt.show()

# plt.plot(x, fi_energy)
# plt.show()

# plt.plot(x, fi_energy2)
# plt.show()

# plt.plot(x, pressure_w_fi)
# plt.show()

# plt.plot(x, pressure)
# plt.show()

# # plt.plot(x, pressure_w_fi-pressure)
# # plt.show()

# # plt.plot(x, cur)
# # plt.show()

# # plt.plot(x, curb)
# # plt.show()