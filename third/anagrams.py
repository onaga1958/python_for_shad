from collections import Counter

number = int(input())

anagrams = set()
dict_anagram = {}

for i in range(number):
    string = input().lower()
    for anagram in anagrams:
        if Counter(string) == Counter(anagram):
            dict_anagram[anagram].append(string)
            break
    else:
        anagrams.add(string)
        dict_anagram[string] = [string]

for example in sorted(anagrams):
    anagram_list = sorted(dict_anagram[example])
    if len(anagram_list) > 1:
        for i, word in enumerate(anagram_list):
            print(word, end=' ' if i < len(anagram_list) else "")
        print()
