import json
import numpy as np

def parse_problem(json_str):
    try:
        data = json.loads(json_str)

        if "matrix" in data:
            matrix = data["matrix"]

            if isinstance(matrix, list) and all(isinstance(line, list) for line in matrix):
                return np.array(matrix)
            else:
                raise ValueError("Неверный формат матрицы в JSON.")
        else:
            raise ValueError("Отсутствует поле 'matrix' в JSON.")

    except json.JSONDecodeError as e:
        raise ValueError(f"Ошибка декодирования JSON: {e}")

def simplefy_matrix(matrix):
    if matrix.dtype != np.float64:
        matrix //= np.gcd.reduce(matrix)

    matrix += matrix.min() if matrix.min() < 0 else 0

    return matrix

def reduce_matrix(matrix):
    abbreviated = True
    deleteLines = []
    deleteColumn = []

    while abbreviated:
        ilines = list(set(range(matrix.shape[0]))-set(deleteLines))
        icolumns = list(set(range(matrix.shape[1]))-set(deleteColumn))

        abbreviated = False
        for iline1 in ilines:
            for iline2 in ilines:
                if iline1 != iline2 and np.all(matrix[iline1,icolumns] > matrix[iline2,icolumns]):
                    deleteLines.append(iline2)
                    print("delete line:",iline2)
                    abbreviated = True
                    break
        

        for icolumn1 in icolumns:
            for icolumn2 in icolumns:
                if icolumn1 != icolumn2 and np.all(matrix[ilines,icolumn1] > matrix[ilines,icolumn2]):
                    deleteColumn.append(icolumn1)
                    print("delete column:",icolumn1)
                    abbreviated = True
                    break

    matrix = np.delete(matrix, deleteColumn, axis=1)
    matrix = np.delete(matrix, deleteLines, axis=0)
    return matrix, sorted(deleteLines), sorted(deleteColumn)

def strategies(matrix, deleteLines, deleteColumn):
    Pa = []
    Qb = []

    if matrix.shape[0] == 1 and matrix.shape[1] == 1:
        for i in range(len(deleteLines) + 1):
            Pa.append(0) if i in deleteLines else Pa.append(1)
        for i in range(len(deleteColumn) + 1):
            Qb.append(0) if i in deleteColumn else Qb.append(1)
#   else:
#   !!! ТУТ ДОЛЖНО БЫТЬ ПРОДОЛЖЕНИЕ
# 
#   Должны быть рассмотрены случаи, когда невозможно решение в чистых стратегиях
# 
#   В качестве входных данных:
#       matrix - уже сокращенная матрица
#       deleteLines, deleteColumn - номера строк и столбцов которые были удалены в первоначальной матрице
# 
#   В Pa индексы которые есть в delteLines нужно оприравнять нулю, а в Qb индексы deleteColumn
#       остальные индексы должны быть расчитаны с помощью симплекс метода

    return Pa, Qb

# json_string = '{"matrix": [[4,5,6,7], [3,4,6,5], [7,6,10,8], [8,5,4,3]]}'
# json_string = '{"matrix": [[-20,-10,0,10], [-30,-20,0,-10], [10,0,40,20], [20,-10,-20,-30]]}'
json_string = '{"matrix":[[10,4,11,7],[7,6,8,20],[6,2,1,11]]}'
try:
    matrix = parse_problem(json_string)
    matrix = simplefy_matrix(matrix)
    r_matrix, deleteLines, deleteColumn = reduce_matrix(matrix)
    result = strategies(r_matrix, deleteLines, deleteColumn)
    print(result) #вывод: ([0, 1, 0], [0, 1, 0, 0])

except ValueError as e:
    print(f"Ошибка: {e}")
