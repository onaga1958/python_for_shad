class TableException(BaseException):
    pass

class WrongIndexException(TableException):
    pass

class WrongShapeException(TableException):
    pass


class Table:
    """2d Table"""
    def __init__(self, rows=[]):
        self.rows = rows

    def Tail(self, count=1):
        """Returns table which contains last count rows of self.
        If table is too small for this count throws exception"""
        try:
            return Table(self.rows[-count:])
        except IndexError:
            print("table too small for this count")
            raise WrongIndexException()

    def Head(self, count=1):
        """Returns table which contains first count rows of self.
        If table is too small for this count throws exception"""
        try:
            return Table(self.rows[:count])
        except IndexError:
            print("table too small for this count")
            raise WrongIndexException()

    def SelectRows(self, indexes):
        """Returns table which contains listed rows of self.
        If some index is invalid throws exception"""
        try:
            return Table([self.rows[i] for i in indexes]) 
        except IndexError:
            print("wrong indexes")
            raise WrongIndexException()

    def SelectCols(self, indexes):
        """Returns table which contains listed columns of self.
        If there is at least one row without suitable elements throws exception"""
        result = []
        try:
            for row in self.rows:
                result.append([row[i] for i in indexes])
            return Table(result)
        except:
            print("wrong indexes")
            raise WrongIndexException()

    def ConcatRows(self, another):
        """Returns table which contains concatination of rows of two tables"""
        return Table(self.rows + another.rows)

    def ConcatCols(self, another):
        """Returns table which contains concatination of columns of two tables"""
        result = []
        for i in range(max(len(self.rows), len(another.rows))):
            selfRow = self.rows[i] if i < len(self.rows) else []
            anotherRow = another.rows[i] if i < len(another.rows) else []
            result.append(selfRow + anotherRow)
        return Table(result)

    def __str__(self):
        return "\n".join([" ".join(map(str, row)) for row in self.rows])


if __name__ == '__main__':
    t1 = Table([[1, 0], [0, 1]])
    t2 = Table([[0, 0, 0], [0, 0, 0]])

    print(t1)
    print()
    print(t2)
    print()
    print(t1.ConcatCols(t2))
    print()
    print(t1.ConcatRows(t2))
    print()
    print(t2.SelectCols([1, 2]))
    print()
    print(t1.SelectRows([1]))

