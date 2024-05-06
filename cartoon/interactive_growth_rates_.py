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

def main():
    
    consid_mode = {'1':False,'2':False, '3':False, '4':False, '5':False, '7':False, '10':False, '20':False, '30':False, '40':False, '50':False}
    euroname_1 = []
    euroname_2 = []
    euroname_3 = []
    euroname_4 = []
    checkbox_envelope_ = [False]
    crit_value = 0.03
    filter_wrong_slope = True



    crit = 'alfven'
    plot_hline = True
    plot_vline = True
    x_parameter = 'alpha_helena_max'

    fig = plt.figure(figsize=(20, 10))
    gs = gridspec.GridSpec(10, 3, width_ratios=[10, 1, 1], hspace=0, wspace=0)

    # Create subplots using the grid specification
    ax_plot = plt.subplot(gs[:,0])
    
    # First text box: MAIN NAME EUROPED: modify euroname_bas1 (mandatory)
    ax_textbox_1 = plt.subplot(gs[0,1:]) 
    euroname_1 = TextBox(ax_textbox_1, '', initial='f4_eta')
    def update_euroname_1(val):
        euroname_1[0] = val.split(',')
    euroname_1.on_submit(update_euroname_1)


    # Second text box: NAME EUROPED: modify euroname_var1 (optional)
    ax_textbox_2 = plt.subplot(gs[1,1:]) 
    euroname_2 = TextBox(ax_textbox_2, '', initial='0,1,2')
    def update_euroname_2(val):
        euroname_2[0] = val.split(',')
    euroname_2.on_submit(update_euroname_2)


    # Third text box: NAME EUROPED: modify euroname_bas2 (optional)
    ax_textbox_3 = plt.subplot(gs[2,1:]) 
    euroname_3 = TextBox(ax_textbox_3, '', initial='_ds')
    def update_euroname_3(val):
        euroname_3[0] = val.split(',')
    euroname_3.on_submit(update_euroname_3)


    # Fourth text box: NAME EUROPED: modify euroname_var2 (optional)
    ax_textbox_4 = plt.subplot(gs[3,1:]) 
    euroname_4 = TextBox(ax_textbox_4, '', initial='0')
    def update_euroname_4(val):
        euroname_4[0] = val.split(',')
    euroname_4.on_submit(update_euroname_4)


    # Fifth box: Radiobuttons for x-axis parameter
    ax_x_parameter = plt.subplot(gs[4,1:])
    radio_button1 = RadioButtons(ax_x_parameter, [r'$\alpha$',r'$T_e^{\mathrm{ped}}$',r'$\Delta$',r'$p_{tot}^{\mathrm{ped}}$'], orientation='horizontal')
    def change_xaxis(label):
        if label == r'$\alpha$':
            x_parameter = 'alpha_helena_max'
        elif label == r'$T_e^{\mathrm{ped}}$':
            x_parameter = 'teped'  
        elif label == r'$\Delta$':
            x_parameter = 'delta' 
        elif label == r'$p_{tot}^{\mathrm{ped}}$':
            x_parameter = 'pped'
    radio_button1.on_clicked(change_xaxis)

    
    # Sixth box: Envelope
    ax_checkbox_envelope = plt.subplot(gs[5,1:3])
    checkbox_envelope = CheckButtons(ax_checkbox_envelope, ['Envelope'], [False])
    def change_envelope(label):
        checkbox_envelope_[0] = not checkbox_envelope_[0]
    checkbox_envelope.on_clicked(change_envelope)

    # Seventh box: crit_value
    ax_textbox_crit_value = plt.subplot(gs[6,1:3])
    textbox_crit_value = TextBox(ax_textbox_crit_value, '', initial='0.03')
    def update_crit_value(val):
        crit_value = float(val)
    textbox_crit_value.on_submit(update_crit_value)

    # Eigth box: crit
    ax_radiobutton_crit = plt.subplot(gs[7:9,1:3])
    radiobutton_crit = RadioButtons(ax_radiobutton_crit, ['alfven', 'diamag'], active=0)
    def change_crit(label):
        crit = label
    radiobutton_crit.on_clicked(change_crit)
    

    # Ninth box: checkboxes for modes considered
    list_mode = ['1','2','3','4','5','7','10','20','30','40','50']
    checkbox_states_mode = {mode: mode in consid_mode for mode in list_mode}
    ax_checkbox_mode = plt.subplot(gs[5:9,3])
    checkboxes_mode = CheckButtons(ax_checkbox_mode, consid_mode.keys(), [False]*len(consid_mode.keys()))
    def add_element_mode(label):
        checkbox_states_mode[label] = not checkbox_states_mode[label]
        consid_mode[label] = checkbox_states_mode[label]
    checkboxes_mode.on_clicked(add_element_mode)

    # Tenth box: Run button
    ax_run_button = plt.subplot(gs[9, 1:])
    run_button = Button(ax_run_button, 'Run')
    def run_on_click(event):
        run(consid_mode, euroname_1[0], euroname_2[0], euroname_3[0], euroname_4[0], checkbox_envelope_[0], crit_value, filter_wrong_slope, crit, plot_hline, plot_vline, x_parameter)
    run_button.on_clicked(run_on_click)

    plt.show()



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

                pattern1 = r'eta\d_density_shift'
                eta_temp = re.search(pattern1, europed_run).group()[3]

                pattern2 = r'density_shift.*\.\d\d\d\d'
                dshift_temp = re.search(pattern2, europed_run).group()[13:]
                
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
                custom_legend = [plt.Line2D([0,100], [0,0], color='k', linestyle = linestyles[ln], markersize=0, linewidth=2,label=str(round(float(ln)*100,5)) + '%')  for ln in lastname]
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

    #run(consid_mode_input, lastname, filter_wrong_slope, plot_hline, plot_vline, x_parameter, crit, crit_value)
    plt.show()




if __name__ == '__main__':
    main()