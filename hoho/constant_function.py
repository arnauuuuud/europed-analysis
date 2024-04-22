from ppf import *
import matplotlib.pyplot as plt
import numpy as np
from os.path import exists
import os


markersize = 10
fontsizelabel = 15
fontsizetitle = 18

####################################
# list_shotddaM gives the list of shot number, dda for ELMs, and Meff
list_shotddaM = [[96208, 'T058', 2],
                 [100808, 'T012', 2.02],
                 [99480, 'T003', 2.26],
                 [99490, 'T005', 2.67],
                 [99490, 'T007', 2.59],
                 [99491, 'T003', 2.42],
                 [99491, 'T005', 2.49],
                 [100184, 'T004', 3.02],
                 [100247, 'T003', 3],
                 [100247, 'T004', 2.98]]

list_shotddaT = [
        [100808,'T012',48.1],
        [96208,'T058',51.6],
        [99480,'T003',48.1],
        [99490,'T005',48.3],
        [99490,'T007',50.2],
        [99491,'T003',48.2],
        [99491, 'T005',50.1],
        [100184,'T004',47.5],
        [100247,'T003',47.8],
        [100247,'T004',49.8]
    ]


list_shotddaT2 = [
        [100808,'T012',2.02,48.1,49.3],
        [96208,'T058',2,51.5876,52.8086],
        [99480,'T003',2.26,48.0027,49.3939],
        [99490,'T005',2.67,48.2911,49.7069],
        [99490,'T007',2.59,50.1029,51.3162],
        [99491,'T003',2.42,48.1414,49.4463],
        [99491,'T005',2.49,50.0889,51.8093],
        [100184,'T004',3.02,47.4440,47.8516],
        [100247,'T003',3,47.7768,49.1045],
        [100247,'T004',2.98,49.7488,50.9455]
    ]
    

list_shotddaT2 = [
        [100808,'T012',2.02,48.1,49.3],
        [99490,'T005',2.67,48.2911,49.7069],
        [100247,'T003',3,47.7768,49.1045]
    ]



#list_shotddaT2 = [[99480,'T003',2.26,48.0027,49.3939]]

####################################
def list_drops(phys_quantity, dda_global, dtype_global, shot, dda_elm, lim_1_minus, lim_1_plus, minimal_drop, distance_drop, continuous_drop, lim_2_minus, lim_2_plus, take_mean = False, continuous_drop_0 = 0):
    # get data that we are interested in
    dda = dda_global
    dtype = dtype_global
    uid = 'JETPPF'
    sequence_number = 0
    ppfuid(uid,"r")
    ihdat,iwdat,density,x,time,ier=ppfget(pulse=shot,dda=dda,dtyp=dtype)

    # get information already stored for ELMs
    dtype_elm = 'TELM'
    uid_elm = 'lfrassin'
    sequence_number = 0
    ppfuid(uid_elm,"r")
    ihdat,iwdat,data,x, t_elm, ier=ppfget(pulse=shot,dda=dda_elm,dtyp=dtype_elm, no_x=1)

    try:
        a = density[0]
        b = time[0]
        c = t_elm[0]
    except:
        return None
       

    # filter to keep only the ELMs given in the code already made
    n_time = len(time)
    n_elm = len(t_elm)
    i_start = 1
    while time[i_start] <= t_elm[0]:
        i_start += 1
    i_end = n_time - 1
    while time[i_end] >= t_elm[n_elm-1]:
        i_end -= 1


    list_t_1 = []
    list_d_1 = []

    list_t_2 = []
    list_d_2 = []

    for i in range(i_start-min(lim_1_minus, lim_2_minus),i_end-max(lim_1_plus,lim_2_plus)):
        # bool_1 states if i correspond to a point 1 (beginning of the drop of the ELM)
        bool_1 = density[i]>density[i-1] and density[i]>=np.min(density[i:i+distance_drop]) + minimal_drop
        
        if bool_1:
            for j in range(lim_1_minus, lim_1_plus):
                if bool_1 and (density[i] < density[i+j]):
                    bool_1 = False

            for j in range(continuous_drop):
                if bool_1 and (density[i+j] < density[i+j+1]):
                    bool_1 = False

        if bool_1:
            i1 = i
            densityi1 = density[i1]
        else:
            continue

        # for the value at the top of the ELM, if we want to take the mean of the values before the ELM
        # we need to define a point 0 that gives the beginning of the physical quantity to be at a high value
        if bool_1 and take_mean:
            bool_0 = False
            i0 = i1
            while not bool_0:
                i0 -= 1
                bool_0 = True
                for j in range(continuous_drop_0):
                    bool_0 = bool_0 and (density[i0-j]<density[i0-j+1])
            densityi1 = np.mean(density[i0:i1])
        else:
            pass

        # once we have the beginning of the ELM, we need to find where does it end
        # i2 defines the point where the ELM stops
        if bool_1:
            i2 = i
            bool_2 = False
            lim_min = 2
            while not bool_2:
                i2 += 1
                bool_2 = (density[i2] <= densityi1-minimal_drop)
                for j in range(lim_2_minus, lim_2_plus):
                    if density[i2]>density[i2+j]:
                        bool_2 = False
                 
            list_t_1.append(time[i1])
            list_d_1.append(densityi1)
            list_t_2.append(time[i2])
            list_d_2.append(density[i2])

    t_1 = np.array(list_t_1)
    d_1 = np.array(list_d_1)
    t_2 = np.array(list_t_2)
    d_2 = np.array(list_d_2)

    # for density, divide by 1e19
    if phys_quantity == 'DENSITY':
        d_1 = d_1 * 1e-19
        d_2 = d_2 * 1e-19
        density = density * 1e-19

    if phys_quantity == 'ENERGY':
        d_1 = d_1 * 1e-6
        d_2 = d_2 * 1e-6
        density = density * 1e-6

    return time, density, t_elm, t_1, d_1, t_2, d_2



