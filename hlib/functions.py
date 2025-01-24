import numpy as np
import scipy.special as spec

#-----------------------------
#---- Smoothstep function ----
#-----------------------------
def finite_smoothstep(x, left, right, smoothness):
    """
    A finitely smooth stepfunction between 'left' and 'right' with a number
    of continous derivatives equal to 'smoothness'
    returns the function values evaluated in the points given by 'x'
    """
    x = np.clip((x - left) / (right - left), 0, 1)
    result = 0
    N = smoothness
    for n in range(0, N + 1):
        result += spec.comb(N + n, n) * spec.comb(2 * N + 1, N - n) * (-x) ** n
    result *= x ** (N + 1)
    return result

def infinite_smoothstep(x, left, right):
    """
    An infinitely smooth stepfunction between 'left' and 'right'
    returns the function values evaluated in the points given by 'x'
    """
    def f(xp):
        return np.exp(-1/xp)

    result = np.zeros(x.shape)
    ind = np.where(x > right)
    result[ind] = 1

    ind = np.where((x < right) & (x > left))
    xp = (x[ind] - left) / (right - left)
    result[ind] += f(x) / (f(x) + f(1 - x))

    return result

def smoothstep(x, left, right, smoothness = None):
    """
    A smooth stepfunction between 'left' and 'right' with a number
    of continous derivatives equal to 'smoothness'. If 'smoothness' is left
    as 'None' then an infinitely smooth stepfunction is returned.
    returns the function values evaluated in the points given by 'x'
    """
    assert left < right
    if smoothness is None:
        return infinite_smoothstep(x, left, right)
    else:
        return finite_smoothstep(x, left, right, smoothness)


#-----------------------------
#---- Polynomial function ----
#-----------------------------

def polynomial(x, *pars):
    """
    returns the polynomial given by 'pars' on the form:
    return pars[0] + x * pars[1] + x**2 * pars[2] + ... + x**n * pars[n]
    """
    return sum([x**i * par for i, par in enumerate(pars)])

def apply_polyconds(pars, conds):
    def derivative_matrix(order):
        """ Creates derivative matrix """
        dm = np.zeros((order + 1, order + 1))
        for i in range(order):
            dm[i, i+1] = i + 1
        return dm
    """
    Applies conditions to polynomial parameters by increasing the order of the polynomial
    conds should be an iterable of iterables: conds = [cond1, cond2, ..., condn]
    where each iterable should be of the form:
    cond = ['x', 'value', 'order of derivative']
    for instance cond = [1.2, 3.2, 1] would mean that the first derivative 
    in x = 1.2 is equal to 3.2

    OBS! Will run into problems if you try to apply conditions at 'x' = 0 due
    to the fact that the algorithm applies the conditions by increasing the 
    order of the polynomial and calculating the new coefficients.
    """
    #TODO: Optimize this function as it is currently very slow
    order = len(pars)-1
    nr_conds = len(conds)

    #Initializing matrices		
    M = []
    val = []
    for i, cond in enumerate(conds):
        x, y, d = cond[0], cond[1], cond[2]
        #Creating matrix
        M.append([])
        for j in range(order + 1, order + 1 + nr_conds):
            M[i].append(math.factorial(j)/math.factorial(j-d)*x**(j - d))
        #Calculating parameters
        temp_pars = np.array(pars)
        dm = derivative_matrix(order)
        for i in range(d):
            temp_pars = dm.dot(temp_pars)
        #Appending value to resulting matrix
        val.append(y - poly(temp_pars, x))
    M = np.linalg.inv(M)
    new_pars = M.dot(val)
    return np.append(pars, new_pars)

def get_polynomial_function_with_conds(conds):
    """
    returns a polynomial function where certain conds are applied.
    For definition of 'conds', see the documentation for 'apply_polyconds'
    Mainly meant for use with scipy.curve_fit and similar functions where
    the final polynomial paramaters can be aquired by passing the resulting
    'pars' to 'apply_polyconds' with the same 'conds' that are used here.
    """
    def polynomial_function_with_conds(x, *pars):
        pars = apply_polyconds(pars, conds)
        return polynomial(x, *pars)
    return polynomial_function_with_conds

#-------------------------
#---- Mtanh functions ----
#-------------------------

def extended_mtanh(x, height, position, width, s1, s2):
    xp = 2 * (position - x) / width 
    profile = (
        (height / 2) * (
            ((1 + s1*xp) * np.exp(xp) - (1 + s2*xp) * np.exp(-xp)) / (np.exp(xp) + np.exp(-xp)) + 1
        )
    )
    return profile

def mtanh(x, height, position, width, s1):
    return extended_mtanh(x, height, position, widht, s1, 0)

#-------------------------
#----                 ----
#-------------------------
