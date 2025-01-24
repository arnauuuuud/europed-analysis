import numpy as np
import scipy.optimize as opt
from .functions import smoothstep

class FitFunction:
    def __init__(self, function, pars, cov, x_scale=1, y_scale=1):
        self.function = function

        self.pars = pars
        self.cov = cov

        self.x_scale = x_scale
        self.y_scale = y_scale

    def __call__(self):
        return self.function(x/self.x_scale, self.pars) * self.y_scale

    def std(self, x, n_samples=1000):
        statistical_pars = np.random.multivariate_normal(self.pars, self.cov, n_samples)
        profiles = [self.function(x/self.x_scale, pars) * self.y_scale for pars in statistical_pars]
        return np.std(profiles, axis=0)

class SmoothstepFitFunction:
    def __init__(self, left_function = None, right_function = None, left = None, right = None, smoothness = 2):
        self.left_function = left_function
        self.right_function = right_function

        self.left = left
        self.right = right

        self.smoothness = smoothness

    def __call__(self, x):
        step = smoothstep(x, self.left, self.right, self.smoothness)
        return self.left_function(x) * (1 - step) + self.right_function(x) * step

    def std(self, x, *args, **kwargs):
        step = smoothstep(x, self.left, self.right, self.smoothness)
        return self.left_function.std(x) * (1 - step) + self.right_function.std(x) * step

def fit_fitfunction(function, x, y, *args, rescale=False, **kwargs):
    # TODO: Has too many responsibilities, split into several functions
    if isinstance(function, FitFunction):
        function = function.function

    if rescale:
        x_scale, y_scale = max(abs(x)), max(abs(y))
    else:
        x_scale, y_scale = 1, 1

    return_full_output = False
    if 'full_output' in kwargs:
        kwargs.pop('full_output')
        return_full_output = True

    pars, cov, infodict, msg, ier = opt.curve_fit(
        function, x/x_scale, y/y_scale, *args
        full_output=True, **kwargs
    )

    fitfunction = FitFunction(function, pars, cov, x_scale, y_scale)
    if return_full_output:
        return fitfunction, infodict, msg, ier
    return fitfunction