def list_drops_timediff(phys_quantity, dda_global, dtype_global, shot, dda_elm, lim_1_minus, lim_1_plus, minimal_drop, distance_drop, continuous_drop, lim_2_minus, lim_2_plus, take_mean = False, continuous_drop_0 = 0):
    # get data that we are interested in
    dda = dda_global
    dtype = dtype_global
    uid = 'JETPPF'
    sequence_number = 0
    ppfuid(uid,"r")
    ihdat,iwdat,density,x,time,ier=ppfget(pulse=shot,dda=dda,dtyp=dtype)

    # get information already stored for ELMs
    dtype_elm = 'TELM'
    uid_elm = 'lfrassin'
    sequence_number = 0
    ppfuid(uid_elm,"r")
    ihdat,iwdat,data,x, t_elm, ier=ppfget(pulse=shot,dda=dda_elm,dtyp=dtype_elm, no_x=1)

    time = np.array(time)
    density = np.array(density)

    try:
        a = density[0]
        b = time[0]
        c = t_elm[0]
    except:
        return None
       

    # filter to keep only the ELMs given in the code already made
    n_time = len(time)
    n_elm = len(t_elm)
    i_start = 1
    while time[i_start] <= t_elm[0]:
        i_start += 1
    i_end = n_time - 1
    while time[i_end] >= t_elm[n_elm-1]:
        i_end -= 1


    list_t_1 = []
    list_d_1 = []

    list_t_2 = []
    list_d_2 = []

    for i in range(i_start,i_end):
        # bool_1 states if i correspond to a point 1 (beginning of the drop of the ELM)
        bool_1 = density[i]>density[i-1]
        
        ti = time[i]
        j = i
        bool_drop = False
        idrop = np.argmax(time>ti+distance_drop)
        bool_drop = np.min(density[i:idrop])<=  density[i]-minimal_drop 

        bool_1 = bool_1 and bool_drop

        if bool_1:
            mask = time>time[i]+lim_1_plus
            iplus = np.argmax(mask)
            mask = time>time[i]+lim_1_minus
            iminus = np.argmax(mask)

            bool_1 = density[i]>=np.max(density[iminus:iplus])

            j = i
            while bool_1 and time[j] <= ti + continuous_drop:
                bool_1 = (density[j] > density[j+1])
                j += 1


        if bool_1:
            i1 = i
            densityi1 = density[i1]
        else:
            continue

        # for the value at the top of the ELM, if we want to take the mean of the values before the ELM
        # we need to define a point 0 that gives the beginning of the physical quantity to be at a high value
        if bool_1 and take_mean:
            bool_0 = False
            i0 = i1
            while not bool_0:
                i0 -= 1
                bool_0 = True
                for j in range(continuous_drop_0):
                    bool_0 = bool_0 and (density[i0-j]<density[i0-j+1])
            densityi1 = np.mean(density[i0:i1])
        else:
            pass

        # once we have the beginning of the ELM, we need to find where does it end
        # i2 defines the point where the ELM stops
        if bool_1:
            i2 = i + np.argmin(density[i:np.argmax(time>time[i]+lim_2_plus-lim_2_minus)])
            bool_2 = False
            lim_min = 2
            i2 -= 1
            while not bool_2:
                i2 += 1
                t2 = time[i2]
                bool_2 = (density[i2] <= densityi1-minimal_drop)
                
                iplus = np.argmax(time>t2+lim_2_plus)
                iminus = np.argmax(time>t2+lim_2_minus)

                bool_2 = bool_2 and density[i2]<= np.min(density[iminus:iplus])
                
                
                 
            list_t_1.append(time[i1])
            list_d_1.append(densityi1)
            list_t_2.append(time[i2])
            list_d_2.append(density[i2])


    t_1 = np.array(list_t_1)
    d_1 = np.array(list_d_1)
    t_2 = np.array(list_t_2)
    d_2 = np.array(list_d_2)

    # for density, divide by 1e19
    if phys_quantity == 'DENSITY':
        d_1 = d_1 * 1e-19
        d_2 = d_2 * 1e-19
        density = density * 1e-19

    if phys_quantity == 'ENERGY':
        d_1 = d_1 * 1e-6
        d_2 = d_2 * 1e-6
        density = density * 1e-6

    return time, density, t_elm, t_1, d_1, t_2, d_2


