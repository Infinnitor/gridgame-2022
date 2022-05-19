# ---- CLASS DECORATORS ----
def methodclass(classf):
	def method_class_warn(obj, *args, **kwargs):
		msg = f"Class {classf.__name__} is a method collection meant to be inherited. It does not have a constructor"
		raise TypeError(msg)

	classf.__init__ = method_class_warn
	return classf


def staticclass(classf):
	def static_class_warn(obj, *args, **kwargs):
		msg = f"Class {classf.__name__} is static and cannot use a constructor"
		raise TypeError(msg)

	classf.__init__ = static_class_warn
	return finalclass(classf)


def finalclass(classf):
	# No args because __init_subclass__ ??
	def final_class_warn():
		msg = f"Class {classf.__name__} is final and cannot be inherited"
		raise TypeError(msg)

	classf.__init_subclass__ = final_class_warn
	return classf


def copyclass(classf):
	def init_capture(func):
		def inner(self, *args, **kwargs):
			func(self, *args, **kwargs)
			self.__CACHEARGS = [args, kwargs]
		return inner

	def copy_method(self):
		return classf(*self.__CACHEARGS[0], **self.__CACHEARGS[1])

	classf.__init__ = init_capture(classf.__init__)
	classf.copy = copy_method
	return classf


# ---- FUNCTION DECORATORS ----
def kwargsdefaults(**defaults):
	def outer(func):
		def inner(*args, **kwargs):
			for d in defaults:
				if d not in kwargs:
					kwargs[d] = defaults[d]
			return func(*args, **kwargs)
		return inner
	return outer


def errorconv(a, b, message=None):
	def outer(func):
		def inner(*args, **kwargs):
			try:
				return func(*args, **kwargs)
			except a:
				raise b(message) from a
		return inner
	return outer
