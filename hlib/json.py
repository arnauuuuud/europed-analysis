import numpy as np

def convert_numpy_dict(input_dict):
    converted_dict = {}
    for key, value in input_dict.items():
        if isinstance(key, np.generic):
            key = str(key)
        if isinstance(value, np.ndarray):
            value = value.tolist()
        elif isinstance(value, np.generic):
            value = value.item()
        elif isinstance(value, dict):
            value = convert_numpy_dict(value)
        converted_dict[key] = value
    return converted_dict