####################################
def std_sum(X,Y):
    A = np.sqrt(np.std(X)**2 + np.std(Y)**2 + 2*np.mean((X-np.mean(X))*(Y-np.mean(Y))))
    return(A)


####################################
def plot_zoom(shot,time,density,t_elm, t_1, t_2, d_1, d_2, xlim, ylabel = "", plot_1 = False, plot_2 = False):
    fig, ax = plt.subplots()
    ax = fig.add_subplot(1, 1, 1)
    ax.margins(0.5)
    ax.set_xlim(xlim)
    ax.plot(time,density)
    data = ax.get_lines()[0].get_xydata()
    data = data[np.logical_and(data[:, 0] >= xlim[0], data[:, 0] <= xlim[1])]
    
    ax.set_ylim(0, np.max(data[:, 1])+(np.max(data[:, 1])-np.min(data[:, 1]))/20)
#    ax.set_ylim(np.min(data[:, 1])-(np.max(data[:, 1])-np.min(data[:, 1]))/20, np.max(data[:, 1])+(np.max(data[:, 1])-np.min(data[:, 1]))/20)
    
    for ti in t_elm:
        plt.axvline(x = ti, color = 'k')
    if plot_1:
        plt.plot(t_1,d_1,'ob')
    if plot_2:
        plt.plot(t_2,d_2,'or')
    plt.xlabel("Time [s]")
    plt.ylabel(ylabel)
    plt.title(" Shot N{}".format(shot))

    plt.show()

####################################
def mean_std_drop(phys_quantity, dda_global, dtype_global, shot, dda_elm, lim_1_minus, lim_1_plus, minimal_drop, distance_drop, continuous_drop, lim_2_minus, lim_2_plus, take_mean = False, continuous_drop_0 = 0):
    res = list_drops_timediff(phys_quantity, dda_global, dtype_global, shot, dda_elm, lim_1_minus, lim_1_plus, minimal_drop, distance_drop, continuous_drop, lim_2_minus, lim_2_plus, take_mean, continuous_drop_0)
    if res == None:
        return None
    else:
        time, density, t_elm, t_1, d_1, t_2, d_2 = res
        mean = np.mean(d_1-d_2)
        std = std_sum(d_1,-d_2)
        return mean, std

####################################
def mean_std_relative_drop(phys_quantity, dda_global, dtype_global, shot, dda_elm, lim_1_minus, lim_1_plus, minimal_drop, distance_drop, continuous_drop, lim_2_minus, lim_2_plus, take_mean = False, continuous_drop_0 = 0):
    res = list_drops_timediff(phys_quantity, dda_global, dtype_global, shot, dda_elm, lim_1_minus, lim_1_plus, minimal_drop, distance_drop, continuous_drop, lim_2_minus, lim_2_plus, take_mean, continuous_drop_0)
    if res == None:
        return None
    else:
        time, density, t_elm, t_1, d_1, t_2, d_2 = res
        mean = np.mean((d_1-d_2)*100/d_1)
        std = std_sum(d_1*100/d_1,-d_2*100/d_1)
        return mean, std

####################################
def mean_std_duration(phys_quantity, dda_global, dtype_global, shot, dda_elm, lim_1_minus, lim_1_plus, minimal_drop, distance_drop, continuous_drop, lim_2_minus, lim_2_plus, take_mean = False, continuous_drop_0 = 0):
    res = list_drops_timediff(phys_quantity, dda_global, dtype_global, shot, dda_elm, lim_1_minus, lim_1_plus, minimal_drop, distance_drop, continuous_drop, lim_2_minus, lim_2_plus, take_mean, continuous_drop_0)
    if res == None:
        return None
    else:
        time, density, t_elm, t_1, d_1, t_2, d_2 = res
        mean = np.mean(t_2-t_1)
        std = std_sum(t_2,-t_1)
        return mean, std

####################################
def mean_std_drop_w_list(phys_quantity, dda_global, dtype_global, shot, dda_elm, lim_1_minus, lim_1_plus, minimal_drop, distance_drop, continuous_drop, lim_2_minus, lim_2_plus, take_mean = False, continuous_drop_0 = 0):
    res = list_drops_timediff(phys_quantity, dda_global, dtype_global, shot, dda_elm, lim_1_minus, lim_1_plus, minimal_drop, distance_drop, continuous_drop, lim_2_minus, lim_2_plus, take_mean, continuous_drop_0)
    if res == None:
        return None
    else:
        time, density, t_elm, t_1, d_1, t_2, d_2 = res
        mean = np.mean(d_1-d_2)
        std = std_sum(d_1,-d_2)
        return mean, std, d_1-d_2

