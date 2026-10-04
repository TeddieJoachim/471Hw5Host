import numpy as np 
import matplotlib.pyplot as plt
from lglnodes import lglnodes 

# The integrand
def f(k, x):
  return np.e**np.cos(k*x)

'''
def trapezoid(func, k, n):
  interval = np.linspace(-1, 1, n+1) # need +1 points to get n intervals
  h = 2 / n # basically hard coded since the interval is -1 to 1
  fVals = func(k, interval) # get f at every point on interval.

  return h * ( ((fVals[0] + fVals[-1]) / 2) + np.sum(fVals[1:-1]))
'''
  
# added gauss ------------------
def gauss(func, k, n):
  # nodes and weights from LGL file 
  nodes, weights = lglnodes(n)
  # evaluates e^cos(kx) for every node
  fVals = func(k, nodes)
  # returns sum of products between fVals and their weights
  return np.sum(weights * fVals)

# max quad. order to test
N = 10000 
# chose 50 arbitrarily and found that the error estimate was within tolerance inside this number of intervals
# for k=pi but not pi^2, which makes sense as the larger number as an argument to cosine is going to massively 
# shrink the period

# gauss quad approximations 
resultsK1 = []
resultsK2 = []

# (n, error estimate) pairs
errorEstK1 = []
errorEstK2 = []
# error tolerance per assignment requirement
tol = 10**-10

# this was the experimental block but I also used it to collect the values of the trapezoid method, 
# will eventually put them into latex tables
# using this for gauss instead of trap. --------------
for k in [np.pi, np.pi**2]:
  previous = None
  # changed range to maintain N inclusive --------------
  for n in range(2, N +1):
    # calculting next approx. using G-L nodes & weights -------------
    current = gauss(f, k, n)
    if (k == np.pi): 
      resultsK1.append(current)
    else:
      resultsK2.append(current)

    if previous is not None:
      error_est = np.abs(current - previous)
      if (k == np.pi): 
        errorEstK1.append((n, error_est))
      else:
        errorEstK2.append((n, error_est))
      if error_est < tol:
        print("k =", k, "tolerance reached at n =", n)
        print("Approximation =", current)
        print("Estimated error =", error_est)
        break

    previous = current

# unpack the n and err values into lists
n1, e1 = zip(*errorEstK1)
n2, e2 = zip(*errorEstK2)

# convert to numpy arrays
n1 = np.array(n1)
e1 = np.array(e1)
n2 = np.array(n2)
e2 = np.array(e2)


# use the full range of n values from both Gauss calcs. -----------
# n_ref = np.arange(min(n1[0], n2[0]), max(n1[-1], n2[-1]) + 1)

# giving each reference curve its own range:
# reference range for k=pi
n_ref_pi = np.arange(n1[0], n1[-1] + 1)

# reference range for k=pi^2
n_ref_pi_2 = np.arange(n2[0], n2[-1] + 1)

# Use the first error from k = pi as the reference curve
# n0 = n1[0]
# e0 = e1[0]
# n0 = n_ref[0] ---------------------------
# e0 = e1[0]

# didn't need the following block ------------------
'''
# the ratio n_nref/n0 makes the curve equal to e0 when n = n0
# linear = e0 * (n_ref / n0)**(-1)
# quadratic = e0 * (n_ref / n0)**(-2)
# cubic = e0 * (n_ref / n0)**(-3)
# chose C = e and alpha = 0.01 (just a small number) for exponential decay 
# i don't anticipate trapezoid will converge exponentially, so can save twiddling c and a for 2.
# subtract n0 from n so that when n = n0:
#     C^(-alpha*(n-n0)) = C^0 = 1
# and therefore the curve starts at exactly e0.
'''
# init vals for exp. ref. curve
C = np.e
# experimenting with different alpha vals
# alpha1 = 0.1
# alpha2 = 0.3
# for k = pi^2
alpha3 = 0.5
# alpha4 = 0.7
# alpha5 = 0.9
# alpha6 = 1.1
# for k = pi
alpha7 = 1.5

# k=pi
n01 = n1[0]
e01 = e1[0]

# k=pi^2
n02 = n2[0]
e02 = e2[0]
'''
# reused from trap. model 
exp1 = e0 * C**(-alpha1 * (n_ref - n0))
# using experimental alpha vals
exp2 = e0 * C**(-alpha2 * (n_ref - n0))
exp3 = e0 * C**(-alpha3 * (n_ref - n0))
exp4 = e0 * C**(-alpha4 * (n_ref - n0))
exp5 = e0 * C**(-alpha5 * (n_ref - n0))
exp6 = e0 * C**(-alpha6 * (n_ref - n0))
exp7 = e0 * C**(-alpha7 * (n_ref - n0))
'''

# for alpha 3 and alpha 7 (k=pi and k=pi^2)
exp8 = e01 * C**(-alpha7 * (n_ref_pi - n01))
exp9 = e02 * C**(-alpha3 * (n_ref_pi_2 - n02)) 

plt.loglog(n1, e1, label=r'$k=\pi$')
plt.loglog(n2, e2, label=r'$k=\pi^2$')

'''
plt.loglog(n_ref, linear, '--', label='Linear')
plt.loglog(n_ref, quadratic, '--', label='Quadratic')
plt.loglog(n_ref, cubic, '--', label='Cubic')
'''
# plt.loglog(n_ref, exp1, '--', label=r'Exponential, $\alpha=0.1$')
# # adding other experimental plots
# plt.loglog(n_ref, exp2, '--', label=r'Exponential, $\alpha=0.3$')
# plt.loglog(n_ref, exp3, '--', label=r'Exponential, $\alpha=0.5$')
# plt.loglog(n_ref, exp4, '--', label=r'Exponential, $\alpha=0.7$')
# plt.loglog(n_ref, exp5, '--', label=r'Exponential, $\alpha=0.9$')
# plt.loglog(n_ref, exp6, '--', label=r'Exponential, $\alpha=1.1$')
# plt.loglog(n_ref, exp7, '--', label=r'Exponential, $\alpha=1.5$')
plt.loglog(n_ref_pi, exp8, '--', label=r'Exp. ref., $k=\pi,\ \alpha=1.5$')
plt.loglog(n_ref_pi_2, exp9, '--', label=r'Exp. ref., $k=\pi^2, \alpha=0.5$')

# changed labels ----------------------
plt.xlabel('Quad order, n')
plt.ylabel('Error estimate')
plt.title('Convergence of Gauss Quad')

# changed file name ---------------------
plt.legend()
plt.grid(True, which='both')
plt.savefig('gauss_converg.png', dpi=300, bbox_inches='tight')
plt.show()