#!/usr/local/depot/Python-3.7/bin/python
# /usr/local/depot/Python-3.5.1/bin/python

import pandas as pd
import matplotlib.pyplot as plt
from hoho import pedestal_values, global_functions, experimental_values
import numpy as np
from matplotlib import cm
from matplotlib.colors import Normalize
from sklearn.linear_model import LinearRegression




list_shot = [87342, 84794, 84791, 84792, 84793, 84795, 84796, 84797, 84798, 87335, 87336, 87337, 87338, 87339, 87340, 87341, 87342, 87344, 87346, 87348, 87349, 87350]
list_dda = [global_functions.dict_shot_dda[s] for s in list_shot]

x = []
y = []
colors = []


# fig, ax = plt.subplots()


# colors = []
# markers = []

# lists = []

# for shot, dda in zip(list_shot, list_dda):
#     alpha, a_err = experimental_values.get_alpha_max(shot, dda)
#     nesepneped, p_err = experimental_values.get_nesepneped(shot, dda)
#     gasrate, g_err = experimental_values.get_gasrate(shot, dda)
#     betan, g_err = experimental_values.get_betan(shot, dda)

#     if gasrate <= 0.5e22:
#         marker = 's'
#         color = 'blue'
#         i = 0
#     elif gasrate <= 1.5e22:
#         marker = 'o'
#         color = 'green'
#         i = 1
#     else:
#         marker = '^'
#         color = 'magenta'
#         i = 2
#     # colors.append(color)
#     markers.append(marker)
#     ax.scatter(nesepneped,alpha,c=color, marker=marker)
#     lists.append((nesepneped,alpha))


# lbeta = np.array([l[0] for l in lists])
# lalph = [l[1] for l in lists]
# model1 = LinearRegression()
# lbeta = lbeta.reshape(-1, 1)
# model1.fit(lbeta, lalph)
# lbeta_to_plot = np.linspace(min(lbeta),max(lbeta),2).reshape(-1,1)
# lalph_to_plot = model1.predict(lbeta_to_plot)

# ax.plot(lbeta_to_plot, lalph_to_plot, c='black')

# ax.set_xlabel(global_functions.nesepneped_label)
# ax.set_ylabel(global_functions.alpha_label)
# ax.set_ylim(bottom=0)
# ax.set_xlim(left=0)
# plt.show()



# fig, ax = plt.subplots()


# colors = []
# markers = []

# lists = []

# for shot, dda in zip(list_shot, list_dda):
#     alpha, a_err = experimental_values.get_alpha_max(shot, dda)
#     nesepneped, p_err = experimental_values.get_nesepneped(shot, dda)
#     gasrate, g_err = experimental_values.get_gasrate(shot, dda)
#     power, g_err = experimental_values.get_power(shot, dda)

#     if not power<6*1e6:
#         continue



#     if gasrate <= 0.5e22:
#         marker = 's'
#         color = 'blue'
#         i = 0
#     elif gasrate <= 1.5e22:
#         marker = 'o'
#         color = 'green'
#         i = 1
#     else:
#         marker = '^'
#         color = 'magenta'
#         i = 2
#     # colors.append(color)
#     markers.append(marker)
#     ax.scatter(nesepneped,alpha,c=color, marker=marker)
#     lists.append((nesepneped,alpha))


# lbeta = np.array([l[0] for l in lists])
# lalph = [l[1] for l in lists]
# model1 = LinearRegression()
# lbeta = lbeta.reshape(-1, 1)
# model1.fit(lbeta, lalph)
# lbeta_to_plot = np.linspace(min(lbeta),max(lbeta),2).reshape(-1,1)
# lalph_to_plot = model1.predict(lbeta_to_plot)

# ax.plot(lbeta_to_plot, lalph_to_plot, c='black')

# ax.set_xlabel(global_functions.nesepneped_label)
# ax.set_ylabel(global_functions.alpha_label)
# ax.set_ylim(bottom=0)
# ax.set_xlim(left=0)
# plt.show()


# fig, ax = plt.subplots()


# colors = []
# markers = []

# lists = []

# for shot, dda in zip(list_shot, list_dda):
#     alpha, a_err = experimental_values.get_alpha_max(shot, dda)
#     nesepneped, p_err = experimental_values.get_nesepneped(shot, dda)
#     gasrate, g_err = experimental_values.get_gasrate(shot, dda)
#     power, g_err = experimental_values.get_power(shot, dda)

#     if not power>10*1e6:
#         continue



#     if gasrate <= 0.5e22:
#         marker = 's'
#         color = 'blue'
#         i = 0
#     elif gasrate <= 1.5e22:
#         marker = 'o'
#         color = 'green'
#         i = 1
#     else:
#         marker = '^'
#         color = 'magenta'
#         i = 2
#     # colors.append(color)
#     markers.append(marker)
#     ax.scatter(nesepneped,alpha,c=color, marker=marker)
#     lists.append((nesepneped,alpha))


# lbeta = np.array([l[0] for l in lists])
# lalph = [l[1] for l in lists]
# model1 = LinearRegression()
# lbeta = lbeta.reshape(-1, 1)
# model1.fit(lbeta, lalph)
# lbeta_to_plot = np.linspace(min(lbeta),max(lbeta),2).reshape(-1,1)
# lalph_to_plot = model1.predict(lbeta_to_plot)

# ax.plot(lbeta_to_plot, lalph_to_plot, c='black')

# ax.set_xlabel(global_functions.nesepneped_label)
# ax.set_ylabel(global_functions.alpha_label)
# ax.set_ylim(bottom=0)
# ax.set_xlim(left=0)
# plt.show()

# fig, ax = plt.subplots()


# colors = []
# markers = []

