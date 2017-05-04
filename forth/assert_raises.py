import sys


class AssertRaises:
    def __init__(self, error_type):
        self.error_type = error_type

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        if not isinstance(exc_val, self.error_type):
            raise AssertionError
        else:
            return True

exec(sys.stdin.read())
