#!/usr/local/depot/Python-3.7/bin/python3
from hoho import find_pedestal_values_old
import numpy as np

europed_names1 = [f'sb_eta{eta}_rs0.022_neped2.57' for eta in [0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0,1.5,2.0]]
europed_names2 = [f'sb_eta{eta}_rs{rs}_neped2.57' for eta in [0.0,1.0,2.0] for rs in [-0.01,0.0,0.01,0.02,0.022,0.03]]
europed_names3 = [f'sb_eta{eta}_rs0.022_neped{neped}' for eta in [0.0,1.0,2.0] for neped in [1.07,1.57,2.07,2.57,3.07,3.57,4.07]]
europed_names4 = [f'sb_eta{eta}_rs0.022_neped2.57_betap{betap}' for eta in [0.0,1.0,2.0] for betap in [0.55,0.7,0.85,1.0,1.15,1.3]]


europed = europed_names1+europed_names2+europed_names3+europed_names4

res = [find_pedestal_values_old.critical_pedestal_position(eu) for eu in europed]

print(min(res))
print(max(res))
print(np.mean(res))

