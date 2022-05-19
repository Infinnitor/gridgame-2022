from time import time


def format_dict(d, indent=1):
	s = ""

	s += "\t" * (indent-1) + "{\n"
	for k, v in zip(d.keys(), d.values()):
		if type(v) == dict:
			s += format_dict(v, indent+1)
		else:
			s += "\t"*indent
			s += f"{k} : {v}\n"

	s += "\t" * (indent-1) + "}\n"
	return s


def debugattr(classf):
	classf.__repr__ = lambda self: format_dict(self.__dict__)
	return classf


class Debug():
	def __repr__(self):
		return format_dict(self.__dict__)


def timecheck(func):
	def inner(*args, **kwargs):
		start_time = time()
		val = func(*args, **kwargs)

		print(f"Function {func.__name__} took {'{:f}'.format(time()-start_time)} secs")
		return val

	return inner
