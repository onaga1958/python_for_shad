def multipliers(n):
    if n == 1:
        return [[1, 1]]

    result = []
    for multiplier in range(2, n + 1):
        power = 0
        while n % multiplier == 0:
            n /= multiplier
            power += 1

        if power > 0:
            result.append([multiplier, power])

    return result

for i in range(1, 20):
    print i, ':', multipliers(i)
