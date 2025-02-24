#!/usr/local/depot/Python-3.7/bin/python
# /usr/local/depot/Python-3.5.1/bin/python

from pytokamak.pyTokamak.tokamak.formats import geqdsk
import os


run_name = 'EFIT_kbm0076.DATA'

a = geqdsk.read(f'/home/jwp9427/JT-60SA/{run_name}') 
nbdry = a['nbdry']
rbdry = a['rbdry']
zbdry = a['zbdry']

europed_dir = os.environ['EUROPED_DIR']
bnd_dir = f'{europed_dir}../bndfour'

with open(f'{bnd_dir}/{run_name}', 'w') as file:
    file.write(f'{nbdry}\n')
    for r,z in zip(rbdry, zbdry):
        file.write(f'{r} {z}\n')
