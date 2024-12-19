#!/usr/local/depot/Python-3.7/bin/python
# /usr/local/depot/Python-3.5.1/bin/python

import pandas as pd
import matplotlib.pyplot as plt
from hoho import pedestal_values, global_functions, critical_helena_profile, helena_output_file, helena_read
import numpy as np


helena_name = 'jt-60sa0.1043_crit1'
file_path = '/home/jwp9427/JT-60SA/profiles_refreshed.txt'
skip_lines = list(range(34))+[35]
df = pd.read_csv(file_path, sep=r',\s*', skiprows=skip_lines, dtype=np.float)

helena_path = '/home/jwp9427/work/helena/output/'
helena_path += helena_name

psi_jt = df['psi']
jbs_jt = df['j_BS']

plt.plot(psi_jt, jbs_jt, label='Local')

a = helena_output_file.HelenaOutput('/home/jwp9427/work/helena/output/jt-60sa0.1043_crit1')
jbs = a.jbs
psi = a.psi2
bt = a.bt
rbphi = a.rbphi
b = helena_read.read_eliteinp('jt-60sa0.1043_crit1')
R = b['R'].reshape(301, len(b['R'])//301)
R_average = np.mean(R, axis=1)
rbphi = np.array(rbphi)
R0 = a.rmag

bt_profile = rbphi * R0 * bt / R_average
bt_profile = bt_profile[1:-1]

jbs = jbs * 1e-6 / bt_profile
plt.plot(psi, jbs, label='Europed - Sauter')

# hjbt = a.hjbt * 1e-6 / bt_profile
# plt.plot(psi, hjbt, label='Test - Sauter')

# a = helena_output_file.HelenaOutput('/home/jwp9427/work/helena/output/jt-60sa0.1044_crit1')
# jbs = a.jbs
# psi = a.psi2
# bt = a.bt
# rbphi = a.rbphi
# b = helena_read.read_eliteinp('jt-60sa0.1044_crit1')
# R = b['R'].reshape(301, len(b['R'])//301)
# R_average = np.mean(R, axis=1)
# rbphi = np.array(rbphi)
# R0 = a.rmag

# bt_profile = rbphi * R0 * bt / R_average
# bt_profile = bt_profile[1:-1]

# jbs = jbs * 1e-6 / bt_profile
# plt.plot(psi, jbs, label='Europed - Hager')

# hjbt = a.hjbt * 1e-6 / bt_profile
# plt.plot(psi, hjbt, label='Test - Hager')

# a = helena_output_file.HelenaOutput('/home/jwp9427/work/helena/output/jt-60sa0.1048_crit1')
# jbs = a.jbs
# psi = a.psi2
# bt = a.bt
# rbphi = a.rbphi
# b = helena_read.read_eliteinp('jt-60sa0.1048_crit1')
# R = b['R'].reshape(301, len(b['R'])//301)
# R_average = np.mean(R, axis=1)
# rbphi = np.array(rbphi)
# R0 = a.rmag

# bt_profile = rbphi * R0 * bt / R_average
# bt_profile = bt_profile[1:-1]

# jbs = jbs * 1e-6 / bt_profile
# plt.plot(psi, jbs, label='Europed - Redl')

# hjbt = a.hjbt * 1e-6 / bt_profile
# plt.plot(psi, hjbt, label='Test - Redl')

# a = helena_output_file.HelenaOutput('/home/jwp9427/work/helena/output/jt-60sa0.1046_crit1')
# jbs = a.jbs
# psi = a.psi2
# bt = a.bt
# rbphi = a.rbphi
# b = helena_read.read_eliteinp('jt-60sa0.1046_crit1')
# R = b['R'].reshape(301, len(b['R'])//301)
# R_average = np.mean(R, axis=1)
# rbphi = np.array(rbphi)
# R0 = a.rmag

# bt_profile = rbphi * R0 * bt / R_average
# bt_profile = bt_profile[1:-1]

# jbs = jbs * 1e-6 / bt_profile
# bt_profile = rbphi * R0 * bt / R_average
# bt_profile = bt_profile[1:-1]
# plt.plot(psi, jbs, label='Europed - Koh')

# # hjbt = a.hjbt * 1e-6 / bt_profile
# # plt.plot(psi, hjbt, label='Test - Koh')

# a = helena_output_file.HelenaOutput('/home/jwp9427/work/helena/output/jt-60sa0.1047_crit1')
# jbs = a.jbs
# psi = a.psi2
# bt = a.bt
# rbphi = a.rbphi
# b = helena_read.read_eliteinp('jt-60sa0.1047_crit1')
# R = b['R'].reshape(301, len(b['R'])//301)
# R_average = np.mean(R, axis=1)
# rbphi = np.array(rbphi)
# R0 = a.rmag

# bt_profile = rbphi * R0 * bt / R_average
# bt_profile = bt_profile[1:-1]

# jbs = jbs * 1e-6 / bt_profile
# plt.plot(psi, jbs, label='Europed - NEO')

# hjbt = a.hjbt * 1e-6 / bt_profile
# plt.plot(psi, hjbt, label='Test - NEO')

plt.xlabel(r'$\psi_N$')
plt.ylabel(r'${J_{bs}}_{\mathrm{[MA]}}$')
plt.legend()

plt.show()