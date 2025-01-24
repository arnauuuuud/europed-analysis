from getpass import getuser
from re import search
import numpy as np
import subprocess
import traceback
import datetime
import time
import stat
import os
import ppf
from scipy.interpolate import UnivariateSpline

def derivative(x, y, k = 4, s = 0):
    """" Calculates the derivative of the function using splines """
    spl = UnivariateSpline(x, y, k = k, s = s)
    der_spl = spl.derivative()
    return der_spl(x)

# ======================================================================== #

def read_until_string(f, string):
    line = f.readline()
    while string not in line:
        line = f.readline()
    return line

class ReadFile():
    """
    Context manager for reading file with additional methods compared to 'open'.

    This class is still not optimized and has certain bugs when normal read
    methods are combined with the read_words_generator.

    TODO: Optimize readwords()
    """
    def __init__(self, filepath):
        self.filepath = filepath
        self.file = None
        self.rwg = None

    #===========================#
    # Read a file word for word #
    #===========================#
    def _read_words_generator(self):
        for line in self.file:
            for word in line.split():
                yield word

    def readword(self, data_type):
        return data_type(next(self.rwg))

    def readwords(self, count, data_type):
        """
        Reads several words and returns as a numpy array.
        Converts each word to data_type.

        TODO: Optimize. Currently the np.transpose() call 
        increases execution time by a factor 5
        """
        def _readwords(rwg, count, data_type):
            words = np.empty(count)
            for i in range(count):
                words[i] = data_type(next(rwg))
            return words

        if isinstance(count, (list, tuple)):
            if len(count) > 1:
                words = np.empty(count[::-1])
                for i in range(count[-1]):
                    words[i] = self.readwords(count[:-1], data_type)
                return np.transpose(words)
            else:
                return _readwords(self.rwg, count[0], data_type)
        else:
            return _readwords(self.rwg, count, data_type)

    #=====================#
    # Normal read methods #
    #=====================#
    def read(self, count):
        return self.file.read(count)

    def readline(self):
        return self.file.readline()

    def readlines(self):
        return self.file.readlines()

    def read_until_string(string):
        line = self.file.readline()
        while string not in line:
            line = self.file.readline()
        return line

    #====================#
    # Context management #
    #====================#
    def __enter__(self):
        self.file = open(self.filepath)
        self.rwg = self._read_words_generator()
        return self

    def __exit__(self, exc_type, exc_value, tb):
        self.file.close()
        if exc_type is not None:
            traceback.print_exception(exc_type, exc_value, tb)
            return False
        return True

def remove_line(file, keyword):
    """
    reads the file and removes each line that contains the keyword
    """
    with open(file, 'r') as f:
        lines = [line for line in f if keyword not in line]
    with open(file, 'w') as f:
        for line in lines:
            f.write(line)

#=================================#
# Need sorting                    #
#=================================#

def shift_profile(x, y, xval, yval):
    """
    shifts a profile given by x and y to have yval at xval 
    returns the new x (assumes that x is sorted)
    """
    index = np.where(y > yval)[0][-1]
    k = (y[index+1] - y[index]) / (x[index + 1] - x[index])
    return x + xval - (yval - y[index])/k - x[index]

def axisEqual3D(ax):
    #TODO: Remember what this does.....
    extents = np.array([getattr(ax, 'get_{}lim'.format(dim))() for dim in 'xyz'])
    sz = extents[:,1] - extents[:,0]
    centers = np.mean(extents, axis=1)
    maxsize = max(abs(sz))
    r = maxsize / 2
    for ctr, dim in zip(centers, 'xyz'):
        getattr(ax, 'set_{}lim'.format(dim))(ctr - r, ctr + r)
    return centers, r

def wait_for_night_or_weekend():
    while True:
        hour=datetime.datetime.now().hour
        day=datetime.datetime.now().weekday()
        if (hour>16 or hour < 9) or (day>4):
            break
        time.sleep(600)

