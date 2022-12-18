def fib(m, n):
	n1, n2 = 0, 1
	if m == 0:
		yield 1
	for i in range(1,n+m):
		t = n1 + n2
		n1 = n2
		n2 = t
		if i >= m:
			yield n2

import sys
exec(sys.stdin.read())
