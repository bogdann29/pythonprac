from itertools import tee, islice

def slide(seq, n):
	its = list(tee(seq,len(seq)))
	for i in range(len(seq)):
		s = islice(its[i], i, i+n)
		yield from s
		i += 1

import sys
exec(sys.stdin.read())