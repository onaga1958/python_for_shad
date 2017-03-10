import sys

limit = int(input())
text = [line for line in sys.stdin]

for line in text:
    current_len = 0
    for word in line.split(" "):
        if current_len + len(word) + (1 if current_len != 0 else 0) > limit:
            current_len = 0
            print()

        if current_len != 0:
            current_len += 1
            print(" ", end="")

        current_len += len(word)
        print(word, end="")
