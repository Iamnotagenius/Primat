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
    helper_vars = []
    for i, constraint in enumerate(parsed['constraints']):
        A.append(np.array(constraint['coefs']))
        b.append(constraint['b'])
        if constraint['type'] == "gte":
            A[-1] *= -1
            b[-1] *= -1
            helper_vars.append(i)
        if constraint['type'] == "lte":
            helper_vars.append(i)
    A = np.array(A)
    helper_matrix = np.zeros((A.shape[0], len(helper_vars)))
    for i, j in enumerate(helper_vars):
        helper_matrix[j, i] = 1
    A = np.hstack((A, np.array(helper_matrix)))
    b = np.array(b)
    return f, A, b

print(*parse_problem(example), sep='\n')

def simplex(f, A, b):
    tableau = np.hstack((b, A))
    tableau = np.stack((tableau, np.hstack((0, f))))
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


# TODO: улучшить поиск опорного плана, вынести шаг симплекса в отдельную функцию
