#!/usr/local/depot/Python-3.7/bin/python
# /usr/local/depot/Python-3.5.1/bin/python

import pandas as pd
import matplotlib.pyplot as plt
from hoho import pedestal_values, global_functions, critical_helena_profile, helena_read, helena_output_file
import numpy as np
from scipy.interpolate import splrep, splev
from pytokamak.pyTokamak.tokamak.formats import geqdsk

fig, axs = plt.subplots(3,2, sharex=True)

file_path = '/home/jwp9427/JT-60SA/profiles_kbm0076.txt'
skip_lines = list(range(34))+[35]
df = pd.read_csv(file_path, sep=r',\s*', skiprows=skip_lines, dtype=np.float)

psis = np.array(df['psi'])
te = np.array(df['Te'])
ne = np.array(df['ne'])

area = np.array(df['area'])

axs[0,0].plot(psis,te, color='tab:orange')
axs[1,0].plot(psis,ne, color='tab:orange')
axs[2,0].plot(psis,1.6*ne*te, label='Local', color='tab:orange')



europed_name = 'jt-60sa_op2baseline_2_eta0_Zeff1.8'
te_crit, ne_crit = pedestal_values.create_critical_profiles(europed_name, psis, crit='alfven', crit_value=0.03, exclud_mode = [40,50], list_consid_mode = None)
axs[0,0].plot(psis,te_crit, color='tab:blue')
axs[1,0].plot(psis,ne_crit, color='tab:blue')
axs[2,0].plot(psis,1.6*te_crit*ne_crit, label='Europed - newEQDSK', color='tab:blue')

europed_name_bis = 'jt-60sa_op2baseline_mishka_oldEQDSK'
te_crit, ne_crit = pedestal_values.create_critical_profiles(europed_name_bis, psis, crit='alfven', crit_value=0.03, exclud_mode = [40,50], list_consid_mode = None)
axs[0,0].plot(psis,te_crit, color='tab:red')
axs[1,0].plot(psis,ne_crit, color='tab:red')
axs[2,0].plot(psis,1.6*te_crit*ne_crit, label='Europed - oldEQDSK', color='tab:red')


psin_label = global_functions.psiN_label
ne_label = global_functions.ne_label
te_label = global_functions.te_label
pe_label = global_functions.pe_label

axs[2,0].set_xlabel(psin_label)
axs[1,0].set_xlabel(psin_label)
axs[0,0].set_xlabel(psin_label)
axs[2,1].set_xlabel(psin_label)
axs[1,1].set_xlabel(psin_label)
axs[0,1].set_xlabel(psin_label)
axs[0,0].set_ylabel(te_label)
axs[1,0].set_ylabel(ne_label)
axs[2,0].set_ylabel(pe_label)

axs[1,0].tick_params(labelbottom=True)
axs[0,0].tick_params(labelbottom=True)
axs[1,1].tick_params(labelbottom=True)
axs[0,1].tick_params(labelbottom=True)

axs[2,0].legend()
axs[2,0].set_xlim(left=0, right=1)
axs[0,0].set_ylim(bottom=0)
axs[1,0].set_ylim(bottom=0)
axs[2,0].set_ylim(bottom=0)


try:
    psi = critical_helena_profile.get_profile_eliteinp('Psi',europed_name, exclud_mode=[40,50])
    psi = psi/psi[-1]
    q = critical_helena_profile.get_profile_eliteinp('q',europed_name, exclud_mode=[40,50])
    axs[0,1].plot(psi, q, color='tab:blue')
    psi = critical_helena_profile.get_profile_eliteinp('Psi',europed_name_bis, exclud_mode=[40,50])
    psi = psi/psi[-1]
    q = critical_helena_profile.get_profile_eliteinp('q',europed_name_bis, exclud_mode=[40,50])
    axs[0,1].plot(psi, q, color='tab:red')
except TypeError:
    pass

# try:
#     psi = critical_helena_profile.get_profile_eliteinp('Psi',europed_name, exclud_mode=[40,50])
#     psi = psi/psi[-1]
#     Bp = critical_helena_profile.get_profile_eliteinp('Bp',europed_name, exclud_mode=[40,50])

#     Bp = np.array(Bp)
#     Bp_reshaped = Bp.reshape(len(Bp)//301,301)
#     Bp_average = np.mean(Bp_reshaped, axis=0)
#     axs[2,1].plot(psi, Bp_average, color='tab:blue')
#     psi = critical_helena_profile.get_profile_eliteinp('Psi',europed_name_bis, exclud_mode=[40,50])
#     psi = psi/psi[-1]
#     Bp = critical_helena_profile.get_profile_eliteinp('Bp',europed_name_bis, exclud_mode=[40,50])

#     Bp = np.array(Bp)
#     Bp_reshaped = Bp.reshape(len(Bp)//301,301)
#     Bp_average = np.mean(Bp_reshaped, axis=0)
#     axs[2,1].plot(psi, Bp_average, color='tab:red')

# except TypeError:
#     pass

