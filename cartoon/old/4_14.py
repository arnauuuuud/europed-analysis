#!/usr/local/depot/Python-3.7/bin/python
# /usr/local/depot/Python-3.5.1/bin/python

from paper import constants
import matplotlib.pyplot as plt
from hoho import europed_analysis, global_functions, startup
import matplotlib.transforms as transforms
from matplotlib.colors import Normalize
from matplotlib.colors import ListedColormap, BoundaryNorm
import math
from matplotlib.gridspec import GridSpec,GridSpecFromSubplotSpec
import numpy as np

major_linewidth = constants.major_linewidth
fontsizelabel = constants.fontsizelabel
fontsizetick = constants.fontsizetick


class CustomError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

def main():
    firstname = 'eagle_eta'
    prefixes = [0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1]
    middlname = '_ds0'
    considered_modes_input = [1,2,3,4,5,7,10,20,30,40]
    crit = 'diamag'
    crit_value = 0.25
    y_parameter = 'alpha_helena_max'
    excluded_modes = None

    fig = plt.figure(figsize=(9.6, 6.8))

    gs1 = GridSpec(1, 1)
    gs1.update(left=0.94, right=0.99, bottom=0.15, top=0.98, wspace=0.05)
    gs2 = GridSpec(1, 1)
    gs2.update(left=0.15, right=0.85, bottom=0.15, top=0.98, wspace=0.02)

    labels = prefixes
    list_ycrit = {}

    ax = plt.subplot(gs2[0])

    list_ycrit = []
    list_ycrit_min = []
    list_ycrit_plus = []
    critical_modes = []
    list_eta = [] 
    for iprefix,prefix in enumerate(prefixes):
            europed_run = firstname+str(prefix)+middlname
            try:
                if y_parameter == 'peped':
                    ne = europed_analysis.get_x_parameter(europed_run, 'neped')
                    te = europed_analysis.get_x_parameter(europed_run, 'teped')
                    x_param = ne*te
                else:
                    x_param = europed_analysis.get_x_parameter(europed_run, y_parameter)

                gammas, modes = europed_analysis.get_gammas(europed_run, crit)

                tab, considered_modes = europed_analysis.filter_tab_general(gammas, modes, considered_modes_input, excluded_modes)

                deltas = europed_analysis.get_x_parameter(europed_run, 'delta')
                filter_delta15 = np.where(deltas>=0.015)
                x_param = x_param[filter_delta15]
                tab = tab[filter_delta15] 

                has_unstable, y_crit, i_mode, mode = europed_analysis.find_critical(x_param, tab, considered_modes_input, crit_value)
                y_crit_min = None
                y_crit_plus = None

                if y_crit:
                    proportionality = 0.85
                    while y_crit_min == None:
                        has_unstable, y_crit_min, poop, poop2 = europed_analysis.find_critical(x_param, tab, considered_modes_input, crit_value*proportionality)
                        proportionality += 0.01
                    
                    proportionality = 1.15
                    while y_crit_plus == None:
                        has_unstable, y_crit_plus, poop, poop2 = europed_analysis.find_critical(x_param, tab, considered_modes_input, crit_value*proportionality)
                        proportionality -= 0.01

                if y_crit is  None:
                    raise CustomError(f"No critical value found")

                
                list_eta.append(float(prefix))

                if i_mode == -1:
                    critical_modes.append(-1)
                else:
                    critical_modes.append(considered_modes[i_mode])
                list_ycrit.append(y_crit)
                list_ycrit_plus.append(y_crit_plus)
                list_ycrit_min.append(y_crit_min)

                print("WENT GOOD : " + europed_run)

            except CustomError:
                print(f"{europed_run:>40} NO CRITICAL VALUE FOUND")
            except FileNotFoundError:
                print(f"{europed_run:>40} FILE NOT FOUND")
            except RuntimeError:
                print(f"{europed_run:>40} RUNTIME ERROR : NO FIT FOUND")
            # except IndexError:
            #     print(f"{europed_run:>40} KEY ERROR : NO FIT FOUND")
            except TypeError:
                print("icicici")

    list_x = list_eta
    list_y = list_ycrit

    list_x = np.array(list_x)
    list_y = np.array(list_y)
    critical_modes = np.array(critical_modes)

    x_nones = np.where(list_x == None)[0]
    y_nones = np.where(list_y == None)[0]

    nones = np.concatenate((x_nones, y_nones))

    list_x = [float(x) for i,x in enumerate(list_x) if i not in nones]
    list_y = [y for i,y in enumerate(list_y) if i not in nones]
    list_ycrit_min = [y for i,y in enumerate(list_ycrit_min) if i not in nones]
    list_ycrit_plus = [y for i,y in enumerate(list_ycrit_plus) if i not in nones]
    critical_modes = [mode for i,mode in enumerate(critical_modes) if i not in nones]

    list_x = np.array(list_x)
    minus = np.where(list_x<0.65)
    list_y = np.array(list_y)
    list_x_pupu= list_x[minus]
    list_y_pupu = list_y[minus]
    # ax.plot(list_x_pupu, list_y_pupu*2.3, 'D', color='k', markersize=10, mec='k',mew=0.5)
    ax.plot(list_x_pupu, list_y_pupu, 'D', color='k', markersize=10, mec='k',mew=0.5)

    list_x_toto = [0.7,0.7,0.8,0.8,0.9,0.9,1,1]
    list_y_toto = [4.65,2.86,4.48,3.14,4.35,3.36,4.21,3.57]
    # list_y_toto = [1.18,2.49,1.35,2.34,1.49,2.23,1.635,2.13]
    # list_y_toto = [0.177,0.375,0.2,0.35,0.224,0.334,0.245,0.318]
    list_y_toto = np.array(list_y_toto)#*2.3
    ax.plot(list_x_toto, list_y_toto, 'D', color='k', markersize=10, mec='k',mew=0.5)

    list_ycrit_plus[-1] = 4.8
    #ax.fill_between(list_x, np.array(list_ycrit_min)*2.3, np.array(list_ycrit_plus)*2.3, color='k', alpha=0.2)
    ax.fill_between(list_x, np.array(list_ycrit_min), np.array(list_ycrit_plus), color='k', alpha=0.2)

    

    y_label = global_functions.get_critical_plot_label(y_parameter)
    ax.set_ylabel(y_label, fontsize=fontsizelabel)
    ax.set_xlabel(r'$\eta / \eta_{\mathrm{Sp}}$', fontsize=fontsizelabel)
    ax.tick_params(axis='both', which='major', labelsize=fontsizetick)
    ax.set_ylim(bottom=0)

    # ax = plt.subplot(gs1[0])    

    # dict_mode_color=global_functions.dict_mode_new_color

    # colors = list(dict_mode_color.values())[:-1]
    # cmap = ListedColormap(colors)

    # # Create a colorbar with specified colors
    # bounds = list(dict_mode_color.keys())[:-1] + [max(dict_mode_color.keys())+1]
    # norm = BoundaryNorm(bounds, cmap.N)
    # cm = plt.cm.ScalarMappable(norm=norm, cmap=cmap)
    # cm.set_array([])
    # cb = plt.colorbar(cm, cax=ax, orientation='vertical')
    # ticks_positions = [(i + j) / 2 for i, j in zip(bounds[:-1], bounds[1:])]
    # cb.set_ticks(ticks_positions)
    # cb.set_ticklabels(list(dict_mode_color.keys()))
    # ax.text(0.5, -0.01, r'$n$', ha='center', va='top', fontsize=fontsizelabel)   

    # ax.tick_params(axis='both', which='both', length=0)
    # ax.yaxis.set_ticks_position('left')

    fig.tight_layout()
    # plt.show()
    plt.savefig('/home/jwp9427/bouloulou/414')
    plt.close()

if __name__ == '__main__':
    main()

