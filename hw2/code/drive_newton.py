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

def f2(x,d):
    if (d == 0):
        return x
    elif d == 1:
        return 1

def f3(x,d):
    if (d == 0):
        return np.sin(x) + np.cos(x**2)
    elif (d == 1):
        return np.cos(x) - ((2*x) * np.sin(x**2))

fcn_list = [f1, f2, f3]

x0 = -0.5
fcnt = 1
for fcn in fcn_list:
    print("Function: " + str(fcnt))
    fcnt = fcnt + 1
    data = newton(fcn, x0,100,10**-10)

    # Here, you can post-process data, and test convergence rates 
    k_l = 0
    k_q = 0
    errors = []
    output = []

    for i in range(len(data) - 1):
        errors.append(abs(data[i+1] - data[i]))

    for i in range(len(errors) - 1):
        k_l = errors[i+1] / errors[i]
        k_q = errors[i+1] / (errors[i]**2)

        output.append(
            f"& ${float(k_l):.8g}$ & ${float(k_q):.8g}$ \\\\")

    np.savetxt(f"convergence_{fcnt-1}.txt", output, fmt="%s")