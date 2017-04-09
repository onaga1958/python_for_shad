#!/usr/bin/env python3.5

import re
import sys
import argparse
import random


def do_tokenize(text, no_print=False, add_sapce=True, only_alpha=False):
    tokens = []
    for line in text:
        if only_alpha:
            pattern = '[A-Za-zа-яА-ЯёЁ]+'
        else:
            letter = 'а-яёЁА-Яa-zA-Z\''
            space = '' if add_sapce else ' '
            pattern = ('([' + letter + ']+|[0-9]+|[^' +
                       letter + '0-9' + space + '])')

        match = re.finditer(pattern, line)
        tokens.append([m.group(0) for m in match])

    if not no_print:
        for token in tokens[0]:
            print(token)
    return tokens


def print_proba_dict(proba_dict):
    sorted_keys = sorted(proba_dict.keys())
    for first_key in sorted_keys:
        print(" ".join(first_key))

        for second_key, proba in sorted(proba_dict[first_key].items()):
            print("  " + second_key + ": {:.2f}".format(proba))


def normalize_proba_dict(proba_dict):
    for first_key, end_variety in proba_dict.items():
        total_entries = sum(end_variety.values())
        for second_key in end_variety.keys():
            end_variety[second_key] /= total_entries


def get_probabilities(text, depth, no_print=False, only_alpha=True):
    tokens = do_tokenize(text, True, False, only_alpha)
    probabilities_dict = {}
    for line_tokens in tokens:
        for i in range(len(line_tokens)):
            for j in range(min(len(line_tokens) - i, depth + 1)):
                first_key = tuple(line_tokens[i:i + j])
                second_key = line_tokens[i + j]
                if probabilities_dict.get(first_key) is None:
                    probabilities_dict[first_key] = {second_key: 1}
                else:
                    if probabilities_dict[first_key].get(second_key) is None:
                        probabilities_dict[first_key][second_key] = 1
                    else:
                        probabilities_dict[first_key][second_key] += 1

    normalize_proba_dict(probabilities_dict)
    if not no_print:
        print_proba_dict(probabilities_dict)
    return probabilities_dict


def smart_print(result, no_print, string):
    if no_print:
        result += string
    else:
        print(string, end='')
    return result

def generate(depth, size, text=None, no_print=False, proba_dict=None):
    if text is None and proba_dict is None:
        raise ValueError('both text and proba_dict cannot be None')

    if proba_dict is None:
        proba_dict = get_probabilities(text, depth, True, False)
    last_words = []
    prev_word = None
    ban_before = ["'", "-", ',', '.', '!', '?', ':', ';', ')', '"']
    ban_after = [None, "'", '(']
    capitalize_after = [None, '.', '-']
    was_quote = False

    result = ""

    for _ in range(size):
        history = tuple(last_words)
        while proba_dict.get(history) is None:
            history = history[1:]

        next_word = generate_next_word(proba_dict[history])
        num_iter = 0
        while not ((prev_word is not None or
                    next_word.isalpha()) and
                   (next_word.isalpha() or
                    prev_word is None or
                    prev_word.isalpha())):
            if num_iter == 5:
                if len(history) > 0:
                    history = history[1:]
                    num_iter = 0
                else:
                    raise ValueError('Alphas should be in the text!')

            next_word = generate_next_word(proba_dict[history])
            num_iter += 1

        if next_word == '"':
            was_quote = not was_quote
            if was_quote:
                ban_before = ban_before[:-1]
                ban_after.append('"')
            else:
                ban_after = ban_after[:-1]
                ban_before.append('"')

        if next_word == '-':
            if was_quote:
                result = smart_print(result, no_print, '"')
            if prev_word != '.':
                result = smart_print(result, no_print, '.')

            prev_word = None
            result = smart_print(result, no_print, '\n')

        if next_word not in ban_before and prev_word not in ban_after:
            result = smart_print(result, no_print, ' ')

        if prev_word in capitalize_after:
            next_word = next_word.capitalize()
        result = smart_print(result, no_print, next_word)

        if next_word == '-':
            last_words = []
        elif len(last_words) == depth:
            last_words = last_words[1:]
        last_words.append(next_word)
        prev_word = next_word
    if no_print:
        return result
    else:
        print()


def generate_next_word(words_dict):
    number = random.random()
    cnt = 0
    for i, (key, value) in enumerate(words_dict.items()):
        cnt += value
        if number < cnt:
            return key


def main_test(instruction):
    all_test_flag = instruction is None
    tests_number = [0, 0]
    commands = ['tokenize', 'probabilites', 'generate']
    test_funcs = [test_tokenize, test_probabilites, test_generate]

    for command, test_func in zip(commands, test_funcs):
        if all_test_flag or command == instruction:
            test_func(tests_number)

    print()
    print("total tests    : {}".format(tests_number[0]))
    print("completed tests: {}".format(tests_number[1]))


