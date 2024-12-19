#!/usr/local/depot/Python-3.7/bin/python
# /usr/local/depot/Python-3.5.1/bin/python

from hoho import useful_recurring_functions, europed_analysis, global_functions,startup, find_pedestal_values_old
import argparse
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Slider, CheckButtons, RadioButtons, Button
import matplotlib.gridspec as gridspec
from functools import partial

class useful_recurring_functions.CustomError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

def parse_modes(mode_str):
    return mode_str.split(',')

def argument_parser():
    """Defining comandline parser and returning the arguments"""
    parser = argparse.ArgumentParser(description = "Plots the profile of the critical alpha versus density shift")
    parser.add_argument("prefixes", type=useful_recurring_functions.parse_modes, help = "list of prefixes to construct the Europed run names")
    parser.add_argument("variations", type=useful_recurring_functions.parse_modes, help = "name variations of the Europed runs (the Europed runs will have the name [prefix]+[variation]{+[suffix]})  If set to 'full_list', variations=['-0.0100','-0.0050','0.0000','0.050','0.0100','0.0050','0.0150','0.0200','0.0250','0.0350','0.0400']")

    parser.add_argument("-A", "--firstname", type=useful_recurring_functions.parse_modes, help = "first part of the names, if you want to write before the prefixes")
    parser.add_argument("-B", "--middlname", help = "between prefixes and variations")

    parser.add_argument("-d", "--diamag", action = 'store_const', const = 'diamag', dest = 'crit', default = 'alfven', help = "normalize growth rate to diamagnetic frequency instead of Alfven frequency")
    parser.add_argument("-v", "--critical_value", help= "critical value of the growth rate, default : 0.03 for alfven, 0.25 for diamagnetic")
    parser.add_argument("-l", "--labels", type=useful_recurring_functions.parse_modes, help= "labels to display for the different Europed run prefixes")
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
    group.add_argument('-x',"--exclude_mode", type=useful_recurring_functions.parse_modes, help = "list of modes to exclude, comma-separated (will consider all modes except for these ones)")
    group.add_argument('-m',"--modes", type=useful_recurring_functions.parse_modes, help = "list of modes to consider, comma-separated (will consider only these modes)")

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
        prefixes,labels,legendtitle = global_functions.dict_input_prefixes[prefixes[0]]


    variations = args.variations
    if len(variations) == 1 and variations[0] in list(global_functions.dict_input_variations.keys()):
        variations = global_functions.dict_input_variations[variations[0]]

    return prefixes, variations, args.firstname, args.middlname, args.crit, critical_value, labels, legendtitle, args.shown, args.plot, args.ypar, args.exclude_mode, args.modes


