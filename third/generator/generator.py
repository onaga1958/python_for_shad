#!/usr/bin/env python3.5

import re
import sys
import argparse
import random
import unittest


letter = 'а-яёЁА-Яa-zA-Z\''
default_pattern = ('([' + letter + ']+|[0-9]+|[^' +
                   letter + '0-9 ])')


def do_tokenize(text, pattern=default_pattern):
    tokens = []
    for line in text:
        match = re.finditer(pattern, line)
        tokens.append([m.group(0) for m in match])

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


def get_probabilities(depth, tokens):
    probabilities_dict = {}
    for line_tokens in tokens:
        for begin in range(len(line_tokens)):
            for lenght in range(min(len(line_tokens) - begin, depth + 1)):
                first_key = tuple(line_tokens[begin:begin + lenght])
                second_key = line_tokens[begin + lenght]
                if probabilities_dict.get(first_key) is None:
                    probabilities_dict[first_key] = {second_key: 1}
                else:
                    if probabilities_dict[first_key].get(second_key) is None:
                        probabilities_dict[first_key][second_key] = 1
                    else:
                        probabilities_dict[first_key][second_key] += 1

    normalize_proba_dict(probabilities_dict)
    return probabilities_dict


def preparation(text, depth):
    tokens = do_tokenize(text)
    return get_probabilities(depth, tokens)


def set_was_quote(new_was_quote, ban_after, ban_before):
    if new_was_quote:
        ban_before.pop()
        ban_after.append('"')
    else:
        ban_after.pop()
        ban_before.append('"')
    return new_was_quote


def generate(depth, size, proba_dict):
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

        if next_word == '.' and was_quote:
            was_quote = set_was_quote(False, ban_after, ban_before)
            result += '"'

        if next_word == '"':
            was_quote = set_was_quote(not was_quote, ban_after, ban_before)

        if next_word == '-':
            if was_quote:
                was_quote = set_was_quote(False, ban_after, ban_before)
                result += '"'
            if prev_word != '.':
                result += '.'

            prev_word = None
            result += '\n'

        if next_word not in ban_before and prev_word not in ban_after:
            result += ' '

        if prev_word in capitalize_after:
            next_word = next_word.capitalize()
        result += next_word

        if next_word == '-':
            last_words = []
        elif len(last_words) == depth:
            last_words = last_words[1:]
        last_words.append(next_word)
        prev_word = next_word

    return result


def generate_next_word(words_dict):
    number = random.random()
    cnt = 0
    for i, (key, value) in enumerate(words_dict.items()):
        cnt += value
        if number < cnt:
            return key


class TestTokenize(unittest.TestCase):
    def test_1(self):
        text = ["Hello, world!"]
        answer = [['Hello', ',', 'world', '!']]
        self.assertEqual(do_tokenize(text), answer)

    def test_2(self):
        text = ["Joker beat000, since 199!!11joker."]
        answer = [['Joker', 'beat', '000', ',', 'since', '199', '!', '!',
                   '11', 'joker', '.']]
        self.assertEqual(do_tokenize(text), answer)

    def test_3(self):
        text = ["test for multilined text",
                "this is second line, obviously",
                "let's put one more line"]
        answer = [['test', 'for', 'multilined', 'text'],
                  ['this', 'is', 'second', 'line', ',', 'obviously'],
                  ['let\'s', 'put', 'one', 'more', 'line']]
        self.assertEqual(do_tokenize(text), answer)


class TestProbabilites(unittest.TestCase):
    def test_1(self):
        tokens = [["First", "test", "sentence"],
                  ["Second", "test", "line"]]
        answer = {(): {'First': 1/6,
                       'Second': 1/6,
                       'line': 1/6,
                       'sentence': 1/6,
                       'test': 1/3},
                  ('First',): {'test': 1},
                  ('Second',): {'test': 1},
                  ('test',): {'line': 0.5,
                              'sentence': 0.5}}
        self.assertEqual(get_probabilities(1, tokens), answer)

    def test_2(self):
        tokens = [["a", "a", "b"], ["b", "b", "b", "c"]]
        answer = {(): {"a": 2/7, "b": 4/7, "c": 1/7},
                  ("a",): {"a": 1/2, "b": 1/2},
                  ("b",): {"b": 2/3, "c": 1/3},
                  ("a", "a"): {"b": 1},
                  ("b", "b"): {"b": 1/2, "c": 1/2}}
        self.assertEqual(get_probabilities(2, tokens), answer)

    def test_3(self):
        tokens = [["a", "a"], ["b", "a"], ["ab", "b", "c", "a"],
                  ["a", "a", "a", "c", "a"]]
        answer = {(): {"a": 8/13, "ab": 1/13, "b": 2/13, "c": 2/13},
                  ("a",): {"a": 3/4, "c": 1/4},
                  ("ab",): {"b": 1},
                  ("b",): {"a": 1/2, "c": 1/2},
                  ("c",): {"a": 1},
                  ("a", "a"): {"a": 1/2, "c": 1/2},
                  ("ab", "b"): {"c": 1}, ("b", "c"): {"a": 1},
                  ("a", "c"): {"a": 1},
                  ("ab", "b", "c"): {"a": 1},
                  ("a", "a", "a"): {"c": 1},
                  ("a", "a", "c"): {"a": 1}}
        self.assertEqual(get_probabilities(3, tokens), answer)


