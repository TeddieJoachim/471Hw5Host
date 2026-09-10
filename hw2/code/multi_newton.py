import numpy as np

def multi_newton(f, jacob, x0, maxIter, tol):
  x = x0.copy()
  toReturn = [x]

  for k in range(maxIter):
    # Evaluate f and the Jacobian at the current iterate
    fx = f(x)
    J = jacob(x)

    # Newton correction
    delta = np.linalg.pinv(J) @ fx

    # Newton update
    x = x - delta
    toReturn.append(x)

    if np.linalg.norm(delta) < tol:
      print("Halted due to tolerance.")
      break

  return toReturn