####################################
def mean_std_relative_drop_w_list(phys_quantity, dda_global, dtype_global, shot, dda_elm, lim_1_minus, lim_1_plus, minimal_drop, distance_drop, continuous_drop, lim_2_minus, lim_2_plus, take_mean = False, continuous_drop_0 = 0):
    res = list_drops_timediff(phys_quantity, dda_global, dtype_global, shot, dda_elm, lim_1_minus, lim_1_plus, minimal_drop, distance_drop, continuous_drop, lim_2_minus, lim_2_plus, take_mean, continuous_drop_0)
    if res == None:
        return None
    else:
        time, density, t_elm, t_1, d_1, t_2, d_2 = res
        mean = np.mean((d_1-d_2)*100/d_1)
        std = std_sum(d_1*100/d_1,-d_2*100/d_1)
        return mean, std, (d_1-d_2)*100/d_1

####################################
def mean_std_duration_w_list(phys_quantity, dda_global, dtype_global, shot, dda_elm, lim_1_minus, lim_1_plus, minimal_drop, distance_drop, continuous_drop, lim_2_minus, lim_2_plus, take_mean = False, continuous_drop_0 = 0):
    res = list_drops_timediff(phys_quantity, dda_global, dtype_global, shot, dda_elm, lim_1_minus, lim_1_plus, minimal_drop, distance_drop, continuous_drop, lim_2_minus, lim_2_plus, take_mean, continuous_drop_0)
    if res == None:
        return None
    else:
        time, density, t_elm, t_1, d_1, t_2, d_2 = res
        mean = np.mean(t_2-t_1)
        std = std_sum(t_2,-t_1)
        return mean, std, t_2-t_1


####################################
def plot_mean_drop(phys_quantity, dda_global, dtype_global, lim_1_minus, lim_1_plus, minimal_drop, distance_drop, continuous_drop, lim_2_minus, lim_2_plus, ylabel = "", take_mean = False, continuous_drop_0 = 0):
    fig, ax = plt.subplots()
    list_mass = []
    list_drop = []
    list_error_drop = []
    for shot,dda_elm,Meff in list_shotddaM:
        res = mean_std_drop(phys_quantity, dda_global, dtype_global, shot, dda_elm, lim_1_minus, lim_1_plus, minimal_drop, distance_drop, continuous_drop, lim_2_minus, lim_2_plus, take_mean, continuous_drop_0)
        if res != None:
            mean_drop, std_drop = res
            list_mass.append(Meff)
            list_drop.append(mean_drop)
            list_error_drop.append(std_drop)

    plt.errorbar(x = list_mass, y = list_drop, yerr = list_error_drop, linestyle='', marker = 'D')
    plt.xlim([1.8,3.2])
    plt.xlabel("Effective mass")
    plt.ylabel(ylabel)
    plt.title("Mean ELM "+ phys_quantity.lower() + r" losses in function of $A_{eff}$")

    props = dict(boxstyle='round', facecolor='white', alpha=0.5)
    text = "DDA : " + dda_global 
    text += '\n' + "DTYPE : " + dtype_global 
    text += '\n' + 'Def 1 : [' + str(lim_1_minus) + ',' + str(lim_1_plus) + ']'
    text += '\n' + 'Min drop : ' + str(minimal_drop)
    text += '\n' + 'Continuous drop : ' + str(continuous_drop>0)
    text += '\n' + 'Take mean : ' + str(take_mean)
    ax.text(0.95, 0.95, text, transform=ax.transAxes, fontsize=10,
        verticalalignment='top', horizontalalignment='right', bbox = props)
    plt.show()

####################################
def plot_mean_relative_drop(phys_quantity, dda_global, dtype_global, lim_1_minus, lim_1_plus, minimal_drop, distance_drop, continuous_drop, lim_2_minus, lim_2_plus, ylabel = "", take_mean = False, continuous_drop_0 = 0):
    fig, ax = plt.subplots()
    list_mass = []
    list_drop = []
    list_error_drop = []
    for shot,dda_elm,Meff in list_shotddaM:
        res = mean_std_relative_drop(phys_quantity, dda_global, dtype_global, shot, dda_elm, lim_1_minus, lim_1_plus, minimal_drop, distance_drop, continuous_drop, lim_2_minus, lim_2_plus, take_mean, continuous_drop_0)
        if res != None:
            mean_drop, std_drop = res
            list_mass.append(Meff)
            list_drop.append(mean_drop)
            list_error_drop.append(std_drop)

    plt.errorbar(x = list_mass, y = list_drop, yerr = list_error_drop, linestyle='', marker = 'D')
    plt.xlim([1.8,3.2])
    plt.xlabel("Effective mass")
    plt.ylabel(ylabel)
    plt.title("Mean ELM " + phys_quantity.lower() + r" relative losses in function of $A_{eff}$", fontsize = fontsizetitle)
    
    props = dict(boxstyle='round', facecolor='white', alpha=0.5)
    text = "DDA : " + dda_global 
    text += '\n' + "DTYPE : " + dtype_global 
    text += '\n' + 'Def 1 : [' + str(lim_1_minus) + ',' + str(lim_1_plus) + ']'
    text += '\n' + 'Min drop : ' + str(minimal_drop)
    text += '\n' + 'Continuous drop : ' + str(continuous_drop>0)
    text += '\n' + 'Take mean : ' + str(take_mean)
    ax.text(0.95, 0.95, text, transform=ax.transAxes, fontsize=10,
        verticalalignment='top', horizontalalignment='right', bbox = props)

    plt.show()

