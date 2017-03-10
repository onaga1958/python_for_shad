def is_pair(sym1, sym2):
    if sym1 == "(" and sym2 == ")":
        return True
    if sym1 == "{" and sym2 == "}":
        return True
    if sym1 == "[" and sym2 == "]":
        return True
    return False

def check(string):
    if string == "":
        return "yes"

    stack = []
    for char in string:
        if len(stack) != 0 and is_pair(stack[-1], char):
            stack.pop()
        else:
            stack.append(char)

    return "yes" if len(stack) == 0 else "no"


n = int(input())

for i in range(n):
    print(check(input()))
