f = lambda x, y: ((x * x) % 100) < ((y * y) % 100)

l = list(eval(input()))
for i in range(1, len(l)):
	for j in range(i):
		if f(l[i],l[j]):
			l[i], l[j] = l[j], l[i]

print(l)