# lists = []

# for shot, dda in zip(list_shot, list_dda):
#     alpha, a_err = experimental_values.get_alpha_max(shot, dda)
#     nesepneped, p_err = experimental_values.get_nesepneped(shot, dda)
#     gasrate, g_err = experimental_values.get_gasrate(shot, dda)
#     betan, g_err = experimental_values.get_betan(shot, dda)

#     if not (betan>1.85 and betan<2.2):
#         continue



#     if gasrate <= 0.5e22:
#         marker = 's'
#         color = 'blue'
#         i = 0
#     elif gasrate <= 1.5e22:
#         marker = 'o'
#         color = 'green'
#         i = 1
#     else:
#         marker = '^'
#         color = 'magenta'
#         i = 2
#     # colors.append(color)
#     markers.append(marker)
#     ax.scatter(nesepneped,alpha,c=color, marker=marker)
#     lists.append((nesepneped,alpha))


# lbeta = np.array([l[0] for l in lists])
# lalph = [l[1] for l in lists]
# model1 = LinearRegression()
# lbeta = lbeta.reshape(-1, 1)
# model1.fit(lbeta, lalph)
# lbeta_to_plot = np.linspace(min(lbeta),max(lbeta),2).reshape(-1,1)
# lalph_to_plot = model1.predict(lbeta_to_plot)

# ax.plot(lbeta_to_plot, lalph_to_plot, c='black')

# ax.set_xlabel(global_functions.nesepneped_label)
# ax.set_ylabel(global_functions.alpha_label)
# ax.set_ylim(bottom=0)
# ax.set_xlim(left=0)
# plt.show()


# fig, axs = plt.subplots(1,2)
# ax1 = axs[0]
# ax2 = axs[1]

# norm = Normalize(vmin=0, vmax=1)  # Normalize the data between -100 and 100
# cmap = cm.inferno_r  # Use the 'viridis' colormap
# # Create a scatter plot with colors mapped to 'z'
# colors = []
# markers = []

# lists = [[],[],[]]

# for shot, dda in zip(list_shot, list_dda):
#     print()
#     print(shot)
#     print(dda)
#     alpha, a_err = experimental_values.get_alpha_max(shot, dda)
#     power, p_err = experimental_values.get_power(shot, dda)
#     gasrate, g_err = experimental_values.get_gasrate(shot, dda)

#     y.append(alpha)
#     x.append(power)
#     nesepneped = experimental_values.get_nesepneped(shot, dda)[0]
#     color = cmap(norm(nesepneped))
#     colors.append(color)

#     if gasrate <= 0.5e22:
#         marker = 's'
#         color = 'blue'
#         i = 0
#     elif gasrate <= 1.5e22:
#         marker = 'o'
#         color = 'green'
#         i = 1
#     else:
#         marker = '^'
#         color = 'magenta'
#         i = 2
#     # colors.append(color)
#     markers.append(marker)
#     power = power*1e-6

#     print(alpha)
#     ax1.scatter(power,alpha,c=color, marker=marker)
#     ax2.scatter(power,nesepneped,c=color, marker=marker)
#     lists[i].append((power,alpha,nesepneped))

# colors_i = ['blue','green','magenta']
# for i in range(3):
#     ll = lists[i]
#     lbeta = np.array([l[0] for l in ll])
#     lalph = [l[1] for l in ll]
#     lfrac = [l[2] for l in ll]
#     model1 = LinearRegression()
#     model2 = LinearRegression()
#     lbeta = lbeta.reshape(-1, 1)
#     model1.fit(lbeta, lalph)
#     model2.fit(lbeta, lfrac)
#     lbeta_to_plot = np.linspace(min(lbeta),max(lbeta),2).reshape(-1,1)
#     lalph_to_plot = model1.predict(lbeta_to_plot)
#     lfrac_to_plot = model2.predict(lbeta_to_plot)

#     ax1.plot(lbeta_to_plot, lalph_to_plot, c=colors_i[i])
#     ax2.plot(lbeta_to_plot, lfrac_to_plot, c=colors_i[i])


# ax1.set_xlabel(r'$P_{\mathrm{[MW]}}$')
# ax1.set_ylabel(r'$\alpha_{\mathrm{max}}$')
# ax1.set_ylim(bottom=0)
# ax1.set_xlim(left=0)
# ax2.set_xlabel(r'$P_{\mathrm{[MW]}}$')
# ax2.set_ylabel(global_functions.nesepneped_label)
# ax2.set_ylim(bottom=0)
# ax2.set_xlim(left=0)
# plt.show()

fig, ax = plt.subplots()


colors = []
markers = []

lists = [[],[],[]]

for shot, dda in zip(list_shot, list_dda):
    neped, a_err = experimental_values.get_neped(shot, dda)
    nesepneped, p_err = experimental_values.get_nesepneped(shot, dda)
    gasrate, g_err = experimental_values.get_gasrate(shot, dda)
    betan, g_err = experimental_values.get_betan(shot, dda)
    alpha, g_err = experimental_values.get_alpha_max(shot, dda)


    x_here = betan
    y_here = alpha

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
    # colors.append(color)
    markers.append(marker)
    ax.scatter(x_here,y_here,c=color, marker=marker)
    lists[i].append((x_here,y_here))

colors_i = ['blue','green','magenta']
for i in range(3):
    ll = lists[i]
    lbeta = np.array([l[0] for l in ll])
    lalph = [l[1] for l in ll]
    model1 = LinearRegression()
    lbeta = lbeta.reshape(-1, 1)
    model1.fit(lbeta, lalph)
    lbeta_to_plot = np.linspace(min(lbeta),max(lbeta),2).reshape(-1,1)
    lalph_to_plot = model1.predict(lbeta_to_plot)

    ax.plot(lbeta_to_plot, lalph_to_plot, c=colors_i[i])

