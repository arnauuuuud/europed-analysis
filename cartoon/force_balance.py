#!/usr/local/depot/Python-3.7/bin/python
# /usr/local/depot/Python-3.5.1/bin/python

from hoho import useful_recurring_functions, europed_analysis, global_functions, startup, find_pedestal_values_old, read_helena_files, helena_read
import argparse
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.tri as tri
from hoho import helena_data as hd
import sympy as sp

mu_0 = 1.25663706127e-6


data = hd.HelenaData(mapping_path='/home/jwp9427/work/helena/mapping/tost')
chi = data.chi
csh = data.csh
psi = csh**2

Psi, Chi = np.meshgrid(psi, chi)
# print(Psi.shape)
# print(Chi.shape)



gem11 = data.GEM11
gem12 = data.GEM12
gem33 = data.GEM33

eps = data.eps
x = data.XX
y = data.YY
R0 = data.raxis
a = data.radius
# print(a)
# print(R0)
# print(0.88/2.94)
# print(eps)

# print(x.shape)
# print(y.shape)

jphi, psi = read_helena_files.extract_psi_and_j('tost')

jphi = np.concatenate((jphi,[0]))
jphi = np.array(jphi)





##############################################
# # we have x[psi,chi] and y[psi,chi]
# # we eant psi[x,y] and chi[x,y]
# new_x = np.linspace(np.min(x),np.max(x),100)
# new_y = np.linspace(np.min(y),np.max(y),100)

# new_X, new_Y = np.meshgrid(new_x,new_y)


# a = 0.88
# R0 = 2.94   
B0 = 1.699224968642145
# eps = a / R0
B0 = 0.1027E+01




# d2psid2x = np.zeros((513,301))
# d2psid2y = np.zeros((513,301))
# dpsidx = np.zeros((513,301))

# for i in range(513):
#     line_x = x[i]
#     line_y = y[i]
#     line_psi = psi_tab[i]

#     line_dpsidx = np.gradient(line_psi, line_x)    
#     line_dpsidy = np.gradient(line_psi, line_y)    
#     line_d2psid2x = np.gradient(line_dpsidx, line_x)
#     line_d2psid2y = np.gradient(line_dpsidy, line_y)

#     d2psid2x[i] = line_d2psid2x
#     d2psid2y[i] = line_d2psid2y
#     dpsidx[i] = line_dpsidx

#     # plt.plot(line_x, line_y)
#     # # plt.plot(line_psi, line_y)
        
#     # plt.plot(line_x, line_psi)
#     # plt.xlabel(r'$x=(R-R_0)/a$')
#     # plt.ylabel(r'$\bar{\psi}$')
#     # plt.show()       


#     # plt.plot(line_y, line_psi)
#     # plt.xlabel(r'$y=z/a$')
#     # plt.ylabel(r'$\bar{\psi}$')
#     # plt.show()


#     # # plt.plot(line_x, l


# # plt.plot(x[:,::10],y[:,::10])
# # plt.xlabel(r'$(R-R_0)/a$')
# # plt.ylabel(r'$z/a$')
# # plt.axis('equal')
# # plt.show()


# Example usage
file_path = 'tost'  # Replace with your file path
dict_inp = helena_read.read_eliteinp(file_path)

psi_eliteinp = dict_inp['Psi']
dpdpsi = dict_inp['dp/dpsi']
ffp = dict_inp['dffp']
psi1_eliteinp = psi_eliteinp[-1]

psi1_output = 0.8663
a =0.9234

dpdpsi = dpdpsi * psi1_output
ffp = ffp * psi1_output
alpha = a**2 * B0 / psi1_eliteinp
# print(alpha)
alpha = 1.672
eps = 0.317

print((mu_0 * alpha**2 / (eps * B0**2)))



dpdpsi_N = (mu_0 * alpha**2 / (eps * B0**2))**(-1) * dpdpsi
ffp_N = (eps * alpha**2 / (a**2 * B0))**(-1) * ffp

print(np.std(dpdpsi_N*10**5))
print(np.std(gem33/mu_0 * ffp_N))
print(np.std(gem33**0.5 * jphi*10**6))

kN = 1+ (gem33**0.5 * jphi*10**6 + gem33 / mu_0 * ffp_N) / (dpdpsi_N*10**5)


# kN = mu_0 * 1 / gem33**0.5 * kphi

# kN = 1 - gem33**0.5 * jphi / dpdpsi + gem33 * ffp / dpdpsi 




# K = d2psid2x - d2psid2y - eps/(1+eps*x) * dpsidx + (1- eps*x)**2 / eps * dpdpsi_N + 1/eps * ffp_N

# K = K/dpdpsi_N


# # # dgem33dpsi = (gem33[0,1:] - gem33[0,:-1])/psi[1:]

# # print(dpdpsi.shape)
# # print(gem33.shape)
# # print(ffp.shape)
# # print(dgem33dpsi.shape)
# # K = dpdpsi + 1/mu_0 * gem33 * [ffp + dgem33dpsi/gem33]


scatter = plt.scatter(x, y, c=kN, cmap='seismic', s=1, vmin=-1, vmax=1)
cbar = plt.colorbar(scatter)
plt.show()

# # cbar.set_label(r'$K$')
# # cbar.ax.yaxis.set_label_position('left')
# cbar.ax.set_title(r'$K_{[a.u.]}$')
# # cbar.ax.set_title_position('top')
# plt.axis('equal')
# plt.xlabel(r'$(R-R_0)/a$')
# plt.ylabel(r'$z/a$')
# plt.show()

# print(np.nanmax(K))
# print(np.nanmean(np.abs(K)))
# print(np.nanmin(K))
# # print(R0)
# print(a)
# print(data.eps)

# theta = np.linspace(0, 2*np.pi, len(Z[0]))

# plt.plot(np.linspace(0,2*np.pi,len(chi)),np.abs(np.sin(chi)))
# plt.plot(np.linspace(0,2*np.pi,len(Z[:,-1])),np.abs(Z[:,-1]/max(Z[:,-1])))

# theta_from_R = np.arccos(R)[:,-1]

# plt.plot(np.linspace(0,2*np.pi,len(theta_from_R)), np.abs(np.sin(theta_from_R)))

# plt.show()


# plt.plot(chi, Z[:,-1])
# plt.plot(chi, Z[:,0])
# plt.show()


# g1 = data.GEM22
# g2 = data.lolo 
# plt.plot(chi, g1[:,-1])
# plt.plot(chi, g2[:,-1])
# plt.show()

# plt.plot(chi, R[:,-1])
# plt.plot(chi, R[:,0])
# plt.show()

# psi = data.csh**2

# plt.plot(psi, R[0])
# plt.plot(psi, R[len(R)//2])
# plt.show()

# plt.plot(psi, Z[0])
# plt.plot(psi, Z[len(Z)//2])
# plt.show()