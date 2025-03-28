#!/usr/local/depot/Python-3.7/bin/python
# /usr/local/depot/Python-3.5.1/bin/python

import pandas as pd
import matplotlib.pyplot as plt
from hoho import pedestal_values, global_functions, experimental_values
from scipy.interpolate import griddata
import numpy as np
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.colors import Normalize
from sklearn.linear_model import LinearRegression




list_shot = [87342, 84794, 84791, 84792, 84793, 84795, 84796, 84797, 84798, 87335, 87336, 87337, 87338, 87339, 87340, 87341, 87342, 87344, 87346, 87348, 87349, 87350]
list_dda = [global_functions.dict_shot_dda[s] for s in list_shot]




norm = Normalize(vmin=0, vmax=1)  # Normalize the data between -100 and 100
cmap = cm.inferno_r  # Use the 'viridis' colormap
# Create a scatter plot with colors mapped to 'z'
colors = []
markers = []

lists = [[],[],[]]

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')


for shot, dda in zip(list_shot, list_dda):
    neped, neped_err = experimental_values.get_neped(shot, dda)
    nesepneped, nesepneped_err = experimental_values.get_nesepneped(shot, dda)
    betan, betan_err = experimental_values.get_betan(shot, dda)
    gasrate, g_err = experimental_values.get_gasrate(shot, dda)

    if gasrate <= 0.5e22:
        marker = 's'
        color = 'blue'
        i = 0
    elif gasrate <= 1.5e22:
        marker = 'o'
        color = 'green'
        i = 1
    else:
        marker = '^'
        color = 'magenta'
        i = 2

    ax.scatter(neped, nesepneped, betan, c=color, marker=marker)

    lists[i].append((neped, nesepneped, betan))

ax.set_xlabel(global_functions.neped_label)
ax.set_ylabel(global_functions.nesepneped_label)
ax.set_zlabel(global_functions.betan_label)


colors_i = ['blue','green','magenta']
for i in range(3):
    ll = lists[i]
    x = np.array([l[0] for l in ll])
    y = [l[1] for l in ll]
    z = [l[2] for l in ll]

    # Prepare the input for the regression
    X = np.column_stack((x, y))
    model = LinearRegression()
    model.fit(X, z)


    data = np.vstack((x, y, z)).T  # Transpose to get shape (120, 3)

    # Calculate the mean of the points, i.e. the 'center' of the cloud
    datamean = data.mean(axis=0)

    # Do an SVD on the mean-centered data.
    uu, dd, vv = np.linalg.svd(data - datamean)

    # Now vv[0] contains the first principal component, i.e. the direction
    # vector of the 'best fit' line in the least squares sense.

    # Now generate some points along this best fit line, for plotting.

    # I use -7, 7 since the spread of the data is roughly 14
    # and we want it to have mean 0 (like the points we did
    # the svd on). Also, it's a straight line, so we only need 2 points.
    linepts = vv[0] * np.mgrid[-7:7:2j][:, np.newaxis]

    # shift by the mean to get the line in the right place
    linepts += datamean
    ax.plot3D(*linepts.T, color=colors_i[i])

ax.set_xlim(2,4)
ax.set_ylim(0.2,0.7)
ax.set_zlim(1,3.5)

plt.show()
