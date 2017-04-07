import argparse
import sys


symbols = list('@%#*+=-:. ')
brightness = dict([(j, i) for i, j in enumerate(symbols)])


def get_image():
    row_image = [line for line in sys.stdin] + [[]]
    for line in row_image[:-1]:
        for ch in line[:-1]:
            if ch not in symbols:
                print('Wrong symbol: ', ch)
                err = 'Incorrect symbols, must be only {}'.format(symbols)
                raise ValueError(err)
    return row_image


def do_crop(args):
    image = get_image()
    for line in image[args.top:-args.bottom - 1]:
        print(line[args.left:-args.right - 1])


def do_expose(args):
    new_image = [''.join([symbols[min(9, max(0, brightness[ch] + args.shift))]
                         for ch in line[:-1]])
                 for line in get_image()[:-1]]
    for line in new_image:
        print(line)


def rotate(image):
    return [''.join([image[i][j] for i in range(len(image))])
            for j in range(len(image[0]) - 1, -1, -1)]


def do_rotate(args):
    image = [line[:-1] for line in get_image()[:-1]]

    for i in range(int(args.angle / 90)):
        image = rotate(image)

    for line in image:
        print(line)


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='command')

    parser_crop = subparsers.add_parser('crop')
    parser_crop.add_argument('-t', '--top', default=0, type=int)
    parser_crop.add_argument('-r', '--right', default=0, type=int)
    parser_crop.add_argument('-l', '--left', default=0, type=int)
    parser_crop.add_argument('-b', '--bottom', default=0, type=int)

    parser_expose = subparsers.add_parser('expose')
    parser_expose.add_argument('shift', type=int)

    parser_rotate = subparsers.add_parser('rotate')
    parser_rotate.add_argument('angle', type=int)

    args = parser.parse_args(input().split())

    if args.command == 'crop':
        do_crop(args)
    if args.command == 'expose':
        do_expose(args)
    if args.command == 'rotate':
        do_rotate(args)

if __name__ == '__main__':
    main()
