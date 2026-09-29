from numpy import *
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
        domain [-1, 1] x [-1, 1]  to  the domain of interest
    

    output
    ------
    scalar, approximate integral value according to 2D trapezoid rule

    '''
    pts = linspace(-1,1,n)
    h = pts[1] - pts[0]
    
    # compute 2D trapezoid rule

    return # numerical integral value 


#########
# Define u_1
def u1(x,y):
    return ones_like(x)*ones_like(y)

def transformation0(r,s):
    '''
    Map (r,s) -->  (x,y)
      where (r,s) is on the [-1,1] x [-1,1] reference domain
    
    This is the dummy example, where the transformation is the identity 

    x = r 
    y = s
    '''
    return r, s

def transformation1(r,s):
    '''
    Map (r,s) -->  (x,y)
      where (r,s) is on the [-1,1] x [-1,1] reference domain
    
    x = r + 0.1*s
    y = s
    '''
    return r + 0.1*s, s

plot_transformed_grid(transformation0, 10, fname='hw3_transformed_grid0')

plot_transformed_grid(transformation1, 10, fname='hw3_transformed_grid1')
##########



#########
# Define u_2
def u2(x,y):
    return sin(x)*cos(y)


##########


##########
# Define u_3 
def u3(x,y):
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



plot_transformed_grid(transformation2, 33, fname='hw3_transformed_grid2')
##########


##########
# Compute error in numerical derivative for u_3 using first order forward finite differencing



##########