ax.set_xlabel(global_functions.betan_label)
ax.set_ylabel(global_functions.alpha_label)
ax.set_ylim(bottom=0)
ax.set_xlim(left=0)
plt.show()

fig, ax = plt.subplots()


colors = []
markers = []

lists = [[],[],[]]

for shot, dda in zip(list_shot, list_dda):
    neped, a_err = experimental_values.get_neped(shot, dda)
    nesepneped, p_err = experimental_values.get_nesepneped(shot, dda)
    gasrate, g_err = experimental_values.get_gasrate(shot, dda)
    betan, g_err = experimental_values.get_betan(shot, dda)
    alpha, g_err = experimental_values.get_alpha_max(shot, dda)


    x_here = betan
    y_here = alpha

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
    # colors.append(color)
    markers.append(marker)
    ax.scatter(x_here,y_here,c=color, marker=marker)
    lists[i].append((x_here,y_here))

colors_i = ['blue','green','magenta']
for i in range(3):
    ll = lists[i]
    lbeta = np.array([l[0] for l in ll])
    lalph = [l[1] for l in ll]
    model1 = LinearRegression()
    lbeta = lbeta.reshape(-1, 1)
    model1.fit(lbeta, lalph)
    lbeta_to_plot = np.linspace(min(lbeta),max(lbeta),2).reshape(-1,1)
    lalph_to_plot = model1.predict(lbeta_to_plot)

    ax.plot(lbeta_to_plot, lalph_to_plot, c=colors_i[i])

ax.set_xlabel(global_functions.betan_label)
ax.set_ylabel(global_functions.pep)
ax.set_ylim(bottom=0)
ax.set_xlim(left=0)
plt.show()

# fig, axs = plt.subplots(1,2)
# ax1 = axs[0]
# ax2 = axs[1]

# lists = [[],[],[]]

# for shot, dda in zip(list_shot, list_dda):
#     alpha, a_err = experimental_values.get_alpha_max(shot, dda)
#     betan, betan_err = experimental_values.get_betan(shot, dda)
#     gasrate, g_err = experimental_values.get_gasrate(shot, dda)

#     nesepneped = experimental_values.get_nesepneped(shot, dda)[0]
#     if gasrate <= 0.5e22:
#         marker = 's'
#         color = 'blue'
#         i=0
#     elif gasrate <= 1.5e22:
#         marker = 'o'
#         color = 'green'
#         i=1
#     else:
#         marker = '^'
#         color = 'magenta'
#         i=2
#     # colors.append(color)
#     lists[i].append((betan,alpha,nesepneped))
#     ax1.scatter(betan,alpha,c=color, marker=marker)
#     ax2.scatter(betan,nesepneped,c=color, marker=marker)

# colors_i = ['blue','green','magenta']
# for i in range(3):
#     ll = lists[i]
#     lbeta = np.array([l[0] for l in ll])
#     lalph = [l[1] for l in ll]
#     lfrac = [l[2] for l in ll]
#     model1 = LinearRegression()
#     model2 = LinearRegression()
#     lbeta = lbeta.reshape(-1, 1)
#     model1.fit(lbeta, lalph)
#     model2.fit(lbeta, lfrac)
#     lbeta_to_plot = np.linspace(min(lbeta),max(lbeta),2).reshape(-1,1)
#     lalph_to_plot = model1.predict(lbeta_to_plot)
#     lfrac_to_plot = model2.predict(lbeta_to_plot)

#     ax1.plot(lbeta_to_plot, lalph_to_plot, c=colors_i[i])
    # ax2.plot(lbeta_to_plot, lfrac_to_plot, c=colors_i[i])



# ax1.set_xlabel(global_functions.betan_label)
# ax1.set_ylabel(r'$\alpha_{\mathrm{max}}$')
# ax1.set_ylim(bottom=0)
# ax1.set_xlim(left=0)
# ax2.set_xlabel(global_functions.betan_label)
# ax2.set_ylabel(global_functions.nesepneped_label)
# ax2.set_ylim(bottom=0)
# ax2.set_xlim(left=0)
# plt.show()


# fig, axs = plt.subplots(1,2)
# ax1 = axs[0]
# ax2 = axs[1]

# lists = [[],[],[]]

# for shot, dda in zip(list_shot, list_dda):
#     peped, a_err = experimental_values.get_peped(shot, dda)
#     betan, betan_err = experimental_values.get_betan(shot, dda)
#     gasrate, g_err = experimental_values.get_gasrate(shot, dda)

#     nesepneped = experimental_values.get_nesepneped(shot, dda)[0]
#     if gasrate <= 0.5e22:
#         marker = 's'
#         color = 'blue'
#         i=0
#     elif gasrate <= 1.5e22:
#         marker = 'o'
#         color = 'green'
#         i=1
#     else:
#         marker = '^'
#         color = 'magenta'
#         i=2
#     # colors.append(color)
#     lists[i].append((betan,peped,nesepneped))
#     ax1.scatter(betan,peped,c=color, marker=marker)
#     ax2.scatter(betan,nesepneped,c=color, marker=marker)

# colors_i = ['blue','green','magenta']
# for i in range(3):
#     ll = lists[i]
#     lbeta = np.array([l[0] for l in ll])
#     lalph = [l[1] for l in ll]
#     lfrac = [l[2] for l in ll]
#     model1 = LinearRegression()
#     model2 = LinearRegression()
#     lbeta = lbeta.reshape(-1, 1)
#     model1.fit(lbeta, lalph)
#     model2.fit(lbeta, lfrac)
#     lbeta_to_plot = np.linspace(min(lbeta),max(lbeta),2).reshape(-1,1)
#     lalph_to_plot = model1.predict(lbeta_to_plot)
#     lfrac_to_plot = model2.predict(lbeta_to_plot)

