from math import *

def calc(s, t, u):
	x = lambda x: eval(s)
	y = lambda x: eval(t)
	f = lambda x, y: eval(u)
	return lambda s: f(x(s), y(s))

F = calc(*eval(input()))
print(F(eval(input())))

