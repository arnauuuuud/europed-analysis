#!/usr/local/depot/Python-3.7/bin/python
# /usr/local/depot/Python-3.5.1/bin/python

from hoho import useful_recurring_functions, europed_analysis, global_functions, startup, find_pedestal_values_old, h5_manipulation, spitzer
from poster import plot_canvas
from mpl_toolkits.axes_grid1 import Divider, Size
import sys
import numpy as np
import matplotlib.pyplot as plt
# from hoho import  #europed_analysis#, startup, global_functions
import matplotlib.transforms as transforms
import math
import numpy as np
from matplotlib.patches import FancyArrowPatch
import matplotlib as mpl
from matplotlib.colors import ListedColormap, BoundaryNorm, Normalize
import matplotlib.colors as mcolors


markers = [ 'D', 's', 'p', '*', 'h', 'H', '+', 'x', 'd', 'o', 'v', '^', '<', '>', '1', '2', '3', '4']
colors = ['blue', 'green', 'red', 'cyan', 'magenta', 'yellow', 'orange', 'purple', 'brown', 'pink', 'gray', 'olive', 'lime', 'teal', 'navy', 'sky blue', 'lavender', 'peach', 'maroon', 'turquoise', 'gold', 'silver', 'indigo', 'violet', 'burgundy', 'mustard', 'ruby', 'emerald', 'sapphire', 'amethyst']


europed_names = [f'sb_eta{eta}_rs0.022_neped2.57' for eta in [1.0]]
x_parameter = 'alpha_helena_max'
crit = 'alfven'
crit_value = 0.05
envelope = True
list_consid_mode = [1,2,3,4,5,7,10,20]
hline = True
vline = False
legend = False

cm = 1/2.54

# fig, axs = plt.subplots(1,2,figsize=(13.7*cm,13.4*cm), gridspec_kw={'width_ratios': [10, 1]})
fig = plt.figure(figsize=(13*cm,14*cm),dpi=300)

# Define fixed size for the axes in inches
horiz = [Size.Fixed(2.5*cm),Size.Fixed(9.5*cm),Size.Fixed(0.2*cm),Size.Fixed(0.7*cm)]
vert = [Size.Fixed(1.6*cm),Size.Fixed(11*cm)]

divider = Divider(fig, (0, 0, 1, 1), horiz, vert, aspect=True, anchor=(0,0))

ax = fig.add_axes(divider.get_position(), axes_locator=divider.new_locator(nx=1, ny=1))
ax2 = fig.add_axes(divider.get_position(), axes_locator=divider.new_locator(nx=3, ny=1))


# # Print new settings
# print("After adjustment:")
# print(f"  left: {fig.subplotpars.left}")
# print(f"  right: {fig.subplotpars.right}")
# print(f"  top: {fig.subplotpars.top}")
# print(f"  bottom: {fig.subplotpars.bottom}")

# # Adjust the layout
# # fig.subplots_adjust(top=0.9,left=0.2,right=0.99,bottom=0.2,hspace=0.02)

# # Print new settings
# print("After adjustment:")
# print(f"  left: {fig.subplotpars.left}")
# print(f"  right: {fig.subplotpars.right}")
# print(f"  top: {fig.subplotpars.top}")
# print(f"  bottom: {fig.subplotpars.bottom}")



# ax = axs[0]


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


sample_points = np.linspace(0.3, 1, len(europed_names))
colors = plt.cm.inferno_r(sample_points)

for iplot,europed_run in enumerate(europed_names):
    try:
        res = europed_analysis.get_x_parameter(europed_run, x_parameter)
        if type(res) == str and res == 'File not found':
            continue
        else:
            x_param = res
        gammas, modes = europed_analysis.get_gammas(europed_run, crit)
        try:
            tab, consid_mode = europed_analysis.filter_tab_general(gammas, modes, list_consid_mode,[])
        except TypeError as e:
            print(e)
            continue        
        sorted_indices = np.argsort(x_param)
        x_param = x_param[sorted_indices]
        tab = tab[sorted_indices]
        
        list_mode_to_plot = [mode for mode in list_consid_mode if mode in modes]



        for i, mode in enumerate(list_mode_to_plot):
            temp_x = x_param
            temp_y = tab[:,i]
            nan_indices = np.isnan(temp_y)
            x_filtered = temp_x[~nan_indices]
            y_filtered = temp_y[~nan_indices]
            ax.plot(x_filtered,y_filtered, color=global_functions.dict_mode_newnew_color[int(mode)], marker=markers[iplot], label=f'{europed_run} - {mode}')
    

        x_envelope, y_envelope = europed_analysis.give_envelop(tab, x_param)
        ax.plot(x_envelope, y_envelope,  color=plt.cm.inferno_r(0.5), label=europed_run, linestyle='-', linewidth=4)#, alpha=0.8)


        has_unstable, x_crit, col, critn = europed_analysis.find_critical(x_param, tab, list_mode_to_plot, crit_value)
        colorvline = colors[iplot]
        if has_unstable and vline:
            if not envelope:
                colorvline = 'r'
            else:
                colorvline = colors[iplot] 

            ax.axvline(x_crit, color=colorvline, linestyle=':')
        xmin,xmax,ymin,ymax = ax.axis()
        ratio = (x_crit-xmin)/(xmax-xmin)
        trans = transforms.blended_transform_factory(ax.transData, ax.transAxes)
        x_crit = np.abs(x_crit)
        x_crit_order = math.floor(math.log10(x_crit))
        x_crit_round = np.around(np.around(x_crit*10**-x_crit_order,1)*10**x_crit_order,6)
        # ax.text(x_crit, 1.0, str(x_crit_round), color=colorvline, horizontalalignment='center', verticalalignment='bottom',transform=trans)
        # if europed_run != 'sb_eta2.0_rs0.022_neped2.57':
        #     ax.scatter(x_crit, 1.03, color=colorvline,transform=trans,zorder=20,marker='x', clip_on=False)
    except RuntimeError:
        print(f"{europed_run:>40} RUNTIME ERROR : NO FIT FOUND")
    except FileNotFoundError:
        print(f"{europed_run:>40} FILE DOES NOT EXIST")
    except IndexError as e:
        print(e)
        continue

