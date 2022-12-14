import numpy as np
from math import sqrt


def rand_2d_list(rows, cols):
  return np.random.randint(1, 100, size=(rows, cols))


rand_arr = rand_2d_list(5, 5)

res_sum = list(map(lambda arr: sum(arr), rand_arr))
res_filter = list(filter(lambda arr: sqrt(arr) * sqrt(arr) == arr, res_sum))

print(rand_arr)
print(res_sum)
print(res_filter)