import numpy as np
from json import loads
from sys import stdin

def parse_problem(json: str):
    parsed = loads(json)
    f = np.array(parsed['f'])
    A = []
    b = []
    for constraint in parsed['constraints']:
        A.append(np.array(constraint['coefs']))
        b.append(constraint['b'])
        if constraint['type'] == "gte":
            A[-1] *= -1
            b[-1] *= -1
        if constraint['type'] == "eq":
            A.append(np.array(constraint['coefs']) * -1)
            b.append(-constraint['b'])
    A = np.array(A)
    A = np.hstack((A, np.eye(A.shape[0])))
    b = np.array(b)
    return f, A, b, parsed['goal'] == "min"


def simplex(f, A, b: np.ndarray, isMin):
    tableau = np.hstack((b.reshape(-1, 1), A))
    tableau = np.vstack((tableau, np.hstack((np.zeros((1,)), f, np.zeros((A.shape[0]))))))
    basis = np.arange(A.shape[0], A.shape[0] * 2) - 1
    while (tableau[:-1, 0].min() < 0):
        i = tableau[:-1, 0].argmin()
        l = tableau[i, 1:].argmin() + 1
        if tableau[i, l] >= 0:
            raise Exception("No solution.")
        ratios = tableau[:-1, 0] / tableau[:-1, l]
        r = np.where(ratios > 0, ratios, np.inf).argmin()
        simplex_step(tableau, r, l)
        basis[r] = l
    s = (tableau[-1, 1:].argmax() if isMin else tableau[-1, 1:].argmin()) + 1
    last_max = -1
    while tableau[-1, 1:].min() < 0 if isMin else tableau[-1, 1:].max() > 0:
        # print(tableau[:-1, s])
        temp = tableau[:-1, s]
        temp[temp == 0] = -1
        ratios = tableau[:-1, 0] / temp
        print(f"ratios:\n{ratios}")
        j = ratios.argmin()
        simplex_step(tableau, j, s)
        basis[j] = s
        s = (tableau[-1, 1:].argmax() if isMin else tableau[-1, 1:].argmin()) + 1
        if tableau[-1, s] == last_max:
            break
        last_max = tableau[-1, s]
    return -tableau[-1, 0]

def simplex_step(tableau, r, l):
    for i in range(tableau.shape[0]):
        if i == r:
            tableau[i] /= tableau[i, l]
            continue
        tableau[i] -= tableau[r] * tableau[i, l] / tableau[r, l]

if __name__ == '__main__':
    print(simplex(*parse_problem(stdin.read())))
