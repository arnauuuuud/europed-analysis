import numpy as np
import matplotlib.tri as tri
import matplotlib as mpl
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

def colorFader(c1,c2,eta=0): #fade (linear interpolate) from color c1 (at mix=0) to c2 (mix=1)
    mix=eta/2
    c1=np.array(mpl.colors.to_rgb(c1))
    c2=np.array(mpl.colors.to_rgb(c2))
    return mpl.colors.to_hex((1-mix)*c1 + mix*c2)


color0 = 'orange'
color2 = 'darkred'
colors = [color0,color2]

cmap = plt.cm.inferno_r

# Create a copy of the colormap to modify
new_cmap = cmap(np.linspace(0.2, 0.8, 256))
new_cmap = mcolors.ListedColormap(new_cmap)
color0 = new_cmap(0)
color1 = new_cmap(128)
color15 = new_cmap(192)
color2 = new_cmap(255)

colorlowgas = 'blue'
colormedgas = 'green'
colorhighgas = 'magenta'

colorHPLG = colorlowgas

linestyle_n50 = '-'
linestyle_n20 = ':'

color_eta0 = 'orange'
color_eta1 = 'purple'

color_n20 = 'darkred'
linestyle_n20 = 'dashdot'
color_n50 = 'coral'

linestyle_t01 = '-'
linestyle_t003 = '--'

# cmap = LinearSegmentedColormap.from_list("orange_darkred", colors)


colors = [mpl.colors.to_hex(color0),mpl.colors.to_hex(color1),mpl.colors.to_hex(color15),mpl.colors.to_hex(color2)]
linestyles = ['solid','dashed','dashed','dotted']

plt.rcParams['xtick.labelsize'] = 10
plt.rcParams['ytick.labelsize'] = 10
plt.rcParams['axes.labelsize'] = 15


# custom_rc_path = '/home/jwp9427/work/python/poster/matplotlibrc'
# mpl.rc_file(custom_rc_path)