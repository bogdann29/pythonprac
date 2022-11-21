def bin_search(elem, seq):
	ln = len(seq)
	if ln == 1 and seq[0] != elem:
		return False
	if seq[(ln-1)//2] == elem:
		return True
	elif seq[(ln-1)//2] > elem:
		return bin_search(elem, seq[:(ln-1)//2])
	return bin_search(elem, seq[(ln-1)//2 + 1:])

print(bin_search(*eval(input())))