# try:
#     psij, j = critical_helena_profile.get_profile_psij(europed_name_bis, exclud_mode=[40,50])
#     j = j
#     axs[1,1].plot(psij, j, color='tab:pink')
#     psij, j = critical_helena_profile.get_profile_psij_bis(europed_name_bis, exclud_mode=[40,50])
#     j = j
#     axs[1,1].plot(psij, j, color='tab:red')
# except FileNotFoundError as e:
#     pass

run_name = 'EFIT.DATA'
eqdsk = geqdsk.read(f'/home/jwp9427/JT-60SA/{run_name}') 

f_eqdsk1 = eqdsk['fpol']
psi_eqdsk1 = eqdsk['psi']

# print(psi_eqdsk1.shape)
# print(f_eqdsk1.shape)

# print(psi_eqdsk1.shape)
# print(f_eqdsk1.shape)

# ffprime1 = f_eqdsk1 * np.gradient(f_eqdsk1, psi_eqdsk1[:,0])

# axs[1,1].plot(psi_eqdsk1[:,0], ffprime1, color='tab:orange')

# run_name = 'jt-60sa0.964_5_new'
# eqdsk = geqdsk.read(f'/home/jwp9427/work/chease/eqdsk/{run_name}') 

# f_eqdsk2 = eqdsk['fpol']
# psi_eqdsk2 = eqdsk['psi']

# print('HEEEEERE')
# print(psi_eqdsk2.shape)
# print(f_eqdsk2.shape)




# ffprime2 = f_eqdsk2 * np.gradient(f_eqdsk2, psi_eqdsk2[:,0])

# axs[1,1].plot(psi_eqdsk2[:,0], ffprime2, color='tab:red')




q_aiba = np.array(df['q'])
j_aiba = np.array(df['j_total'])
j_aibaBS = np.array(df['j_BS'])
Bp_aiba = np.array(df['<Bp>'])
area_aiba = np.array(df['area'])
length = np.array(df['len'])



file_path = '/home/jwp9427/JT-60SA/profiles_refreshed.txt'
skip_lines = list(range(34))+[35]
df = pd.read_csv(file_path, sep=r',\s*', skiprows=skip_lines, dtype=np.float)
q_aiba2 = np.array(df['q'])


# a = helena_output_file.HelenaOutput('/home/jwp9427/work/helena/output/jt-60sa0.1241_crit1')
# s_jz = a.s_jz
# psi_jz = s_jz**2
# jz = a.jz

# jbs = a.jbs
# psi_bs = a.psi2
# bt = a.bt
# rbphi = a.rbphi
# b = helena_read.read_eliteinp('jt-60sa0.1240_crit1')
# R = b['R'].reshape(301, len(b['R'])//301)
# R_average = np.mean(R, axis=1)
# rbphi = np.array(rbphi)
# R0 = a.rmag

# bt_profile = rbphi * R0 * bt / R_average
# bt_profile = bt_profile[1:-1]

# # jbs = jbs * 1e-6 / bt_profile
# # j = j * np.mean(bt_profile)/bt_profile
# # axs[1,1].plot(psij, j, color='tab:gray')



axs[0,1].plot(psis, q_aiba2, linestyle=':', color='tab:orange')
axs[0,1].plot(psis, q_aiba, color='tab:orange')
# # axs[1,1].plot(psis, j_aiba, color='tab:orange')
# # axs[1,1].plot(psi_jz, jz, color='tab:blue', label='Europed')
# # # axs[1,1].plot(psis, j_aiba-j_aibaBS, color='tab:orange', linestyle='--')
# # axs[1,1].plot(psis, j_aibaBS, color='tab:green', linestyle='dotted')
# # axs[1,1].plot(psi_bs, jbs, color='tab:purple', linestyle='dotted')
# # # axs[1,1].plot(psis, j_aibaBS, color='tab:orange', linestyle='dashed')
# axs[2,1].plot(psis, Bp_aiba, color='tab:orange')

axs[0,1].set_ylabel(r'$q$')
# axs[1,1].set_ylabel(r'${j_{tot}}_{[MA\cdot m^{-2}]}$')
axs[1,1].set_ylabel(r'$F Fprime$')
axs[2,1].set_ylabel(r'${B_{p}}_{[T]}$')

axs[0,1].set_ylim(bottom=0)
axs[1,1].set_ylim(bottom=0)
axs[2,1].set_ylim(bottom=0)



plt.show()




ja = j_aiba*area_aiba
length = np.array(length)
Bp_aiba = np.array(Bp_aiba)
cricB = Bp_aiba*length

integratedjds = np.array([np.sum(ja[:i]) for i in range(len(ja))])
normalisedJds = integratedjds * 1e6 * 4*np.pi*1e-7

# plt.plot(psis, normalisedJds)
# plt.plot(psis, cricB)
# plt.show()

helena_name = 'jt-60sa0.1241_crit1'
a = helena_read.read_output(helena_name)
psi = a['LIST 1']['PSI']
j = a['LIST 1']['<J>']
area = a['LIST 1']['AREA']
area = np.array(area)
other_j = a['LIST 11']['AVERAGE']
other_j = np.array(other_j)*1e-6
other_s = a['LIST 11']['S']
other_s = np.array(other_s)
other_psi = other_s**2

