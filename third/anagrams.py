number = int(input())

letters_set_variaty = {}

for i in range(number):
    string = input().lower()
    letter_dict = {}
    for ch in string:
        if letter_dict.get(ch) is None:
            letter_dict[ch] = 1
        else:
            letter_dict[ch] += 1
    fs = frozenset(letter_dict.items())
    if letters_set_variaty.get(fs) is None:
        letters_set_variaty[fs] = [string]
    else:
        letters_set_variaty[fs].append(string)

result_strings = []

for anagrams in letters_set_variaty.values():
    if len(anagrams) > 1:
        new_s = ""
        for i, word in enumerate(sorted(anagrams)):
            new_s += word + (" " if i != len(anagrams) - 1 else "") 
        result_strings.append(new_s)

for s in sorted(result_strings):
    print(s)
