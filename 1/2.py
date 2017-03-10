def cutter(seq, a, b):
    return [a if i < a 
            else b if i > b 
            else i for i in seq]

print(cutter(range(5), 3, 10))
print(cutter(range(5), -7, 10120))
print(cutter(range(5), 0, 2))
print(cutter(range(5), 2, 3))
