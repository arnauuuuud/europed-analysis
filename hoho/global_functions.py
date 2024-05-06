### global_functions.py sets the plotting routine for the project, it fixes the names of the axis, the different colors, some key input and how the subplots are made

from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable
import matplotlib.pyplot as plt
from matplotlib.colors import to_hex

ne_color = '#db7a58'
te_color = '#6198d2'

def get_plot_labels_gamma_profiles(x_parameter, crit):
    """translates the parameters to plot labels"""
    ylabels = {
        'alfven' : r'$\gamma/\omega_A$',
        'diamag' :  r'$\gamma/\omega^*$',
        'omega': r'$\omega$'
    }
    xlabels = {
        'delta' : r'$w_{[\psi_N]}$',
        'teped' : r'${T_e^{\mathrm{ped}}}_{[\mathrm{keV}]}$',
        'alpha_helena_max' : r'$\alpha_{\mathrm{max}}$',
        'peped' : r'${p_e^{\mathrm{ped}}}_{[\mathrm{kPa}]}$',
        'pped' : r'${p_{tot}^{\mathrm{ped}}}_{[\mathrm{kPa}]}$',
        'neped' : r'${n_e^{\mathrm{ped}}_{[10^{19} \mathrm{m}^{-3}]}$'
    }
    return xlabels[x_parameter], ylabels[crit]

def get_critical_plot_label(y_param):
    ylabels = {
        'alpha_helena_max' : r'critical $\alpha_{\mathrm{max}}$',
        'teped' : r'critical ${T_e^{\mathrm{ped}}}_{[\mathrm{keV}]}$',
        'delta' : r'critical $w_{[\psi_N]}$',
        'pped' : r'critical ${p_{tot}^{\mathrm{ped}}}_{[\mathrm{kPa}]}$',
        'neped' : r'critical ${n_e^{\mathrm{ped}}}_{[10^{19} \mathrm{m}^{-3}]}$',
        'peped' : r'critical ${p_e^{\mathrm{ped}}}_{[\mathrm{kPa}]}$',
    }
    return ylabels[y_param]

def get_critical_profiles_label(y_param):
    ylabels = {
        'te' : r'critical ${T_e}$ $_{[\mathrm{keV}]}$',
        'ne' : r'critical ${n_e}$ $_{[10^{19} \mathrm{m}^{-3}]}$',
        'pe' : r'critical ${p_e}$ $_{[\mathrm{kPa}]}$',
        'p' : r'critical ${p_{tot}}$ $_{[\mathrm{kPa}]}$',
    }
    return ylabels[y_param]

def get_profiles_label(y_param):
    ylabels = {
        'te' : r'${T_e}$ $_{[\mathrm{keV}]}$',
        'ne' : r'${n_e}$ $_{[10^{19}e\cdot \mathrm{m}^{-3}]}$',
        'pe' : r'${p_e}$ $_{[\mathrm{kPa}]}$',
        'p'  : r'${p_{tot}}$ $_{[\mathrm{kPa}]}$',
        'alpha' : r'$\alpha$',
        'q':'q',
        'shear':'shear',
        'ballooning_stability':'ballooning stability',
    }
    return ylabels[y_param]

dict_mode_color = {
    1: 'b',   # blue
    2: 'g',   # green
    3: 'r',   # red
    4: 'c',   # cyan
    5: 'm',   # magenta
    7: 'y',   # yellow
    10: 'k',  # black
    15: 'orange',
    20: '#FFA07A',  # light salmon
    30: '#8A2BE2',  # blue violet
    40: '#32CD32',  # lime green
    50: 'orange',  # gold
    60: '#FF4500',  # orange red
    70: '#00CED1',  # dark turquoise
    80: '#FFD700',  # gold
    90: '#800080',  # purple
    100: '#6B8E23'  # olive drab
}

keys = [1,2,3,4,5,7,10,20,30,40,50]
num_colors = len(keys)
# Create equally spaced colors from the gnuplot colormap
cmap = plt.get_cmap('rainbow_r')
colors = [to_hex(cmap(i / (num_colors - 1))) for i in range(num_colors)]
# Update the dictionary with equally spaced colors
dict_mode_new_color = dict(zip(keys, colors))

# list_modes = [1, 2, 3, 4, 5, 7, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
# cmap = plt.get_cmap('summer_r')
# norm = Normalize(vmin=0, vmax=len(list_modes)-1)
# colors_mode = [cmap(norm(i)) for i in range(len(list_modes))]
# dict_mode_color = dict(zip(list_modes, colors_mode))