def test_tokenize(tests_number):
    texts = [["Hello, world!"],
             ["Joker beat000, since 199!!11joker."],
             ["test for multilined text",
              "this is second line, obviously",
              "let's put one more line"]]

    params = [{'no_print': True, 'text': text, 'add_sapce': False}
              for text in texts]

    answers = [[['Hello', ',', 'world', '!']],
               [['Joker', 'beat', '000', ',', 'since', '199', '!', '!',
                 '11', 'joker', '.']],
               [['test', 'for', 'multilined', 'text'],
                ['this', 'is', 'second', 'line', ',', 'obviously'],
                ['let\'s', 'put', 'one', 'more', 'line']]]

    simple_test(do_tokenize, params, answers, tests_number)


def test_probabilites(tests_number):
    texts = [["First test sentence",
              "Second test line"],
             ["a a b",
              "b b b c"],
             ["a a",
              "b a",
              "ab b c a",
              "a a a c a"]]
    depths = [1, 2, 3]
    params = [{'no_print': True, 'text': text, 'depth': depth}
              for depth, text in zip(depths, texts)]

    answers = [{(): {'First': 1/6,
                     'Second': 1/6,
                     'line': 1/6,
                     'sentence': 1/6,
                     'test': 1/3},
                ('First',): {'test': 1},
                ('Second',): {'test': 1},
                ('test',): {'line': 0.5,
                            'sentence': 0.5}},
               {(): {"a": 2/7, "b": 4/7, "c": 1/7},
                ("a",): {"a": 1/2, "b": 1/2},
                ("b",): {"b": 2/3, "c": 1/3},
                ("a", "a"): {"b": 1},
                ("b", "b"): {"b": 1/2, "c": 1/2}},
               {(): {"a": 8/13, "ab": 1/13, "b": 2/13, "c": 2/13},
                ("a",): {"a": 3/4, "c": 1/4},
                ("ab",): {"b": 1},
                ("b",): {"a": 1/2, "c": 1/2},
                ("c",): {"a": 1},
                ("a", "a"): {"a": 1/2, "c": 1/2},
                ("ab", "b"): {"c": 1}, ("b", "c"): {"a": 1},
                ("a", "c"): {"a": 1},
                ("ab", "b", "c"): {"a": 1},
                ("a", "a", "a"): {"c": 1},
                ("a", "a", "c"): {"a": 1}}]

    simple_test(get_probabilities, params, answers, tests_number)


def test_generate(tests_number):
    texts = [['A B C D E F G H'], ['A B A C B C'], ['A B C A B A'],
             ['A B', 'A C', 'A D', 'B A', 'B C', 'B E', 'C A', 'E D', 'D A']]
    sizes = [2, 2, 3, 3]
    params = [{'no_print': True, 'text': text, 'depth': size - 1, 'size': size}
              for text, size in zip(texts, sizes)]

    possible_answers = [['A B', 'B C', 'C D', 'D E', 'E F', 'F G', 'G H'] +
                        ['H ' + alpha for alpha in "ABCDEFGH"],
                        ['A B', 'A C', 'B A', 'B C', 'C B'],
                        ['A B C', 'A B A', 'B C A', 'B A B', 'C A B'],
                        ['A B A', 'A B C', 'A B E', 'A C A', 'A D A',
                         'B A B', 'B A C', 'B A D', 'B C A', 'B E D',
                         'C A B', 'C A C', 'C A D', 'D A D', 'D A B',
                         'D A C', 'E D A']]
    for i in range(4):
        simple_test(generate, params, possible_answers, tests_number,
                    lambda x, y: x in y)


def simple_test(func, test_params, test_outputs, tests_number,
                compare=lambda x, y: x == y):
    for right_answer, params in zip(test_outputs, test_params):
        tests_number[0] += 1
        answer = func(**params)
        if compare(answer, right_answer):
            print('OK')
            tests_number[1] += 1
        else:
            print("get output:")
            print(answer)
            print("right answer:")
            print(right_answer)


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='command')

    tokenize_parser = subparsers.add_parser('tokenize')

    proba_parser = subparsers.add_parser('probabilities')
    proba_parser.add_argument('--depth', required=True, type=int)

    generate_parser = subparsers.add_parser('generate')
    generate_parser.add_argument('--depth', required=True, type=int)
    generate_parser.add_argument('--size', required=True, type=int)

    test_parser = subparsers.add_parser('test')
    test_parser.add_argument('--instruction', '-i', '-c')

    args = parser.parse_args(input().split())

    text = [line.strip() for line in sys.stdin]

    if args.command == 'tokenize':
        do_tokenize(text)
    if args.command == 'probabilities':
        get_probabilities(text, args.depth)
    if args.command == 'generate':
        generate(args.depth, args.size, text=text)
    if args.command == 'test':
        main_test(args.instruction)

if __name__ == '__main__':
    main()
