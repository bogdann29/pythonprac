class Num:
	def __get__(self, obj, cls):
		if '_value' in dir(obj):
			return getattr(obj, '_value')
		return 0

	def __set__(self, obj, val):
		if 'real' in dir(val):
			val = val
		elif '__len__' in dir(val):
			val = len(val)
		setattr(obj, '_value', val)


import sys
exec(sys.stdin.read()) 

    