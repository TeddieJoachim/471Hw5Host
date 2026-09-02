import numpy as np

def newton(f, x0, maxIter, tol):
    '''
    Newton's method of root finding
    
    input
    -----
    f           : function to find zero of
                  Interface for f:  f(x, 0)  returns f(x)
                                    f(x, 1)  returns f'(x)
    x0          : initial guess
    maxIter     : the maximum number of iterations before the code halts, in 
                  case Newton's does not converge in time
    tol         : a tolerance such that the function will iterate until the 
                  error is less than this tolerance
    
    output
    ------
    data   : array of approximate roots
    '''
    
    data = np.zeros((maxIter,1))
    x = x0
    
    for i in range(maxIter):
        xold = x
        x = x - f(x, 0)/f(x, 1)
        
        s = "Iter  " + str(i) + "   Approx. root  " + str(x)
        print(s)
    
        data[i,0] = x

        # Insert some logic for halting, if the tolerance is met
        if (abs(x - xold) < tol):
            print("Broke due to tolerance.")
            break
    
    ##
    # end for-loop

    return data[0:(i+1)]

