from copy import deepcopy
import numpy as np


def is_singletone(obj, noprint=False):
    x = deepcopy(obj)
    y = deepcopy(obj)
    if noprint:
        return x is y
    else:
        print(obj, x is y)


candidates = range(10) + [0.0, (1,), frozenset((1,)), 'joke',
                          0.1, 6.2342113414, True, 4**18,
                          [1], 2j, 1.11111111111111j]
for i in candidates:
    is_singletone(i)

for i in np.linspace(0, 1, 10000):
    if not is_singletone(i, noprint=True):
        s = "is_singletone({}) = {}"
        print(s.format(i, is_singletone(i, noprint=True)))
        is_singletone(0.0)
        break
else:
    print("all is True")
