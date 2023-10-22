import numpy as np
from json import loads

example = """{"f": [1, 2, 3],
              "goal": "max",
              "constraints": [{"coefs": [1, 0, 0],
                                "type": "eq",
                                "b": 1},
                               {"coefs": [1, 1, 0],
                                "type": "gte",
                                "b": 2},
                               {"coefs": [1, 1, 1],
                                "type": "lte",
                                "b": 3}]}"""

def parse_problem(json: str):
    parsed = loads(json)
    f = np.array(parsed['f'])
    if parsed['goal'] == "min":
        f *= -1
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
    b = b.reshape((b.shape[0], 1))
    return f, A, b


def simplex(f, A, b):
    tableau = np.hstack((b, A))
    tableau = np.vstack((tableau, np.hstack((np.zeros((1,)), f, np.zeros((A.shape[0]))))))
    # print(tableau)
    if b[b < 0].any():
        i = tableau[:-1, 0].argmin()
        l = tableau[i, 1:].argmin()
        if tableau[i, l] >= 0:
            raise Exception("No solution.")
        ratios = tableau[:-1, 0] / tableau[:-1, l]
        r = ratios.argmin()
        simplex_step(tableau, r, l)
        # print(tableau)
    s = tableau[-1].argmax()

    last_max = -1
    while s > 0:
        # print(tableau[:-1, s])
        temp = tableau[:-1, s]
        temp[temp == 0] = -1
        ratios = tableau[:-1, 0] / temp
        j = ratios.argmin()
        simplex_step(tableau, j, s)
        # print(tableau)
        s = tableau[-1].argmax()
        if tableau[-1, s] == last_max:
            break
        last_max = tableau[-1, s]
    return tableau[-1, 0]

def simplex_step(tableau, r, l):
    for i in range(tableau.shape[0]):
        if i == r:
            tableau[i] /= tableau[i, l]
            continue
        tableau[i] -= tableau[r] * tableau[i, l] / tableau[r, l]

# print(simplex(*parse_problem(example)))
