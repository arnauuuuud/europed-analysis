#!/usr/local/depot/Python-3.7/bin/python
# /usr/local/depot/Python-3.5.1/bin/python

from hoho import europed_analysis, global_functions, startup
import argparse
import matplotlib.pyplot as plt
import matplotlib.transforms as transforms
import math
import re
from matplotlib.widgets import CheckButtons, Button, RadioButtons, TextBox
import matplotlib.gridspec as gridspec
import numpy as np

def parse_modes(mode_str):
    return mode_str.split(',')


def argument_parser():
    """Defining comandline parser and returning the arguments"""
    parser = argparse.ArgumentParser(description = "Plots the growth rate of the individual toroidal modes versus alpha for the given europed run (the growth rate is normalized to the Alfven frequency) ")
    
    
    parser.add_argument("-A", "--firsname", help = "first part of the names, if you want to write before the prefixes")
    parser.add_argument("-C", "--middname", help = "between prefixes and variations")
    parser.add_argument("-B", "--europed_runs", type=parse_modes, help = "names of the Europed run to plot the modes of")
    parser.add_argument("-Z", "--lastname", type=parse_modes, help = "variations")


    parser.add_argument("-d", "--diamag", action = 'store_const', const = 'diamag', dest = 'crit', default = 'alfven', help = "normalize growth rate to diamagnetic frequency instead of Alfven frequency")
    parser.add_argument("-o", "--omega", action = 'store_const', const = 'omega', dest = 'crit', default = 'alfven', help = "plot omega instead of gamma")

    parser.add_argument("-v", "--critical_value", help= "critical value of the growth rate, default : 0.03 for alfven, 0.25 for diamagnetic")

    group = parser.add_mutually_exclusive_group()
    group.add_argument("-T", "--teped", action = 'store_const', const = 'teped', dest = 'xpar', default = 'alpha_helena_max', help = "plot versus pedestal temperature instead of alpha")
    group.add_argument("-D", "--delta", action = 'store_const', const = 'delta', dest = 'xpar', help = "plot versus width instead of alpha")
    group.add_argument("-P", "--pped", action = 'store_const', const = 'pped', dest = 'xpar', help = "plot versus pedestal pressure instead of alpha")
    group.add_argument("-p", "--peped", action = 'store_const', const = 'peped', dest = 'xpar', help = "plot versus pedestal electron pressure instead of alpha")

    parser.add_argument("-l", "--labels", type=parse_modes, help= "labels to display for the different Europed run prefixes")

    group = parser.add_mutually_exclusive_group()
    group.add_argument('-x',"--exclud_mode", type=parse_modes, help = "list of modes to exclude, comma-separated (will plot all modes except for these ones)")
    group.add_argument('-m',"--consid_mode", type=parse_modes, help = "list of modes to consider, comma-separated (will plot only these modes)")

    parser.add_argument("-V", "--vertical_line", action = 'store_const', const = True, dest = 'plot_vline', default=False, help = "plot vertical line")
    parser.add_argument("-H", "--horizontal_line", action = 'store_const', const = True, dest = 'plot_hline', default=False, help = "plot horizontal line")

    parser.add_argument("-s", "--same_plot", action = 'store_const', const = True, dest = 'same_plot', default=False, help = "plot everything on the same plot")


    args = parser.parse_args()

    if args.exclud_mode and args.consid_mode:
        parser.error("Arguments --exclud_mode and --consid_mode are mutually exclusive. Use one or the other.")

    if args.critical_value:
        critical_value = float(args.critical_value)
    else:
        critical_value = None

    return args.europed_runs, args.firsname, args.middname, args.lastname, args.crit, critical_value, args.labels, args.xpar, args.exclud_mode, args.consid_mode, args.plot_vline, args.plot_hline, args.same_plot


