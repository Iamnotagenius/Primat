import numpy as np

def simplex(A, b, f):
    tableau = np.hstack((b, A))
    tableau = np.stack((tableau, f))
    s = tableau[-1].argmax()
    while s > 0:
        ratios = tableau[:, 0] / tableau[:, s]
        j = ratios.argmin()
        for i in range(tableau.shape[0]):
            if i == j:
                tableau[i] /= tableau[i, s]
                continue
            tableau[i] = tableau[j] * -(tableau[j, s] / tableau[i, s]) + tableau[i]
        s = tableau[-1].argmax()


