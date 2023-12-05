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
    min_modul_of_number = 1e9
    min_number = 1e9

    for line in matrix:
        for num in line:
            if abs(num) < min_modul_of_number and num != 0:
                min_modul_of_number = abs(num)
            if num < min_number:
                min_number = num
    
    findDel = True

    for line in matrix:
        if not findDel:
            break
        for num in line:
            if num % min_modul_of_number != 0:
                findDel = False
                break
    
    if findDel:
        min_number /= min_modul_of_number
        for i in range(matrix.shape[0]):
            for j in range(matrix.shape[1]):
                matrix[i][j] = matrix[i][j] / min_modul_of_number
    
    if min_number < 0:
        for i in range(matrix.shape[0]):
            for j in range(matrix.shape[1]):
                matrix[i][j] += -min_number
    return matrix

def reduce_matrix(matrix):
    abbreviated = True

    while abbreviated:
        abbreviated = False
        deleteLines = []
        for iline1 in range(0, matrix.shape[0]):
            for iline2 in range(0, matrix.shape[0]):
                is_reduce = True
                if iline1 == iline2:
                    continue
                for column in range(0, matrix.shape[1]):
                    if not matrix[iline1][column] >= matrix[iline2][column]:
                        is_reduce = False
                        break
                if not is_reduce:
                    continue
                else:
                    deleteLines.append(iline2)
                    abbreviated = True
        matrix = np.delete(matrix, deleteLines, axis=0)
        
        deleteColumn = []
        for icolumn1 in range(0, matrix.shape[1]):
            for icolumn2 in range(0, matrix.shape[1]):
                is_reduce = True
                if icolumn1 == icolumn2:
                    continue
                for iline in range(0, matrix.shape[0]):
                    if not matrix[iline][icolumn1] >= matrix[iline][icolumn2]:
                        is_reduce = False
                        break
                if not is_reduce:
                    continue
                else:
                    deleteColumn.append(icolumn1)
                    abbreviated = True
        matrix = np.delete(matrix, deleteColumn, axis=1)
    
    return matrix


# json_string = '{"matrix": [[4,5,6,7], [3,4,6,5], [7,6,10,8], [8,5,4,3]]}'
json_string = '{"matrix": [[-20,-10,0,10], [-30,-20,0,-10], [10,0,40,20], [20,-10,-20,-30]]}'
try:
    result_matrix = parse_problem(json_string)
    result_matrix = simplefy_matrix(result_matrix)
    result_matrix = reduce_matrix(result_matrix)
    print(result_matrix)
except ValueError as e:
    print(f"Ошибка: {e}")