####################################
def plot_mean_duration(phys_quantity, dda_global, dtype_global, lim_1_minus, lim_1_plus, minimal_drop, distance_drop, continuous_drop, lim_2_minus, lim_2_plus, take_mean = False, continuous_drop_0 = 0):
    fig, ax = plt.subplots()
    list_mass = []
    list_duration = []
    list_error_duration = []
    for shot,dda_elm,Meff in list_shotddaM:
        print(shot)
        res = mean_std_duration(phys_quantity, dda_global, dtype_global, shot, dda_elm, lim_1_minus, lim_1_plus, minimal_drop, distance_drop, continuous_drop, lim_2_minus, lim_2_plus, take_mean, continuous_drop_0)
        if res != None:
            mean_duration, std_duration = res
            list_mass.append(Meff)
            list_duration.append(mean_duration*1e3)
            list_error_duration.append(std_duration*1e3)

    plt.errorbar(x = list_mass, y = list_duration, yerr = list_error_duration, linestyle='', marker = 'D')
    plt.xlim([1.8,3.2])
    plt.xlabel("Effective mass")
    plt.ylabel("Mean duration of an ELM [ms]")
    plt.title("Mean duration of an ELM in function of Meff - " + phys_quantity)
    
    props = dict(boxstyle='round', facecolor='white', alpha=0.5)
    text = "DDA : " + dda_global 
    text += '\n' + "DTYPE : " + dtype_global 
    text += '\n' + 'Def 1 : [' + str(lim_1_minus) + ',' + str(lim_1_plus) + ']'
    text += '\n' + 'Min drop : ' + str(minimal_drop)
    text += '\n' + 'Continuous drop : ' + str(continuous_drop>0)
    text += '\n' + 'Take mean : ' + str(take_mean)
    ax.text(0.95, 0.95, text, transform=ax.transAxes, fontsize=10,
        verticalalignment='top', horizontalalignment='right', bbox = props)

    plt.show()


####################################
def save_mean_drop(phys_quantity, dda_global, dtype_global, lim_1_minus, lim_1_plus, minimal_drop, distance_drop, continuous_drop, lim_2_minus, lim_2_plus, ylabel = "", take_mean = False, continuous_drop_0 = 0, folder = ""):
    fig, ax = plt.subplots()
    list_mass = []
    list_drop = []
    list_error_drop = []
    for shot,dda_elm,Meff in list_shotddaM:
        print(shot)
        res = mean_std_drop_w_list(phys_quantity, dda_global, dtype_global, shot, dda_elm, lim_1_minus, lim_1_plus, minimal_drop, distance_drop, continuous_drop, lim_2_minus, lim_2_plus, take_mean, continuous_drop_0)
        if res != None:
            mean_drop, std_drop, list_drop_specific = res
            list_mass.append(Meff)
            list_drop.append(mean_drop)
            list_error_drop.append(std_drop)
            
            list_Meff = [Meff] * len(list_drop_specific)

            if Meff <= 2.02:
                color = 'blue'
            elif Meff >= 2.98:
                color = 'magenta'
            else:
                color = 'gold'

            plt.plot(list_Meff, list_drop_specific, linestyle='', marker = 'o', alpha = 0.7, markersize = 2., color = color)
            plt.errorbar(x = Meff, y = mean_drop, yerr = std_drop, linestyle='', marker = 'D', color = color, markersize=markersize)

    #plt.errorbar(x = list_mass, y = list_drop, yerr = list_error_drop, linestyle='', marker = 'D')
    plt.xlim([1.8,3.2])
    plt.ylim(bottom=0)
    plt.xlabel("Effective mass", fontsize = fontsizelabel)
    plt.ylabel(ylabel, fontsize=fontsizelabel)
    plt.title("Mean ELM "+ phys_quantity.lower() + r" losses in function of $A_{eff}$", fontsize=fontsize)

    props = dict(boxstyle='round', facecolor='white', alpha=0.5)
    text = "Method : \'" + folder + "\'"
    ax.text(0.95, 0.95, text, transform=ax.transAxes, fontsize=10,
        verticalalignment='top', horizontalalignment='right', bbox = props)
        
    plt.savefig("../Pictures/" + folder + "/mean_drop.png")
    plt.close()