#     ax1.plot(lbeta_to_plot, lalph_to_plot, c=colors_i[i])
#     ax2.plot(lbeta_to_plot, lfrac_to_plot, c=colors_i[i])





# ax1.set_xlabel(global_functions.betan_label)
# ax1.set_ylabel(global_functions.peped_label)
# ax1.set_ylim(bottom=0)
# ax1.set_xlim(left=0)
# ax2.set_xlabel(global_functions.betan_label)
# ax2.set_ylabel(global_functions.nesepneped_label)
# ax2.set_ylim(bottom=0)
# ax2.set_xlim(left=0)
# plt.show()


# fig, ax = plt.subplots()

# lists = [[],[],[]]

# for shot, dda in zip(list_shot, list_dda):
#     alpha, a_err = experimental_values.get_alpha_max(shot, dda)
#     power, p_err = experimental_values.get_power(shot, dda)
#     betan, betan_err = experimental_values.get_betan(shot, dda)
#     gasrate, g_err = experimental_values.get_gasrate(shot, dda)
#     power = power*1e-6

#     nesepneped = experimental_values.get_nesepneped(shot, dda)[0]

#     if gasrate <= 0.5e22:
#         marker = 's'
#         color = 'blue'
#         i=0
#     elif gasrate <= 1.5e22:
#         marker = 'o'
#         color = 'green'
#         i=1
#     else:
#         marker = '^'
#         color = 'magenta'
#         i=2
#     # colors.append(color)

#     lists[i].append((power,betan))
#     ax.scatter(power,betan,c=color, marker=marker)

# colors_i = ['blue','green','magenta']
# for i in range(3):
#     ll = lists[i]
#     lbeta = np.array([l[0] for l in ll])
#     lalph = [l[1] for l in ll]
#     model1 = LinearRegression()
#     lbeta = lbeta.reshape(-1, 1)
#     model1.fit(lbeta, lalph)
#     lbeta_to_plot = np.linspace(min(lbeta),max(lbeta),2).reshape(-1,1)
#     lalph_to_plot = model1.predict(lbeta_to_plot)

#     ax.plot(lbeta_to_plot, lalph_to_plot, c=colors_i[i])

# ax.set_xlabel(r'$P_{\mathrm{[MW]}}$')
# ax.set_ylabel(global_functions.betan_label)
# ax.set_ylim(bottom=0)
# ax.set_xlim(left=0)
# plt.show()


# fig, ax = plt.subplots()

# lists = [[],[],[]]

# for shot, dda in zip(list_shot, list_dda):
#     alpha, a_err = experimental_values.get_alpha_max(shot, dda)
#     power, p_err = experimental_values.get_power(shot, dda)
#     neped, neped_err = experimental_values.get_neped(shot, dda)
#     peped, peped_err = experimental_values.get_peped(shot, dda)
#     gasrate, g_err = experimental_values.get_gasrate(shot, dda)
#     power = power*1e-6

#     nesepneped = experimental_values.get_nesepneped(shot, dda)[0]

#     if gasrate <= 0.5e22:
#         marker = 's'
#         color = 'blue'
#         i=0
#     elif gasrate <= 1.5e22:
#         marker = 'o'
#         color = 'green'
#         i=1
#     else:
#         marker = '^'
#         color = 'magenta'
#         i=2
#     # colors.append(color)

#     lists[i].append((neped,peped))
#     ax.scatter(neped,peped,c=color, marker=marker)

# colors_i = ['blue','green','magenta']
# for i in range(3):
#     ll = lists[i]
#     lbeta = np.array([l[0] for l in ll])
#     lalph = [l[1] for l in ll]
#     model1 = LinearRegression()
#     lbeta = lbeta.reshape(-1, 1)
#     model1.fit(lbeta, lalph)
#     lbeta_to_plot = np.linspace(min(lbeta),max(lbeta),2).reshape(-1,1)
#     lalph_to_plot = model1.predict(lbeta_to_plot)

#     ax.plot(lbeta_to_plot, lalph_to_plot, c=colors_i[i])

# ax.set_xlabel(global_functions.neped_label)
# ax.set_ylabel(global_functions.peped_label)
# ax.set_ylim(bottom=0)
# ax.set_xlim(left=0)
# plt.show()

# fig, ax = plt.subplots()

# lists = [[],[],[]]

# for shot, dda in zip(list_shot, list_dda):
#     alpha, a_err = experimental_values.get_alpha_max(shot, dda)
#     power, p_err = experimental_values.get_power(shot, dda)
#     nesepneped, neped_err = experimental_values.get_nesepneped(shot, dda)
#     peped, peped_err = experimental_values.get_peped(shot, dda)
#     gasrate, g_err = experimental_values.get_gasrate(shot, dda)
#     power = power*1e-6

#     nesepneped = experimental_values.get_nesepneped(shot, dda)[0]

#     if gasrate <= 0.5e22:
#         marker = 's'
#         color = 'blue'
#         i=0
#     elif gasrate <= 1.5e22:
#         marker = 'o'
#         color = 'green'
#         i=1
#     else:
#         marker = '^'
#         color = 'magenta'
#         i=2
#     # colors.append(color)

#     lists[i].append((nesepneped,peped))
#     ax.scatter(nesepneped,peped,c=color, marker=marker)

