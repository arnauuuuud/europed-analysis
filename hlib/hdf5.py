import h5py

def read_datasets_from_hdf5(hdf5):
    output = {}
    for key in list(hdf5.keys()):
        if isinstance(hdf5[key], h5py._hl.dataset.Dataset):
            output[key] = hdf5[key].value
    return output

def hdf5_to_dict(hdf5):
    output = {}
    for key in list(hdf5.keys()):
        if isinstance(hdf5[key], h5py._hl.dataset.Dataset):
            output[key] = hdf5[key].value
        else:
            output[key] = hdf5_to_dict(hdf5[key])
    return output

def set_attrs_from_hdf5(hdf5, obj, attrs = None, allow_groups = False, allow_dunder = False):
    hdf5_dict = hdf5_to_dict(hdf5)
    if attrs is None:
        attrs = list(hdf5_dict.keys())
    for attr in attrs:
        if allow_dunder or not (attr[:2] == "__" and attr[-2:] == "__"):
            val = hdf5_dict[attr]
            if allow_groups or not isinstance(val, dict):
                setattr(obj, attr, val)
