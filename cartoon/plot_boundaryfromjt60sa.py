#!/usr/local/depot/Python-3.7/bin/python
# /usr/local/depot/Python-3.5.1/bin/python

from hoho import overlay_plot_on_image
import pandas as pd
import matplotlib.pyplot as plt

# image_input = '/home/jwp9427/pp'
# image_xticks = '/home/jwp9427/ppX'
# image_yticks = '/home/jwp9427/ppY'
# xticklabels = [1,'-',2,'-',3,'-',4,'-',5,'-',6]
# yticklabels = [4,3.5,3,2.5,2,1.5,1,0.5,0,-0.5,-1,-1.5,-2,-2.5,-3,-3.5,'-']
# image_output = 'yess'

df = pd.read_table('/home/jwp9427/work/bndfour/EFIT.DATA', skiprows=1, sep=' ', names=['x','y'])
x_array = df['x']
y_array = df['y']
plt.plot(x_array, y_array, label='Previous EQDSK')

df = pd.read_table('/home/jwp9427/work/bndfour/EFIT_kbm0076.DATA', skiprows=1, sep=' ', names=['x','y'])
x_array = df['x']
y_array = df['y']
plt.plot(x_array, y_array, label='Updated EQDSK (C=0076)')

plt.legend()
plt.xlabel(r'$R$ [$\mathrm{m}$]')
plt.ylabel(r'$Z$ [$\mathrm{m}$]')
plt.axis('equal')
plt.show()  

# overlay_plot_on_image.add_to_image(image_input, image_xticks, image_yticks, xticklabels, yticklabels, image_output, x_array, y_array)