import types

def f(name, fn, *args, **kwargs):
    def rnd(*args, **kwargs):
        print(f'{name}: {args[1:]}, {kwargs}')
        return fn(*args, **kwargs)
    return rnd

class dump(type):
    @staticmethod
    def __new__(metacls, name, parents, ns, **kwds):
        for n, value in ns.items():
            if type(value) is types.FunctionType or type(value) is types.MethodType:
                ns[n] = f(n, value)
        return super().__new__(metacls, name, parents, ns)

import sys
exec(sys.stdin.read())