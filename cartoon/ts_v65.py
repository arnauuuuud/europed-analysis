#!/usr/local/depot/Python-3.7/bin/python
# /usr/local/depot/Python-3.5.1/bin/python

from ppf import *
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.cm as cm
from matplotlib.colors import Normalize
from hoho import constant_function,read_kk3_2022,find_pedestal_values,global_functions
from paper import constants
from tqdm import tqdm
import matplotlib.patches as patches


major_linewidth = 5#constants.major_linewidth
fontsizelabel = constants.fontsizelabel
fontsizetick = constants.fontsizetick
fontsizetext = constants.fontsizetext



#####################################################################
# TEMPERATURE
dda_global = 'HRTS'
dtype_ne = 'NE'
dtype_te = 'TE'
shot = 84794
ne_color = global_functions.ne_color
te_color = global_functions.te_color
fontsizelabel = 30
fontsizetick = 20

xlim = (0.85,1)
ylim_ne = (0,3.2)

#####################################################################
def main():
    
    print('')
    print(shot)

    

    list_psin = []
    list_temperature = []




    ihdat,iwdat,data_ne,x_ne,time_ne,ier=ppfget(pulse=shot,dda=dda_global,dtyp=dtype_ne)
    data_ne = np.array(data_ne)
    x_ne = np.array(x_ne)
    time_ne = np.array(time_ne)
    data_ne = data_ne.reshape(len(time_ne),len(x_ne))
    data_ne = data_ne*10**(-19)

    ihdat,iwdat,data_te,x_te,time_te,ier=ppfget(pulse=shot,dda=dda_global,dtyp=dtype_te)
    data_te = np.array(data_te)
    x_te = np.array(x_te)
    time_te = np.array(time_te)
    data_te = data_te.reshape(len(time_te),len(x_te))
    data_te = data_te/1000


    ihdat,iwdat,data_psi,x_psi,time_psi,ier=ppfget(pulse=shot,dda=dda_global,dtyp='PSI')
    data_psi = data_psi.reshape(len(time_psi),len(x_psi))
   
    fig, ax = plt.subplots(figsize=(6,5))
    # ax2 = ax.twinx()

    list_psis = []
    list_te = []
    list_ne = []

    list_to_include = [93,94,96,108,112,115,116]

    #for it,t in tqdm(enumerate(time_ne[:10])):
    for it,t in tqdm(zip(list_to_include,time_ne[list_to_include])):

        list_psis = np.concatenate((list_psis,data_psi[it]))
        list_ne = np.concatenate((list_ne,data_ne[it]))
        list_te = np.concatenate((list_te,data_te[it]))

    # ax.scatter(list_psis,list_ne,color=ne_color,marker='h',edgecolor='k')
    # ax.scatter(list_psis,list_te,color=te_color,marker='D',edgecolor='k')
    # ax2.scatter(list_psis,list_te,color=te_color,marker='D',edgecolor='k')


    # ax.set_ylabel(r'${n_e}_{[10^{19}{\mathrm{m}}^{-3}]}$, ${T_e}_{[\mathrm{keV}]}$', fontsize = fontsizelabel)
    # ax.set_ylabel(r'${n_e}_{[10^{19}{\mathrm{m}}^{-3}]}$',color=ne_color, fontsize = fontsizelabel)
    ax.set_xlabel(r'$\psi_N$',fontsize = fontsizelabel)

    # ax2.set_ylabel(r'${T_e}_{[\mathrm{keV}]}$',color=te_color, fontsize=fontsizelabel)
    
        #ax.text(0.95, 0.95, rf'$t={round(float(t),2)}$'+r'$\mathrm{s}$', transform=ax.transAxes, fontsize=fontsizetick, va='top', ha='right')
    ax.text(-0.15, 0.55, r'${n_e}_{[10^{19}{\mathrm{m}}^{-3}]}$',zorder=6, transform=ax.transAxes, color=ne_color, va='center', ha='center', rotation=90, fontsize=fontsizelabel)
    ax.text(-0.15, 0.5, r'${T_e}_{[\mathrm{keV}]}$', zorder=5,transform=ax.transAxes, color='w', va='center', ha='center', rotation=90, fontsize=fontsizelabel)
    # ax.text(-0.15, 0.62, r'${T_e}_{[\mathrm{keV}]}$', transform=ax.transAxes, color=te_color, va='bottom', ha='center', rotation=90, fontsize=fontsizelabel)
    # ax.text(-0.15, 0.605, r'-', transform=ax.transAxes, color='k', va='center', ha='center', rotation=90, fontsize=fontsizelabel)


    ax.set_ylim(ylim_ne[0],ylim_ne[1])
    ax.set_xlim(left=xlim[0],right=xlim[1])         
    # ax2.set_ylim(ylim_te[0],ylim_te[1])


    params_te = find_pedestal_values.fit_mtanh(list_psis, list_te)
    params_ne = find_pedestal_values.fit_mtanh(list_psis, list_ne)
    ppos_te, delta_te, h_te, s_te, offset_te = params_te
    ppos_ne, delta_ne, h_ne, s_ne, offset_ne = params_ne

    fit_ne = np.zeros(1000)
    fit_te = np.zeros(1000)
    psis = np.linspace(0.7,1,1000)

    for i,psi in enumerate(psis):
        fit_ne[i] = find_pedestal_values.mtanh_offset(psi, ppos_ne, delta_ne, h_ne, s_ne, offset_ne)
        fit_te[i] = find_pedestal_values.mtanh_offset(psi, ppos_te, delta_te, h_te, s_te, offset_te)


    ax.plot(psis,fit_ne,color=ne_color,linewidth=major_linewidth)
    

    plt.tick_params(axis='both',labelsize=fontsizetick)

    # HEIGHT
    p1 = patches.FancyArrowPatch((0.88, offset_ne), (0.88, offset_ne+h_ne), arrowstyle='<->', mutation_scale=20,shrinkA=False,shrinkB=False)
    ax.add_patch(p1)
    ax.text(0.88, offset_ne+h_ne/2, r'$h$', transform=ax.transData, ha='right',va='center', fontsize=fontsizetick,rotation=90)

    # WIDTH
    p2 = patches.FancyArrowPatch((ppos_ne-delta_ne/2, 0.2), (ppos_ne+delta_ne/2, 0.2), arrowstyle='<->', mutation_scale=20,shrinkA=False,shrinkB=False)
    ax.add_patch(p2)
    ax.text(ppos_ne, 0.2, r'$w$', transform=ax.transData, ha='center',va='top', fontsize=fontsizetick)

    # OFFSET
    p3 = patches.FancyArrowPatch((0.99, 0), (0.99, offset_ne), arrowstyle='|-|', mutation_scale=5,shrinkA=False,shrinkB=False)
    ax.add_patch(p3)
    arrow = patches.FancyArrowPatch((0.98, 0.4), (0.99, offset_ne/2), connectionstyle="arc3,rad=0.7", arrowstyle='->', mutation_scale=20, linestyle='-', color='black',linewidth=0.5)
    ax.text(0.98, 0.4, r'$o$', transform=ax.transData, ha='center',va='bottom', fontsize=fontsizetick)
    ax.add_patch(arrow)

    # POSITION NE
    ax.vlines(ppos_ne, ymin=1.3, ymax=5, linestyle=':',linewidth=2.5, color=ne_color,zorder=10)
    ax.text(ppos_ne+0.005, ylim_ne[1], r'$p^{\mathrm{pos}}$', transform=ax.transData, ha='center',va='bottom', fontsize=fontsizetick)


    # DELTA
    # ax.plot(psis,fit_te,color=te_color,linewidth=major_linewidth,zorder=-1)
    # ax.vlines(ppos_te,ymin=0.375,ymax=5,linestyle=':',color=te_color,linewidth=2.5,zorder=10)
    # p4 = patches.FancyArrowPatch((ppos_te, 1), (ppos_ne, 1), arrowstyle='|-|', mutation_scale=5,shrinkA=False,shrinkB=False, zorder=0)
    # ax.add_patch(p4)
    # ax.text((ppos_ne+ppos_te)/2, 0.98, r'$\Delta$', transform=ax.transData, ha='center',va='top', fontsize=fontsizetick)


    plt.savefig(f'../../../bouloulou/global4e.png')
    plt.close()

    



if __name__ == '__main__':
    main()
