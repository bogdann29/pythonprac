import collections
import sys

class DivStr(collections.UserString):
    def __init__(self, s=''):
        super().__init__(s)

    def __floordiv__(self, n):
        ln = len(self) // n
        return iter(self[i:i + ln] for i in range(0, ln * n, ln))

    def __mod__(self, n):
        return self[-(len(self) % n):]


exec(sys.stdin.read())