def main(prefixes, variations, firstnames, middlname, crit, crit_value, labels, legendtitle, shown_input, plot, y_parameter, excluded_modes, considered_modes_input):

    if considered_modes_input is None:
        considered_modes_input = ['1','2','3','4','5','7','10','20','30','40','50']

    crit = 'diamag'
    shown = True
    if crit_value is None:
        if crit == "alfven":
            crit_value=0.03
        elif crit == "diamag":
            crit_value=0.25

    if firstnames is None:
        firstnames = ['']
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

    fig = plt.figure(figsize=(10, 4))
    gs = gridspec.GridSpec(9, 2, width_ratios=[5, 1])

    # Create subplots using the grid specification
    ax_plot = plt.subplot(gs[:,0])
    ax_checkbox_crit = plt.subplot(gs[0,1])             
    ax_slider_crit_value = plt.subplot(gs[1,1]) 
    ax_checkbox_shown = plt.subplot(gs[2,1]) 
    ax_checkbox_mode = plt.subplot(gs[3:6,1])
    ax_checkbox_xaxis = plt.subplot(gs[6,1])
    ax_checkbox_yaxis = plt.subplot(gs[7,1])
    ax_checkbox_run = plt.subplot(gs[8,1])  

    ax = ax_plot

    filter_wrong_slope = False
    filter_wrong_slope_list = [filter_wrong_slope]
    crit_list = [crit]
    shown_list = [shown]
    crit_value_list = [crit_value]
    checkboxes_mode = {}
    list_mode = ['1','2','3','4','5','7','10','20','30','40','50']
    checkbox_states_mode = {mode: mode in considered_modes_input for mode in list_mode}
    considered_modes_input_list = [considered_modes_input]
    y_parameter_list = [y_parameter]
    x_parameter_list = [plot]

    def change_crit(label):
        crit_list[0] = label
    def update_crit_value(val):
        crit_value_list[0] = val
    def change_checkbox3(label):
        if label == 'show n':
            shown_list[0] = not shown_list[0]
        elif label == 'filter wrong slope':
            filter_wrong_slope_list[0] = not filter_wrong_slope_list[0]
    def add_element_mode(label):
        checkbox_states_mode[label] = not checkbox_states_mode[label]
        if checkbox_states_mode[label]:
            considered_modes_input_list[0].append(label)
            considered_modes_input_list[0] = sorted(considered_modes_input_list[0], key=lambda x: int(x))
        else:
            considered_modes_input_list[0].remove(label)
    def change_xaxis(label):
        if label == 'Density shift':
            x_parameter_list[0] = 'dshift'
        elif label == r'$n_e^{sep}/n_e^{\mathrm{ped}}$':
            x_parameter_list[0] = 'frac'  
        elif label == r'$n_e^{sep}$':
            x_parameter_list[0] = 'nesep' 
    def change_yaxis(label):
        if label == r'$\alpha$':
            y_parameter_list[0] = 'alpha_helena_max'
        elif label == r'$T_e^{\mathrm{ped}}$':
            y_parameter_list[0] = 'teped'  
        elif label == r'$\Delta$':
            y_parameter_list[0] = 'delta' 
        elif label == r'$p_{tot}^{\mathrm{ped}}$':
            y_parameter_list[0] = 'pped'         
    def run_on_click(label):
        ax.clear()
        run(crit_list[0], crit_value_list[0], considered_modes_input_list[0], shown_list[0], y_parameter_list[0], x_parameter_list[0], filter_wrong_slope_list[0])
        plt.draw() 
        

    check1 = RadioButtons(ax_checkbox_crit, ['diamag','alfven'], active=0)
    slider2 = Slider(ax_slider_crit_value, 'Crit value', 0, 0.5, valinit=crit_value)
    check3 = CheckButtons(ax_checkbox_shown, ['show n','filter wrong slope'], [shown,filter_wrong_slope])
    check4 = CheckButtons(ax_checkbox_mode, list_mode, list(checkbox_states_mode.values()))
    check5 = RadioButtons(ax_checkbox_xaxis, ['Density shift',r'$n_e^{sep}/n_e^{\mathrm{ped}}$', r'$n_e^{sep}$'], active=0)
    check6 = RadioButtons(ax_checkbox_yaxis, [r'$\alpha$',r'$T_e^{\mathrm{ped}}$',r'$\Delta$',r'$p_{tot}^{\mathrm{ped}}$'], active=0)
    check7 = Button(ax_checkbox_run, 'Run')


    check1.on_clicked(change_crit)  
    slider2.on_changed(update_crit_value)
    check3.on_clicked(change_checkbox3)
    check4.on_clicked(add_element_mode)  
    check5.on_clicked(change_xaxis)  
    check6.on_clicked(change_yaxis)  
    check7.on_clicked(run_on_click)

    
    
    def run(crit, crit_value, considered_modes_input, shown, y_parameter, plot, filter_wrong_slope):
        print()
        print('#######################')
        print(f'Criterion: {crit}')
        print(f'Critical value: {crit_value}')
        print(f'Modes considered: {considered_modes_input}')
        print(f'Show n: {shown}')
        print(f'X axis: {plot}')
        print(f'Y axis: {y_parameter}')
        print('#######################')
        print()
        for firstname in firstnames:
            for iprefix,prefix in enumerate(prefixes):
                list_ycrit = []
                critical_modes = []
                list_frac = []
                list_nesep = []
                list_dshifts = []

                for dshift in variations:
                    europed_run = firstname+prefix+middlname+dshift
                    try:

                        x_param = europed_analysis.get_x_parameter(europed_run, y_parameter)
                        gammas, modes = europed_analysis.get_gammas(europed_run, crit)

                        tab, considered_modes = europed_analysis.filter_tab_general(gammas, modes, considered_modes_input, excluded_modes)

                        has_unstable, y_crit, i_mode = europed_analysis.find_critical(x_param, tab, crit_value, filter_wrong_slope)
                        if y_crit is  None:
                            raise useful_recurring_functions.CustomError(f"No critical value found")

                        list_ycrit.append(y_crit)

                        if plot == 'frac':
                            frac = find_pedestal_values_old.get_frac(europed_run, crit)
                            list_frac.append(frac)
                        elif plot == 'nesep':
                            nesep = find_pedestal_values_old.get_nesep(europed_run, crit)
                            list_nesep.append(nesep)

                        if i_mode == -1:
                            critical_modes.append(-1)
                        else:
                            critical_modes.append(considered_modes[i_mode])
                        list_dshifts.append(dshift)


                    except useful_recurring_functions.CustomError:
                        pass
                    except FileNotFoundError:
                        pass
                    except RuntimeError:
                        pass
                    except IndexError:
                        pass
                    except TypeError:
                        pass

                dict_listsx = {
                    'dshift':list_dshifts,
                    'frac':list_frac,
                    'nesep':list_nesep
                }
                list_x = dict_listsx[plot]
                list_y = list_ycrit

                list_x = np.array(list_x)
                list_y = np.array(list_y)
                critical_modes = np.array(critical_modes)

                x_nones = np.where(list_x == None)[0]
                y_nones = np.where(list_y == None)[0]

                nones = np.concatenate((x_nones, y_nones))

                list_x = [float(x) for i,x in enumerate(list_x) if i not in nones]
                list_y = [y for i,y in enumerate(list_y) if i not in nones]
                critical_modes = [mode for i,mode in enumerate(critical_modes) if i not in nones]

                # list_x = [x for x,y in zip(list_x, list_y) if x is not None and y is not None]
                # list_y = [y for (x,y) in zip(list_x, list_y) if ((x,y) is not (None,None))] 
                # critical_modes = [str(critmode) for critmode,x,y in zip(critical_modes,list_x, list_y) if x is not None and y is not None]

                if labels:
                    label = labels[iprefix]
                    marker = 'o'
                    linestyle = 'solid'
                    linewidth = 1
                    if 'eta0' in prefix:
                        marker = 'o'
                    elif 'eta1' in prefix:
                        marker = 's'
                    elif 'eta2' in prefix:
                        marker = '^'

                    ax.plot(list_x, list_y, '-', marker=marker, linewidth = 2, markersize=10, linestyle=linestyle,label=label, color=dict_color[label])  
                    if shown:    
                        for i_critmode, critmode in enumerate(critical_modes):
                            ax.annotate(critmode, (list_x[i_critmode], list_y[i_critmode]), color=dict_color[label], textcoords="offset points", fontsize=13, xytext=(0,5), ha='center') 
                else:
                    ax.plot(list_x, list_y, 'o-')

        
        if legendtitle is not None:
            ax.legend(title=legendtitle, fontsize=10, handlelength = 3,title_fontsize=12)

        y_label = global_functions.get_critical_plot_label(y_parameter)
        ax.set_ylabel(y_label)

        if plot == 'frac':
            ax.set_xlim(left=0)
            ax.set_xlabel(r"$n_e^{sep}/n_e^{\mathrm{ped}}$")
        elif plot == 'nesep':
            ax.set_xlabel(r"$n_e^{sep}$")
        elif plot == 'dshift':
            ax.set_xlabel("Density shift")
        ax.set_ylim(bottom=0)
        fig.tight_layout()

    run(crit, crit_value, considered_modes_input, shown, y_parameter, plot, filter_wrong_slope)
    plt.show()

if __name__ == '__main__':
    prefixes, variations, firstname, middlname, crit, crit_value, labels, legendtitle, shown, plot, y_parameter, excluded_modes, modes = argument_parser()
    main(prefixes, variations, firstname, middlname, crit, crit_value, labels, legendtitle, shown, plot, y_parameter, excluded_modes, modes)