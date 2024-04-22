from hoho import startup
import argparse
import matplotlib.pyplot as plt
import matplotlib.transforms as transforms
import math
import numpy as np
import matplotlib.tri as tri
import os






def extract_psi_and_j(filename):
    foldername = f"{os.environ['HELENA_DIR']}output"
    os.chdir(foldername)

    psi_values = []
    j_values = []

    ready1 = False
    ready2 = False

    s = False

    with open(filename, 'r') as file:
        lines = file.readlines()
        for line in lines:

            if 'PSI' in line and '<J>' in line:
                ready1 = True
                pass

            if 'S' in line and 'AVERAGE JPHI' in line:
                ready1 = True
                s = True
                pass

            if ready1 and '*****' in line:
                ready2 = True
                ready1 = False
                pass
            
            elif ready2 and '*****' in line:
                ready2 = False
                break

            elif ready2 and '*****' not in line and not s:
                elements = line.split()
                psi = float(elements[1])
                j = float(elements[3])
                psi_values.append(psi)
                j_values.append(j)

            elif ready2 and '*****' not in line and s:
                elements = line.split()
                if len(elements)>=2:
                    psi = float(elements[0])**2
                    j = float(elements[1])
                    psi_values.append(psi)
                    j_values.append(j)

    return psi_values,j_values

