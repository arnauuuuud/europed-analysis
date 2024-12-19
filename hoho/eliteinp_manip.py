import os, gzip, re, shutil
from hoho import useful_recurring_functions
import h5py




def remove_notcompressed(filename):
    foldername = f"{os.environ['HELENA_DIR']}eliteinp"
    os.chdir(foldername)
    os.remove(f'{filename}.eliteinp')

def decompress_gz(filename):
    foldername = f"{os.environ['HELENA_DIR']}eliteinp"
    os.chdir(foldername)
    with gzip.open(f'{filename}.eliteinp.gz', 'rb') as f_in, open(f'{filename}.eliteinp', 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)

def compress_to_gz(filename):
    foldername = f"{os.environ['HELENA_DIR']}eliteinp"
    os.chdir(foldername)
    with open(f'{filename}.eliteinp', 'rb') as f_in, gzip.open(f'{filename}.eliteinp', 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)
    removedoth5(filename)
