import re


def print_result(string):
    string = string.lower()
    chars = [m.start() for m in re.finditer('[а-я|a-z]', string)]

    for left, right in zip(chars, reversed(chars)):
        if left >= right:
            print('yes')
            return
        if string[left] != string[right]:
            print('no')
            return

str_number = int(input())
for i in range(str_number):
    print_result(input())
