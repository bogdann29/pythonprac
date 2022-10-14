from fractions import *
def isSol(s, w, p_A, A, p_B, B):
	pol_A = A[-1]
	pow_s = type(s)(1)
	for i in range(p_A, 0, -1):
		pow_s *= s
		pol_A += pow_s * A[i-1]

	pol_B = B[-1]
	pow_s = type(s)(1)
	for i in range(p_B, 0, -1):
		pow_s *= s
		pol_B += pow_s * B[i-1]

	return((pol_A/pol_B) == w if pol_B.numerator != 0 else False)





a = input().replace(' ', '').split(',')
p_A = int(a[2])
p_B = int(a[4 + p_A])
s = Fraction(a[0])
w = Fraction(a[1])
print(isSol(s, w, p_A, [Fraction(i) for i in a[3:4+p_A]], p_B, [Fraction(i) for i in a[-p_B-1:]]))

 