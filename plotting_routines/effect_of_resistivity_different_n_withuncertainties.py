#!/usr/local/depot/Python-3.7/bin/python
# /usr/local/depot/Python-3.5.1/bin/python

from hoho import europed_analysis, global_functions,startup, find_pedestal_values
import argparse
import matplotlib.pyplot as plt
import numpy as np

class CustomError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

def parse_modes(mode_str):
    return mode_str.split(',')

def argument_parser():
    """Defining comandline parser and returning the arguments"""
    parser = argparse.ArgumentParser(description = "Plots the profile of the critical alpha versus density shift")
    parser.add_argument("prefixes", type=parse_modes, help = "list of prefixes to construct the Europed run names")

    parser.add_argument("-A", "--firstname", help = "first part of the names, if you want to write before the prefixes")
    parser.add_argument("-B", "--middlname", help = "between prefixes and variations")

    parser.add_argument("-d", "--diamag", action = 'store_const', const = 'diamag', dest = 'crit', default = 'alfven', help = "normalize growth rate to diamagnetic frequency instead of Alfven frequency")
    parser.add_argument("-v", "--critical_value", help= "critical value of the growth rate, default : 0.03 for alfven, 0.25 for diamagnetic")
    parser.add_argument("-l", "--labels", type=parse_modes, help= "labels to display for the different Europed run prefixes")
    parser.add_argument("-L", "--legendtitle", help= "legend title")

    parser.add_argument("-n", "--shown", action = 'store_const', const = True, dest = 'shown', default = False, help = "show critical n for each point")

    group = parser.add_mutually_exclusive_group()
    group.add_argument("-f", "--frac", action = 'store_const', const = 'frac', dest = 'plot', default = 'dshift', help = "plot versus the fraction nesep/neped instead of versus density shift")
    group.add_argument("-s", "--nesep", action = 'store_const', const = 'nesep', dest = 'plot', help = "plot versus nesep instead of versus density shift")


    group = parser.add_mutually_exclusive_group()
    group.add_argument("-T", "--teped", action = 'store_const', const = 'teped', dest = 'ypar', default = 'alpha_helena_max', help = "plot critical pedestal temperature instead of alpha")
    group.add_argument("-D", "--delta", action = 'store_const', const = 'delta', dest = 'ypar', help = "plot critical width instead of aplha")
    group.add_argument("-P", "--pped", action = 'store_const', const = 'pped', dest = 'ypar', help = "plot critical pedestal pressure instead of alpha")
    group.add_argument("-p", "--peped", action = 'store_const', const = 'peped', dest = 'ypar', help = "plot critical pedestal electron pressure instead of alpha")


    group = parser.add_mutually_exclusive_group()
    group.add_argument('-x',"--exclude_mode", type=parse_modes, help = "list of modes to exclude, comma-separated (will consider all modes except for these ones)")
    group.add_argument('-m',"--modes", type=parse_modes, help = "list of modes to consider, comma-separated (will consider only these modes)")

    args = parser.parse_args()

    if args.exclude_mode and args.modes:
        parser.error("Arguments --exclude_mode and --modes are mutually exclusive. Use one or the other.")

    critical_value = args.critical_value
    if critical_value:
        critical_value = float(args.critical_value)

    prefixes = args.prefixes
    labels = args.labels
    legendtitle = args.legendtitle

    if len(prefixes) == 1 and prefixes[0] in list(global_functions.dict_input_prefixes.keys()):
        print(f"Prefix list loaded from {prefixes[0]}")
        prefixes,labels,legendtitle = global_functions.dict_input_prefixes[prefixes[0]]


    return prefixes, args.firstname, args.middlname, args.crit, critical_value, labels, legendtitle, args.shown, args.plot, args.ypar, args.exclude_mode, args.modes


def main(prefixes, firstname, middlname, crit, crit_value, labels, legendtitle, shown, plot, y_parameter, excluded_modes, considered_modes_input):

    if crit_value is None:
        if crit == "alfven":
            crit_value=0.03
        elif crit == "diamag":
            crit_value=0.25



    fig, ax = plt.subplots()

    if firstname is None:
        firstname = ['']
    if middlname is None:
        middlname = ''

    if labels is None:
        labels = prefixes


    if legendtitle == "eta":
        dict_color = global_functions.dict_eta_color
        legendtitle = r'$\eta$'
    elif legendtitle == "neped":
        dict_color = global_functions.dict_neped_color
        legendtitle = r'$n_e^{\mathrm{ped}} [10^{19}e.s^{-1}]$'
    else:
        keys = labels
        colors = ['C'+str(i) for i in range(len(labels))]
        dict_color = dict(zip(keys, colors))

    if legendtitle == 'betap':
        legendtitle = r'$\beta_p$'

    list_ycrit = {}

    for included_mode in considered_modes_input:  
        list_ycrit = []
        list_ycrit_min = []
        list_ycrit_plus = []
        critical_modes = []
        list_eta = [] 
        for iprefix,prefix in enumerate(prefixes):
            

            
                europed_run = firstname+str(prefix)+middlname
                try:
                    x_param = europed_analysis.get_x_parameter(europed_run, y_parameter)
                    gammas, modes = europed_analysis.get_gammas(europed_run, crit)

                    tab, considered_modes = europed_analysis.filter_tab_general(gammas, modes, [included_mode], excluded_modes)

                    has_unstable, y_crit, i_mode = europed_analysis.find_critical(x_param, tab, crit_value)
                    y_crit_min = None
                    y_crit_plus = None

                    if y_crit:
                        proportionality = 0.85
                        while y_crit_min == None:
                            has_unstable, y_crit_min, poop = europed_analysis.find_critical(x_param, tab, crit_value*proportionality)
                            proportionality += 0.01
                        
                        proportionality = 1.15
                        while y_crit_plus == None:
                            has_unstable, y_crit_plus, poop = europed_analysis.find_critical(x_param, tab, crit_value*proportionality)
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

        dict_mode_color = global_functions.dict_mode_color

        #list_y = np.array(list_y)/list_y[0]


        ax.plot(list_x, list_y, '-o',label=included_mode, color=dict_mode_color[int(included_mode)])  
        # for i,xtemp in enumerate(list_x):

        #     ax.plot([xtemp,xtemp], [list_ycrit_min[i],list_ycrit_plus[i]], '-', color=dict_mode_color[int(included_mode)])  

        ax.fill_between(list_x, list_ycrit_min, list_ycrit_plus, color=dict_mode_color[int(included_mode)], alpha=0.2)

        if shown:    
            for i_critmode, critmode in enumerate(critical_modes):
                ax.annotate(critmode, (list_x[i_critmode], list_y[i_critmode]), color=dict_mode_color[int(included_mode)], textcoords="offset points", xytext=(0,5), ha='center') 


      
    if legendtitle is not None:
        ax.legend(title=legendtitle, fontsize=8)

    y_label = global_functions.get_critical_plot_label(y_parameter)
    ax.set_ylabel(y_label)
    ax.set_xlabel(r'$\eta$')
    ax.legend()

    ax.set_ylim(bottom=0)
    fig.tight_layout()
    plt.show()

if __name__ == '__main__':
    prefixes, firstname, middlname, crit, crit_value, labels, legendtitle, shown, plot, y_parameter, excluded_modes, modes = argument_parser()
    main(prefixes, firstname, middlname, crit, crit_value, labels, legendtitle, shown, plot, y_parameter, excluded_modes, modes)