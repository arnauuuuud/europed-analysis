#!/usr/local/depot/Python-3.7/bin/python
# /usr/local/depot/Python-3.5.1/bin/python
import argparse
from hoho import useful_recurring_functions, global_functions, experimental_values
from goodtools import setinput, add_to_waitinglist

dict_shot_dda = global_functions.dict_shot_dda
list_shotno = dict_shot_dda.keys()

# list_shotno = [84794]

for shot in list(list_shotno)[::3]:

    dda = dict_shot_dda[shot]

    nesepneped, nesepneped_error = experimental_values.get_nesepneped(shot, dda)
    neped, neped_error = experimental_values.get_neped(shot, dda)
    betan, betan_error = experimental_values.get_betan(shot, dda)


    for eta in [0,1]:
        round_betan = round(float(betan), 2)
        round_neped = round(float(neped), 2)
        round_frac = round(nesepneped, 2)
        runname = f'global_v3_{shot}_eta{eta}_betan{round_betan}_neped{round_neped}_nesepneped{round_frac}'

        dict_setinput = {
            'run_name':runname,
            'betan':betan,
            'neped':neped,
            'nesepneped_value':nesepneped,
            'eta':eta,
            'n':'10,20,50'
        }

        setinput.main('global_v3', **dict_setinput)
        add_to_waitinglist.main([runname])



