"""Cut several fields from the file."""


import argparse
import sys


class TableError(Exception):
    pass


class Table(object):
    def __init__(self, rows=()):
        self.rows = list(rows)

    def head(self, count=10):
        return Table(self.rows[:count])

    def tail(self, count=10):
        return Table(self.rows[-count:])

    def select_columns(self, indices):
        new_rows = []
        for row in self.rows:
            try:
                new_row = [row[i] for i in indices]
            except IndexError:
                raise TableError("Row has too few fields.")
            new_rows.append(new_row)
        return Table(new_rows)

    def paste(self, other):
        new_rows = []
        for row, row_other in zip(self.rows, other.rows):
            new_rows.append(row + row_other)
        return Table(new_rows)

    def concatenate(self, other):
        return Table(self.rows + other.rows)

    def __add__(self, other):
        return self.concatenate(other)

    def extend(self, other):
        self.rows += other.rows

    def __iadd__(self, other):
        self.extend(other)

    def __getitem__(self, index):
        return self.rows[index]

    def __str__(self):
        return '\n'.join('\t'.join([str(el) for el in row])
                         for row in self.rows)

    def write(self, delimiter='\t', file=sys.stdout):
        for row in self.rows:
            file.write(delimiter.join([str(el) for el in row]) + '\n')


def parse_row(text, delimiter='\t'):
    return text.split(delimiter)


def read_table(filename, delimiter='\t'):
    rows = []
    try:
        with open(filename) as f:
            for line in f:
                rows.append(parse_row(line.strip(), delimiter))
    except IOError:
        raise TableError("Input file " + filename + " not found.")
    return Table(rows)


def build_fields_list(fields_str):
    try:
        return [int(field) for field in fields_str.split(',')]
    except ValueError:
        raise TableError("Some fields cannot be parsed as integer.")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--separator', metavar='TEXT', default='\t',
                        help="fields separator")

    subparsers = parser.add_subparsers(dest='command')

    parser_cut = subparsers.add_parser('cut', help='Cut columns from table.')
    parser_cut.add_argument('filename', help="path to the file to work with")
    parser_cut.add_argument('-f', '--fields', metavar='LIST', required=True,
                            help="fields to cut from the file")

    parser_paste = subparsers.add_parser('paste',
                                         help='Join table by columns.')
    parser_paste.add_argument('first_file')
    parser_paste.add_argument('second_file')

    parser_head = subparsers.add_parser('head', help='Get several first rows.')
    parser_head.add_argument('filename', help="path to the file to work with")
    parser_head.add_argument('-n', '--size', metavar='NUM', required=True,
                             type=int, help="How many rows to get.")

    parser_tail = subparsers.add_parser('tail', help='Get several last rows.')
    parser_tail.add_argument('filename', help="path to the file to work with")
    parser_tail.add_argument('-n', '--size', metavar='NUM', required=True,
                             type=int, help="How many rows to get.")

    args = parser.parse_args()

    try:
        if args.separator in ['\n', '']:
            raise TableError("Invalid field separator.")

        if args.command == 'cut':
            table = read_table(args.filename, args.separator)
            fields = build_fields_list(args.fields)
            table_cut = table.select_columns(fields)
            table_cut.write(args.separator)
        elif args.command == 'paste':
            table1 = read_table(args.first_file, args.separator)
            table2 = read_table(args.second_file, args.separator)
            table_pasted = table1.paste(table2)
            table_pasted.write(args.separator)
        elif args.command == 'head':
            table = read_table(args.filename, args.separator)
            table_head = table.head(args.size)
            table_head.write(args.separator)
        elif args.command == 'tail':
            table = read_table(args.filename, args.separator)
            table_tail = table.tail(args.size)
            table_tail.write(args.separator)

    except TableError as e:
        parser.error(e.message)


if __name__ == '__main__':
    main()