plt.plot(other_psi, other_j)
plt.plot(psis, j_aiba)
plt.show()

tck = splrep(psi, area, s=0)
area_3 = splev(other_s**2, tck)
area_3 = np.array(area_3)*1.1459**2

jdS = j[:-1]*(area[1:]-area[:-1])
integratedjds_2 = np.array([np.sum(jdS[:i]) for i in range(len(jdS))])



jdS_3 = other_j[:-1]*(area_3[1:]-area_3[:-1])
integratedjds_3 = np.array([np.sum(jdS_3[:i]) for i in range(len(jdS_3))])

jdS_4 = other_j[1:]*(area_3[1:]-area_3[:-1])
integratedjds_4 = np.array([np.sum(jdS_4[:i]) for i in range(len(jdS_4))])

plt.plot(psis, integratedjds, color='tab:orange')
plt.plot((other_s**2)[:-1], integratedjds_3, color='tab:purple')
plt.plot((other_s**2)[1:], integratedjds_4, color='tab:purple', linestyle=':')
plt.xlabel(r'$\psi_N$')
plt.ylabel(r'Integrated $J_{[MA]}$')
plt.show()

tck = splrep(other_psi[:-1], integratedjds_4, s=0)
integratedjds_4_onpsiaiba = splev(psis, tck)
diff_j_popo = integratedjds-integratedjds_4_onpsiaiba
plt.plot(psis,diff_j_popo)

plt.xlabel(r'$\psi_N$')
plt.ylabel(r'Integrated $J_{[MA]}$')
plt.show()


jmine = other_j
psimine = other_psi
j_aiba = j_aiba
psis_aiba = psis

tck = splrep(psimine, jmine, s=0)
jmine_onpsiaiba = splev(psis_aiba, tck)

diff_j = j_aiba - jmine_onpsiaiba
ja = diff_j*area_aiba
integrateddiffj = np.array([np.sum(ja[:i]) for i in range(len(ja))])

plt.plot(psis_aiba, integrateddiffj)

tck = splrep(psis_aiba, j_aiba, s=0)
jaiba_on_psimine = splev(psimine, tck)

diff_j_2 = jaiba_on_psimine - jmine
jdS = diff_j_2*(area[1:]-area[:-1])
integrateddiffj_2 = np.array([np.sum(jdS[:i]) for i in range(len(jdS))])
plt.plot(psi[:-1], integrateddiffj_2)

plt.xlabel(r'$\psi_N$')
plt.ylabel(r'Integrated $J_{[MA]}$')
plt.show()

# jdpsi_1 = j_aiba[:-1]*(psis[1:]-psis[:-1]) 
# jdpsi_2 = other_j[:-1]*(other_psi[1:]-other_psi[:-1]) 

# integrate_1 = [np.sum(jdpsi_1[:i]) for i in range(len(jdpsi_1))]
# integrate_2 = [np.sum(jdpsi_2[:i]) for i in range(len(jdpsi_2))]
# plt.plot(psis[:-1], integrate_1, color='tab:orange')
# plt.plot(other_psi[:-1], integrate_2, color='tab:purple')
# plt.xlabel(r'$\psi_N$')
# plt.ylabel(r'Integrated $J_{[MA \cdot m^{-2}]}$')
# plt.show()

# tck = splrep(psis, j_aiba, s=0)
# j_aiba_interp = splev(other_psi, tck)

# jdpsi_1 = j_aiba_interp[:-1]*(other_psi[1:]-other_psi[:-1]) 
# jdpsi_2 = other_j[:-1]*(other_psi[1:]-other_psi[:-1]) 

# integrate_1 = [np.sum(jdpsi_1[:i]) for i in range(len(jdpsi_1))]
# integrate_2 = [np.sum(jdpsi_2[:i]) for i in range(len(jdpsi_2))]
# plt.plot(other_psi[:-1], integrate_1, color='tab:orange')
# plt.plot(other_psi[:-1], integrate_2, color='tab:purple')
# plt.xlabel(r'$\psi_N$')
# plt.ylabel(r'Integrated $J_{[MA \cdot m^{-2}]}$')
# plt.show()



plt.plot(psis, np.array([np.sum(area_aiba[:i]) for i in range(len(area_aiba))]), color='tab:orange')
# plt.plot(psi, area, color='tab:blue')
plt.plot((other_s**2), area_3, color='tab:purple')
plt.xlabel(r'$\psi_N$')
plt.ylabel(r'$S_{[m^2]}$')
plt.show()


# tck = splrep(psi, q, s=0)
# q_on_psi_aiba = splev(psis, tck)

# tck = splrep(psi, Bp_average, s=0)
# Bp_on_psi_aiba = splev(psis, tck)

# plt.plot(psis, q_on_psi_aiba/q_aiba)
# plt.plot(psis, Bp_aiba /Bp_on_psi_aiba)
# plt.show()


