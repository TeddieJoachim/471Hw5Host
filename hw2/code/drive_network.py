import numpy as np
from multi_newton import multi_newton 

#8x6 matrix A
A = np.array([
    [-1,  0,  0,  1,  0,  0],
    [ 0,  0,  0, -1,  1,  0],
    [ 0,  0,  0,  0, -1,  1],
    [ 0,  0,  1,  0,  0, -1],
    [ 0,  1, -1,  0,  0,  0],
    [ 1, -1,  0,  0,  0,  0],
    [ 0, -1,  0,  0,  0,  1],
    [ 0,  0,  0, -1,  0,  1]
])

# source vector s
s = np.array([1, -1, 0, 0, 0, 0]) 
# entries will correspond to nodes 0, 1, 2, 3, 4, 5.
# so, node 0 has s0 = 1, node 1 has s1 = -1.
# all other nodes will have zero external current.

# test print
print("Shape of A:", A.shape)
print("Sum of s:", np.sum(s))
# result: Shape of A: (8, 6)
#         Sum of s: 0
# interpretation: A is an 8x6 matrix, and the sum of s is zero, which is consistent with Kirchhoff's current law.

# parameters for the nonlinear electrical network.
Y = 1.0 # represents the admittance
alpha = 0.5 # controls how strongly the resistance changes as the voltage drop increase.

# Nonlinear admittance fxn from eqn 4
# d = voltage drop for an array of voltage drops across the directed edges.
def y_tilde(d):
    return Y / (1 + alpha * d**2)

# derivative of nonlinear admittance fxn from eqn 4
def y_tilde_prime(d):
    return (-2 * alpha * d * Y) / ((1 + alpha * d**2)**2)

# test print
print("y_tilde(0):", y_tilde(0.0))
# since d = 0, the derivative should also be 0.
print("y_tilde_prime(0):", y_tilde_prime(0.0))

# nonlinear system for electrial network.
# v = voltages at each node, size of v is 6.
def f(v):
    d = A @ v # voltage difference across each edge (d = Av, size of d is 8, e.g. d0 = v3 - v0, d1 = v4 - v3, etc.)

    y = y_tilde(d) # nonlinear admittance for each edge

    return A.T @ np.diag(y) @ d - s # f(v) = A^T * diag(y) * d - s

v_test = np.zeros(6)

print("f(0):", f(v_test))

# compute Jacobian matrix J_f(v) for nonlinear system f(v) = A^T * diag(y) * d - s, where d = Av.
def jacobian(v):

    d = A @ v # voltage difference across each edge (d = Av, size of d is 8, e.g. d0 = v3 - v0, d1 = v4 - v3, etc.)

    # compute y_tilde(d) and its derivative for each edge (8 total admittance vals & 8 derivative vals)
    y = y_tilde(d)
    y_prime = y_tilde_prime(d)

    K = np.diag(y + y_prime * d) # placing along diagonal matrix with entries y(d_j) + y'(d_j) * d_j

    # (6x8) * (8x8) * (8x6) = (6x6)
    return A.T @ K @ A # Jacobian of f(v) = A^T * K * A

J_test = jacobian(v_test)
print("Shape of J(0):", J_test.shape)

# build of initial guess v^(0) given by assignment.
d0 = np.zeros(A.shape[0]) # 8 network edges, so d0 = [0,0,0,0,0,0,0,0].

y0 = y_tilde(d0) # nonlinear admittance for each edge, y_tilde(0) = 1, so y0 = [1,1,1,1,1,1,1,1].

initial_matrix = A.T @ np.diag(y0) @ A # initial matrix will be used for pseudoinverse.

# v0 is the starting guess for the six unknown node voltages.
v0 = np.linalg.pinv(initial_matrix) @ s # computes req'd initial v guess using Moore-Penrose pseudoinverse.

print("Initial guess v0:", v0)

#commit: added pseudoinverse initial voltage guess 

# attempt to begin Newton's iteration.
tol = 10**-10 # tolerance for convergence
max_iter = 100 # maximum number of iterations

v = v0.copy() # initialize v to the initial guess v0, using copy() to avoid modifying v0 in place.

fv = f(v) # compute nonlin residual f(v) at the initial guess v0.

# using linalg shown in class. 
# computes the 2-norm of the residual vector f(v). gives one number, how far f(v) is from zero.
residual_norm = np.linalg.norm(fv) 

print("Initial residual norm:", residual_norm)
# output: Initial residual norm: 0.20733046973419503
# output matches values shown in Table 1 Newton iteration k = 0. SUCCESS!

# commit: added Newton stopping params and init residual

#
J = jacobian(v) # compute Jacobian matrix J_f(v) at the initial guess v0.

delta_v = np.linalg.pinv(J) @ fv # compute Newton correction

v = v - delta_v # update voltage guess

fv = f(v) # compute new residual
residual_norm = np.linalg.norm(fv)

print("Residual norm after one Newton step:", residual_norm)


network_solution = multi_newton(
    f,
    jacobian,
    v0,
    max_iter,
    tol
)

print("Network solution:", network_solution)
for k in range(0, len(network_solution)):
  print("K " + str(k) + " Residual norm " + str(np.linalg.norm(f(network_solution[k]))))