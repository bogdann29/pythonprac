def dominate(pair_1, pair_2):
	return (pair_1[0] <= pair_2[0] and pair_1[1] < pair_2[1]) or (pair_1[0] < pair_2[0] and pair_1[1] <= pair_2[1])

def Pareto(*pairs):
	if len(pairs) == 2 and type(pairs[0]) != 'tuple':
		return pairs
	res = [p for p in pairs if all([not dominate(p,x) for x in pairs])]
	return tuple(res)

print(Pareto(*eval(input())))