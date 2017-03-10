number = int(input())
while number != 1:
    number = number // 2 if number % 2 == 0 else 3 * number + 1
    print(number)
