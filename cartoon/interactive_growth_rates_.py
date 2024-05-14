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

markers = ['.', 'o', 'v', '^', '<', '>', '1', '2', '3', '4', 's', 'p', '*', 'h', 'H', '+', 'x', 'D', 'd']
colors = ['blue', 'green', 'red', 'cyan', 'magenta', 'yellow', 'orange', 'purple', 'brown', 'pink', 'gray', 'olive', 'lime', 'teal', 'navy', 'sky blue', 'lavender', 'peach', 'maroon', 'turquoise', 'gold', 'silver', 'indigo', 'violet', 'burgundy', 'mustard', 'ruby', 'emerald', 'sapphire', 'amethyst']


radiobutton_crit = None


def main():
    plt.ion()
    
    consid_mode = {'1':True,'2':True, '3':True, '4':True, '5':True, '7':True, '10':True, '20':True, '30':True, '40':True, '50':True}
    list_consid_mode = [['1','2','3','4','5','7','10','20','30','40','50']]
    euroname_1 = [['sb_eta']]
    euroname_2 = [['0.0','0.1','0.2','0.3','0.5','0.6','1.0']]
    euroname_3 = [['_rs0.022_neped2.57']]
    euroname_4 = [['']]
    check_envelope = [False]
    crit_value = [0.25]
    filter_wrong_slope = True



    crit = ['diamag']
    hline = [False]
    vline = [False]
    x_parameter = ['alpha_helena_max']

    fig = plt.figure(figsize=(30, 20))
    gs = gridspec.GridSpec(9, 3, width_ratios=[10, 1, 1], hspace=0, wspace=0)

    # Create subplots using the grid specification
    ax_plot = plt.subplot(gs[:,0])
    
    # First text box: MAIN NAME EUROPED: modify euroname_bas1 (mandatory)
    ax_textbox_1 = plt.subplot(gs[0,1]) 
    eurobox_1 = TextBox(ax_textbox_1, '', initial='sb_eta')
    eurobox_1.on_submit(lambda val: update_euroname_1(euroname_1,val))

    # Second text box: NAME EUROPED: modify euroname_var1 (optional)
    ax_textbox_2 = plt.subplot(gs[0,2]) 
    eurobox_2 = TextBox(ax_textbox_2, '', initial='0.0,0.1,0.2,0.3,0.5,0.6,1.0')
    eurobox_2.on_submit(lambda val: update_euroname_2(euroname_2,val))

    # Third text box: NAME EUROPED: modify euroname_bas2 (optional)
    ax_textbox_3 = plt.subplot(gs[1,1]) 
    eurobox_3 = TextBox(ax_textbox_3, '', initial='_rs0.022_neped2.57')
    eurobox_3.on_submit(lambda val: update_euroname_3(euroname_3,val))

    # Fourth text box: NAME EUROPED: modify euroname_var2 (optional)
    ax_textbox_4 = plt.subplot(gs[1,2]) 
    eurobox_4 = TextBox(ax_textbox_4, '', initial='') 
    eurobox_4.on_submit(lambda val: update_euroname_4(euroname_4,val))

    # Fifth box: Radiobuttons for x-axis parameter
    ax_x_parameter = plt.subplot(gs[2:4,1], aspect='equal')
    ax_x_parameter.set_frame_on(False)
    radio_button1 = RadioButtons(ax_x_parameter, [r'$\alpha$',r'$T_e^{\mathrm{ped}}$',r'$\Delta$',r'$p_{tot}^{\mathrm{ped}}$'])
    radio_button1.on_clicked(lambda label: change_xaxis(x_parameter,label))
    
    # Sixth box: Envelope
    ax_checkbox_envelope = plt.subplot(gs[7,1], aspect='equal')
    ax_checkbox_envelope.set_frame_on(False)
    checkbox_envelope = CheckButtons(ax_checkbox_envelope, ['Envelope'], [False])
    checkbox_envelope.on_clicked(lambda label: change_envelope(check_envelope,label))

    # Sixth box: Envelope
    ax_checkbox_plotlines = plt.subplot(gs[6:8,2], aspect='equal')
    ax_checkbox_plotlines.set_frame_on(True)
    checkbox_plotlines = CheckButtons(ax_checkbox_plotlines, ['Plot H-line','Plot V-line'], [False,False])
    checkbox_plotlines.on_clicked(lambda label: change_plotlines(hline,vline,label))

    # Seventh box: crit_value
    ax_textbox_crit_value = plt.subplot(gs[6,1])
    textbox_crit_value = TextBox(ax_textbox_crit_value, '', initial='0.25')
    textbox_crit_value.on_submit(lambda val: update_crit_value(crit_value, val))

    # Eigth box: crit
    ax_radiobutton_crit = plt.subplot(gs[4:6,1], aspect='equal')
    ax_radiobutton_crit.set_frame_on(False)
    radiobutton_crit = RadioButtons(ax_radiobutton_crit, ['alfven', 'diamag'], active=1)
    radiobutton_crit.on_clicked(lambda label: change_crit(crit,label))
   
    # Ninth box: checkboxes for modes considered
    checkbox_states_mode = list(consid_mode.values())


    ax_checkbox_modes = plt.subplot(gs[2:6,2])

    ax_checkbox_mode1 = plt.subplot(gs[2,2], aspect='equal')
    checkboxes_mode1 = CheckButtons(ax_checkbox_mode1, list(consid_mode.keys())[:3], checkbox_states_mode[:3])
    checkboxes_mode1.on_clicked(lambda label: add_element_mode(consid_mode,list_consid_mode,label))

    ax_checkbox_mode2 = plt.subplot(gs[3,2], aspect='equal')
    checkboxes_mode2 = CheckButtons(ax_checkbox_mode2, list(consid_mode.keys())[3:6], checkbox_states_mode[3:6])
    checkboxes_mode2.on_clicked(lambda label: add_element_mode(consid_mode,list_consid_mode,label))

    ax_checkbox_mode3 = plt.subplot(gs[4,2], aspect='equal')
    checkboxes_mode3 = CheckButtons(ax_checkbox_mode3, list(consid_mode.keys())[6:9], checkbox_states_mode[6:9])
    checkboxes_mode3.on_clicked(lambda label: add_element_mode(consid_mode,list_consid_mode,label))

    ax_checkbox_mode4 = plt.subplot(gs[5,2], aspect='equal')
    checkboxes_mode4 = CheckButtons(ax_checkbox_mode4, list(consid_mode.keys())[9:], checkbox_states_mode[9:])
    checkboxes_mode4.on_clicked(lambda label: add_element_mode(consid_mode,list_consid_mode,label))

    # Tenth box: Run button
    ax_run_button = plt.subplot(gs[8, 1:])
    run_button = Button(ax_run_button, 'Run')
    run_button.on_clicked(lambda event: run_on_click(ax_plot,euroname_1,euroname_2,euroname_3,euroname_4,x_parameter,crit,crit_value,check_envelope,list_consid_mode,hline,vline))
    plt.ioff()
    plt.show()

