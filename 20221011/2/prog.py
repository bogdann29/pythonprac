from math import *

def print_gr(W, H, A, B, f):
	screen = [['.'] * W for i in range(H)]

	ar = [f(A + i/(W - 1) * (B - A)) for i in range(W)]
	
	max_f = max(*ar)
	min_f = min(*ar)

	#print(max_f, min_f, sep='  ')
	dist = max_f - min_f
	prev = 0
	for i in range(W):
		x = H - round((ar[i]-min_f)*(H-1)/dist) - 1
		screen[x][i] = '*'
		if i != 0:
			for j in range(min(x,prev)+1, max(x,prev)):
				screen[j][i-1] = '*'
		prev = x

	output = '\n'
	for st in screen:
		output += ''.join(st) + '\n'
	print(output)

data = input().split()
print_gr(*[eval(d) for d in data[:-1]], lambda x: eval(data[-1]))