# colors_i = ['blue','green','magenta']
# for i in range(3):
#     ll = lists[i]
#     lbeta = np.array([l[0] for l in ll])
#     lalph = [l[1] for l in ll]
#     model1 = LinearRegression()
#     lbeta = lbeta.reshape(-1, 1)
#     model1.fit(lbeta, lalph)
#     lbeta_to_plot = np.linspace(min(lbeta),max(lbeta),2).reshape(-1,1)
#     lalph_to_plot = model1.predict(lbeta_to_plot)

#     ax.plot(lbeta_to_plot, lalph_to_plot, c=colors_i[i])

# ax.set_xlabel(global_functions.nesepneped_label)
# ax.set_ylabel(global_functions.peped_label)
# ax.set_ylim(bottom=0)
# ax.set_xlim(left=0)
# plt.show()

# fig, ax = plt.subplots()

# lists = [[],[],[]]

# for shot, dda in zip(list_shot, list_dda):
#     alpha, a_err = experimental_values.get_alpha_max(shot, dda)
#     power, p_err = experimental_values.get_power(shot, dda)
#     neped, neped_err = experimental_values.get_neped(shot, dda)
#     peped, peped_err = experimental_values.get_peped(shot, dda)
#     gasrate, g_err = experimental_values.get_gasrate(shot, dda)
#     power = power*1e-6

#     nesepneped = experimental_values.get_nesepneped(shot, dda)[0]

#     if gasrate <= 0.5e22:
#         marker = 's'
#         color = 'blue'
#         i=0
#     elif gasrate <= 1.5e22:
#         marker = 'o'
#         color = 'green'
#         i=1
#     else:
#         marker = '^'
#         color = 'magenta'
#         i=2
#     # colors.append(color)

#     lists[i].append((neped,alpha))
#     ax.scatter(neped,alpha,c=color, marker=marker)

# colors_i = ['blue','green','magenta']
# for i in range(3):
#     ll = lists[i]
#     lbeta = np.array([l[0] for l in ll])
#     lalph = [l[1] for l in ll]
#     model1 = LinearRegression()
#     lbeta = lbeta.reshape(-1, 1)
#     model1.fit(lbeta, lalph)
#     lbeta_to_plot = np.linspace(min(lbeta),max(lbeta),2).reshape(-1,1)
#     lalph_to_plot = model1.predict(lbeta_to_plot)

#     ax.plot(lbeta_to_plot, lalph_to_plot, c=colors_i[i])

# ax.set_xlabel(global_functions.neped_label)
# ax.set_ylabel(global_functions.alpha_label)
# ax.set_ylim(bottom=0)
# ax.set_xlim(left=0)
# plt.show()


# fig, ax = plt.subplots()

# lists = [[],[],[]]

# for shot, dda in zip(list_shot, list_dda):
#     alpha, a_err = experimental_values.get_alpha_max(shot, dda)
#     power, p_err = experimental_values.get_power(shot, dda)
#     neped, neped_err = experimental_values.get_neped(shot, dda)
#     peped, peped_err = experimental_values.get_peped(shot, dda)
#     gasrate, g_err = experimental_values.get_gasrate(shot, dda)
#     power = power*1e-6

#     nesepneped = experimental_values.get_nesepneped(shot, dda)[0]

#     if gasrate <= 0.5e22:
#         marker = 's'
#         color = 'blue'
#         i=0
#     elif gasrate <= 1.5e22:
#         marker = 'o'
#         color = 'green'
#         i=1
#     else:
#         marker = '^'
#         color = 'magenta'
#         i=2
#     # colors.append(color)

#     lists[i].append((power,gasrate))
#     ax.scatter(power,gasrate,c=color, marker=marker)

# colors_i = ['blue','green','magenta']
# for i in range(3):
#     ll = lists[i]
#     lbeta = np.array([l[0] for l in ll])
#     lalph = [l[1] for l in ll]
#     model1 = LinearRegression()
#     lbeta = lbeta.reshape(-1, 1)
#     model1.fit(lbeta, lalph)
#     lbeta_to_plot = np.linspace(min(lbeta),max(lbeta),2).reshape(-1,1)
#     lalph_to_plot = model1.predict(lbeta_to_plot)

#     ax.plot(lbeta_to_plot, lalph_to_plot, c=colors_i[i])

# ax.set_xlabel(global_functions.power_label)
# ax.set_ylabel(global_functions.gasrate_label)
# ax.set_ylim(bottom=0)
# ax.set_xlim(left=0)
# plt.show()

# fig, ax = plt.subplots()

# lists = [[],[],[]]

# for shot, dda in zip(list_shot, list_dda):
#     alpha, a_err = experimental_values.get_alpha_max(shot, dda)
#     power, p_err = experimental_values.get_power(shot, dda)
#     neped, neped_err = experimental_values.get_neped(shot, dda)
#     peped, peped_err = experimental_values.get_peped(shot, dda)
#     delta, peped_err = experimental_values.get_width_pe(shot, dda)
#     gasrate, g_err = experimental_values.get_gasrate(shot, dda)
#     power = power*1e-6

#     gradp = peped/delta

#     nesepneped = experimental_values.get_nesepneped(shot, dda)[0]

#     if gasrate <= 0.5e22:
#         marker = 's'
#         color = 'blue'
#         i=0
#     elif gasrate <= 1.5e22:
#         marker = 'o'
#         color = 'green'
#         i=1
#     else:
#         marker = '^'
#         color = 'magenta'
#         i=2
#     # colors.append(color)

#     lists[i].append((neped,gradp))
#     ax.scatter(neped,gradp,c=color, marker=marker)

