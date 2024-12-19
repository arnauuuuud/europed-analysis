#!/usr/local/depot/Python-3.7/bin/python
# /usr/local/depot/Python-3.5.1/bin/python

from hoho import useful_recurring_functions, startup, find_pedestal_values_old
import argparse
import matplotlib.pyplot as plt
from pylib.misc import ReadFile
import os
from scipy import interpolate
from ppf import ppfuid,ppfget
from scipy.interpolate import interp1d
import numpy as np
from netCDF4 import Dataset # Import netCDF library
from matplotlib.ticker import ScalarFormatter

def extract_from_lines(lines, eta):
    s_values = []
    p_values = []
    ready = False
    reading = False

    if eta == 'NEO':
        inline = 'SIG(neo)'
        index_neo = 6
    if eta == 'SPITZER':
        inline = 'SIG(Spitz)'
        index_neo = 5

    for line in lines:
        if 'S' in line and inline in line:
            ready = True
            pass
        elif ready and not reading and '*' in line:
            reading=True
            pass

        elif reading and len(line.split('  ')) > 0 and not '*' in line:
            elements = line.split()
            if len(elements)>=2:
                s = float(elements[0])
                p = float(elements[index_neo])
                s_values.append(s)
                p_values.append(p)
        elif reading and '*' in line or len(line.split('  ')) == 0:
            break
    return np.array(s_values),np.array(p_values)

def extract_s_and_eta(filename, eta):
    foldername = f"{os.environ['HELENA_DIR']}output"
    os.chdir(foldername)
    with open(filename, 'r') as file:
        lines = file.readlines()
        s_values, p_values = extract_from_lines(lines, eta)
    return s_values, p_values



def get_helena_filename(europed_name):
    filepath = europed_name
    if '/' not in filepath:
        filepath = f"{os.environ['EUROPED_DIR']}output/{filepath}"
    with ReadFile(filepath) as f:
        for line in f.readlines():
            if line.startswith('run id:'):
                runid = line.split(': ')[1]
                if runid.endswith('\n'):
                    runid = runid[:-1]
                return runid
            else:
                continue

def plot(filename, ax):
    psi_values, j_values_sp = extract_s_and_eta(filename,'SPITZER')
    # ax.plot(psi_values**2,1/j_values_sp, linestyle='--', linewidth=3, label=r'Spitzer - Output of HELENA')
    # ax.plot(psi_values,2/j_values_sp, label=r'$2 \eta_{Sp}$')
    psi_values, j_values_neo = extract_s_and_eta(filename,'NEO')
    # ax.plot(psi_values**2,1/j_values_neo, linewidth=3, color='purple', label=r'Neoclassical - Output of HELENA')
    over_value  = np.where(psi_values**2>=0.8)
    ratio = j_values_sp/j_values_neo
    filtered = ratio[over_value]
    psi_filter = psi_values[over_value]**2
    
    interp = interp1d(psi_filter, filtered, bounds_error=False)

    psi = np.linspace(0.9,1,100)
    res = interp(psi)


    average = np.nanmean(res)
    print(f'ratio eta: {average}')
    average = np.average(res)
    print(f'ratio eta: {average}')

    print(f'min eta ratio:{interp(0.9405)}')
    print(f'max eta ratio:{interp(0.9999)}')

    # ax.axhline(average)
    # ax.axvline(0.9)
    
    ax.plot(psi_values**2,j_values_sp/j_values_neo, linewidth=3, color='purple', label=r'Neoclassical/Spitzer - HELENA')
    # ax.plot(psi_values**2,1e7/j_values_sp, linewidth=3, color='red', label=r'Spitzer')
    # ax.plot(psi_values**2,2*1e7/j_values_sp, linewidth=3, color='green', label=r'2*Spitzer')
    # ax.plot(psi_values**2,1e7/j_values_neo, linewidth=3, color='blue', label=r'Neoclassical')
    # ax.plot(psi_filter,filtered, linewidth=3, color='orange', label=r'Neoclassical/Spitzer - HELENA')



