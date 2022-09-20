a = eval(input())
s = "A"

if a % 25 == 0:
	if a % 2 == 0:
		s += " + B - "
	else:
		s += " - B + "
else:
	s += " - B - "
if a % 8 == 0:
	s += "C +"
else:
	s += "C -"

print(s)