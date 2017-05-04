import sys


class inexhaustible_generator:
    def __init__(self, generator):
        self.generator_func = generator
        self.__name__ = generator.__name__
        self.__doc__ = generator.__doc__
        self.__module = generator.__module__

    def __call__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.start_again()
        return self

    def start_again(self):
        self.generator = self.generator_func(*self.args, **self.kwargs)

    def __iter__(self):
        return self

    def __next__(self):
        try:
            next_elem = self.generator.__next__()
            return next_elem
        except StopIteration as error:
            self.start_again()
            raise error


def inexhaustible(generator):
    return inexhaustible_generator(generator)

exec(sys.stdin.read())