ax.text(0.01,1.01,r'$\eta=\eta_{\mathrm{Sp}}$', transform=ax.transAxes, ha='left', va='bottom', fontsize=30, fontweight='bold',  color=plt.cm.inferno_r(0.5))
ax.text(4.8,0.145,r'$\mathrm{max}(\gamma/\omega_A)$', color=plt.cm.inferno_r(0.5), transform=ax.transData, ha='left', va='bottom')
ax.scatter(x_crit, 0.95, color='black',transform=trans,zorder=20,marker='x',s=100)
ax.axvline(x_crit, color='red', linestyle='-',ymin=crit_value/0.16)

has_unstable, x_crit_min, col, critn = europed_analysis.find_critical(x_param, tab, list_mode_to_plot, 0.85*crit_value)
has_unstable, x_crit_max, col, critn = europed_analysis.find_critical(x_param, tab, list_mode_to_plot, 1.15*crit_value)

# ax.spines['top'].set_position(('outward', 10))

ax.axvline(x_crit_min, color='red', linestyle=':',ymin=0.85*crit_value/0.16)
ax.axvline(x_crit_max, color='red', linestyle=':',ymin=1.15*crit_value/0.16)    
ax.axvspan(x_crit_min, x_crit_max, color='red', ymin=1.15*crit_value/0.16, alpha=0.2)
p2 = FancyArrowPatch((x_crit_min, 0.95*0.16), (x_crit_max, 0.95*0.16), arrowstyle='|-|', mutation_scale=2, shrinkA=0, shrinkB=0)
ax.add_patch(p2)

if hline:
    ax.axhline(crit_value, linestyle="--",color="black")
    ax.axhspan(0.85*crit_value, 1.15*crit_value, color="black", alpha=0.1)

p3 = FancyArrowPatch((0.5, 0.85*crit_value), (0.5, 1.15*crit_value), arrowstyle='|-|', mutation_scale=5, shrinkA=0, shrinkB=0, color='black')
ax.add_patch(p3)

ax.text(2, crit_value, r'$\pm 15 \%$', color='black', ha='left', va='bottom', fontsize=10)

x_label, y_label = global_functions.get_plot_labels_gamma_profiles(x_parameter, crit)

y_label = r'$\gamma/\omega_A$'
ax.set_xlabel(x_label, fontsize=20)
ax.set_ylabel(y_label, fontsize=20)
# # if crit != 'omega':
# #     ax.set_ylim(bottom=0)
# # ax.set_xlim(left=0)

# if legend:
#     ax.legend()



ax.set_xlim(left=1.8, right=6.7)
ax.set_ylim(bottom=0, top=0.16)


# ax2 = axs[1]

dict_mode_color=global_functions.dict_mode_newnew_color

colors = list(dict_mode_color.values())
cmap = ListedColormap(colors)

# Create a colorbar with specified colors
bounds = list(dict_mode_color.keys()) + [max(dict_mode_color.keys()) + 1]
norm = BoundaryNorm(bounds, cmap.N)
cm = plt.cm.ScalarMappable(norm=norm, cmap=cmap)
cm.set_array([])
cb = plt.colorbar(cm, cax=ax2, orientation='vertical')
ticks_positions = [(i + j) / 2 for i, j in zip(bounds[:-1], bounds[1:])]
cb.set_ticks(ticks_positions)
cb.set_ticklabels(list(dict_mode_color.keys()))
cb.set_ticks([])
cb.set_ticklabels([])
ax2.text(0.5, 1.01, r'$n$', ha='center', va='bottom', fontsize=20)   
ax2.text(0.5, 0.05, r'1', ha='center', va='center', fontsize=15, fontweight='bold')   
ax2.text(0.5, 0.175, r'2', ha='center', va='center', fontsize=15, fontweight='bold')   
ax2.text(0.5, 0.3, r'3', ha='center', va='center', fontsize=15, fontweight='bold')   
ax2.text(0.5, 0.425, r'4', ha='center', va='center', fontsize=15, fontweight='bold')   
ax2.text(0.5, 0.55, r'5', ha='center', va='center', fontsize=15, fontweight='bold')   
ax2.text(0.5, 0.55, r'5', ha='center', va='center', fontsize=15, fontweight='bold')   
ax2.text(0.5, 0.675, r'7', ha='center', va='center', fontsize=15, fontweight='bold')   
ax2.text(0.5, 0.8, r'10', ha='center', va='center', fontsize=15, fontweight='bold')   
ax2.text(0.5, 0.925, r'20', ha='center', va='center', fontsize=15, fontweight='bold')   

ax2.tick_params(axis='both', which='both', length=0)
ax2.yaxis.set_ticks_position('left')

# Adjust the layout
# fig.subplots_adjust(top=0.9,left=0.2,right=0.99,bottom=0.2,hspace=0.02)

# Adjust the subplot parameters
# fig.subplots_adjust(left=0.2, right=0.8, top=0.8, bottom=0.2)


plt.savefig('/home/jwp9427/cococo/3a')
plt.close()

