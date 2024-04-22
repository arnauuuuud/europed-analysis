import os
import re
import math
from hoho import europed_hampus as europed
import h5py
import gzip
import tempfile
import glob


foldername = f"{os.environ['EUROPED_DIR']}hdf5"
os.chdir(foldername)

file_path = "model1_densityshift_0.004.h5.gz"

def get_structure(europed_run):

    pattern = os.path.join(europed_run + '.h5*')
    europed_run = glob.glob(pattern)[0]

    if europed_run.endswith(".gz"):
        print("File has a '.gz' extension")
        # Create a temporary file to decompress the .h5.gz file
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            with gzip.open(europed_run, 'rb') as gz_file:
                tmp_file.write(gz_file.read())
                tmp_file_name = tmp_file.name
        temp = True
    else:
        print("File does not have a '.gz' extension")
        tmp_file_name = europed_run
        temp = False

    with h5py.File(tmp_file_name, 'r') as hdf5_file:
        print("Dataset Attributes:")
        for dataset_name, dataset in hdf5_file.items():
            if isinstance(dataset, h5py.Dataset):
                print(f"Dataset Name: {dataset_name}")
                print(f"Attributes:")
                for attr_name, attr_value in dataset.attrs.items():
                    print(f"{attr_name}: {attr_value}")

        dataset_names = [name for name in hdf5_file if isinstance(hdf5_file[name], h5py.Dataset)]
        print("Dataset Names:")
        for name in dataset_names:
            print(name)

        print("Dataset Information:")
        for dataset_name, dataset in hdf5_file.items():
            if isinstance(dataset, h5py.Dataset):
                print(f"Dataset Name: {dataset_name}")
                print(f"Shape: {dataset.shape}")
                print(f"Data Type: {dataset.dtype}")

        print("Dataset Attributes:")
        for dataset_name, dataset in hdf5_file.items():
            if isinstance(dataset, h5py.Dataset):
                print(f"Dataset Name: {dataset_name}")
                print(f"Attributes:")
                for attr_name, attr_value in dataset.attrs.items():
                    print(f"{attr_name}: {attr_value}")

        print("File Info:")
        print("----------")
        print(f"File Name: {europed_run}")

        print("\nGroups and Datasets:")
        print("--------------------")
        def print_group_structure(group, indent=0):
            for name, item in group.items():
                if isinstance(item, h5py.Group):
                    print(f"{' ' * indent}Group: {name}")
                    print_group_structure(item, indent + 2)
                elif isinstance(item, h5py.Dataset):
                    print(f"{' ' * indent}Dataset: {name} (Shape: {item.shape}, Dtype: {item.dtype})")
                    for attr_name, attr_value in item.attrs.items():
                        print(f"{' ' * (indent + 2)}Attribute: {attr_name} = {attr_value}")

        print_group_structure(hdf5_file)

        print("\nAttributes:")
        print("-----------")
        for attr_name, attr_value in hdf5_file.attrs.items():
            print(f"Global Attribute: {attr_name} = {attr_value}")



    if temp == True:
        os.remove(tmp_file_name)



def give_list_modes(europed_run,n_profiles):
    pattern = os.path.join(europed_run + '*')
    europed_run = glob.glob(pattern)[0]

    if europed_run.endswith(".gz"):
        print("File has a '.gz' extension")
        # Create a temporary file to decompress the .h5.gz file
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            with gzip.open(europed_run, 'rb') as gz_file:
                tmp_file.write(gz_file.read())
                tmp_file_name = tmp_file.name
        temp = True
    else:
        print("File does not have a '.gz' extension")
        tmp_file_name = europed_run
        temp = False

    with h5py.File(tmp_file_name, 'r') as hdf5_file:
        for i in range(n_profiles):
            print(i)
            for name, item in hdf5_file["scan"][str(i)]["castor"].items():
                print("    "+name)





# Example usage:
# get_structure(file_path)