def update_euroname_1(euroname_1,val):
    euroname_1[0] = val.split(',')

def update_euroname_2(euroname_2,val):
    euroname_2[0] = val.split(',')

def update_euroname_3(euroname_3,val):
    euroname_3[0] = val.split(',')

def update_euroname_4(euroname_4,val):
    euroname_4[0] = val.split(',')

def change_envelope(check_envelope,label):
    check_envelope[0] = not check_envelope[0]

def change_xaxis(x_parameter,label):
    if label == r'$\alpha$':
        x_parameter[0] = 'alpha_helena_max'
    elif label == r'$T_e^{\mathrm{ped}}$':
        x_parameter[0] = 'teped'  
    elif label == r'$\Delta$':
        x_parameter[0] = 'delta' 
    elif label == r'$p_{tot}^{\mathrm{ped}}$':
        x_parameter[0] = 'pped'


def update_crit_value(crit_value,val):
    crit_value[0] = float(val)


def change_plotlines(hline,vline,label):
    if label == 'Plot H-line':
        hline[0] = not hline[0]
    elif label == 'Plot V-line':
        vline[0] = not vline[0]

def change_crit(crit,label):
    crit[0] = label

def add_element_mode(consid_mode,list_consid_mode,label):
    consid_mode[label] = not consid_mode[label]
    list_consid_mode[0] = [key for key in list(consid_mode.keys()) if consid_mode[key]]

