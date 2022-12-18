def dig_sum(n: int) -> int:
	s = 0
	while n > 0:
		s += n % 10
		n = n // 10
	return s

k = n = eval(input())

while n < k + 3:
	m = k
	s = []
	while m < k + 3:
		tmp = m * n
		pr = str(tmp) if dig_sum(tmp) != 6 else ':=)'
		s.append(f'{n} * {m} = ' + pr)
		m += 1
	print(" ".join(s))
	n += 1