####################################
def save_mean_relative_drop(phys_quantity, dda_global, dtype_global, lim_1_minus, lim_1_plus, minimal_drop, distance_drop, continuous_drop, lim_2_minus, lim_2_plus, ylabel = "", take_mean = False, continuous_drop_0 = 0, folder = ""):   
    fig, ax = plt.subplots()
    list_mass = []
    list_drop = []
    list_error_drop = []
    for shot,dda_elm,Meff in list_shotddaM:
        print(shot)
        res = mean_std_relative_drop_w_list(phys_quantity, dda_global, dtype_global, shot, dda_elm, lim_1_minus, lim_1_plus, minimal_drop, distance_drop, continuous_drop, lim_2_minus, lim_2_plus, take_mean, continuous_drop_0)
        if res != None:
            mean_drop, std_drop, list_drop_specific = res
            list_mass.append(Meff)
            list_drop.append(mean_drop)
            list_error_drop.append(std_drop)
            
            list_Meff = [Meff] * len(list_drop_specific)

            if Meff <= 2.02:
                color = 'blue'
            elif Meff >= 2.98:
                color = 'magenta'
            else:
                color = 'gold'

            plt.plot(list_Meff, list_drop_specific, linestyle='', marker = 'o', alpha = 0.7, markersize = 2., color = color)
            plt.errorbar(x = Meff, y = mean_drop, yerr = std_drop, linestyle='', marker = 'D', color = color, markersize=markersize)

    # plt.errorbar(x = list_mass, y = list_drop, yerr = list_error_drop, linestyle='', marker = 'D')
    plt.xlim([1.8,3.2])
    plt.ylim(bottom=0)
    plt.xlabel("Effective mass", fontsize = fontsizelabel)
    plt.ylabel(ylabel, fontsize = fontsizelabel)
    plt.title("Mean ELM " + phys_quantity.lower() + r" relative losses in function of $A_{eff}$", fontsize = fontsizetitle)
    
    props = dict(boxstyle='round', facecolor='white', alpha=0.5)
    text = "Method : " + folder
    ax.text(0.95, 0.95, text, transform=ax.transAxes, fontsize=10,
        verticalalignment='top', horizontalalignment='right', bbox = props)

    plt.savefig("../Pictures/" + folder + "/mean_relative_drop.png")
    plt.close()

####################################
def save_mean_duration(phys_quantity, dda_global, dtype_global, lim_1_minus, lim_1_plus, minimal_drop, distance_drop, continuous_drop, lim_2_minus, lim_2_plus, take_mean = False, continuous_drop_0 = 0, folder = ""):
    fig, ax = plt.subplots()
    list_mass = []
    list_duration = []
    list_error_duration = []
    for shot,dda_elm,Meff in list_shotddaM:
        print(shot)
        res = mean_std_duration_w_list(phys_quantity, dda_global, dtype_global, shot, dda_elm, lim_1_minus, lim_1_plus, minimal_drop, distance_drop, continuous_drop, lim_2_minus, lim_2_plus, take_mean, continuous_drop_0)
        if res != None:
            mean_duration, std_duration, list_drop_specific = res
            list_mass.append(Meff)
            list_duration.append(mean_duration)
            list_error_duration.append(std_duration)
            
            list_drop_specific = list_drop_specific*1e3
            list_Meff = [Meff] * len(list_drop_specific)

            if Meff <= 2.02:
                color = 'blue'
            elif Meff >= 2.98:
                color = 'magenta'
            else:
                color = 'gold'
            
            plt.plot(list_Meff, list_drop_specific, linestyle='', marker = 'o', alpha = 0.7, markersize = 2., color = color)
            plt.errorbar(x = Meff, y = mean_duration*1e3, yerr = std_duration*1e3, linestyle='', marker = 'D', color = color, markersize = markersize)


    plt.xlim([1.8,3.2])
    plt.ylim(bottom=0)
    plt.xlabel("Effective mass", fontsize = fontsizelabel)
    plt.ylabel("Mean duration of an ELM [ms]", fontsize = fontsizelabel)
    plt.title("Mean duration of an ELM in function of Meff - " + phys_quantity, fontsize = fontsizetitle)
    
    props = dict(boxstyle='round', facecolor='white', alpha=0.5)
    text = "Method : " + folder
    ax.text(0.95, 0.95, text, transform=ax.transAxes, fontsize=10,
        verticalalignment='top', horizontalalignment='right', bbox = props)

    plt.savefig("../Pictures/" + folder + "/mean_duration.png")
    plt.close()


####################################
def save_zoom(shot,time,density,t_elm, t_1, t_2, d_1, d_2, xlim, ylabel = "", plot_elm = False, plot_1 = False, plot_2 = False, folder = ""):
    fig, ax = plt.subplots()
    ax = fig.add_subplot(1, 1, 1)
    ax.margins(0.5)
    ax.set_xlim(xlim)
    ax.plot(time,density)
    data = ax.get_lines()[0].get_xydata()
    data = data[np.logical_and(data[:, 0] >= xlim[0], data[:, 0] <= xlim[1])]
    
    #ax.set_ylim(0 , np.max(data[:, 1])+(np.max(data[:, 1])-np.min(data[:, 1]))/20)
    ax.set_ylim(np.min(data[:, 1])-(np.max(data[:, 1])-np.min(data[:, 1]))/20, np.max(data[:, 1])+(np.max(data[:, 1])-np.min(data[:, 1]))/20)
    
    if plot_elm:
        for ti in t_elm:
            plt.axvline(x = ti, color = 'k')
    if plot_1:
        plt.plot(t_1,d_1,'ob')
    if plot_2:
        plt.plot(t_2,d_2,'or')
    plt.xlabel("Time [s]", fontsize=fontsizelabel)
    plt.ylabel(ylabel, fontsize=fontsizelabel)
    plt.title(" Shot N{}".format(shot), fontsize=fontsizetitle)
    if not exists("../Pictures/" + folder + "/" + str(shot) + ".png"):
        plt.savefig("../Pictures/" + folder + "/" + str(shot) + ".png")
    else:
        plt.savefig("../Pictures/" + folder + "/" + str(shot) + "(1).png")
    plt.close()


