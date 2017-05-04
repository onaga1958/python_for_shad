import sys


def unique(iterable):
    previous = None
    for current in iterable:
        if current != previous:
            previous = current
            yield current

exec(sys.stdin.read())
