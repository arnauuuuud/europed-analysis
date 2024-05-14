import numpy as np

def parse_modes(mode_str):
    return mode_str.split(',')
    
def parse_delta(str):
    if ',' in str:
        return [float(delta) for delta in str.split(',')]
    elif '-' in str:
        delta_min = round(float(str.split('-')[0]),5)
        delta_max = round(float(str.split('-')[1]),5)
        step_size = 0.002
        deltas = np.arange(delta_min, delta_max + step_size, step_size)
        return deltas

class CustomError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)