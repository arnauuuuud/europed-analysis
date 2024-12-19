from hoho import europed_analysis_2, h5_manipulation, pedestal_values
import numpy as np
import matplotlib.tri as tri
import os

def distance(tab, element1, element2):
    idx1 = np.where(tab==element1)
    idx2 = np.where(tab==element2)
    i1 = idx1[0][0]
    j1 = idx1[1][0]
    i2 = idx2[0][0]
    j2 = idx2[1][0]
    
    distance = ((i1-i2)**2 + (j1-j2)**2)**0.5
    if i1 == i2 and i1 == len(tab)-1:
        distance = np.abs(j1-j2)
    else:
        distance = 0

    return distance



def filter_triangle(z, tab, triangles):
    tab_array = np.zeros((len(tab),max([len(line) for line in tab])))
    for i, line in enumerate(tab):
        tab_array[i,:len(line)] = line

    filtered_triangles = []
    for triangle in triangles:
        try:
            z_values = z[triangle]
            z1, z2, z3 = z_values[0], z_values[1], z_values[2]
            d12 = distance(tab_array, z1, z2)<= 5 # sqrt(2)
            d13 = distance(tab_array, z1, z3)<= 5 # sqrt(2)
            d23 = distance(tab_array, z2, z3)<= 5 # sqrt(2)

            idx1 = np.where(tab_array == z1)
            idx2 = np.where(tab_array == z2)
            idx3 = np.where(tab_array == z3)


            if idx1[0][0] == idx2[0][0] and idx2[0][0] == idx3[0][0] and (idx1[0][0] == 0 or idx1[0][0] == len(tab_array)-1):
                continue

            elif d12 and d13 and d23:
                filtered_triangles.append(triangle)
        except IndexError:
            pass
    filtered_triangles = np.array(filtered_triangles)
    return filtered_triangles

def create_lists(europed_names, xaxis, yaxis, crit, consid_mode_input, exclud_mode, q_ped_def):
    z = []
    x = []
    list_n = []
    y = []
    tab = []
    for europed_name in europed_names:
        tab.append([])
        bool_first = True
        dict_gamma = europed_analysis_2.get_filtered_dict(europed_name, crit, consid_modes=consid_mode_input, exclud_modes=exclud_mode)
        for delta in dict_gamma.keys():
            dict_gamma_profile = dict_gamma[delta]
            try:
                (n,gamma) = max(list(dict_gamma_profile.items()), key=lambda x: x[1])

                list_n.append(n)
                z.append(gamma)

                profile = h5_manipulation.find_profile_with_delta(europed_name, delta)

                for (isx,par) in zip([True, False], [xaxis, yaxis]):
                    if par in ['peped','teped','neped']:
                        value = pedestal_values.pedestal_value_all_definition(par, europed_name, profile=profile, q_ped_def=q_ped_def)
                    elif par == 'frac':
                        value = pedestal_values.nesep_neped(europed_name, profile=profile, q_ped_def=q_ped_def)
                    elif par == 'betan':
                        value = float(h5_manipulation.get_data(europed_name,['scan',str(profile),'betan']))
                    elif par == 'betap':
                        value = float(h5_manipulation.get_data(europed_name,['scan',str(profile),'betap']))
                    elif par == 'alpha':
                        value = float(h5_manipulation.get_data(europed_name,['scan',str(profile),'alpha_helena_max']))


                    if isx:
                        xvalue = value
                    else:
                        yvalue = value

                x.append(xvalue)
                y.append(yvalue)
                
                if not np.isnan(xvalue) and not np.isnan(yvalue) and not np.isnan(gamma):
                    tab[-1].append((xvalue+1)*gamma+yvalue)
    
            except ValueError:
                pass
    x, y, z, tab, list_n = filter_(x, y, z, tab, list_n)
    return x, y, z, tab, list_n


def filter_(x, y, z, tab, list_n):
    x = np.array(x)
    y = np.array(y)
    z = np.array(z)
    valid_indices = ~np.isnan(x) & ~np.isnan(y) & ~np.isnan(z)
    x = np.array(x)[valid_indices]
    y = np.array(y)[valid_indices]
    z = np.array(z)[valid_indices]
    list_n = np.array(list_n)[valid_indices]

    return x, y, z, tab, list_n


def give_triangles_to_plot(europed_names, xpar, ypar, crit, consid_mode_input, exclud_mode, q_ped_def):
    x, y, z, tab, list_n = create_lists(europed_names, xpar, ypar, crit, consid_mode_input, exclud_mode, q_ped_def)

    triang = tri.Triangulation(x,y)
    triangles_to_keep = filter_triangle((x+1)*z+y, tab, triang.triangles)
    triang_good = tri.Triangulation(x,y, triangles=triangles_to_keep)

    return x, y, z, list_n, triang_good