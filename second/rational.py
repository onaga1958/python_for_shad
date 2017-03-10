import sys

class Rational:
    def GCD(self):
        a = self.denominator
        b = self.numerator
        while (b):
            a %= b
            b, a = a, b
        self.denominator //= a
        self.numerator //= a

        if (self.denominator < 0 and self.numerator > 0):
            self.denominator *= -1
            self.numerator *= -1

    def __init__(self, numerator=0, denominator=1):
        if denominator == 0:
            raise ValueError("zero division")
        self.numerator = numerator
        self.denominator = denominator
        self.GCD()

    def __add__(self, another):
        return Rational(self.numerator*another.denominator
                        + self.denominator*another.numerator,
                        self.denominator*another.denominator)

    def __mul__(self, another):
        return Rational(self.numerator * another.numerator,
                        self.denominator * another.denominator)

    def __sub__(self, another):
        return Rational(self.numerator*another.denominator
                        - self.denominator*another.numerator,
                        self.denominator * another.denominator)

    def __truediv__(self, another):
        return Rational(self.numerator * another.denominator,
                        self.denominator * another.numerator)

    def __eq__(self, another):
        return (self.numerator == another.numerator and
                self.denominator == another.denominator)

    def __ne__(self, another):
        return (self.numerator != another.numerator or
                self.denominator != another.denominator)

    def __neg__(self):
        return Rational(-self.numerator, self.denominator)

    def __str__(self):
        return '{}/{}'.format(self.numerator, self.denominator)

exec(sys.stdin.read())