def plot_transp(ax):
    TRANSPDat = Dataset("/common/transp_shared/Data/result/JET/84794/D05/D05.CDF")
    ieta1 = np.array(TRANSPDat.variables["ETA_SP"])
    ieta2 = np.array(TRANSPDat.variables["ETA_SPS"])
    ieta3 = np.array(TRANSPDat.variables["ETA_WNC"])
    ieta4 = np.array(TRANSPDat.variables["ETA_SNC"])
    time = np.array(TRANSPDat.variables["TIME"])
    zeff = np.array(TRANSPDat.variables["ZEFF"])
    print(zeff)
    x = np.array(TRANSPDat.variables["PLFLX"])
    print(x.shape)
    for i in range(len(x)):
        x[i] = x[i]/x[i,-1]

    eta1 = np.zeros((1,50))
    eta2 = np.zeros((1,50))
    eta3 = np.zeros((1,50))
    eta4 = np.zeros((1,50))
    x_profile = np.zeros((1,50))


    time_points = np.linspace(5.51, 8, 1)

    interp_func_eta1 = interpolate.interp1d(time, ieta1, kind='linear', axis=0)
    interp_func_eta2 = interpolate.interp1d(time, ieta2, kind='linear', axis=0)
    interp_func_eta3 = interpolate.interp1d(time, ieta3, kind='linear', axis=0)
    interp_func_eta4 = interpolate.interp1d(time, ieta4, kind='linear', axis=0)
    interp_func2 = interpolate.interp1d(time, x, kind='linear', axis=0)
    for i,timepoimt in enumerate(time_points):

        eta1[i] = interp_func_eta1(timepoimt)
        eta2[i] = interp_func_eta2(timepoimt)
        eta3[i] = interp_func_eta3(timepoimt)
        eta4[i] = interp_func_eta4(timepoimt)

        x_profile[i] = interp_func2(timepoimt)

    x_profile = np.mean(x_profile,axis=0)
    eta1 = np.mean(eta1,axis=0)/100
    eta2 = np.mean(eta2,axis=0)/100
    eta3 = np.mean(eta3,axis=0)/100
    eta4 = np.mean(eta4,axis=0)/100

    # ax.plot(x_profile, eta1,'--', linewidth=3, label=r'Spitzer - Output of TRANSP')
    # ax.plot(x_profile, eta2,':', linewidth=3, label=r'Spitzer - Output of TRANSP (Spitzer - Sauter)')
    # ax.plot(x_profile, eta3,'--', linewidth=3, label=r'Neoclassical - TRANSP')
    # ax.plot(x_profile, eta4,'--', color='k', linewidth=3, label=r'Neoclassical - TRANSP (Sauter)')

    ax.plot(x_profile, eta3/eta1,'--', linewidth=3, label=r'Neoclassical/Spitzer - TRANSP')
    ax.plot(x_profile, eta4/eta1,'--', color='k', linewidth=3, label=r'Neoclassical(Sauter)/Spitzer - TRANSP')





def calculate_spitzer(psis,ne,te,zeff=1.5872224569):
    def nz(z):
        res = 0.58+0.74/(0.76+z)
        return res

    def lnlambdae(ne,te):
        res = 31.3 - np.log(np.sqrt(ne)/te)
        return res

    def spitzersigma(te,ne,z):
        res = 1.9012e4 * te**1.5 / (z * nz(z) * lnlambdae(ne,te))
        return res

    psi_plot = []
    sigma_plot = []

    for psi1,n1,t1 in zip(psis,ne,te):
        try:
            temp_sigma = spitzersigma(t1,n1,zeff)
        except TypeError:
            continue
        psi_plot.append(psi1)
        sigma_plot.append(temp_sigma)


    psi_plot = np.array(psi_plot)
    sigma_plot = np.array(sigma_plot)
    eta_plot = 1/(sigma_plot)
    return psi_plot, eta_plot

def calculated_spitzer():
    dda_global = 'T052'
    dtype_psi_fit = 'PSIF'
    dtype_temp_fit = 'TEF5'
    dtype_density_fit = 'NEF3'

    uid = 'lfrassin'
    shot = 84794
    ppfuid(uid)

    list_psin = []
    list_temperature = []

    ihdat,iwdat,temperature_fit,x,time,ier=ppfget(pulse=shot,dda=dda_global,dtyp=dtype_temp_fit)
    ihdat,iwdat,density_fit,x,time,ier=ppfget(pulse=shot,dda=dda_global,dtyp=dtype_density_fit)
    ihdat,iwdat,psi_fit,x,time,ier=ppfget(pulse=shot,dda=dda_global,dtyp=dtype_psi_fit)

    interp = interp1d(temperature_fit, psi_fit)
    psi_sep = np.interp([0.1], temperature_fit, psi_fit)[0]
    psi_sep = interp(0.1)

    psi_fit = np.array(psi_fit) + 1 - psi_sep


    t = temperature_fit*1000
    n = density_fit*1e19

    psi_plot,eta = calculate_spitzer(psi_fit,n,t)

    return psi_plot,eta

