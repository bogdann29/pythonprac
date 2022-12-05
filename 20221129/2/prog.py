import types
import inspect
import typing

class check(type):
	@staticmethod
	def __new__(metacls, name, parents, ns, **kwds):
		def check_annotations(self, *args):
			ann = inspect.get_annotations(self.__class__)
			for n, value in ann.items():
				#print(n ,value)
				try:
					if type(value) == types.GenericAlias:
						if not isinstance(getattr(self, n), typing.get_origin(value)):
							break
					elif not isinstance(getattr(self, n), value):
						break
				except AttributeError:
					break
			else:
				return True
			return False

		ns["check_annotations"] = check_annotations
		return super().__new__(metacls, name, parents, ns)

import sys
exec(sys.stdin.read())