####################################
def save_zoom_with_bar(shot,time,density,t_elm, t_1, t_2, d_1, d_2, xlim, ylabel = "", plot_elm = False, plot_1 = False, plot_2 = False, folder = "", lim_1_minus=0,lim_1_plus=0,lim_2_minus=0,lim_2_plus=0):
    fig, ax = plt.subplots()
    ax = fig.add_subplot(1, 1, 1)
    ax.margins(0.5)
    ax.set_xlim(xlim)
    ax.plot(time,density, color='black')
    data = ax.get_lines()[0].get_xydata()
    data = data[np.logical_and(data[:, 0] >= xlim[0], data[:, 0] <= xlim[1])]
    
    #ax.set_ylim(0 , np.max(data[:, 1])+(np.max(data[:, 1])-np.min(data[:, 1]))/20)
    ax.set_ylim(np.min(data[:, 1])-(np.max(data[:, 1])-np.min(data[:, 1]))/20, np.max(data[:, 1])+(np.max(data[:, 1])-np.min(data[:, 1]))/20)
    
    if plot_elm:
        for ti in t_elm:
            plt.axvline(x = ti, color = 'k')
    if plot_1:
        for k in range(len(t_1)):
            t_1_uno = t_1[k]
            d_1_uno = d_1[k]
            plt.plot([t_1_uno+lim_1_minus, t_1_uno+lim_1_plus],[d_1_uno,d_1_uno], linewidth= 3, color='violet')
        plt.plot(t_1,d_1,'ob')
    if plot_2:
        for k in range(len(t_2)):
            t_2_uno = t_2[k]
            d_2_uno = d_2[k]
            plt.plot([t_2_uno+lim_2_minus, t_2_uno+lim_2_plus],[d_2_uno,d_2_uno], linewidth=3, color='orange') 
        plt.plot(t_2,d_2,'or')
    plt.xlabel("Time [s]", fontsize=fontsizelabel)
    plt.ylabel(ylabel, fontsize=fontsizelabel)
    plt.title(" Shot N{}".format(shot), fontsize=fontsizetitle)
    if not exists("../Pictures/" + folder + "/" + str(shot) + "withbar.png"):
        plt.savefig("../Pictures/" + folder + "/" + str(shot) + "withbar.png")
    else:
        plt.savefig("../Pictures/" + folder + "/" + str(shot) + "withbar(1).png")
    plt.close()


####################################
def save_zoom_specific(shot,time,density,t_elm, t_1, t_2, d_1, d_2, xlim, ylabel = "", plot_elm = False, plot_1 = False, plot_2 = False, folder = "", title = ""):
    fig, ax = plt.subplots()
    ax = fig.add_subplot(1, 1, 1)
    ax.margins(0.5)
    ax.set_xlim(xlim)
    ax.plot(time,density)
    data = ax.get_lines()[0].get_xydata()
    data = data[np.logical_and(data[:, 0] >= xlim[0], data[:, 0] <= xlim[1])]
    
    #ax.set_ylim(0 , np.max(data[:, 1])+(np.max(data[:, 1])-np.min(data[:, 1]))/20)
    ax.set_ylim(np.min(data[:, 1])-(np.max(data[:, 1])-np.min(data[:, 1]))/20, np.max(data[:, 1])+(np.max(data[:, 1])-np.min(data[:, 1]))/20)
    
    if plot_elm:
        for ti in t_elm:
            plt.axvline(x = ti, color = 'k')
    if plot_1:
        plt.plot(t_1,d_1,'ob')
    if plot_2:
        plt.plot(t_2,d_2,'or')
    plt.xlabel("Time [s]")
    plt.ylabel(ylabel)
    plt.title(" Shot N{}".format(shot))
    plt.savefig("../Pictures/" + folder + "/" + title + ".png")
    plt.close()



