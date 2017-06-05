def fib(n):
    if n < 0:
        raise ValueError('n should be zero or positive integer')
    if n == 0:
        return n

    prev_fib_number = 0
    current_fib_number = 1

    for i in range(1, n):
        tmp = current_fib_number + prev_fib_number
        prev_fib_number = current_fib_number
        current_fib_number = tmp

    return current_fib_number

n = int(input())
print(fib(n))
