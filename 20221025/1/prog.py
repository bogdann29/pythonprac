def fib_gen(n, m):
	n1, n2 = 0, 1
	if n == 0:
		yield 1
	for i in range(1, m+1):
		t = n1 + n2
		n1 = n2
		n2 = t
		if i >= n:
			yield n2

a, b = eval(input())
h = fib_gen(a, b)
for i in range(a,b+1):
	print(next(h))