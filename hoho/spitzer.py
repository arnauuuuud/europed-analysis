#!/usr/local/depot/Python-3.7/bin/python
# /usr/local/depot/Python-3.5.1/bin/python

from ppf import *
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.cm as cm
from matplotlib.colors import Normalize
from hoho import useful_recurring_functions, constant_function,read_kk3_2022
from thesis import constants
from hoho import useful_recurring_functions, find_pedestal_values_old
from scipy.interpolate import interp1d
import math
from scipy.integrate import quad

major_linewidth = constants.major_linewidth
fontsizelabel = constants.fontsizelabel
fontsizetick = constants.fontsizetick
fontsizetext = constants.fontsizetext

#####################################################################
# TEMPERATURE


def nz(z):
    res = 0.58+0.74/(0.76+z)
    return res

def ln_Lambda_e(ne,te):
    res = 31.3 - np.log(np.sqrt(ne)/te)
    return res

def conductivity(ne,te,z):
    res = 1.9012e4 * te**1.5 / (z * nz(z) * ln_Lambda_e(ne,te))
    return res

def resistivity(ne,te,z):
    ## ne in m-3, te in eV
    res = 1/conductivity(ne,te,z)
    return res

def integrand(lambda_, B_max, B):
    return lambda_ / np.mean(np.sqrt(1 - lambda_ * B))

def f_trap(B_max, B):
    integral_result, _ = quad(integrand, 0, 1/B_max, args=(B_max, B))
    term = (3/4) * np.mean(B**2) * integral_result
    return 1 - term


def sigma_ratio(X_33, Z_eff):
    term1 = (0.21 / Z_eff) * X_33
    term2 = (0.54 / Z_eff) * X_33**2
    term3 = (0.33 / Z_eff) * X_33**3
    return 1 - (term1 - term2 + term3)

def f_t_33_eff(f_trap, nu_e_star, Z_eff):
    numerator = f_trap
    term1 = 0.25 * (1 - 0.7 * f_trap) * math.sqrt(nu_e_star) * (1 + 0.45 * math.sqrt(Z_eff - 1))
    term2 = 0.61 * (1 - 0.41 * f_trap) * nu_e_star / math.sqrt(Z_eff)
    denominator = 1 + term1 + term2
    return numerator / denominator


def nu_e_star(q, R, n_e, Z, ln_Lambda_e, T_e, epsilon):
    constant = 6.921e-18
    numerator = q * R * n_e * Z * ln_Lambda_e
    denominator = (T_e**2) * (epsilon**(3/2))
    return constant * (numerator / denominator)







