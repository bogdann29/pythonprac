l1 = []
l1.append(list(eval(input())))
ln = len(l1[0])

for i in range(ln - 1):
	l1.append(list(eval(input())))

l2 = []
for i in range(ln):
	l2.append(list(eval(input())))

res = []
t = 0
for i in range(ln):
	res.append([])
	for j in range(ln):
		s = 0
		for k in range(ln):
			s += l1[i][k] * l2[k][j]
		res[-1].append(s)
	t += 1

for i in res:
	print(*i, sep=',')
