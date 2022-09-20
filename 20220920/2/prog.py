s = 0
a = eval(input())
while a > 0:
	s += a
	if s > 21:
		print(s)
		break
	a = eval(input())
else:
	print(a)
