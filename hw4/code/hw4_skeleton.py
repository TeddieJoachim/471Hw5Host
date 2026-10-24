from numpy import *
from scipy import sparse
import time
from threading import Thread
from matplotlib import pyplot
from poisson import poisson
from check_matvec import check_matvec

def L2norm(e, h):
    return sqrt(sum(e**2) * h**2)
    '''
    Take L2-norm of e
    '''
    # Task:
    # Return the L2-norm, i.e., the square root of the integral of the error squared 
    # Assume a uniform grid in x and y, and apply the midpoint rule.
    # Assume that each grid point represents the midpoint of an equally sized region


def compute_finite_difference(n, nt, k, f, fpp_num):
    '''
    Compute the numeric second derivative of the function 'f' with a 
    threaded matrix-vector multiply.  

    Input
    -----
    n   <int>       :   Number of grid points in x and y for global problem
    nt  <int>       :   Number of threads
    k   <int>       :   My thread number
    f   <func>      :   Function to take second derivative of
    fpp_num <array> :   Global array of size n**2, stands for f-prime-prime-numeric


    Output
    ------
    fpp_num will have this thread's local portion of the second derivative
    written into it


    Notes
    -----
    We do a 1D domain decomposition.  Each thread 'owns' the k*(n/nt) : (k+1)*(n/nt) rows
    of the domain.  
    
    For example, 
    Let the global points in the x-dimension be [0, 0.33, 0.66, 1.0] 
    Let the global points in the y-dimension be [0, 0.33, 0.66, 1.0] 
    Let the number of threads be two (nt=2)
    
    Then for the k=0 case (for the 0th thread), the domain rows  'owned' are
    y = 0,    and x = [0, 0.33, 0.66, 1.0]
    y = 0.33, and x = [0, 0.33, 0.66, 1.0]
    
    Then for the k = 1, case, the domain rows 'owned' are
    y = 0.66, and x = [0, 0.33, 0.66, 1.0]
    y = 1.0,  and x = [0, 0.33, 0.66, 1.0]

    We assume that n/nt divides evenly.

    '''
    # Compute start, end
    # These indices allow you to index into arrays and grab only this thread's
    # portion.  For example, using the y = [0, 0.33, 0.66, 1.0] example above,
    # and considering thread 0, will yield start = 0 and end = 2, so that 
    # y[start:end] --> [0, 0.33]
    start = int(k * (n/nt))
    end = int((k+1) * (n/nt))
    
    # Compute start_halo, and end_halo
    #
    # These values are the same as start and end, only they are expanded to 
    # include the halo region.
    #
    # Halo regions essentially expand a thread's local domain to include enough
    # information from neighboring threads to carry out the needed computation.
    # For the above example, that means
    #   - Including the y=0.66 row of points for the k=0 case
    #     so that y[start_halo : end_halo] --> [0, 0.33, 0.66]
    #   - Including the y=0.33 row of points for the k=1 case
    #     so that y[start_halo : end_halo] --> [0.33, 0.66, 1.0]
    #   - Note that for larger numbers of threads, some threads 
    #     will have halo regions including domain rows above and below.
    if (k == 0):
        start_halo = start
    else:
        start_halo = start - 1
    if (k == (nt-1)):
        end_halo = end
    else:
        end_halo = end + 1
    
    # Construct local CSR matrix.  Here, you're given that function in poisson.py
    # This matrix will contain the extra halo domain rows
    A = poisson((end_halo - start_halo, n), format='csr')
    h = 1./(n-1)
    A *= 1/h**2


    # Inspect a row or two of A, and verify that it's the correct 5 point stencil
    # You can print a few rows of A, with print(A[k,:])
    #print(A[k,:])

    # Construct a grid of evenly spaced points over this thread's halo region
    #
    # x_pts contains all of the points in the x-direction in this thread's halo region
    x_pts = linspace(0,1,n)

    # y_pts contains all of the points in the y-direction for this thread's halo region
    # For the above example and thread 1 (k=1), this is y_pts = [0.33, 0.66, 1.0]
    finalRow = (end_halo - 1) * h
    y_pts = linspace(start_halo*h, finalRow, end_halo - start_halo) 
    
    # There is no coding to do here, but examine how meshgrid works and 
    # understand how it gives you the correct uniform grid.
    X,Y = meshgrid(x_pts, y_pts)
    X = X.reshape(-1,)
    Y = Y.reshape(-1,) 

    #print(f"Thread {k}: start={start}, end={end}")
    #print(f"Thread {k}: start_halo={start_halo}, end_halo={end_halo}")
    #print(f"Thread {k}: A.shape={A.shape}")

    # Compute local portion of f by using X and Y
    f_vals = f(X,Y)

    #print(f"Thread {k}: f_vals.shape={f_vals.shape}")

    # Compute the output, that is, the matrix A applied to f_vals 
    output = A @ f_vals
    
    #print("First output values:", output[:10])
    #print("First input values:", f_vals[:10])
    #print(f"Thread {k}: output.shape={output.shape}")

    output = output.reshape((end_halo - start_halo, n))
    ownedFirst = start - start_halo
    ownedLast = ownedFirst + (end - start)
    
    output = output[ownedFirst:ownedLast]
    
    # Set the output array (flatten first)
    fpp_num[start*n:end*n] = output.reshape(-1) 


    #print("First numerical values:", fpp_num[:10])

