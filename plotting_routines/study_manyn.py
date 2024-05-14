#!/usr/local/depot/Python-3.7/bin/python
# /usr/local/depot/Python-3.5.1/bin/python

from hoho import useful_recurring_functions, europed_analysis, global_functions,startup
import argparse
import matplotlib.pyplot as plt
import numpy as np

def main():
    europed_run = "m2_manyn"
    crit = "alfven"
    x_parameter = "pped"
    considered_modes = None
    crit_value = 0.03

    x_param = europed_analysis.get_x_parameter(europed_run, x_parameter)
    gammas, modes = europed_analysis.get_gammas(europed_run, crit)

    list_nb_modes = []
    list_ycrit = []

    fig,ax = plt.subplots()

    for excluded_modes in [[20,30,40,50,60,70,80,90,100],[30,40,50,60,70,'80','90',100],[40,50,60,'70','80','90',100],[50,60,'70','80','90',100],['60','70','80','90','100'],['70','80','90','100'],['80','90','100'],['90','100'],['100'],[]]:
        tab, trash = europed_analysis.filter_tab_general(gammas, modes, considered_modes, excluded_modes)
        has_unstable, y_crit, dumm = europed_analysis.find_critical(x_param, tab, crit_value)
        list_nb_modes.append(16-len(excluded_modes))
        list_ycrit.append(y_crit)


    ax.plot(list_nb_modes, list_ycrit, 'x-')
    ax.set_xlabel("Number of considered modes")
    ax.set_ylabel(r"Critical $p^{\mathrm{ped}}_{tot}$ [$kPa$]")
    ax.set_ylim(bottom=0)
    fig.tight_layout()
    plt.show()

if __name__ == '__main__':
    main()