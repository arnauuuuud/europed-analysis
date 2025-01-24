#!/usr/local/depot/Python-3.7/bin/python
# /usr/local/depot/Python-3.5.1/bin/python

import pandas as pd
import matplotlib.pyplot as plt
from hoho import pedestal_values, global_functions, critical_helena_profile, helena_read, helena_output_file
import numpy as np
from scipy.interpolate import splrep, splev
from pytokamak.pyTokamak.tokamak.formats import geqdsk
import os

fig, axs = plt.subplots(3,2, sharex=True)

file_path = '/home/jwp9427/JT-60SA/profiles_refreshed.txt'
skip_lines = list(range(34))+[35]
df = pd.read_csv(file_path, sep=r',\s*', skiprows=skip_lines, dtype=np.float)

j_oh = df['j_OH']
j_tot = df['j_total']
j_BS = df['j_BS']
j_wo_BS = j_tot - j_BS

europed_dir = os.environ['EUROPED_DIR']
current_dir = f'{europed_dir}/current_profs'
filename = 'currentGOTRESS+_totjwobs'

with open(f'{current_dir}/{filename}', 'w') as file:
    for j in j_wo_BS:
        file.write(f'{j}e+06 \n')
