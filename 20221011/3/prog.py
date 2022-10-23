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

str_w = str(w_sum) + '/' + str(g_sum + w_sum)
str_g = str(g_sum) + '/' + str(g_sum + w_sum)
print(*['.' for i in range(g_sum)], ' ', str_g.rjust(max(w_sum, g_sum) - g_sum + max(len(str_w), len(str_g))), sep='')
print(*['~' for i in range(w_sum)], ' ', str_w.rjust(max(w_sum, g_sum) - w_sum + max(len(str_w), len(str_g))), sep='')
