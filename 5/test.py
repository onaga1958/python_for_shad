import time


def return_none():
    'None'
    return None


def just_pass():
    'pass'
    pass


def test_time(func, N=10**7):
    start = time.clock()
    for i in range(N):
        func()
    print(func.__doc__, time.clock() - start)


test_time(return_none)
test_time(just_pass)

