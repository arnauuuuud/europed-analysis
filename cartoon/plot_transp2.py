#!/usr/local/depot/Python-3.7/bin/python
# /usr/local/depot/Python-3.5.1/bin/python

from hoho import useful_recurring_functions, europed_analysis, global_functions, startup, find_pedestal_values_old
import matplotlib.pyplot as plt
import numpy as np
from netCDF4 import Dataset # Import netCDF library

TRANSPDat = Dataset("/common/transp_shared/Data/result/JET/84794/D05/D05.CDF") # Define the netCDF file path

curb = np.array(TRANSPDat.variables["CURB"]) # Export individual variables as numpy arrays 
cur = np.array(TRANSPDat.variables["CUR"]) # Export individual variables as numpy arrays 
psi = np.array(TRANSPDat.variables["PLFLX"])
q = np.array(TRANSPDat.variables["Q"])
time = np.array(TRANSPDat.variables["TIME"])
x = np.array(TRANSPDat.variables["X"])
ion_temp = np.array(TRANSPDat.variables["TI"])
 


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



plt.plot(time, pressure_w_fi[:,0])
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