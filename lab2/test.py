import numpy as np
arr = np.array([[1,2,3],[1,2,3]])

# print(arr.shape)

# arr = np.delete(arr, 0, axis=0)

# print(arr.shape)

for i in range(arr.shape[0]):
    print(arr)
    arr = np.delete(arr, 0, axis=1)