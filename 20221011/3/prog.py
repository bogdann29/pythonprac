from math import *

d = []
d.append(list(input()))
while((st := list(input())) and any([st[i] != '#' for i in range(len(st))])):
	d.append(st)
d.append(st)

g_sum = 0
for i in range(1,len(d)):
	for j in range(len(d[0])):
		if d[i][j] == '.':
			g_sum += 1
		elif d[i][j] == '~':
			break

height = len(d) - 2
width = len(d[0]) - 2
w_sum = width * height - g_sum

stb = ceil(w_sum/height)

for i in range(1,width+1):
	for j in range(1,height+1):
		if i <= width-stb:
			d[j][i] = '.'
		else:
			d[j][i] = '~'

for i in range(len(d[0])):
	out = ''
	for j in range(len(d)):
		out += d[j][i]
	print(out)

new_w = stb * height
new_g = width * height - new_w

str_w = str(new_w) + '/' + str(new_g + new_w)
str_g = str(new_g) + '/' + str(new_g + new_w)
print(*['.' for i in range(new_g)], ' ', str_g.rjust(max(new_w, new_g) - new_g + max(len(str_w), len(str_g))), sep='')
print(*['~' for i in range(new_w)], ' ', str_w.rjust(max(new_w, new_g) - new_w + max(len(str_w), len(str_g))), sep='')
