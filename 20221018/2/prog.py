from math import *

s = input().split()

str_num = 1
func = {}

while s[0] != 'quit':
	str_num += 1
	if s[0][0] == ':':
		if len(s) == 2:
			func[s[0][1:]] = eval(f'lambda: {s[-1]}')
		else:
			func[s[0][1:]] = eval(f"lambda {','.join(s[1:-1])}: {s[-1]}")
	else:
		print(func[s[0]](*[eval(i) for i in s[1:]]))
	s = input().split()

print(" ".join(s[1:]).replace('"', '').format(len(func)+1, str_num))
