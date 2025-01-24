import matplotlib.pyplot as plt
from typing import Callable


def plotfunction(func) -> Callable:
    """Decorator for replacing kwarg 'ax' with plt.gca() if left as None.
    'ax = None' has to be kwarg argument of function."""
    def wrapped(*args, ax = None, **kwargs):
        if ax is None:
            ax = plt.gca()
        return func(*args, ax = ax, **kwargs)
    return wrapped