import numpy as np

def distance(tab, element1, element2):
    idx1 = np.where(tab==element1)
    idx2 = np.where(tab==element2)
    i1 = idx1[0][0]
    j1 = idx1[1][0]
    i2 = idx2[0][0]
    j2 = idx2[1][0]
    
    distance = ((i1-i2)**2 + (j1-j2)**2)**0.5
    if i1 == i2 and i1 == len(tab):
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
            z1, z2, z3 = z_values[0], z_values[1],z_values[2]
            d12 = distance(tab_array, z1, z2)<= 3 # sqrt(2)
            d13 = distance(tab_array, z1, z3)<= 3 # sqrt(2)
            d23 = distance(tab_array, z2, z3)<= 3 # sqrt(2)

            idx1 = np.where(tab_array == z1)
            idx2 = np.where(tab_array == z2)
            idx3 = np.where(tab_array == z3)

            if idx1[0][0] == idx2[0][0] and idx2[0][0] == idx3[0][0] and (idx1[0][0] == 0 or idx1[0][0] == len(tab_array)-1):
                continue

            if d12 and d13 and d23:
                filtered_triangles.append(triangle)
        except IndexError:
            pass
    filtered_triangles = np.array(filtered_triangles)
    return filtered_triangles