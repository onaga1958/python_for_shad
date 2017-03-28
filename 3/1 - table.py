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
            new_row = [row[i] for i in indices if i < len(row)]
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


def parse_row(text, delimiter='\t'):
    return text.split(delimiter)


def read_table(filename, delimiter='\t'):
    rows = []
    with open(filename) as f:
        for line in f:
            rows.append(parse_row(line.strip(), delimiter))
    return Table(rows)


def main():
    t1 = Table([[1, 2], [3, 4]])
    t2 = Table([['hi', 10, []], [11, 12, 13], ['a', 'b', 'c']])
    print t1
    print
    print t2
    print
    print t1.head(1)
    print
    print t2.tail(2)
    print
    print t2.select_columns([2, 0, 0])
    print
    print t1.paste(t2)
    print
    print t1 + t2
    print
    print t2[2]


main()