class TestGenerate(unittest.TestCase):
    def do_test(self, depth, size, proba_dict, answers, repeat_num=5):
        for _ in range(repeat_num):
            self.assertIn(generate(depth, size, proba_dict), answers)

    def test_1(self):
        # text: ['A B C D E F G H']
        alphas = 'ABCDEFGH'
        proba_dict = {(): {alpha: 1/8 for alpha in alphas}}
        answers = ['H ' + alpha for alpha in "ABCDEFGH"]
        for first, second in zip(alphas, alphas[1:]):
            proba_dict[(first,)] = {second: 1}
            answers.append(first + ' ' + second)

        self.do_test(1, 2, proba_dict, answers)

    def test_2(self):
        # text: ['A B A C B C']
        alphas = 'ABC'
        proba_dict = {(): {alpha: 1/3 for alpha in alphas}}
        proba_dict[('A',)] = {'B': 1/2, 'C': 1/2}
        proba_dict[('B',)] = {'A': 1/2, 'C': 1/2}
        proba_dict[('C',)] = {'B': 1}

        answers = ['A B', 'A C', 'B A', 'B C', 'C B']

        self.do_test(1, 2, proba_dict, answers)

    def test_3(self):
        # text: ['A B C A B A']
        alphas = 'ABC'
        proba_dict = {(): {'A': 1/2, 'B': 1/3, 'C': 1/6}}
        proba_dict[('A',)] = {'B': 1}
        proba_dict[('B',)] = {'C': 1/2, 'A': 1/2}
        proba_dict[('C',)] = {'A': 1}
        proba_dict[('A', 'B')] = {'C': 1/2, 'A': 1/2}
        proba_dict[('B', 'C')] = {'A': 1}
        proba_dict[('C', 'A')] = {'B': 1}

        answers = ['A B C', 'A B A', 'B C A', 'B A B', 'C A B']

        self.do_test(2, 3, proba_dict, answers)

    def test_4(self):
        # text: ['A B', 'A C', 'A D', 'B A', 'B C',
        #        'B E', 'C A', 'E D', 'D A']
        proba_dict = {(): {'A': 1/3, 'B': 2/9, 'C': 1/6, 'D': 1/6, 'E': 1/9}}
        proba_dict[('A',)] = {'B': 1/3, 'C': 1/3, 'D': 1/3}
        proba_dict[('B',)] = {'A': 1/3, 'C': 1/3, 'E': 1/3}
        proba_dict[('C',)] = {'A': 1}
        proba_dict[('E',)] = {'D': 1}
        proba_dict[('D',)] = {'A': 1}

        answers = ['A B A', 'A B C', 'A B E', 'A C A', 'A D A',
                   'B A B', 'B A C', 'B A D', 'B C A', 'B E D',
                   'C A B', 'C A C', 'C A D', 'D A D', 'D A B',
                   'D A C', 'E D A']

        self.do_test(2, 3, proba_dict, answers)


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

    try:
        args = parser.parse_args(input().split())
    except Exception as e:
        print(e.__class__)

    text = [line.strip() for line in sys.stdin]

    if args.command == 'tokenize':
        pattern = default_pattern.replace(' ', '')
        tokens = do_tokenize(text, pattern)
        for token in tokens[0]:
            print(token)

    if args.command == 'probabilities':
        pattern = '[' + letter + ']+'
        tokens = do_tokenize(text, pattern)
        proba_dict = get_probabilities(args.depth, tokens)
        print_proba_dict(proba_dict)

    if args.command == 'generate':
        proba_dict = preparation(text, args.depth)
        print(generate(args.depth, args.size, proba_dict))

    if args.command == 'test':
        unittest.main()

if __name__ == '__main__':
    main()