# colors_i = ['blue','green','magenta']
# for i in range(3):
#     ll = lists[i]
#     lbeta = np.array([l[0] for l in ll])
#     lalph = [l[1] for l in ll]
#     model1 = LinearRegression()
#     lbeta = lbeta.reshape(-1, 1)
#     model1.fit(lbeta, lalph)
#     lbeta_to_plot = np.linspace(min(lbeta),max(lbeta),2).reshape(-1,1)
#     lalph_to_plot = model1.predict(lbeta_to_plot)

#     ax.plot(lbeta_to_plot, lalph_to_plot, c=colors_i[i])

# ax.set_xlabel(global_functions.neped_label)
# ax.set_ylabel(r'$p_e^{\mathrm{ped}}/\Delta(p_e)$')
# ax.set_ylim(bottom=0)
# ax.set_xlim(left=0)
# plt.show()


# fig, ax = plt.subplots()

# lists = [[],[],[]]

# for shot, dda in zip(list_shot, list_dda):
#     alpha, a_err = experimental_values.get_alpha_max(shot, dda)
#     power, p_err = experimental_values.get_power(shot, dda)
#     neped, neped_err = experimental_values.get_neped(shot, dda)
#     peped, peped_err = experimental_values.get_peped(shot, dda)
#     delta, peped_err = experimental_values.get_width_pe(shot, dda)
#     gasrate, g_err = experimental_values.get_gasrate(shot, dda)
#     power = power*1e-6

#     gradp = experimental_values.get_max_pressure_gradient(shot, dda)

#     nesepneped = experimental_values.get_nesepneped(shot, dda)[0]

#     if gasrate <= 0.5e22:
#         marker = 's'
#         color = 'blue'
#         i=0
#     elif gasrate <= 1.5e22:
#         marker = 'o'
#         color = 'green'
#         i=1
#     else:
#         marker = '^'
#         color = 'magenta'
#         i=2
#     # colors.append(color)

#     lists[i].append((neped,gradp))
#     ax.scatter(neped,gradp,c=color, marker=marker)

# colors_i = ['blue','green','magenta']
# for i in range(3):
#     ll = lists[i]
#     lbeta = np.array([l[0] for l in ll])
#     lalph = [l[1] for l in ll]
#     model1 = LinearRegression()
#     lbeta = lbeta.reshape(-1, 1)
#     model1.fit(lbeta, lalph)
#     lbeta_to_plot = np.linspace(min(lbeta),max(lbeta),2).reshape(-1,1)
#     lalph_to_plot = model1.predict(lbeta_to_plot)

#     ax.plot(lbeta_to_plot, lalph_to_plot, c=colors_i[i])

# ax.set_xlabel(global_functions.neped_label)
# ax.set_ylabel(r'$max(\nabla p_e)$')
# ax.set_ylim(bottom=0)
# ax.set_xlim(left=0)
# plt.show()


fig, ax = plt.subplots()

lists = [[],[],[]]

for shot, dda in zip(list_shot, list_dda):
    neped, neped_err = experimental_values.get_neped(shot, dda)
    gasrate, g_err = experimental_values.get_gasrate(shot, dda)
    power, betan_err = experimental_values.get_power(shot, dda)
    power = power*1e-6

    if gasrate <= 0.5e22:
        marker = 's'
        color = 'blue'
        i=0
    elif gasrate <= 1.5e22:
        marker = 'o'
        color = 'green'
        i=1
    else:
        marker = '^'
        color = 'magenta'
        i=2
    # colors.append(color)

    lists[i].append((power,neped))
    ax.scatter(power,neped,c=color, marker=marker)

colors_i = ['blue','green','magenta']
for i in range(3):
    ll = lists[i]
    lbeta = np.array([l[0] for l in ll])
    lalph = [l[1] for l in ll]
    model1 = LinearRegression()
    lbeta = lbeta.reshape(-1, 1)
    model1.fit(lbeta, lalph)
    lbeta_to_plot = np.linspace(min(lbeta),max(lbeta),2).reshape(-1,1)
    lalph_to_plot = model1.predict(lbeta_to_plot)

    ax.plot(lbeta_to_plot, lalph_to_plot, c=colors_i[i])

ax.set_xlabel(global_functions.power_label)
ax.set_ylabel(global_functions.neped_label)
ax.set_ylim(bottom=0)
ax.set_xlim(left=0)
plt.show()

fig, ax = plt.subplots()

lists = [[],[],[]]

for shot, dda in zip(list_shot, list_dda):
    neped, neped_err = experimental_values.get_neped(shot, dda)
    gasrate, g_err = experimental_values.get_gasrate(shot, dda)
    betan, betan_err = experimental_values.get_betan(shot, dda)


    if gasrate <= 0.5e22:
        marker = 's'
        color = 'blue'
        i=0
    elif gasrate <= 1.5e22:
        marker = 'o'
        color = 'green'
        i=1
    else:
        marker = '^'
        color = 'magenta'
        i=2
    # colors.append(color)

    lists[i].append((betan,neped))
    ax.scatter(betan,neped,c=color, marker=marker)

colors_i = ['blue','green','magenta']
for i in range(3):
    ll = lists[i]
    lbeta = np.array([l[0] for l in ll])
    lalph = [l[1] for l in ll]
    model1 = LinearRegression()
    lbeta = lbeta.reshape(-1, 1)
    model1.fit(lbeta, lalph)
    lbeta_to_plot = np.linspace(min(lbeta),max(lbeta),2).reshape(-1,1)
    lalph_to_plot = model1.predict(lbeta_to_plot)

    ax.plot(lbeta_to_plot, lalph_to_plot, c=colors_i[i])

ax.set_xlabel(global_functions.betan_label)
ax.set_ylabel(global_functions.neped_label)
ax.set_ylim(bottom=0)
ax.set_xlim(left=0)
plt.show()


fig, ax = plt.subplots()

lists = [[],[],[]]

