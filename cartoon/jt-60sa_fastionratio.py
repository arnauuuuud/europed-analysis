#!/usr/local/depot/Python-3.7/bin/python
# /usr/local/depot/Python-3.5.1/bin/python

import pandas as pd
import matplotlib.pyplot as plt
from hoho import pedestal_values, global_functions, critical_helena_profile, helena_read, helena_output_file
import numpy as np
from scipy.interpolate import splrep, splev
from pytokamak.pyTokamak.tokamak.formats import geqdsk

fig, axs = plt.subplots(1,2)

file_path = '/home/jwp9427/JT-60SA/profiles_refreshed.txt'
skip_lines = list(range(34))+[35]
df = pd.read_csv(file_path, sep=r',\s*', skiprows=skip_lines, dtype=np.float)

psi = np.array(df['psi'])
p_nbi = np.array(df['p_nbi'])
p_thermal = np.array(df['p_thermal'])

axs[1].plot(psi, p_nbi/p_thermal, label='ratio fast ion pressure')
axs[0].plot(psi, p_nbi, label='fast ion pressure')
axs[0].plot(psi, p_thermal, label='thermal pressure')


x = np.linspace(0,1,500)
b = 0.9

for b in [2]:
    a = 1
    k = 0.2
    y = k*(1-(x/a)**2)**b
    y[x>a] = 0

    axs[1].plot(x,y, label=f'ratio Europed b={b}')

plt.legend()
plt.show()