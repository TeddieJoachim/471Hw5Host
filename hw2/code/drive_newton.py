import numpy as np
from newton import newton

# Define your functions to test Newton on.  You'll need to 
# define two other functions (call them f2 and f3) for 
#   f(x) = x 
# and 
#   f(x) = sin(x) + cos(x**2)

def f1(x, d):
    if d == 0:
        # return f(x) = x^2
        return x**2

    elif d == 1:
        # return the derivative of f(x) = x^2
        return 2*x

fcn_list = [f1]

x0 = -0.5
for fcn in fcn_list:
    data = newton(fcn, x0)

    # Here, you can post-process data, and test convergence rates 

    # Also, use your skills from the last lab, and use savetxt() to dump 
    # data and/or convergence rates to a text file


