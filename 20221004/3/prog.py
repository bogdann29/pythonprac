def subtraction(obj_1, obj_2):
	if type(obj_1)() == 0:
		return obj_1 - obj_2
	
	return type(obj_1)(el for el in obj_1 if el not in obj_2)


print(subtraction(*eval(input())))

