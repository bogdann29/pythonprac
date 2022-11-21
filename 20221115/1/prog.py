def objcount(cls):
	cls.counter = 0

	cls.__init = cls.__init__
	
	def n_init(self, *args):
		cls.counter += 1
		cls.__init(self, *args)

	cls.__init__ = n_init
	
	if '__del__' in dir(cls):
		cls.__del = cls.__del__
	else:
		cls.__del = lambda self, *args: None

	def n_del(self, *args):
		cls.counter -= 1
		cls.__del(self, *args)
	cls.__del__ = n_del

	return cls

import sys
exec(sys.stdin.read())