from collections import Counter

w = int(input())

txt = ''
try:
	while s := input():
		s = s.lower()
		for i in s:
			if i.isalpha():
				txt += i
			else:
				txt += ' '
except Exception:
	pass

if txt:
	word_list = txt.split()
	d = dict(Counter([word for word in word_list if len(word) == w]))
	m = max(d.values())
	print(*sorted([k for k,v in d.items() if v == m]))

