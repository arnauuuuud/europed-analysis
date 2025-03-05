#!/usr/local/depot/Python-3.7/bin/python
# /usr/local/depot/Python-3.5.1/bin/python

import pandas as pd
import matplotlib.pyplot as plt
from hoho import pedestal_values, global_functions, critical_helena_profile, helena_output_file
import numpy as np

plt.rc('axes', labelsize=20)

file_path = '/home/jwp9427/JT-60SA/profiles_kbm0076.txt'
skip_lines = 34
df = pd.read_csv(file_path, sep=r',\s+', skiprows=skip_lines)

psis = list(df['psi'])[1:]
te = list(df['Te'])[1:]
ne = list(df['ne'])[1:]

psis = [float(p) for p in psis]
te = np.array([float(t) for t in te])
ne = np.array([float(n) for n in ne])

europed_name_eta0 = 'jt-60sa_op2baseline_2_eta0_Zeff1.8'
europed_name_eta1 = 'jt-60sa_op2baseline_2_eta0_Zeff1.8_n20_gamma0_zoom'
# europed_name_eta1b = 'jt-60sa_op2baseline_eta1_zeff1'
te_crit_eta0, ne_crit_eta0 = pedestal_values.create_critical_profiles(europed_name_eta0, psis, crit='alfven', crit_value=0.03, exclud_mode = [40,50], list_consid_mode = None)
te_crit_eta1, ne_crit_eta1 = pedestal_values.create_critical_profiles(europed_name_eta1, psis, crit='alfven', crit_value=0.03, exclud_mode = [40,50], list_consid_mode = None)
te_crit_eta1b, ne_crit_eta1b = pedestal_values.create_critical_profiles(europed_name_eta1, psis, crit='alfven', crit_value=0.03, exclud_mode = [30,40,50], list_consid_mode = None)
psin_label = global_functions.psiN_label
ne_label = global_functions.ne_label
te_label = global_functions.te_label
pe_label = global_functions.pe_label


fig, ax = plt.subplots()

ax.plot(psis,te, color='tab:orange', label='QST')
ax.plot(psis,te_crit_eta0, color='tab:blue', label=r'Europed - $\eta=0$')
ax.plot(psis,te_crit_eta1, color='tab:red', label=r'Europed - $\eta=\eta_{\mathrm{neo}}$, $n \leq 30$')
# ax.plot(psis,te_crit_eta1b, color='purple', label=r'Europed - $\eta=\eta_{\mathrm{neo}}$, $n \leq 20$')
ax.set_ylabel(te_label)
ax.set_xlabel(psin_label)
ax.legend()
ax.set_xlim(left=0, right=1)
ax.set_ylim(bottom=0)
plt.show()


fig, ax = plt.subplots()
ax.plot(psis,ne, color='tab:orange', label='Local')
ax.plot(psis,ne_crit_eta0, color='tab:blue', label=r'Europed - $\eta=0$')
ax.plot(psis,ne_crit_eta1, color='tab:red', label=r'Europed - $\eta=\eta_{\mathrm{neo}}$, $n \leq 30$')
# ax.plot(psis,ne_crit_eta1b, color='purple', label=r'Europed - $\eta=\eta_{\mathrm{neo}}$, $n \leq 20$')
ax.set_ylabel(ne_label)
ax.set_xlabel(psin_label)
ax.legend()
ax.set_xlim(left=0, right=1)
ax.set_ylim(bottom=0)
plt.show()

fig, ax = plt.subplots()
ax.plot(psis,1.6*ne*te, color='tab:orange', label='Gotress - EPED')
ax.plot(psis,1.6*te_crit_eta0*ne_crit_eta0, color='tab:blue', label=r'Europed - $\eta=0$ - Compressible perturbation')
ax.plot(psis,1.6*te_crit_eta1*ne_crit_eta1, color='tab:red', label=r'Europed - $\eta=0$ - Incompressible perturbation')
# ax.plot(psis,1.6*te_crit_eta1*ne_crit_eta1, color='tab:red', label=r'Europed - $\eta=\eta_{\mathrm{neo}}$, $n \leq 30$')
# ax.plot(psis,1.6*te_crit_eta1b*ne_crit_eta1b, color='purple', label=r'Europed - $\eta=\eta_{\mathrm{neo}}$, $n \leq 20$')

