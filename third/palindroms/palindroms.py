import re


def print_result(string):
    string = string.lower()
    chars = [m.start() for m in re.finditer('[а-яa-zё]', string)]

    for left, right in zip(chars, reversed(chars)):
        if left >= right:
            print('yes')
            return
        if comp_char(string[left], string[right]):
            print('no')
            return


def comp_char(c1, c2):
    if c1 != 'е' and c1 != 'ё':
        return c1 != c2
    else:
        return c2 != 'е' and c2 != 'ё'

str_number = int(input())
for i in range(str_number):
    print_result(input())
