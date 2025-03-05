#!/usr/local/depot/Python-3.7/bin/python
# /usr/local/depot/Python-3.5.1/bin/python

import pandas as pd
import matplotlib.pyplot as plt
from hoho import pedestal_values, global_functions, critical_helena_profile, helena_read, helena_output_file
import numpy as np
from scipy.interpolate import splrep, splev
from pytokamak.pyTokamak.tokamak.formats import geqdsk


run_name = 'EFIT_kbm0076.DATA'
eqdsk1 = geqdsk.read(f'/home/jwp9427/JT-60SA/{run_name}') 

f_eqdsk1 = eqdsk1['fpol']
psi_eqdsk1 = eqdsk1['psi']
r1 = eqdsk1['r']
z = eqdsk1['z']
index0_1 = np.nanargmin(np.abs(z))

ffprime1 = f_eqdsk1 * np.gradient(f_eqdsk1, psi_eqdsk1[:,0])
ffp_1 = eqdsk1['ffprime']

run_name = 'jt-60sa0.1532_crit1'

eqdsk2 = geqdsk.read(f'/home/jwp9427/work/chease/eqdsk/{run_name}') 
# eqdsk2 = geqdsk.read(f'/home/jwp9427/work/helena/geqdsk/{run_name}') 


ffp_2 = eqdsk2['ffprime']
psi_eqdsk2 = eqdsk2['psi']
r2 = eqdsk2['r']
z = eqdsk2['z']
index0_2 = np.nanargmin(np.abs(z))

a = helena_read.read_eliteinp(run_name)
psi_europed = a['Psi']
ffprime_europed = a['ffp']
R_europed = a['R']
z_europed = a['z']

R_europed = R_europed.reshape(-1,len(ffprime_europed))
z_europed = z_europed.reshape(-1,len(ffprime_europed))


list_z = [np.abs(z) for z in z_europed[:,0]]


index0_2_bis = np.nanargmin(list_z)






# # x, y = psi_eqdsk2.shape

# # temp = psi_eqdsk2.flatten()

# # psi_eqdsk2 = temp.reshape(y,x)

# print(r2[:,index0_2].shape)
# print(psi_eqdsk2[:,index0_2].shape)
# print(r1[:,index0_1].shape)
# print(psi_eqdsk1[:,index0_1].shape)
# # print(f_eqdsk2.shape)

# print()

# plt.plot(r1,[np.sum(psi_eqdsk1[:i,index0_1]) for i in range(len(psi_eqdsk1[:,index0_1]))])
# plt.plot(r2[1::2,index0_2],psi_eqdsk2[1::2,index0_2], color='blue')
# plt.plot(r1[:,index0_1],psi_eqdsk1[:,index0_1], color='red')

correct_r2 = (r2[:,index0_2]-min(r2[:,index0_2]))/(max(r2[:,index0_2])-min(r2[:,index0_2]))

slice_R_europed = R_europed[index0_2_bis,:]
correct_R_europed = (slice_R_europed-min(slice_R_europed))/(max(slice_R_europed)-min(slice_R_europed))
correct_r1 = (r1[:,index0_1]-min(r1[:,index0_1]))/(max(r1[:,index0_1])-min(r1[:,index0_1]))


# plt.plot(psi_europed/np.max(psi_europed),ffprime_europed, color='tab:blue', label='Europed')
# plt.plot(psi_eqdsk1[0]/np.max(psi_eqdsk1[0]),ffp_1, color='tab:orange', label='CDBM')

# plt.plot(correct_R_europed,ffprime_europed, color='tab:blue', label='Europed')
plt.plot(correct_r1,ffp_1, color='tab:orange', label='Local')
plt.plot(correct_r2,ffp_2, color='tab:blue', label='Europed')
# plt.plot(r1,[np.sum(psi_eqdsk1[:i,index0_1]) for i in range(len(psi_eqdsk1[:,index0_1]))])
# plt.plot(r2,[np.sum(psi_eqdsk2[:i,index0_2]) for i in range(len(psi_eqdsk2[:,index0_2]))])
# plt.plot(range(len(psi_eqdsk2[0,:])),psi_eqdsk2[0,:])
plt.xlabel(r'$\bar{r}$')
plt.ylabel(r'$F F^\prime$')
plt.legend()


plt.show()



# plt.plot(psi_eqdsk1[:,0], ffprime1, color='tab:orange')
# plt.plot(psi_eqdsk2[:,0], ffprime2, color='tab:red')


plt.show()