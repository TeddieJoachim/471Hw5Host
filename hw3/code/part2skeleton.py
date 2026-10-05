from numpy import *
import numpy as np
from matplotlib import pyplot as plt
from lglnodes import *
from plot_transformed_grid import plot_transformed_grid


def trapezoid_2D(forig, n, J, transformation):
    '''
    Compute trapezoid rule of f(x,y) on [-1,1] x [-1,1]

    input
    -----
    forig : function of x and y, returns scalar
            This is the function to be integrated over [-1,1] x [-1,1]

    n : integer, determines number of evenly spaced points to use in 
        each dimension

    J : function of x and y, returns scalar    
        This is the determinant of the Jacobian of the transformation

    transformation : function of (r,s), maps a point on the reference 
        domain [-1, 1] x [-1,1] to the domain of interest

    output
    ------
    scalar, approximate integral value according to 2D trapezoid rule
    '''

    # n evenly spaced points in each reference coordinate, and 2D grid of reference points
    pts = linspace(-1, 1, n)
    h = pts[1] - pts[0]
    r, s = meshgrid(pts, pts)
    # r,s space -> x,y
    x, y = transformation(r, s)

    # f(x,y) * |det(Jacobian)|
    vals = forig(x, y) * abs(J(r, s))

    integral = 0.0

    # apply trapezoid method
    for i in range(n):
        for j in range(n):
            weight = 1.0

            # at edges use half weight
            if i == 0 or i == n - 1:
                weight *= 0.5

            if j == 0 or j == n - 1:
                weight *= 0.5
            integral += weight * vals[i, j]
    integral *= h**2

    return integral


def transformation0(r,s):
    '''
    Map (r,s) -->  (x,y)
      where (r,s) is on the [-1,1] x [-1,1] reference domain
    
    This is the dummy example, where the transformation is the identity 

    x = r 
    y = s
    '''
    return r, s

# as explained in the homework description, both trans0 and trans1 have determinants 1
def J0(r, s):
    return ones_like(r)

def transformation1(r,s):
    '''
    Map (r,s) -->  (x,y)
      where (r,s) is on the [-1,1] x [-1,1] reference domain
    
    x = r + 0.1*s
    y = s
    '''
    return r + 0.1*s, s

def J1(r, s):
    return ones_like(r)

# Define u_1
def u1(x,y):
    return ones_like(x)*ones_like(y)

# Define u_2
def u2(x,y):
    return sin(x)*cos(y)

# Define u_3 
def u3(x,y):
    return exp(x + y) 

# for task 5, 
# exact partial derivatives of u2&u3
def u2_x_exact(x,y):
    return cos(x)*cos(y)

def u2_y_exact(x,y):
    return -sin(x)*sin(y)

def u3_x_exact(x,y):
    return exp(x + y)

def u3_y_exact(x,y):
    return exp(x + y)

def transformation2(r,s):
    '''
    Map (r,s) -->  (x,y)
      where (r,s) is on the [-1,1] x [-1,1] reference domain
    
    x = (2.0 + r + 0.2*sin(5*pi*s))*cos(0.5*pi*s)
    y = (2.0 + r + 0.2*sin(5*pi*s))*sin(0.5*pi*s)
    '''
    x = (2.0 + r + 0.2*sin(5*pi*s))*cos(0.5*pi*s)
    y = (2.0 + r + 0.2*sin(5*pi*s))*sin(0.5*pi*s)

    return x, y 

# more complicated determinant computed by hand
def J2(r, s):
    return (pi / 2) * (2.0 + r + 0.2*sin(5*pi*s))


# QUESTION 4A
data = []

for n in [2, 10, 50]:
    omega_R = trapezoid_2D(u1, n, J0, transformation0)
    omega_1 = trapezoid_2D(u1, n, J1, transformation1)
    data.append([n, omega_R, omega_1])

data = np.array(data)

np.savetxt("q4a_table.txt", data, fmt=["%d", "%.10e", "%.10e"], delimiter=" & ", newline=" \\\\\n")


# Compute error in numerical derivative for u_3 using first order forward finite differencing

##########
#plot_transformed_grid(transformation2, 33, fname='hw3_transformed_grid2')
#plot_transformed_grid(transformation0, 10, fname='hw3_transformed_grid0')
#plot_transformed_grid(transformation1, 10, fname='hw3_transformed_grid1')
##########


