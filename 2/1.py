import math

n = int(input())

print([[x, y, z] for x in range(n + 1)
        for y in range(x)
        for z in range(n + 1)
        if x ** 2 + y ** 2 == z ** 2])