def run_on_click(ax_plot,euroname_1,euroname_2,euroname_3,euroname_4,x_parameter,crit,crit_value,check_envelope,list_consid_mode,hline,vline):
    run(ax_plot, euroname_1[0], euroname_2[0], euroname_3[0], euroname_4[0], x_parameter[0], crit[0], crit_value[0], check_envelope[0], list_consid_mode[0], hline[0], vline[0])



def run(ax, euroname_1, euroname_2, euroname_3, euroname_4, x_parameter, crit, crit_value, envelope, list_consid_mode, hline, vline):

    ax.clear()

    euroname_2 = [''] if euroname_2 == [] else euroname_2
    euroname_3 = [''] if euroname_3 == [] else euroname_3
    euroname_4 = [''] if euroname_4 == [] else euroname_4
    europed_names = [e1+e2+e3+e4 for e1 in euroname_1 for e2 in euroname_2 for e3 in euroname_3 for e4 in euroname_4]

    print('')
    print('')
    print('############### Updated parameters ###############')
    print(f'# List of runs:        {europed_names}')
    print(f'# X-axis parameter:    {x_parameter}')
    print(f'# Critical value:      {crit_value}')
    print(f'# Stability criterion: {crit}')
    print(f'# Plot envelope:       {envelope}')
    print(f'# Modes:               {list_consid_mode}')
    print(f'# Plot H-line:         {hline}')
    print(f'# Plot V-line:         {vline}')
    print('##################################################')
    print('')


    for iplot,europed_run in enumerate(europed_names):
        try:
            res = europed_analysis.get_x_parameter(europed_run, x_parameter)
            if type(res) == str and res == 'File not found':
                continue
            else:
                x_param = res
            gammas, modes = europed_analysis.get_gammas(europed_run, crit)
            tab, consid_mode = europed_analysis.filter_tab_general(gammas, modes, list_consid_mode,[])

            sorted_indices = np.argsort(x_param)
            x_param = x_param[sorted_indices]
            tab = tab[sorted_indices]
            

            if not envelope:
                for i, mode in enumerate(list_consid_mode):
                    temp_x = x_param
                    temp_y = tab[:,i]
                    nan_indices = np.isnan(temp_y)
                    x_filtered = temp_x[~nan_indices]
                    y_filtered = temp_y[~nan_indices]
                    ax.plot(x_filtered,y_filtered, color=global_functions.dict_mode_color[int(mode)], marker=markers[iplot], label=f'{europed_run} - {mode}')
            
            else:
                x_envelope, y_envelope = europed_analysis.give_envelop(tab, x_param)
                ax.plot(x_envelope, y_envelope, color=colors[iplot], label=europed_run)


            if vline:
                has_unstable, x_crit, col, critn = europed_analysis.find_critical(x_param, tab, list_consid_mode, crit_value)
                if has_unstable:
                    if not envelope:
                        colorvline = 'r'
                    else:
                        colorvline = colors[iplot] 

                    ax.axvline(x_crit, color=colorvline, linestyle=':')
                    xmin,xmax,ymin,ymax = ax.axis()
                    ratio = (x_crit-xmin)/(xmax-xmin)
                    trans = transforms.blended_transform_factory(ax.transData, ax.transAxes)
                    x_crit_order = math.floor(math.log10(x_crit))
                    x_crit_round = np.around(np.around(x_crit*10**-x_crit_order,1)*10**x_crit_order,6)
                    ax.text(x_crit, 1.0, str(x_crit_round), color=colorvline, horizontalalignment='center', verticalalignment='bottom',transform=trans)


        except RuntimeError:
            print(f"{europed_run:>40} RUNTIME ERROR : NO FIT FOUND")
        except FileNotFoundError:
            print(f"{europed_run:>40} FILE DOES NOT EXIST")


        if hline:
            ax.axhline(crit_value, linestyle="--",color="k")

    x_label, y_label = global_functions.get_plot_labels_gamma_profiles(x_parameter, crit)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_ylim(bottom=0)
    ax.set_xlim(left=0)

    ax.legend()
    plt.draw()


    






if __name__ == '__main__':
    main()