def main(europed_runs, firsname, middname, lastname, crit, crit_value, labels, x_parameter, exclud_mode, consid_mode_input, plot_vline, plot_hline, same_plot):
    
    consid_mode_input = ['1', '2', '3', '4', '5', '7', '10', '20', '30', '40', '50'] if consid_mode_input is None else consid_mode_input
    europed_runs = ['0'] if europed_runs is None else europed_runs
    lastname = ['0'] if lastname is None else lastname
    middname = '_ds' if middname is None else middname
    filter_wrong_slope = True

    list_legends = {}


    if crit_value is None:
        if crit == "alfven":
            crit_value=0.03
        elif crit == "diamag":
            crit_value=0.25




    fig = plt.figure(figsize=(10, 4))
    gs = gridspec.GridSpec(7, 3, width_ratios=[10, 1, 1], hspace=0, wspace=0)

    # Create subplots using the grid specification
    ax_plot = plt.subplot(gs[:,0])
    ax_checkbox_eta = plt.subplot(gs[0,1]) 
    ax_checkbox_filter = plt.subplot(gs[0,2])
    ax_checkbox_mode = plt.subplot(gs[3:5,1])
    ax_checkbox_mode_bis = plt.subplot(gs[3:5,2]) 
    ax_checkbox_dshift = plt.subplot(gs[1:3,1])
    ax_radiobutton_crit = plt.subplot(gs[5,2])
    ax_critvalue = plt.subplot(gs[5,1])
    ax_radiobutton_xaxis = plt.subplot(gs[1:3,2])
    ax_checkbox_run = plt.subplot(gs[6,1:])



    checkboxes_mode = {}
    list_mode = ['1','2','3','4','5','7','10','20','30','40','50']
    checkbox_states_mode = {mode: mode in consid_mode_input for mode in list_mode}
    consid_mode_input_list = [consid_mode_input]

    checkboxes_dshift = {}
    list_dshift = ['-1','-0.5','0','0.5','1','2','3']
    list_dshift_label = [str(float(dshift))+'%' for dshift in list_dshift]
    checkbox_states_dshift = {str(float(dshift))+'%': dshift in lastname for dshift in list_dshift}
    lastname_list = [lastname]

    checkboxes_eta = {}
    list_eta = ['0','0.2','0.5','0.8','1']
    checkbox_states_eta = {eta: eta in europed_runs for eta in list_eta}

    filter_wrong_slope_list = [filter_wrong_slope]
    plot_hline_list = [plot_hline]
    plot_vline_list = [plot_vline]
    x_parameter_list = [x_parameter]
    crit_value_list = [crit_value]
    crit_list = [crit]

    def add_element_mode(label):
        checkbox_states_mode[label] = not checkbox_states_mode[label]
        if checkbox_states_mode[label]:
            consid_mode_input_list[0].append(label)
            consid_mode_input_list[0] = sorted(consid_mode_input_list[0],key=lambda x:int(x))
        else:
            consid_mode_input_list[0].remove(label)


    dict_dshift = {
        "-1.0%":"-1",
        "-0.5%":"-0.5",
        "0.0%":"0",
        "0.5%":"0.5",
        "1.0%":"1",
        "2.0%":"2",
        "3.0%":"3",
        "4.0%":"4"
    }
    def add_element_dshift(label):
        checkbox_states_dshift[label] = not checkbox_states_dshift[label]
        label2 = dict_dshift[label]
        if checkbox_states_dshift[label]:
            lastname_list[0].append(label2)
            lastname_list[0] = sorted(lastname_list[0],key=lambda x:float(x))
        else:
            lastname_list[0].remove(label2)

    def add_element_eta(label):
        checkbox_states_eta[label] = not checkbox_states_eta[label]
        if checkbox_states_eta[label]:
            europed_runs.append(label)
            europed_runs.sort()
        else:
            europed_runs.remove(label)
    def change_crit(label):
        crit_list[0] = label
    def change_plot(label):
        if label == 'filter wrong slope':
            filter_wrong_slope_list[0] = not filter_wrong_slope_list[0]
        elif label == 'H line':
            plot_hline_list[0] = not plot_hline_list[0]
        elif label == 'V line':
            plot_vline_list[0] = not plot_vline_list[0]

    def run_on_click(label):
        ax.clear()
        run(consid_mode_input_list[0], lastname_list[0], filter_wrong_slope_list[0], plot_hline_list[0], plot_vline_list[0], x_parameter_list[0], crit_list[0], crit_value_list[0])
        plt.draw() 

    def change_xaxis(label):
        if label == r'$\alpha$':
            x_parameter_list[0] = 'alpha_helena_max'
        elif label == r'$T_e^{\mathrm{ped}}$':
            x_parameter_list[0] = 'teped'  
        elif label == r'$\Delta$':
            x_parameter_list[0] = 'delta' 
        elif label == r'$p_{tot}^{\mathrm{ped}}$':
            x_parameter_list[0] = 'pped'

    def update_crit_value(val):
        crit_value_list[0] = float(val)

    check1 = CheckButtons(ax_checkbox_mode, list_mode[:len(list_mode)//2], list(checkbox_states_mode.values())[:len(list_mode)//2])
    check1_bis = CheckButtons(ax_checkbox_mode_bis, list_mode[len(list_mode)//2:], list(checkbox_states_mode.values())[len(list_mode)//2:])
    check2 = CheckButtons(ax_checkbox_dshift, list_dshift_label, list(checkbox_states_dshift.values()))
    check3 = CheckButtons(ax_checkbox_eta, list_eta, list(checkbox_states_eta.values()))
    check4 = CheckButtons(ax_checkbox_filter, ['filter wrong slope', 'H line', 'V line'], [filter_wrong_slope, plot_hline, plot_vline])
    check5 = Button(ax_checkbox_run, 'Run')
    check6 = RadioButtons(ax_radiobutton_xaxis, [r'$\alpha$',r'$T_e^{\mathrm{ped}}$',r'$\Delta$',r'$p_{tot}^{\mathrm{ped}}$'])
    if crit == 'diamag':
        active = 0
    elif crit == 'alfven':
        active = 1
    elif crit == 'omega':
        active = 2
    check7 = RadioButtons(ax_radiobutton_crit, ['diamag','alfven','omega'], active=active)
    text = TextBox(ax_critvalue, '', initial=str(crit_value))

    check1.on_clicked(add_element_mode)
    check1_bis.on_clicked(add_element_mode) 
    check2.on_clicked(add_element_dshift) 
    check3.on_clicked(add_element_eta)
    check4.on_clicked(change_plot)
    check5.on_clicked(run_on_click)
    check6.on_clicked(change_xaxis)
    check7.on_clicked(change_crit)
    text.on_submit(update_crit_value)
    

    for i,mode in enumerate(list_mode):
        c = global_functions.dict_mode_color[int(mode)]
        if i < len(list_mode)//2:
            check1.labels[i].set_color(c)
        else:
            check1_bis.labels[i-len(list_mode)//2].set_color(c)
       

    
    ax = ax_plot
    linestyles = {
        '-1':(0,(1, 5)),
        '-0.5':(0,(1, 1)),
        '0':'solid',
        '0.5':(0, (5, 1)),
        '1':(0, (5, 5)),
        '2':(0, (10, 1)),
        '3':(0, (10, 5)),
    }
    markers = {
        '0':'o',
        '1':'s',
        '2':'^'
    }



    def run(consid_mode_input, lastname, filter_wrong_slope, plot_hline, plot_vline, x_parameter, crit, crit_value):

        print()
        print('#######################')
        print(f'Eta: {europed_runs}')
        print(f'Density shift: {lastname}')
        print(f'Modes considered: {consid_mode_input}')
        print('#######################')
        print()
        europed_runs_used = [firsname + europed_run + middname + ln for europed_run in europed_runs for ln in lastname]

        if consid_mode_input:
            consid_mode_input = sorted(consid_mode_input, key=lambda x: int(x))        

        

        for iplot,europed_run in enumerate(europed_runs_used):
            try:
                x_param = europed_analysis.get_x_parameter(europed_run, x_parameter)
                gammas, modes = europed_analysis.get_gammas(europed_run, crit)
                tab, consid_mode = europed_analysis.filter_tab_general(gammas, modes, consid_mode_input, exclud_mode)

                sorted_indices = np.argsort(x_param)
                x_param = x_param[sorted_indices]
                tab = tab[sorted_indices]

                pattern1 = r'eta\d_ds'
                eta_temp = re.search(pattern1, europed_run).group()[3]

                pattern2 = r'ds.*\d'
                dshift_temp = re.search(pattern2, europed_run).group()[2:]
                
                marker = markers[eta_temp]
                linestyle = linestyles[dshift_temp]


                for i, mode in enumerate(consid_mode):
                    temp_x = x_param
                    temp_y = tab[:,i]
                    nan_indices = np.isnan(temp_y)
                    x_filtered = temp_x[~nan_indices]
                    y_filtered = temp_y[~nan_indices]
                    ax.plot(x_filtered,y_filtered, color=global_functions.dict_mode_color[int(mode)], linestyle = linestyle, linewidth=2, marker = marker, markersize=7, markeredgewidth=3)
                
                if plot_vline:
                    has_unstable, x_crit, col = europed_analysis.find_critical(x_param, tab, crit_value, filter_wrong_slope)
                    if has_unstable:
                        ax.axvline(x_crit, color="r")

                        xmin,xmax,ymin,ymax = ax.axis()
                        ratio = (x_crit-xmin)/(xmax-xmin)

                        trans = transforms.blended_transform_factory(ax.transData, ax.transAxes)
                        x_crit_order = math.floor(math.log10(x_crit))
                        x_crit_round = np.around(np.around(x_crit*10**-x_crit_order,1)*10**x_crit_order,6)

                        ax.text(x_crit, 1.0, '%.2E'%x_crit, color="r", horizontalalignment='center', verticalalignment='bottom',transform=trans)
            except RuntimeError:
                print(f"{europed_run:>40} RUNTIME ERROR : NO FIT FOUND")
            except FileNotFoundError:
                print(f"{europed_run:>40} FILE DOES NOT EXIST")
            if plot_hline:
                ax.axhline(crit_value, linestyle="--",color="k")


        x_label, y_label = global_functions.get_plot_labels_gamma_profiles(x_parameter, crit)
        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)
        bot,to = ax.get_ylim()
        if bot > 0:
            ax.set_ylim(bottom=0)
        ax.set_xlim(left=0)

        current_position = 0.005

        if len(consid_mode_input) > 1:
            print(consid_mode_input)
            custom_legend = [plt.Line2D([0], [0], color=global_functions.dict_mode_color[int(mode)], linewidth=2, label=mode)  for mode in consid_mode_input]
            legend1 = ax.legend(handles=custom_legend, fontsize=8, title = r'$n$', loc=(current_position,0.005)) 
            ax.add_artist(legend1)
            try:
                bbox = legend1.get_window_extent()
                width = bbox.inverse_transformed(ax.transAxes).width
                current_position += width + 0.005
            except AttributeError:
                current_position += 0.1
        
        if len(lastname) > 1:
            try:
                custom_legend = [plt.Line2D([0,100], [0,0], color='k', linestyle = linestyles[ln], markersize=0, linewidth=2,label=ln + '%')  for ln in lastname]
                legend2 = ax.legend(handles=custom_legend, fontsize=8, title = r'$\Delta$', loc=(current_position,0.005), handlelength = 6) 
                ax.add_artist(legend2)
                bbox = legend2.get_window_extent()
                width = bbox.inverse_transformed(ax.transAxes).width
                current_position += width + 0.005
            except AttributeError:
                current_position += 0.1

        if len(europed_runs) > 1:
            custom_legend = [plt.Line2D([0], [0], color='k', marker = markers[europed_run], linewidth=0,label=europed_run)  for europed_run in europed_runs]
            legend3 = ax.legend(handles=custom_legend, fontsize=8, title = r'$\eta$', loc=(current_position,0.005)) 
            ax.add_artist(legend3)

    run(consid_mode_input, lastname, filter_wrong_slope, plot_hline, plot_vline, x_parameter, crit, crit_value)
    plt.show()




if __name__ == '__main__':
    europed_runs, firsname, middname, lastname, crit, crit_value, labels, x_parameter, exclud_mode, consid_mode, plot_vline, plot_hline, same_plot = argument_parser()
    main(europed_runs, firsname, middname, lastname, crit, crit_value, labels, x_parameter, exclud_mode, consid_mode, plot_vline, plot_hline, same_plot)