def get_letters_dict(word):
    d = {}
    for ch in word:
        if d.get(ch) is None:
            d[ch] = 1
        else:
            d[ch] += 1
    return d


def check_anagram(word1, word2):
    dict1 = get_letters_dict(word1)
    dict2 = get_letters_dict(word2)
    return dict1 == dict2

number = int(input())

anagrams = []

for i in range(number):
    string = input().lower()
    for anagram in anagrams:
        if check_anagram(string, anagram[0]):
            anagram.append(string)
            break
    else:
        anagrams.append([string])

result_strings = []
for anagram in anagrams:
    if len(anagram) > 1:
        s = ""
        for i, word in enumerate(sorted(anagram)):
            s += word + (" " if i < len(anagram) - 1 else "")
        result_strings.append(s)

for s in sorted(result_strings):
    print(s)
