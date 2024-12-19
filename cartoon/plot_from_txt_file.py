#!/usr/local/depot/Python-3.7/bin/python
# /usr/local/depot/Python-3.5.1/bin/python

import pandas as pd
import matplotlib.pyplot as plt

file_path = '/home/jwp9427/JT60SA/profiles.txt_2024Jul26'
skip_lines = 34
df = pd.read_csv(file_path, sep=r',\s+', skiprows=skip_lines)

psis = list(df['psi'])[1:]
te = list(df['Te'])[1:]
ne = list(df['ne'])[1:]

psis = [float(p) for p in psis]
te = [float(t) for t in te]
ne = [float(n) for n in ne]


plt.plot(psis,te)
plt.plot(psis,ne)
plt.show()