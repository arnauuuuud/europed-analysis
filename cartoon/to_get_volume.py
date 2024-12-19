#!/usr/local/depot/Python-3.7/bin/python
# /usr/local/depot/Python-3.5.1/bin/python

from hoho.ra_flush_v3 import ra_flush_v3
from hoho.startup import reload
from ppf import ppfget
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import interp1d

shot=84794
t0 = 45.61
mu_0 = 1.25663706127e-6
ihdat,iwdat,RMAG,x,time,ier=ppfget(pulse=shot,dda='EFTP',dtyp='RMAG') 
ihdat,iwdat,ZMAG,x,time,ier=ppfget(pulse=shot,dda='EFTP',dtyp='ZMAG') 


def get_value_at_t0(array, time, t0):
    interpolator = interp1d(time, array, axis=0)
    valueatt0 = interpolator(t0)
    return valueatt0


RMAG_0 = get_value_at_t0(RMAG, time, t0)
ZMAG_0 = get_value_at_t0(ZMAG, time, t0)


R = np.linspace(RMAG_0, 4.5, 50)
Z = np.linspace(ZMAG_0, ZMAG_0, 50)


# plt.scatter(R,Z, c = PSNI[:len(R)])
# plt.show()

psi_N, psi_sep, V = ra_flush_v3(84794, t0, R, Z)

dVdpsi = np.gradient(V, psi_N) / psi_sep

alpha = -2 * dVdpsi / (2*np.pi)**2 * (V / (2*np.pi*RMAG_0))**(1/2) * mu_0