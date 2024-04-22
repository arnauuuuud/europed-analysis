import os
import subprocess
from hoho import europed_hampus as europed
import matplotlib.pyplot as plt
from matplotlib import ticker
from pylib.misc import ReadFile
import h5py
import gzip
import tempfile
import numpy as np
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
import glob
import re
import math
from hoho import global_functions, find_pedestal_values, europed_analysis
import scipy.interpolate

