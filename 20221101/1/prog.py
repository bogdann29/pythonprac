from collections import defaultdict

class Omnibus:
	def __init__(self):
		pass

	def __setattr__(self, name, value):
		if name not in self.__dict__:
			self.__dict__[name] = value
			Omnibus.dct[name] += 1

	def __getattribute__(self, name):
		if name in Omnibus.dct:
			return Omnibus.dct[name]
		return object.__getattribute__(self, name)

	def __delattr__(self, name):
		if name in self.__dict__:
			Omnibus.dct[name] -= 1
			self.__dict__.pop(name)
	
	def __del__(self):
		for k in self.__dict__:
			Omnibus.dct[k] -= 1 
   
	dct = defaultdict(int)

import sys
exec(sys.stdin.read())