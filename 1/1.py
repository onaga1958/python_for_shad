def accum(seq):
    ans = [0]
    for i in seq:
        ans.append(ans[-1] + i)
    return ans

print(accum([1, 2, 3]))
print(accum(range(4)))
print(accum([0, 0, 4, 10, -11, 15]))
