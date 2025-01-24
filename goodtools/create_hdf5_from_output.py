#!/usr/local/depot/Python-3.7/bin/python
# /usr/local/depot/Python-3.5.1/bin/python
import argparse
from hoho import useful_recurring_functions, europed_hampus, h5_manipulation
import h5py
import os

def argument_parser():
    """Defining comandline parser and returning the arguments"""
    parser = argparse.ArgumentParser(description = "Merge two results of runs together")
    parser.add_argument("name", help = "name of the old run")
    args = parser.parse_args()
    return args.name

#####################################################################
def create_hdf5(europed_name):

    foldername = f"{os.environ['EUROPED_DIR']}hdf5"
    os.chdir(foldername)

    europed_data = europed_hampus.EuropedData(europed_name)
    nrows = europed_data.nrows
    gamma_alfven = europed_data.gammamax['alfven']
    gamma_diamag = europed_data.gammamax['diamag']
    nepars = europed_data.nepars
    tepars = europed_data.tepars
    betaped = europed_data.betaped
    alpha = europed_data.alpha
    betap = europed_data.betap
    betan = europed_data.betan
    delta = europed_data.delta

    hdf5_name = f'{europed_name}_fromoutput'
    hdf5_name_h5 = f'{europed_name}_fromoutput.h5'
    with h5py.File(hdf5_name_h5, 'w') as hdf:
        grp_scan = hdf.create_group("scan")
        for i in range(nrows):
            grp_i = grp_scan.create_group(str(i))
            grp_i.create_dataset("alpha_helena_max", data=[alpha[i]])
            grp_i.create_dataset("betan", data=[betan[i]])
            grp_i.create_dataset("betap", data=[betap[i]])
            grp_i.create_dataset("betaped", data=[betaped[i]])
            grp_i.create_dataset("delta", data=[delta[i]])
            grp_i.create_dataset("ne_parameters", data=nepars[i])
            grp_i.create_dataset("te_parameters", data=tepars[i])
            grp_castor = grp_i.create_group("castor")
            grp_n = grp_castor.create_group('50')
            grp_n.create_dataset("gamma", data=[gamma_alfven[i]])
            grp_n.create_dataset("gamma_diam", data=[gamma_diamag[i]])
            grp_n.create_dataset("n", data='50')
    h5_manipulation.compress_to_gz(hdf5_name)



if __name__ == '__main__':
    name = argument_parser()
    create_hdf5(name)