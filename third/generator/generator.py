import re
import sys
import argparse

def do_tokenize(text, no_print=False):
    tokens = []
    for line in text:
        match = re.finditer('([a-zA-Z]+|[0-9]+|[^a-zA-Z0-9 ])', line)
        tokens.append([m.group(0) for m in match])

    if not no_print:
        print(tokens)
    return tokens


def print_proba_dict(proba_dict):
    sorted_keys = sorted(proba_dict.keys, key=)
    for key in sorted_keys:
        for



def get_probabilities(args, text, no_print=False):
    tokens = do_tokenize(text)
    probabilities_dict = {}
    for line_tokens in tokens:
        for i in range(len(line_tokens)):
            for j in range(min(len(line_tokens) - i, args.depth)):
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


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='command')

    tokenize_parser = subparsers.add_parser('tokenize')

    proba_parser = subparsers.add_parser('probabilities')
    proba_parser.add_argument('--depth', required=True, type=int)

    args = parser.parse_args(input().split())

    text = [line.strip() for line in sys.stdin]

    if args.command == 'tokenize':
        do_tokenize(text)
    if args.command == 'probabilities':
        get_probabilities(args, text)

if __name__ == '__main__':
    main()
