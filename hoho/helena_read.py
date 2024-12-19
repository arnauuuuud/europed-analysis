import os
import subprocess
from hoho import useful_recurring_functions, europed_hampus as europed
import matplotlib.pyplot as plt
from matplotlib import ticker
from pylib.misc import ReadFile
import h5py
import gzip
import tempfile
import numpy as np
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
import glob
import re
import math
from hoho import useful_recurring_functions, global_functions, find_pedestal_values_old, eliteinp_manip
import scipy.interpolate
import traceback

def read_eliteinp(file_name):
    helena_dir = os.environ['HELENA_DIR']
    output_dir = helena_dir + 'eliteinp/'
    file_path = f'{output_dir}{file_name}'

    try:
        with open(f'{file_path}.eliteinp', 'r') as file:
            lines = file.readlines()
    except FileNotFoundError:
        try:
            eliteinp_manip.decompress_gz(file_name)
            with open(f'{file_path}.eliteinp', 'r') as file:
                lines = file.readlines()        
            eliteinp_manip.remove_notcompressed(file_name)

        except FileNotFoundError:
            print(f'File {file_name} was not found')
            return  

    entities = {}
    current_entity = None 
    data = []
    for line in lines:
        line = line.strip().split(' ')
        if line[0][0].isalpha():  # Check if line is an entity name (e.g., 'Psi', 'Q')
            if current_entity and data:  # Save previous entity's data
                entities[current_entity] = data
                data = []
            current_entity = line[0][:-1]  # Set the current entity
        elif line:  # Process numerical lines
            data += [float(x) for x in line if x != '']
    for key, value in entities.items():
        entities[key] = np.array(value)

    
    return entities

def detect_titles(lines):
    title_should_not_be_there = [' *  HELENA', ' * ITERATION', '    REST =', ' * PRESSURE PROFILE BEFORE NORM.', ' * FINAL ITERATION', ' *          VER', ' * IDEAL AND RESISTIVE MERCIER CRITERION', '  REAL WORLD OUTPUT', ' *        INPUT PROFILES']
    dict_res = {}
    for i in range(len(lines[:-2])):
        if lines[i].startswith(' *****') and lines[i+2].startswith(' *****'):
        # if lines[i+2].startswith(' *****'):
            titles = lines[i+1]
            should_not_be_there = any([titles.startswith(t) for t in title_should_not_be_there])
            if not should_not_be_there:
                dict_res[i+1] = titles
    return dict_res


def detect_empty_line(lines):
    for i,line in enumerate(lines[2:]):
        if len(line.split()) == 0:
            return i+2
        elif line.strip().startswith('*'):
            return i+2

# def get_list(lines):
#     dict_final = {}
#     dict_titles = detect_titles(lines)
#     counts = 0 
#     for i,(line,title) in enumerate(list(dict_titles.items())):
#         list_t = re.sub(',',' ',title).strip().split()
#         dicdic = {}
#         countr = 0
#         dict_final[f'SET{counts}'] = {}
#         for t in list_t:
#             if t != '*':
#                 dict_final[f'SET{counts}'][t] = []
#                 dicdic[countr] = t
#                 countr += 1

#         lines_poupou = lines[line:]
#         line_final = detect_empty_line(lines_poupou)
#         lines_popo = lines_poupou[:line_final]
#         for l in lines_popo[2:]:
#             ll = l.split()
#             for ill, lll in enumerate(ll):
#                 try:
#                     dict_final[f'SET{counts}'][dicdic[ill]].append(float(lll))
#                 except ValueError:
#                     dict_final[f'SET{counts}'][dicdic[ill]].append(lll)
#                 except KeyError:
#                     continue
#         counts += 1

#     return dict_final

def get_list(lines):
    dict_final = {}
    dict_titles = detect_titles(lines)
    counts = 0 
    for i,(line,title) in enumerate(list(dict_titles.items())):
        list_t = re.sub(',',' ',title).strip().split()
        dicdic = {}
        countr = 0
        dict_final[f'LIST {counts}'] = {}
        for t in list_t:
            if t != '*':
                dict_final[f'LIST {counts}'][t] = []
                dicdic[countr] = t
                countr += 1

        lines_poupou = lines[line:]
        line_final = detect_empty_line(lines_poupou)
        lines_popo = lines_poupou[:line_final]
        for l in lines_popo[2:]:
            ll = l.split()
            for ill, lll in enumerate(ll):
                try:
                    dict_final[f'LIST {counts}'][dicdic[ill]].append(float(lll))
                except ValueError:
                    dict_final[f'LIST {counts}'][dicdic[ill]].append(lll)
                except KeyError:
                    continue
        counts += 1

    return dict_final





def read_output(filename):
    helena_dir = os.environ['HELENA_DIR']
    output_dir = helena_dir + 'output/'
    try:
        with open(output_dir+filename, 'r') as f:
            ready_to_read = False
            skip_line = False
            dict_res = get_list(f.readlines())
            for line in f.readlines():
                ll = re.sub(r',|(  )', ' ', line).replace(' = ','=').replace('= ','=').replace(' =','=').strip().split()

                if len(ll) == 0:
                    continue

                elif ll[0].startswith('REST'):
                    continue

                elif line.strip().startswith('* ITERATION') or line.strip().startswith('* FINAL'):
                    continue

                elif ll[0].startswith('$'):
                    current_heading_1 = ll[0][1:]
                    dict_res[current_heading_1] = {}
                    for word in ll[1:]:
                        elems = word.split('=')
                        try:
                            dict_res[current_heading_1][elems[0]] = float(elems[1])
                        except ValueError:
                            dict_res[current_heading_1][elems[0]] = elems[1]
                        except IndexError:
                            continue


                elif '=' in line:
                    for word in ll:
                        elems = word.split('=')
                        try:
                            dict_res[current_heading_1][elems[0]] = float(elems[1])
                        except ValueError:
                            dict_res[current_heading_1][elems[0]] = elems[1]
                        except IndexError:
                            continue

                elif ':' in line:
                    if line.strip().startswith('*  HELENA'):
                        continue
                    ll2 = [a.strip() for a in line.split(':')]

                    try:
                        dict_res[ll2[0]] = float(ll2[1])
                    except ValueError:
                        dict_res[ll2[0]] = ll2[1]
                    except IndexError:
                        continue
    except Exception as e:
        print()
        print()
        print(e)
        traceback.print_exc()
        print()
        print()


    return dict_res