# ax.text(0.05,0.05,r'$\beta_N(\mathrm{Europed}) \sim 2.15$, $\beta_N(\mathrm{Aiba-san}) = 2.184$' '\n' r'$\beta_p(\mathrm{Europed}) \sim 0.5$, $\beta_p(\mathrm{Aiba-san}) = 0.626$', transform=ax.transAxes)

ax.set_ylabel(pe_label)
ax.set_xlabel(psin_label)
ax.legend()
ax.set_xlim(left=0.8, right=1)
ax.set_ylim(bottom=0, top=30)
plt.show()

fig, ax = plt.subplots()
ax.plot(psis,1.8*1.6*ne*te, color='tab:orange', label='QST')
ax.plot(psis,1.8*1.6*te_crit_eta0*ne_crit_eta0, color='tab:blue', label='Europed')

# ax.text(0.05,0.05,r'$\beta_N(\mathrm{Europed}) \sim 2.15$, $\beta_N(\mathrm{Aiba-san}) = 2.184$' '\n' r'$\beta_p(\mathrm{Europed}) \sim 0.5$, $\beta_p(\mathrm{Aiba-san}) = 0.626$', transform=ax.transAxes)

ax.set_ylabel(r'$p_{[\mathrm{kPa}]}$')
ax.set_xlabel(psin_label)
ax.legend()
ax.set_xlim(left=0.8, right=1)
ax.set_ylim(bottom=0, top=30)
plt.show()



try:
    psi = critical_helena_profile.get_profile_eliteinp('Psi',europed_name)
    psi = psi/psi[-1]
    q = critical_helena_profile.get_profile_eliteinp('q',europed_name)
except TypeError:
    pass

try:
    psi = critical_helena_profile.get_profile_eliteinp('Psi',europed_name, exclud_mode=[40,50])
    psi = psi/psi[-1]
    Bp = critical_helena_profile.get_profile_eliteinp('Bp',europed_name, exclud_mode=[40,50])

    Bp = np.array(Bp)
    Bp_reshaped = Bp.reshape(len(Bp)//301,301)
    Bp_average = np.mean(Bp_reshaped, axis=0)
except TypeError:
    pass

try:
    psij, j = critical_helena_profile.get_profile_psij_bis(europed_name)
except FileNotFoundError:
    pass

q_aiba = list(df['q'])[1:]
j_aiba = list(df['j_total'])[1:]
Bp_aiba = list(df['<Bp>'])[1:]

q_aiba = [float(q) for q in q_aiba]
j_aiba = [float(j) for j in j_aiba]
Bp_aiba = [float(b) for b in Bp_aiba]



fig, ax = plt.subplots() 
ax.plot(psis, q_aiba, color='tab:orange', label='Local')
ax.plot(psi, q, color='tab:blue', label='Europed')
ax.set_ylabel(r'$q$')
ax.legend()
ax.set_xlabel(psin_label)
ax.set_ylim(bottom=0)
ax.set_xlim(left=0, right=1)
plt.show()

fig, ax = plt.subplots()
ax.plot(psis, j_aiba, color='tab:orange', label='Local')
ax.plot(psij, j, color='tab:blue', label='Europed')
ax.set_ylabel(r'${j_{tot}}_{[MA\cdot m^{-2}]}$')
ax.set_xlabel(psin_label)
ax.legend()
ax.set_ylim(bottom=0)
ax.set_xlim(left=0, right=1)
plt.show()

fig, ax = plt.subplots()
ax.plot(psis, Bp_aiba, color='tab:orange', label='Local')
ax.plot(psi, Bp_average[:301], color='tab:blue', label='Europed')
ax.set_ylabel(r'${B_{p}}_{[T]}$')
ax.set_xlabel(psin_label)
ax.legend()
ax.set_ylim(bottom=0)
ax.set_xlim(left=0, right=1)
plt.show()