def fcn(x,y):
    return cos((x+1)**(1./3.) + (y+1)**(1./3.)) + sin((x+1)**(1./3.) + (y+1)**(1./3.))

def fcn_prime_prime(x,y):
    arg = (x + 1)**(1./3.) + (y + 1)**(1./3.)

    f_xx = -(cos(arg) + sin(arg)) * (1./9.) * (x + 1)**(-4./3.) \
           - (cos(arg) - sin(arg)) * (2./9.) * (x + 1)**(-5./3.)

    f_yy = -(cos(arg) + sin(arg)) * (1./9.) * (y + 1)**(-4./3.) \
           - (cos(arg) - sin(arg)) * (2./9.) * (y + 1)**(-5./3.)

    return f_xx + f_yy


##
# Here are three problem size options for running.  The instructor has chosen these
# for you.  
option = 2
if option == 1:
    # Choose this if doing a final run on CARC for your strong scaling study
    
    # Problem sizes is an array of grid sizes "n" to loop over
    problem_sizes = array([840*6]) 

    # For each grid size, experiment with all of the different thread numbers in num_threads 
    num_threads = [1,2,3,4,5,6,7,8]

elif option == 2:
    # Choose this for printing convergence plots on your laptop/lab machine,
    # and for initial runs on CARC.  
    # You may want to start with just num_threads=[1] and debug the serial case first.
    
    # Problem sizes is an array of grid sizes "n" to loop over
    problem_sizes = 210*arange(1,6) 
    # this is 5 grid sizes, using 5 trials -> 1 thread per trial, 25 total calls to Thread.
    
    # For each grid size, experiment with all of the different thread numbers in num_threads 
    # First, get this to work for 1 thread, then try for 2 and 3 threads
    num_threads = [1,2,3] 

elif option == 3:
    # Choose this for code development and debugging on your laptop/lab machine
    # You may want to start with just num_threads=[1] and debug the serial case first.
    
    # Problem sizes is an array of grid sizes "n" to loop over
    problem_sizes = array([6]) 

    # For each grid size, experiment with all of the different thread numbers in num_threads 
    # First, get this to work for 1 thread, then try for 2 and 3 threads
    num_threads = [1] 
else:
    print("Incorrect Option!")

##
# Begin main computation loop
##


# Initialize data arrays to store error values and timings results
# You will need to store data for a total number of experiments equal to 
#       (size of num_threads) X (size of problem_sizes)
errorVals = zeros((len(num_threads), len(problem_sizes)))
timingRes = zeros((len(num_threads), len(problem_sizes)))

