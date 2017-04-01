import sys
import re


def read_language(language_dict):
    string = input()
    if len(string) == 0:
        return False
    split = string.split()
    language_dict[split[1]] = split[0].lower()
    return True

language_dict = {}

while read_language(language_dict):
    pass

queries = [line.lower() for line in sys.stdin]
for query in queries:
    answer = set()
    for word in query.split(" "):
        lens = []
        for language in language_dict.items():
            lenght = len(list(re.finditer(r"[{}]".format(language[0]), word)))
            if lenght > 0:
                lens.append((lenght, language[1]))

        if len(lens) > 0:
            answer.add(min(lens, key=lambda x: (-x[0], x[1]))[1])

    print(" ".join(sorted(answer)))
