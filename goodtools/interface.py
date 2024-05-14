#!/usr/local/depot/Python-3.7/bin/python
# /usr/local/depot/Python-3.5.1/bin/python

import sys
import numpy as np
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QRadioButton, QCheckBox
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

def on_button_click():
    # Get the selected radio button text
    if radio_button1.isChecked():
        option = "Option 1"
    elif radio_button2.isChecked():
        option = "Option 2"
    elif radio_button3.isChecked():
        option = "Option 3"
    else:
        option = "No option selected"


    if checkbox1.isChecked():
        print("1 is checked")
    if checkbox2.isChecked():
        print("2 is checked")
    if checkbox3.isChecked():
        print("3 is checked")

    # Get the text from the line edit
    text = euroname.text()

    # Print selected option and entered text
    print("Button clicked! Selected option:", option, 'Text:', text)

    # Update the plot with new data
    update_plot(option)

def update_plot(option):
    # Generate some random data based on the selected option
    x = []
    y = []
    if option == "Option 1":
        x = np.random.rand(100)
        y = np.random.rand(100)
    elif option == "Option 2":
        x = np.random.rand(100)
        y = np.random.rand(100)
    elif option == "Option 3":
        x = np.random.rand(100)
        y = np.random.rand(100)

    # Clear the existing plot
    ax.clear()

    # Plot the new data
    ax.scatter(x, y)
    ax.set_title('Scatter Plot for ' + option)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    canvas.draw()

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Create the main window
    window = QWidget()
    window.setWindowTitle('Simple PyQt Example')

    # Create radio buttons for x-axis
    xaxis_label = QLabel("X-axis parameter")
    radio_button_alpha = QRadioButton(r'$\alpha$')
    radio_button_teped = QRadioButton(r'$T_e^{\mathrm{ped}}$')
    radio_button_delta = QRadioButton(r'$\Delta$')
    radio_button_ptot = QRadioButton(r'$p_{tot}^{\mathrm{ped}}$')

    # Create radio buttons for criterion
    crit_label = QLabel("Criterion")
    radio_button_diamag = QRadioButton("Diamagnetic")
    radio_button_alfven = QRadioButton("Alfvén")

    # Create checkboxes
    n_label = QLabel("n")
    checkbox_n1 = QCheckBox("1")
    checkbox_n2 = QCheckBox("2")
    checkbox_n3 = QCheckBox("3")
    checkbox_n4 = QCheckBox("4")
    checkbox_n5 = QCheckBox("5")
    checkbox_n7 = QCheckBox("7")
    checkbox_n10 = QCheckBox("10")
    checkbox_n20 = QCheckBox("20")
    checkbox_n30 = QCheckBox("30")
    checkbox_n40 = QCheckBox("40")
    checkbox_n50 = QCheckBox("50")

    # Create a line edit (textbox)
    euroname1 = QLineEdit()
    euroname2 = QLineEdit()
    euroname3 = QLineEdit()
    euroname4 = QLineEdit()

    # Create rest widgets
    crit_value = QLineEdit()
    checkbox_hline = QCheckBox("H line")
    checkbox_vline = QCheckBox("V line")
    checkbox_envelope = QCheckBox("envelope")

    # Create a button
    run_button = QPushButton('Plot')
    run_button.clicked.connect(on_button_click)

    # Create a Matplotlib plot
    fig, ax = plt.subplots()
    canvas = FigureCanvas(fig)


    # Create a layout for the line edit and button
    text_layout = QVBoxLayout()
    text_layout.addWidget(euroname1)
    text_layout.addWidget(euroname2)
    text_layout.addWidget(euroname3)
    text_layout.addWidget(euroname4)

    # Create a layout for the checkboxes
    radio_xparam_layout = QVBoxLayout()
    radio_xparam_layout.addWidget(xaxis_label)
    radio_xparam_layout.addWidget(radio_button_alpha)
    radio_xparam_layout.addWidget(radio_button_delta)
    radio_xparam_layout.addWidget(radio_button_teped)
    radio_xparam_layout.addWidget(radio_button_ptot)

    # Create a layout for the checkboxes
    radio_crit_layout = QVBoxLayout()
    radio_crit_layout.addWidget(crit_label)
    radio_crit_layout.addWidget(radio_button_diamag)
    radio_crit_layout.addWidget(radio_button_alfven)

    # Create a layout for the rest of the parameters
    rest_layout = QVBoxLayout()
    rest_layout.addWidget(crit_value)
    rest_layout.addWidget(checkbox_hline)
    rest_layout.addWidget(checkbox_vline)
    rest_layout.addWidget(checkbox_envelope)

    # Create a layout for all the RadioButtons
    radio_layout = QVBoxLayout()
    radio_layout.addLayout(radio_xparam_layout)
    radio_layout.addLayout(radio_crit_layout)
    radio_layout.addLayout(rest_layout)


    # Create a layout for the checkboxes
    checkbox_n_layout = QVBoxLayout()
    checkbox_n_layout.addWidget(n_label)
    checkbox_n_layout.addWidget(checkbox_n1)
    checkbox_n_layout.addWidget(checkbox_n2)
    checkbox_n_layout.addWidget(checkbox_n3)
    checkbox_n_layout.addWidget(checkbox_n4)
    checkbox_n_layout.addWidget(checkbox_n5)
    checkbox_n_layout.addWidget(checkbox_n7)
    checkbox_n_layout.addWidget(checkbox_n10)
    checkbox_n_layout.addWidget(checkbox_n20)
    checkbox_n_layout.addWidget(checkbox_n30)
    checkbox_n_layout.addWidget(checkbox_n40)
    checkbox_n_layout.addWidget(checkbox_n50)




    # Create line layout
    line_layout = QHBoxLayout()
    line_layout.addLayout(radio_layout)
    line_layout.addLayout(checkbox_n_layout)
    #line_layout.addLayout(rest_layout)



    horizontal_layout = QHBoxLayout()


    # Create a vertical layout to arrange the line edit/button layout, the radio buttons, and the checkboxes
    right_layout = QVBoxLayout()
    right_layout.addLayout(text_layout)
    right_layout.addLayout(line_layout)
    right_layout.addWidget(run_button)

    # Create a horizontal layout to arrange the Matplotlib plot and the right layout
    main_layout = QHBoxLayout()
    main_layout.addWidget(canvas)
    main_layout.addLayout(right_layout)

    # Set the main layout for the window
    window.setLayout(main_layout)

    # Show the window
    window.show()

    # Start the event loop
    sys.exit(app.exec_())
