def dig_sum(n: int) -> int:
	s = 0
	while n > 0:
		s += n % 10
		n = n // 10
	return s

k = n = eval(input())

while n < k + 3:
	m = k
	while m < k + 3:
		tmp = m * n
		print(f'{n} * {m} =', tmp if dig_sum(tmp) != 6 else ':=)', end = ' ')
		m += 1
	print('\n')
	n += 1