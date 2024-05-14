#!/usr/local/depot/Python-3.7/bin/python
# /usr/local/depot/Python-3.5.1/bin/python

from hoho import useful_recurring_functions, startup, information_hdf5
import os
import h5py
import gzip
import tempfile
import glob


research_dir = os.environ['EUROPED_DIR']+'hdf5'

def find_stored_name(europed_name):
    paths = glob.glob(f'{research_dir}/{europed_name}.h5*', recursive=False)
    print('{research_dir}/{europed_name}.h5*')
    too_many_with_name = False
    print(paths)
    if len(paths) == 0:
        raise useful_recurring_functions.useful_recurring_functions.CustomError(f"No file found '{europed_name}'")
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
        raise useful_recurring_functions.useful_recurring_functions.CustomError(f"Too many files finishing with '{europed_name}'")

    return stored_name

def uncompress_cp_compress(europed_name):
    stored_name = find_stored_name(europed_name)

    if stored_name.endswith('.h5.gz'):
        is_gz_compressed = True
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            with gzip.open(stored_name, 'rb') as gz_file:
                tmp_file.write(gz_file.read())
                tmp_file_name = tmp_file.name
        temp_file = True
    else:
        temp_file = False
        tmp_file_name = stored_name

    return temp_file, tmp_file_name



    if temp:
        os.remove(tmp_file_name)

    return res


def read(tmp_file_name, list_groups):

    with h5py.File(tmp_file_name, 'r') as hdf5_file:
        temp = hdf5_file
        for group in list_groups:
            print(group, end='/')
            temp = temp[group]
        print()

        print(temp)
    
        if isinstance(temp, h5py.Group):
            print(f"Group Name: ")    
            
        if isinstance(temp, h5py.Dataset):
            print(f"Dataset Name: {dataset_name}")
        
            



def get(europed_name, list_groups):
    
    temp_file, tmp_file_name = uncompress_cp_compress(europed_name)
    result = read(tmp_file_name, list_groups)
    if temp_file:
        os.remove(tmp_file_name)

    return result

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