import numpy as np 

# The integrand
def f(k, x):
  return np.e**np.cos(k*x)

def trapezoid(func, k, n):
  interval = np.linspace(-1, 1, n+1) # need +1 points to get n intervals
  h = 2 / n # basically hard coded since the interval is -1 to 1
  fVals = func(k, interval) # get f at every point on interval.

  return h * ( ((fVals[0] + fVals[-1]) / 2) + np.sum(fVals[1:-1]))

N = 10000 
# chose 50 arbitrarily and found that the error estimate was within tolerance inside this number of intervals
# for k=pi but not pi^2, which makes sense as the larger number as an argument to cosine is going to massively 
# shrink the period
resultsK1 = []
resultsK2 = []
tol = 10**-10

for k in [np.pi, np.pi**2]:
  previous = None
  for n in range(1, N):
    current = trapezoid(f, k, n)
    if (k == np.pi): 
      resultsK1.append(current)
    else:
       resultsK2.append(current)

    if previous is not None:
      error_est = np.abs(current - previous)

      if error_est < tol:
        print("k =", k, "tolerance reached at n =", n)
        print("Approximation =", current)
        print("Estimated error =", error_est)
        break

    previous = current
