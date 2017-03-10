import no_standard_sort
import sys

def partition(array, left, right):
    support = array[right - 1]
    i, j = left, right - 2
    while True:
        #print array, left, right, i, j, support
        while array[i] < support and i < j:
            i += 1
        if (i == j):
            break

        while array[j] >= support and j > i:
            j -= 1
        if (i == j):
            break

        array[i], array[j] = array[j], array[i]

    if array[i] < support:
        array[i + 1], array[right - 1] = support, array[i + 1]
        return i + 1
    else:
        array[i], array[right - 1] = support, array[i]
        return i



def qsort(array, left, right):
    if left < right - 1:
        n = partition(array, left, right)
        qsort(array, left, n)
        qsort(array, n + 1, right)


array = map(int, sys.stdin.readline().split())

qsort(array, 0, len(array))
for i in array:
    print i,
