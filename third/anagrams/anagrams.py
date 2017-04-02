word_number = int(input())

anagrams = {}

for i in range(word_number):
    string = input().lower()
    key = "".join(sorted(string))
    if anagrams.get(key) is None:
        anagrams[key] = {string}
    else:
        anagrams[key].add(string)

result_strings = []

for it in anagrams.values():
    if len(it) > 1:
        result_strings.append(" ".join(sorted(it)))

for s in sorted(result_strings):
    print(s)
