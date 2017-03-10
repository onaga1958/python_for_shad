from math import sqrt

def append_next_simple(simples):
    if len(simples) == 0:
        simples.append(2)
        return

    simples.append(simples[-1])
    while True:
        simples[-1] += 1
        for n in simples:
            if n > sqrt(simples[-1]):
                return
            if simples[-1] % n == 0:
                break

def factorization(number):
    simples = []
    answer = []
    while number != 1:
        append_next_simple(simples)
        while number % simples[-1] == 0:
            if len(answer) == 0 or answer[-1][0] != simples[-1]:
                answer.append([simples[-1], 1])
            else:
                answer[-1][1] += 1
            number /= simples[-1]

    print(answer)

n = int(input())
factorization(n)
