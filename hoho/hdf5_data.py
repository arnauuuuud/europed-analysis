#!/usr/local/depot/Python-3.7/bin/python
# /usr/local/depot/Python-3.5.1/bin/python

from hoho import startup, information_hdf5
import argparse
import os
import re
import math
from hoho import europed_hampus as europed
import h5py
import gzip
import tempfile
import glob
import io


class CustomError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


research_dir = os.environ['EUROPED_DIR']+'hdf5'



def find_stored_name(europed_name):
    paths = glob.glob(f'{research_dir}/{europed_name}.h5*', recursive=False)
    print('{research_dir}/{europed_name}.h5*')
    too_many_with_name = False
    print(paths)
    if len(paths) == 0:
        raise CustomError(f"No file found '{europed_name}'")
    elif len(paths) == 1:
        stored_name = paths[0]
    elif len(paths) == 2:
        if paths[0].endswith('.h5.gz') and paths[1].endswith('.h5'):
            stored_name = paths[0]
        elif paths[1].endswith('.h5.gz') and paths[0].endswith('.h5'):
            stored_name = paths[1]
        else:
            too_many_with_name = True
    else:
        too_many_with_name = True

    if too_many_with_name:
        raise CustomError(f"Too many files finishing with '{europed_name}'")

    print(stored_name)
    return stored_name

def uncompress_cp_compress(europed_name):
    stored_name = find_stored_name(europed_name)

    if stored_name.endswith('.h5.gz'):
        is_gz_compressed = True
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            with gzip.open(europed_run, 'rb') as gz_file:
                tmp_file.write(gz_file.read())
                tmp_file_name = tmp_file.name





def read(europed_name, list_groups):
    stored_name = find_stored_name(europed_name)

    if stored_name.endswith('.h5.gz'):
        with gzip.open(stored_name, 'rb') as f:
            with io.BytesIO(f.read()) as buf:
                # Open the HDF5 file from the wrapped object
                with h5py.File(buf, 'r') as fil:
                    print(fil)

    else:
        with h5py.File(europed_name, 'r') as hdf5_file:
            print(hdf5_file)
            



def get(europed_name, list_groups):
    
    #is_compressed = uncompress_cp_compress(europed_name)
    result = read(europed_name, list_groups)
    delete_copy(europed_name, is_compressed)

    # return result

    # europed_run = glob.glob(pattern)[0]

    # if europed_run.endswith(".gz"):
    #     with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
    #         with gzip.open(europed_run, 'rb') as gz_file:
    #             tmp_file.write(gz_file.read())
    #             tmp_file_name = tmp_file.name
    #     temp = True
    # else:
    #     tmp_file_name = europed_run
    #     temp = False

    # with h5py.File(tmp_file_name, 'r') as hdf5_file:
    #     temp = hdf5_file
    #     for group in list_groups:
    #         print(group, end='/')
    #         temp = temp[group]
    #     print()
    #     print(temp[0])



    # os.remove(tmp_file_name)



if __name__ == '__main__':
    main()