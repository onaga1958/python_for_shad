p = float(input())
vector = list(map(lambda x: float(x), input().split(" ")))

print(sum(map(lambda x: abs(x) ** p, vector)) ** (1/p))