# That is, you will run one timing experiment for each combination of 
# num_threads and problem_sizes
#
numTrials = 5
# Loop over various numbers of threads
for i,nt in enumerate(num_threads):
    # Loop over various problem sizes 
    for j,n in enumerate(problem_sizes):
        # Run a timing experiment for nt threads and a Poisson matrix 
        # from a grid of size (n x n)
        h = 1. / (n-1)
        fpp_num = zeros(n*n) # will be zero everywhere except where this thread writes to it
        trialTimings = []

        for trial in range(numTrials):
            fpp_num[:] = 0.0 # zero out
            threads = []
            startTime = time.perf_counter()

            for k in range(nt):
                t = Thread(target=compute_finite_difference, args=(n,nt,k,fcn,fpp_num))
                threads.append(t)
                t.start()
            for t in threads:
                t.join()
            endTime = time.perf_counter()
            trialTimings.append(endTime - startTime)
        timingRes[i, j] = min(trialTimings)


        # Use testing-harness to make sure your threaded matvec works
        # This call should print zero (or a numerically zero value)
        if option == 2 or option == 3:
            check_matvec(fpp_num, n, fcn)
        
        # Construct an exact solution for f-prime-prime, call it fpp, for
        # computing the L2-norm of the error 
        h = 1./(n-1)
        pts = linspace(0,1,n)
        X,Y = meshgrid(pts, pts)
        X = X.reshape(-1,)
        Y = Y.reshape(-1,) 
        fpp = fcn_prime_prime(X,Y)
       
        # Task: 
        # Compute and store L2-norm of the error.  That is, compare your
        # result from compute_finite_difference(..) to fpp above.
        #
        # The main tricks here are (i) to use the mid-point rule to compute the integral 
        # of the error squared and (ii) to account for boundary conditions
        #
        # You may want to compute the L2-norm of the error only over the domain interior (i.e.,
        # ignore the boundary points).  
        #
        # Or, you may want to make sure that your output from compute_finite_difference(..)
        # properly accounts for the boundary terms that go on the right-hand-side 
        # (see lecture slides) 

        fpp_num_2d = fpp_num.reshape((n,n)) # our results
        fpp_2d = fpp.reshape((n,n)) # true results

        # IGNORES BOUNDARY 
        e = fpp_num_2d[1:-1, 1:-1] - fpp_2d[1:-1, 1:-1]
        errorVals[i,j] = L2norm(e,h)
        #print(f"Threads={nt}, n={n}, " f"L2 error={errorVals[i,j]}, " f"minimum time={timingRes[i,j]:.6e} s")


    ##
    # End Loop over various grid-sizes
    

    # Task:
    # Generate and save plot showing convergence for this thread number, similar to plots in homework PDF
    #
    # Recommended to comment out plotting before running on CARC 
    #

    pyplot.figure()
    pyplot.loglog(problem_sizes, errorVals[i, :], 'o-', label=f'{nt} threads')
    hVals = 1./(problem_sizes - 1)
    firstH = 1./(problem_sizes[0] - 1)
    # theoretically, our code satisfies E(h)=c*(h^2) -> c = e0/h0^2 => ref = e0 / h0^2 * h^2
    reference = 2.0 * (errorVals[i, 0] / (firstH**2)) * hVals**2
    # mult by 2 so that both can be seen

    #print("problem sizes:", problem_sizes)
    #print("errors:", errorVals[i, :])
    #print("reference:", reference)

    pyplot.loglog(problem_sizes, reference, '--', label='Quadratic reference')

    pyplot.xlabel('Grid size n', fontsize=14)
    pyplot.ylabel(r'$L^2$ error', fontsize=14)
    pyplot.title(f'Convergence with {nt} threads', fontsize=16)
    pyplot.xticks(fontsize=12)
    pyplot.yticks(fontsize=12)
    pyplot.legend(fontsize=12)
    pyplot.grid(True, which='both')

    pyplot.savefig('error' + str(nt) + '.png', dpi=500, format='png', bbox_inches='tight', pad_inches=0.0)

    pyplot.close()


# Task:
# Save timing results to text file
# For instance, if your timings results are in an array named "timings", 
# you can output these results to file, with
savetxt('timings.txt', timingRes)


