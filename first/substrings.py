def substrings(string):
    for substr_len in range(len(string)):
        for begin in range(len(string) - substr_len):
            end = " " if substr_len != len(string) - 1 else ""
            print(string[begin:begin + substr_len + 1], end=end)
    print()

n = int(input())

for i in range(n):
    substrings(input())
