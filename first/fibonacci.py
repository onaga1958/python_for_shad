def fib(n):
    if n == 0 or n == 1:
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
