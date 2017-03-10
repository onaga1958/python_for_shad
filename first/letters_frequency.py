import sys

text = [i.rstrip() for i in sys.stdin]
dictionary = dict()

for string in text:
    for char in string:
        if char.isalpha():
            char = char.lower()
            if dictionary.get(char) == None:
                dictionary[char] = 1
            else:
                dictionary[char] += 1

for key, value in sorted(dictionary.items(), key=lambda x: [-x[1], x[0]]):
    print("{}: {}".format(key, value))