def save(folder, phys_quantity, dda_global, dtype_global, lim_1_minus, lim_1_plus, minimal_drop,distance_drop,continuous_drop,lim_2_minus,lim_2_plus,take_mean,continuous_drop_0, plot_1, plot_2, plot_elm, ylabel_zoom, ylabel_global_drop, ylabel_global_drop_normalized):
    if not os.path.exists("../Pictures/" + folder):
        os.makedirs("../Pictures/" + folder)
    print('  STEP 1  ')
    for element in list_shotddaT:
        shot = element[0]
        dda_elm = element[1]
        xlim = [element[2],element[2]+0.3]
        print(shot)
        res = list_drops_timediff(phys_quantity, dda_global, dtype_global, shot, dda_elm, lim_1_minus, lim_1_plus, minimal_drop, distance_drop, continuous_drop, lim_2_minus, lim_2_plus, take_mean, continuous_drop_0)
        if res != None:
            time, density, t_elm, t_1, d_1, t_2, d_2 = res
            save_zoom(shot,time,density,t_elm, t_1, t_2, d_1,d_2, xlim, ylabel_zoom,plot_elm, plot_1, plot_2, folder)
            save_zoom_with_bar(shot,time,density,t_elm, t_1, t_2, d_1,d_2, xlim, ylabel_zoom,plot_elm, plot_1, plot_2, folder, lim_1_minus,lim_1_plus,lim_2_minus,lim_2_plus)

    print('  STEP 2  ')
    save_mean_duration(phys_quantity, dda_global, dtype_global, lim_1_minus, lim_1_plus, minimal_drop, distance_drop, continuous_drop, lim_2_minus, lim_2_plus, take_mean, continuous_drop_0, folder=folder)
    print('  STEP 3  ')
    save_mean_relative_drop(phys_quantity, dda_global, dtype_global, lim_1_minus, lim_1_plus, minimal_drop, distance_drop, continuous_drop, lim_2_minus, lim_2_plus, ylabel_global_drop_normalized, take_mean, continuous_drop_0, folder=folder)
    print('  STEP 4  ')
    save_mean_drop(phys_quantity, dda_global, dtype_global, lim_1_minus, lim_1_plus, minimal_drop, distance_drop, continuous_drop, lim_2_minus, lim_2_plus, ylabel_global_drop, take_mean, continuous_drop_0, folder=folder)


def save_all(list_parameters):
    list_color = ['dodgerblue', 'springgreen', 'sandybrown','indigo', 'lightcoral']
    list_marker = ['^', 'o', 'd', 'p', 's']
    fig, ax = plt.subplots()
    index_marker = 0
    patches = []
    labels = []

    list_mass = []
    list_drop = []
    list_error_drop = []


    for element in list_parameters:

        folder, phys_quantity, dda_global, dtype_global, lim_1_minus, lim_1_plus, minimal_drop,distance_drop,continuous_drop,lim_2_minus,lim_2_plus,take_mean,continuous_drop_0, plot_1, plot_2, plot_elm, ylabel_zoom, ylabel_global_drop, ylabel_global_drop_normalized = element

        list_mass_temp = []
        list_drop_temp = []
        list_error_drop_temp = []


        for shot,dda_elm,Meff in list_shotddaM:
            res = mean_std_drop_w_list(phys_quantity, dda_global, dtype_global, shot, dda_elm, lim_1_minus, lim_1_plus, minimal_drop, distance_drop, continuous_drop, lim_2_minus, lim_2_plus, take_mean, continuous_drop_0)
            if res != None:
                mean_drop, std_drop, list_drop_specific = res
                list_mass_temp.append(Meff)
                list_drop_temp.append(mean_drop)
                list_error_drop_temp.append(std_drop)
                                
        # sort the list_mass and reorder the corresponding list_drop and list_error_drop
        sorted_idx = sorted(range(len(list_mass_temp)), key=lambda k: list_mass_temp[k])
        list_mass_temp = [list_mass_temp[i] for i in sorted_idx]
        list_drop_temp = [list_drop_temp[i] for i in sorted_idx]
        list_error_drop_temp = [list_error_drop_temp[i] for i in sorted_idx]
        plt.plot(list_mass_temp, list_drop_temp, marker = list_marker[index_marker], linestyle=':', linewidth=1, markersize = markersize, color = 'black', label=str(index_marker+1))

    

        index_marker += 1
        
        list_mass.append(list_mass_temp)
        list_drop.append(list_drop_temp)
        list_error_drop.append(list_error_drop_temp)

    plt.legend(title = 'Method', loc='best')
    plt.xlim([1.8,3.2])
    plt.ylim(bottom=0)

    index_marker = 0
    for j in range(len(list_parameters)):
        length = len(list_mass[j])
        for i in range(length):
            if list_mass[j][i] <= 2.02:
                color = 'blue'
            elif list_mass[j][i] >= 2.98:
                color = 'magenta'
            else:
                color = 'gold'
            plt.errorbar(x = list_mass[j][i], y = list_drop[j][i], yerr = list_error_drop[j][i], linestyle=':', marker = list_marker[index_marker], markersize = markersize, color = color, mec=color)

        highlight_index = list_mass[j].index(2.49)
        highlight_mass = list_mass[j][highlight_index]
        highlight_drop = list_drop[j][highlight_index]

        plt.plot(highlight_mass, highlight_drop,  marker = list_marker[index_marker], markersize = markersize, color=color, mfc='white', mec='gold')

        index_marker += 1



    #plt.errorbar(x = list_mass, y = list_drop, yerr = list_error_drop, linestyle='', marker = 'D')
    plt.xlabel("Effective mass", fontsize=fontsizelabel)
    plt.ylabel(ylabel_global_drop, fontsize=fontsizelabel)
    plt.title("Mean ELM "+ phys_quantity.lower() + r" losses in function of $A_{eff}$", fontsize=fontsizetitle)

    plt.savefig("../Pictures/" + "mean_drops" + phys_quantity + ".png")
    plt.close()
