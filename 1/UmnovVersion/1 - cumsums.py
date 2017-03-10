def cum_sums(sequence):
    sums = [0]
    for value in sequence:
        sums.append(sums[-1] + value)
    return sums

print cum_sums([1, 2, 3])
print cum_sums([0, 1, -1])
print cum_sums([1, -2, 3, -4, 5, -6])