def calculated_spitzer2():
    psis = np.linspace(0,1,100)
    europed_name = 'quick_mishka_helsave'
    # te,ne,dump2 = find_pedestal_values_old.create_profiles(europed_name,psis,profile=3)
    te,ne,dump2 = find_pedestal_values_old.create_profiles(europed_name,psis,crit='alfven')

    t = te*1000
    n = ne*1e19

    psi_plot,eta = calculate_spitzer(psis,n,t)

    return psi_plot,eta


def plot_calculated_spitzer(ax):
    psi,eta = calculated_spitzer()
    # ax.plot(psi,eta, linewidth=3, linestyle='-', label=r'Spitzer - calculated from the experimental profile (FIT)')

    psi,eta = calculated_spitzer2()
    # ax.plot(psi,eta, linestyle=':', linewidth=3,label=r'Spitzer - calculated from the Europed critical profiles')


def get_nt_transp():
    ## TE in eV
    ## NE in N.cm-3
    TRANSPDat = Dataset("/common/transp_shared/Data/result/JET/84794/D05/D05.CDF")
    ne = np.array(TRANSPDat.variables["NE"])
    te = np.array(TRANSPDat.variables["TE"])
    time = np.array(TRANSPDat.variables["TIME"])
    x = np.array(TRANSPDat.variables["PLFLX"])
    for i in range(len(x)):
        x[i] = x[i]/x[i,-1]
    time_points = np.linspace(5.51, 8, 1)

    ne_tab = np.zeros((1,50))
    te_tab = np.zeros((1,50))
    x_profile = np.zeros((1,50))



    interp_func_ne = interpolate.interp1d(time, ne, kind='linear', axis=0)
    interp_func_te = interpolate.interp1d(time, te, kind='linear', axis=0)
    interp_func2 = interpolate.interp1d(time, x, kind='linear', axis=0)
    for i,timepoimt in enumerate(time_points):

        ne_tab[i] = interp_func_ne(timepoimt)
        te_tab[i] = interp_func_te(timepoimt)

        x_profile[i] = interp_func2(timepoimt)

    x_profile = np.mean(x_profile,axis=0)
    ne = np.mean(ne_tab,axis=0)
    te = np.mean(te_tab,axis=0)
    return x_profile,ne,te

def calculate_spitzer_from_transp():
    x_profile,ne,te = get_nt_transp()
    ne = ne* 1e6 ## CONVERT TO N.m-3
    psi_plot, eta = calculate_spitzer(x_profile, ne, te)
    return psi_plot, eta

def plot_calculated_spitzer_from_transp(ax):
    psi_plot, eta = calculate_spitzer_from_transp()
    # ax.plot(psi_plot, eta, linestyle=':', linewidth=3, label='Spitzer - calculated from the TRANSP output profiles')



def main(europed_name='quick_mishka_helsave', profile=3):
    fig, ax = plt.subplots(figsize=(6,4))


    runid = get_helena_filename(europed_name)
    helena_name = f'jet84794.{runid}_{profile}'
    print(helena_name)

    plot(helena_name, ax)


    # plot_transp(ax)
    # plot_calculated_spitzer_from_transp(ax)

    # plot_calculated_spitzer(ax)
    # plt.gca().yaxis.set_major_formatter(ScalarFormatter(useMathText=True))
    # plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
    ax.set_xlabel(r'$\psi_N$',fontsize=20)
    ax.set_ylabel(r'$\eta_{\mathrm{neo}}/\eta_{\mathrm{Sp}}$',fontsize=20)
    # ax.set_ylabel(r'${\eta}  _{[10^{-7} \Omega \cdot \mathrm{m}]}$',fontsize=20)
    # ax.set_yscale('log')
    ax.set_xlim(left=0,right=1)
    ax.set_xlim(left=0.85)
    # ax.set_ylim(bottom=0)
    # ax.set_ylim(top=1e-6,bottom=1e-9)
    # ax.set_yscale('log')
    # plt.legend()
    plt.show()

if __name__ == '__main__':
    main()