for shot, dda in zip(list_shot, list_dda):
    alpha, a_err = experimental_values.get_alpha_max(shot, dda)
    power, p_err = experimental_values.get_power(shot, dda)
    neped, neped_err = experimental_values.get_neped(shot, dda)
    peped, peped_err = experimental_values.get_peped(shot, dda)
    delta, peped_err = experimental_values.get_width_pe(shot, dda)
    gasrate, g_err = experimental_values.get_gasrate(shot, dda)
    power = power*1e-6

    gradp = experimental_values.get_max_pressure_gradient(shot, dda)

    nesepneped = experimental_values.get_nesepneped(shot, dda)[0]

    if gasrate <= 0.5e22:
        marker = 's'
        color = 'blue'
        i=0
    elif gasrate <= 1.5e22:
        marker = 'o'
        color = 'green'
        i=1
    else:
        marker = '^'
        color = 'magenta'
        i=2
    # colors.append(color)

    lists[i].append((gasrate,neped))
    ax.scatter(gasrate,neped,c=color, marker=marker)

colors_i = ['blue','green','magenta']
for i in range(3):
    ll = lists[i]
    lbeta = np.array([l[0] for l in ll])
    lalph = [l[1] for l in ll]
    model1 = LinearRegression()
    lbeta = lbeta.reshape(-1, 1)
    model1.fit(lbeta, lalph)
    lbeta_to_plot = np.linspace(min(lbeta),max(lbeta),2).reshape(-1,1)
    lalph_to_plot = model1.predict(lbeta_to_plot)

    ax.plot(lbeta_to_plot, lalph_to_plot, c=colors_i[i])

ax.set_xlabel(global_functions.gasrate_label)
ax.set_ylabel(global_functions.neped_label)
ax.set_ylim(bottom=0)
ax.set_xlim(left=0)
plt.show()



fig, ax = plt.subplots()

lists = [[],[],[]]

for shot, dda in zip(list_shot, list_dda):
    alpha, a_err = experimental_values.get_alpha_max(shot, dda)
    power, p_err = experimental_values.get_power(shot, dda)
    neped, neped_err = experimental_values.get_neped(shot, dda)
    peped, peped_err = experimental_values.get_peped(shot, dda)
    delta, peped_err = experimental_values.get_width_pe(shot, dda)
    gasrate, g_err = experimental_values.get_gasrate(shot, dda)
    power = power*1e-6

    gradp = experimental_values.get_max_pressure_gradient(shot, dda)

    nesepneped = experimental_values.get_nesepneped(shot, dda)[0]

    if gasrate <= 0.5e22:
        marker = 's'
        color = 'blue'
        i=0
    elif gasrate <= 1.5e22:
        marker = 'o'
        color = 'green'
        i=1
    else:
        marker = '^'
        color = 'magenta'
        i=2
    # colors.append(color)

    lists[i].append((nesepneped,delta))
    ax.scatter(nesepneped,delta,c=color, marker=marker)

colors_i = ['blue','green','magenta']
for i in range(3):
    ll = lists[i]
    lbeta = np.array([l[0] for l in ll])
    lalph = [l[1] for l in ll]
    model1 = LinearRegression()
    lbeta = lbeta.reshape(-1, 1)
    model1.fit(lbeta, lalph)
    lbeta_to_plot = np.linspace(min(lbeta),max(lbeta),2).reshape(-1,1)
    lalph_to_plot = model1.predict(lbeta_to_plot)

    ax.plot(lbeta_to_plot, lalph_to_plot, c=colors_i[i])

ax.set_xlabel(global_functions.nesepneped_label)
ax.set_ylabel(global_functions.delta_pe_label)
ax.set_ylim(bottom=0)
ax.set_xlim(left=0)
plt.show()

fig, ax = plt.subplots()

lists = [[],[],[]]

for shot, dda in zip(list_shot, list_dda):
    alpha, a_err = experimental_values.get_alpha_max(shot, dda)
    power, p_err = experimental_values.get_power(shot, dda)
    neped, neped_err = experimental_values.get_neped(shot, dda)
    peped, peped_err = experimental_values.get_peped(shot, dda)
    delta, peped_err = experimental_values.get_width_pe(shot, dda)
    gasrate, g_err = experimental_values.get_gasrate(shot, dda)
    power = power*1e-6

    gradp = peped/delta

    nesepneped = experimental_values.get_nesepneped(shot, dda)[0]

    if gasrate <= 0.5e22:
        marker = 's'
        color = 'blue'
        i=0
    elif gasrate <= 1.5e22:
        marker = 'o'
        color = 'green'
        i=1
    else:
        marker = '^'
        color = 'magenta'
        i=2
    # colors.append(color)

    lists[i].append((neped,delta))
    ax.scatter(neped,delta,c=color, marker=marker)

colors_i = ['blue','green','magenta']
for i in range(3):
    ll = lists[i]
    lbeta = np.array([l[0] for l in ll])
    lalph = [l[1] for l in ll]
    model1 = LinearRegression()
    lbeta = lbeta.reshape(-1, 1)
    model1.fit(lbeta, lalph)
    lbeta_to_plot = np.linspace(min(lbeta),max(lbeta),2).reshape(-1,1)
    lalph_to_plot = model1.predict(lbeta_to_plot)

    ax.plot(lbeta_to_plot, lalph_to_plot, c=colors_i[i])

ax.set_xlabel(global_functions.neped_label)
ax.set_ylabel(global_functions.delta_pe_label)
ax.set_ylim(bottom=0)
ax.set_xlim(left=0)
plt.show()


# fig, ax = plt.subplots()

# lists = [[],[],[]]

