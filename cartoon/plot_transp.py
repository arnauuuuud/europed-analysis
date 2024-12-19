#!/usr/local/depot/Python-3.7/bin/python
# /usr/local/depot/Python-3.5.1/bin/python

from hoho import useful_recurring_functions, europed_analysis, global_functions, startup, find_pedestal_values_old
import matplotlib.pyplot as plt
import numpy as np
from scipy import interpolate
from netCDF4 import Dataset # Import netCDF library
from matplotlib.ticker import ScalarFormatter


TRANSPDat = Dataset("/common/transp_shared/Data/result/JET/84794/D05/D05.CDF") # Define the netCDF file path
# TRANSPDat = Dataset("/common/transp_shared/Data/result/JET/87342/R01/R01.CDF") # Define the netCDF file path

curb = np.array(TRANSPDat.variables["CURB"]) # Export individual variables as numpy arrays 
cur = np.array(TRANSPDat.variables["CUR"]) # Export individual variables as numpy arrays 
psi = np.array(TRANSPDat.variables["PLFLX"])
q = np.array(TRANSPDat.variables["Q"])
time = np.array(TRANSPDat.variables["TIME"])
x = np.array(TRANSPDat.variables["X"])
ion_temp = np.array(TRANSPDat.variables["TI"])
ieta1 = np.array(TRANSPDat.variables["ETA_SP"])
ieta2 = np.array(TRANSPDat.variables["ETA_SPS"])
ieta3 = np.array(TRANSPDat.variables["ETA_WNC"])
ieta4 = np.array(TRANSPDat.variables["ETA_SNC"])
ne = np.array(TRANSPDat.variables["NE"])
te = np.array(TRANSPDat.variables["TE"])
fi = np.array(TRANSPDat.variables["BDENSTOTMP"])
q0 = np.array(TRANSPDat.variables["Q0"])
fi_energy = np.array(TRANSPDat.variables['EBAPLAV_MP'])
fi_energy2 = np.array(TRANSPDat.variables['EBAPPAV_MP'])
pressure_w_fi = np.array(TRANSPDat.variables['PTOWB'])
pressure = np.array(TRANSPDat.variables['PPLAS'])


# Plotting
print(time.shape)
print(fi.shape)
print(pressure_w_fi.shape)

interp_func = interpolate.interp1d(time, pressure_w_fi, kind='linear', axis=0)
pressure_profile = interp_func(5.51)

interp_func2 = interpolate.interp1d(time, x, kind='linear', axis=0)
x_profile = interp_func2(5.51)

print(min(time))
print(max(time))

ne_tab = np.zeros((1,50))
te_tab = np.zeros((1,50))
x_profile = np.zeros((1,50))


time_points = np.linspace(5.51, 8, 1)

interp_func_ne = interpolate.interp1d(time, ne, kind='linear', axis=0)
interp_func_te = interpolate.interp1d(time, te, kind='linear', axis=0)
interp_func2 = interpolate.interp1d(time, x, kind='linear', axis=0)
for i,timepoimt in enumerate(time_points):
    
    ne_tab[i] = interp_func_ne(timepoimt)
    te_tab[i] = interp_func_te(timepoimt)
   
    x_profile[i] = interp_func2(timepoimt)

x_profile = np.mean(x_profile,axis=0)**2
ne = np.mean(ne_tab,axis=0)*1e6
te = np.mean(te_tab,axis=0)

# plt.plot(x_profile, ne, label='NE')
plt.plot(x_profile, te, label='TE')
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