class Alpha:
	__slots__ = [chr(i) for i in range(ord('a'), ord('z') + 1)]

	def __init__(self, **kwargs):
		for k,v in kwargs.items():
			setattr(self, k, v)

	def __str__(self):
		res = []
		for l in self.__slots__:
			if hasattr(self, l):
				res.append(f'{l}: {getattr(self, l)}')
		return ', '.join(res)



class AlphaQ:
	def __init__(self, **kwargs):
		for k,v in kwargs.items():
			setattr(self, k, v)

	def __getattr__(self, key):
		if key >= 'a' and key <= 'z' and len(key) == 1:
			return self.__dict__[key]
		raise AttributeError
	
	def __setattr__(self, key, value):
		if key >= 'a' and key <= 'z'  and len(key) == 1:
			self.__dict__[key] = value
		else:
			raise AttributeError


	def __str__(self):
		res = []
		for k,v  in self.__dict__.items():
			res.append(f'{k}: {v}')
		return ', '.join(sorted(res))

import sys
exec(sys.stdin.read())