# for shot, dda in zip(list_shot, list_dda):
#     alpha, a_err = experimental_values.get_alpha_max(shot, dda)
#     power, p_err = experimental_values.get_power(shot, dda)
#     neped, neped_err = experimental_values.get_neped(shot, dda)
#     peped, peped_err = experimental_values.get_peped(shot, dda)
#     delta, peped_err = experimental_values.get_width_pe(shot, dda)
#     gasrate, g_err = experimental_values.get_gasrate(shot, dda)
#     power = power*1e-6

#     gradp = experimental_values.get_max_pressure_gradient(shot, dda)

#     nesepneped = experimental_values.get_nesepneped(shot, dda)[0]

#     if gasrate <= 0.5e22:
#         marker = 's'
#         color = 'blue'
#         i=0
#     elif gasrate <= 1.5e22:
#         marker = 'o'
#         color = 'green'
#         i=1
#     else:
#         marker = '^'
#         color = 'magenta'
#         i=2
#     # colors.append(color)

#     lists[i].append((nesepneped,gradp))
#     ax.scatter(nesepneped,gradp,c=color, marker=marker)

# colors_i = ['blue','green','magenta']
# for i in range(3):
#     ll = lists[i]
#     lbeta = np.array([l[0] for l in ll])
#     lalph = [l[1] for l in ll]
#     model1 = LinearRegression()
#     lbeta = lbeta.reshape(-1, 1)
#     model1.fit(lbeta, lalph)
#     lbeta_to_plot = np.linspace(min(lbeta),max(lbeta),2).reshape(-1,1)
#     lalph_to_plot = model1.predict(lbeta_to_plot)

#     ax.plot(lbeta_to_plot, lalph_to_plot, c=colors_i[i])

# ax.set_xlabel(global_functions.nesepneped_label)
# ax.set_ylabel(r'$max(\nabla p_e)$')
# ax.set_ylim(bottom=0)
# ax.set_xlim(left=0)
# plt.show()

# fig, ax = plt.subplots()

# lists = [[],[],[]]

# for shot, dda in zip(list_shot, list_dda):
#     alpha, a_err = experimental_values.get_alpha_max(shot, dda)
#     power, p_err = experimental_values.get_power(shot, dda)
#     neped, neped_err = experimental_values.get_neped(shot, dda)
#     peped, peped_err = experimental_values.get_peped(shot, dda)
#     delta, peped_err = experimental_values.get_width_pe(shot, dda)
#     gasrate, g_err = experimental_values.get_gasrate(shot, dda)
#     power = power*1e-6

#     gradp = peped/delta

#     nesepneped = experimental_values.get_nesepneped(shot, dda)[0]

#     if gasrate <= 0.5e22:
#         marker = 's'
#         color = 'blue'
#         i=0
#     elif gasrate <= 1.5e22:
#         marker = 'o'
#         color = 'green'
#         i=1
#     else:
#         marker = '^'
#         color = 'magenta'
#         i=2
#     # colors.append(color)

#     lists[i].append((nesepneped,gradp))
#     ax.scatter(nesepneped,gradp,c=color, marker=marker)

# colors_i = ['blue','green','magenta']
# for i in range(3):
#     ll = lists[i]
#     lbeta = np.array([l[0] for l in ll])
#     lalph = [l[1] for l in ll]
#     model1 = LinearRegression()
#     lbeta = lbeta.reshape(-1, 1)
#     model1.fit(lbeta, lalph)
#     lbeta_to_plot = np.linspace(min(lbeta),max(lbeta),2).reshape(-1,1)
#     lalph_to_plot = model1.predict(lbeta_to_plot)

#     ax.plot(lbeta_to_plot, lalph_to_plot, c=colors_i[i])

# ax.set_xlabel(global_functions.nesepneped_label)
# ax.set_ylabel(r'$p_e^{\mathrm{ped}}/\Delta(p_e)$')
# ax.set_ylim(bottom=0)
# ax.set_xlim(left=0)
# plt.show()

fig, ax = plt.subplots()

lists = [[],[],[]]

for shot, dda in zip(list_shot, list_dda):
    alpha, a_err = experimental_values.get_alpha_max(shot, dda)
    power, p_err = experimental_values.get_power(shot, dda)
    nesepneped, neped_err = experimental_values.get_nesepneped(shot, dda)
    peped, peped_err = experimental_values.get_peped(shot, dda)
    gasrate, g_err = experimental_values.get_gasrate(shot, dda)
    power = power*1e-6

    nesepneped = experimental_values.get_nesepneped(shot, dda)[0]

    if gasrate <= 0.5e22:
        marker = 's'
        color = 'blue'
        i=0
    elif gasrate <= 1.5e22:
        marker = 'o'
        color = 'green'
        i=1
    else:
        marker = '^'
        color = 'magenta'
        i=2
    # colors.append(color)

    lists[i].append((nesepneped,alpha))
    ax.scatter(nesepneped,alpha,c=color, marker=marker)

colors_i = ['blue','green','magenta']
for i in range(3):
    ll = lists[i]
    lbeta = np.array([l[0] for l in ll])
    lalph = [l[1] for l in ll]
    model1 = LinearRegression()
    lbeta = lbeta.reshape(-1, 1)
    model1.fit(lbeta, lalph)
    lbeta_to_plot = np.linspace(min(lbeta),max(lbeta),2).reshape(-1,1)
    lalph_to_plot = model1.predict(lbeta_to_plot)

    ax.plot(lbeta_to_plot, lalph_to_plot, c=colors_i[i])
    
ax.set_xlabel(global_functions.nesepneped_label)
ax.set_ylabel(global_functions.alpha_label)
ax.set_ylim(bottom=0)
ax.set_xlim(left=0)
plt.show()