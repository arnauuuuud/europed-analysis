#!/usr/local/depot/Python-3.7/bin/python
# /usr/local/depot/Python-3.5.1/bin/python

import sys
import numpy as np
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import (
    QApplication, QWidget, QRadioButton, QVBoxLayout, QHBoxLayout,
    QLabel, QCheckBox, QLineEdit, QPushButton, QButtonGroup
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar
from hoho import europed_analysis, global_functions, startup
import argparse
import matplotlib.pyplot as plt
import matplotlib.transforms as transforms
import math
import re
import matplotlib.gridspec as gridspec
import numpy as np

markers = ['.', 'o', 'v', '^', '<', '>', '1', '2', '3', '4', 's', 'p', '*', 'h', 'H', '+', 'x', 'D', 'd']
colors = ['blue', 'green', 'red', 'cyan', 'magenta', 'yellow', 'orange', 'purple', 'brown', 'pink', 'gray', 'olive', 'lime', 'teal', 'navy', 'sky blue', 'lavender', 'peach', 'maroon', 'turquoise', 'gold', 'silver', 'indigo', 'violet', 'burgundy', 'mustard', 'ruby', 'emerald', 'sapphire', 'amethyst']



def run(europed_names, x_parameter, crit, crit_value, envelope, list_consid_mode, hline, vline, legend):

    # Clear the existing plot
    plot_ax.clear()

    euroname_1 = europed_names[0].split(',')
    euroname_2 = europed_names[1].split(',')
    euroname_3 = europed_names[2].split(',')
    euroname_4 = europed_names[3].split(',')

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
            
            list_mode_to_plot = [mode for mode in list_consid_mode if mode in modes]


            if not envelope:
                for i, mode in enumerate(list_mode_to_plot):
                    temp_x = x_param
                    temp_y = tab[:,i]
                    nan_indices = np.isnan(temp_y)
                    x_filtered = temp_x[~nan_indices]
                    y_filtered = temp_y[~nan_indices]
                    plot_ax.plot(x_filtered,y_filtered, color=global_functions.dict_mode_color[int(mode)], marker=markers[iplot], label=f'{europed_run} - {mode}')
            
            else:
                x_envelope, y_envelope = europed_analysis.give_envelop(tab, x_param)
                plot_ax.plot(x_envelope, y_envelope, color=colors[iplot], label=europed_run)


            if vline:
                has_unstable, x_crit, col, critn = europed_analysis.find_critical(x_param, tab, list_mode_to_plot, crit_value)
                if has_unstable:
                    if not envelope:
                        colorvline = 'r'
                    else:
                        colorvline = colors[iplot] 

                    plot_ax.axvline(x_crit, color=colorvline, linestyle=':')
                    xmin,xmax,ymin,ymax = plot_ax.axis()
                    ratio = (x_crit-xmin)/(xmax-xmin)
                    trans = transforms.blended_transform_factory(plot_ax.transData, plot_ax.transAxes)
                    x_crit_order = math.floor(math.log10(x_crit))
                    x_crit_round = np.around(np.around(x_crit*10**-x_crit_order,1)*10**x_crit_order,6)
                    plot_ax.text(x_crit, 1.0, str(x_crit_round), color=colorvline, horizontalalignment='center', verticalalignment='bottom',transform=trans)


        except RuntimeError:
            print(f"{europed_run:>40} RUNTIME ERROR : NO FIT FOUND")
        except FileNotFoundError:
            print(f"{europed_run:>40} FILE DOES NOT EXIST")


        if hline:
            plot_ax.axhline(crit_value, linestyle="--",color="k")

    x_label, y_label = global_functions.get_plot_labels_gamma_profiles(x_parameter, crit)
    plot_ax.set_xlabel(x_label)
    plot_ax.set_ylabel(y_label)
    if crit != 'omega':
        plot_ax.set_ylim(bottom=0)
    plot_ax.set_xlim(left=0)

    if legend:
        plot_ax.legend()

    plot_canvas.draw()
    plt.ion()

def checkAll(self):
    for checkbox in checkboxes_n:
        checkbox.setChecked(True)

def uncheckAll(self):
    for checkbox in checkboxes_n:
        checkbox.setChecked(False)


def on_button_click():
    # Get the selected radio button text
    if radio_button_alpha.isChecked():
        x_parameter = "alpha_helena_max"
    elif radio_button_teped.isChecked():
        x_parameter = "teped"
    elif radio_button_delta.isChecked():
        x_parameter = "delta"
    elif radio_button_ptot.isChecked():
        x_parameter = "pped"
    else:
        print("No x parameter is selected, alpha is used")
        x_parameter = "alpha_helena_max"

    # Get the selected radio button text
    if radio_button_diamag.isChecked():
        crit = "diamag"
        crit_value_edit.setText('0.25')
    elif radio_button_alfven.isChecked():
        crit_value_edit.setText('0.03')
        crit = "alfven"    
    elif radio_button_omega.isChecked():
        crit = "omega"


    list_consid_mode = []
    for checkbox in checkboxes_n:
        if checkbox.isChecked():
            list_consid_mode.append(int(checkbox.text()))


    hline = checkbox_hline.isChecked()
    vline = checkbox_vline.isChecked()
    envelope = checkbox_envelope.isChecked()
    legend = checkbox_legend.isChecked()
    crit_value = float(crit_value_edit.text())

    text_values = []
    for line_edit in line_edits:
        text_values.append(line_edit.text())

    # Update the plot with new data
    run(text_values, x_parameter, crit, crit_value, envelope, list_consid_mode, hline, vline, legend)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Create the main window
    main_window = QWidget()
    main_window.setWindowTitle('Growth rates plotting')


    # Create radio buttons for x-axis parameters
    group_xaxis = QButtonGroup()
    x_axis_label = QLabel("X-axis parameter")
    radio_button_alpha = QRadioButton('alpha')
    radio_button_teped = QRadioButton('teped')
    radio_button_delta = QRadioButton('width')
    radio_button_ptot = QRadioButton('pped')
    group_xaxis.addButton(radio_button_alpha)
    group_xaxis.addButton(radio_button_teped)
    group_xaxis.addButton(radio_button_delta)
    group_xaxis.addButton(radio_button_ptot)
    radio_button_alpha.setChecked(True)

    # Create radio buttons for criteria
    group_crit = QButtonGroup()
    criterion_label = QLabel("Criterion")
    radio_button_diamag = QRadioButton("Diamagnetic")
    radio_button_alfven = QRadioButton("Alfvén")
    radio_button_omega = QRadioButton("Omega")
    group_crit.addButton(radio_button_diamag)
    group_crit.addButton(radio_button_alfven)
    group_crit.addButton(radio_button_omega)
    radio_button_diamag.setChecked(True)

    # Create checkboxes for 'n' values
    check_all_button = QPushButton("All")
    none_button = QPushButton("None")
    check_all_button.clicked.connect(checkAll)
    none_button.clicked.connect(uncheckAll)
    n_label = QLabel("n")
    checkboxes_n = [QCheckBox(str(n_value)) for n_value in [1, 2, 3, 4, 5, 7, 10, 20, 30, 40, 50]]
    for checkbox in checkboxes_n:
        checkbox.setChecked(True)

    # Create line edit widgets
    line_edits = [QLineEdit() for _ in range(4)]

    # Create widgets for the rest of the parameters
    crit_value_edit = QLineEdit()
    crit_value_edit.setText('0.25')
    checkbox_hline = QCheckBox("H line")
    checkbox_vline = QCheckBox("V line")
    checkbox_envelope = QCheckBox("Envelope")
    checkbox_legend = QCheckBox("Legend")
    checkbox_legend.setChecked(True)

    # Create a button
    plot_button = QPushButton('Plot')
    plot_button.clicked.connect(on_button_click)

    # Create a Matplotlib plot
    fig, plot_ax = plt.subplots()
    plot_canvas = FigureCanvas(fig)
    toolbar = NavigationToolbar(plot_canvas,plot_canvas)

    # Layouts
    xparam_layout = QVBoxLayout()
    xparam_layout.addWidget(x_axis_label)
    xparam_layout.addWidget(radio_button_alpha)
    xparam_layout.addWidget(radio_button_delta)
    xparam_layout.addWidget(radio_button_teped)
    xparam_layout.addWidget(radio_button_ptot)

    crit_layout = QVBoxLayout()
    crit_layout.addWidget(criterion_label)
    crit_layout.addWidget(radio_button_diamag)
    crit_layout.addWidget(radio_button_alfven)
    crit_layout.addWidget(radio_button_omega)
    crit_layout.addWidget(crit_value_edit)

    n_layout = QVBoxLayout()
    n_layout.addWidget(n_label)
    n_layout.addStretch()
    n_layout.addWidget(check_all_button)
    n_layout.addWidget(none_button)
    for checkbox in checkboxes_n:
        n_layout.addWidget(checkbox)

    text_layout = QVBoxLayout()
    for line_edit in line_edits:
        text_layout.addWidget(line_edit)

    rest_layout = QVBoxLayout()
    rest_layout.addWidget(checkbox_hline)
    rest_layout.addWidget(checkbox_vline)
    rest_layout.addWidget(checkbox_envelope)
    rest_layout.addWidget(checkbox_legend)

    button_layout = QVBoxLayout()
    button_layout.addWidget(plot_button)

    column_layout = QVBoxLayout()
    column_layout.addLayout(xparam_layout)
    column_layout.addLayout(crit_layout)
    column_layout.addLayout(rest_layout)

    line_layout = QHBoxLayout()
    line_layout.addLayout(column_layout)
    line_layout.addLayout(n_layout)

    right_layout = QVBoxLayout()
    right_layout.addLayout(text_layout)
    right_layout.addLayout(line_layout)
    right_layout.addLayout(button_layout)

    left_layout = QVBoxLayout()
    left_layout.addWidget(toolbar)
    left_layout.addWidget(plot_canvas)

    main_layout = QHBoxLayout()
    main_layout.addLayout(left_layout,2)
    main_layout.addLayout(right_layout,1)

    main_window.setLayout(main_layout)
    main_window.show()
    sys.exit(app.exec_())


