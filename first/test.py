import random

min_size = 150  
max_size = 200
A = -5000
B = 5000
n = random.randint(min_size, max_size)

for i in range(n):
    print(random.randint(A, B), end=" " if i != n - 1 else "\n")