allneped_prefixes = ['m2_neped' + str(neped) + '_density_shift' for neped in [1.93,2.57,2.89,3.21,3.86,5.14,7.71]] 
allneped_labels = ["1.93","2.57","2.89","3.21","3.86","5.14","7.71"]

shiftedneped_prefixes = ['m7_neped' + str(neped) + '_density_shift' for neped in [1.93,2.57,2.89,3.21,3.86,5.14]] 
shiftedneped_labels = ["1.93","2.57","2.89","3.21","3.86","5.14","7.71"]

alleta_prefixes_m3v3 = [f'm3_v3_eta{str(eta)}_density_shift' for eta in [0,0.25,0.5,1, 1.5, 2]]
alleta_prefixes_f1 = [f'f1_eta{str(eta)}_density_shift' for eta in [0,0.25,0.5,1, 1.5, 2]]
alleta_prefixes_diff = [f'f1_eta{str(eta)}_density_shift' for eta in [0,0.25,0.5,1, 1.5, 2]]+[f'diff_eta{eta}_density_shift' for eta in ['0.0000','0.2500','0.5000','1.0000', '1.5000', '2.0000']]
someeta_prefixes = [f'f2_eta{str(eta)}_density_shift' for eta in [0, 1, 2]]

alleta_labels = ['0.00','0.25','0.50','1.00','1.50','2.00'] 
someeta_labels = ['0.00','1.00','2.00'] 

bees_prefixes = [f'bee_eta{eta}_density_shift' for eta in ['0.0000','0.2500','0.5000','1.0000', '1.5000', '2.0000']]
bees_labels = ['0.00','0.25','0.50','1.00','1.50','2.00']
bee_shifts = ['-0.0100','0.0000','0.0100','0.0200']


full_list = ['-0.0100','-0.0087','-0.0075','-0.0050','-0.0037','-0.0025','0.0000','0.0050','0.0100','0.0133','0.0150','0.0166','0.0200','0.0250','0.0300','0.0350','0.0400']
lilypad = ['0.0000','0.0050','0.0100','0.0150','0.0200','0.0220','0.0300','0.0350']
coquelicot = ['-0.0100','-0.0050','0.0000','0.0050','0.0100','0.0200','0.0300']
list_eta = ['-0.0100','0.0000','0.0100','0.0200','0.0300']


keys = ["1.93", "2.57", "2.89", "3.21", "3.86", "5.14", "7.71"]
colors = ['C' + str(i+1) for i in range(len(keys))]
dict_neped_color = dict(zip(keys, colors))


keys = ["0.00","0.25","0.50","0.75","1.00","1.25","1.50","1.75","2.00","5.67"]
colors = ['C' + str(i) for i in range(len(keys))]
dict_eta_color = dict(zip(keys, colors))



subplots_dict = {
    1:(1,1),
    2:(1,2),
    3:(1,3),
    4:(2,2),
    5:(2,3),
    6:(2,3),
    7:(2,4),
    8:(2,4),
    9:(3,3),
    10:(4,3),
    11:(4,3),
    12:(4,3),
    15:(5,3),
}



dict_input_prefixes = {
    "allneped":(allneped_prefixes, allneped_labels, 'neped'),
    "shiftedneped": (shiftedneped_prefixes, shiftedneped_labels, 'neped'),
    "alleta_m3v3": (alleta_prefixes_m3v3, alleta_labels,' eta'),
    "alleta_f1": (alleta_prefixes_f1, alleta_labels, 'eta'),
    "alleta_diff": (alleta_prefixes_diff, alleta_labels+alleta_labels, 'eta'),
    "someeta": (someeta_prefixes, someeta_labels, 'eta'),
    "bees": (bees_prefixes, bees_labels, 'eta')
}

dict_input_variations = {
    "full_list": full_list,
    "lilypad": lilypad,
    "coquelicot": coquelicot,
    "list_eta": list_eta,
    "bee_shifts": bee_shifts
}

def get_axis_subplot(nplot, axs, iplot):
    if nplot == 1:
        ax = axs
    elif nplot in [2,3]:
        ax = axs[iplot]
    elif nplot==4:
        ax=axs[iplot//2,iplot%2]
    elif nplot in [5,6,9,10,11,12,15]:
        ax=axs[iplot//3,iplot%3]
    elif nplot in [7,8]:
        ax=axs[iplot//4,iplot%4]
    return ax



    
