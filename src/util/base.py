class Namespace():
	def __init__(self, **kwargs):
		self.__dict__ = kwargs

	def __iter__(self):
		return zip(self.__dict__.keys(), self.__dict__.values())

	def __repr__(self):
		return repr(self.__dict__)


class NamespaceRecursive():
	def __init__(self, **kwargs):
		self.__dict__ = kwargs

		# Iterate over values from JSON file and convert them to NamespaceRecursive if they are dictionaries
		for k, v in self:
			if type(v) == dict:
				self.__dict__[k] = NamespaceRecursive(**v)
			if type(v) == list:
				if v and all([type(i) == dict for i in v]):
					self.__dict__[k] = [NamespaceRecursive(**i) for i in v]

	# Convert NamespaceRecursive to dictionary
	def to_dictionary(self):
		new_dict = self.__dict__
		for k, v in self:
			if type(v) == NamespaceRecursive:
				new_dict[k] = v.to_dictionary()
			if type(v) == list:
				if v and all([type(i) == NamespaceRecursive for i in v]):
					new_dict[k] = [i.to_dictionary() for i in v]
		return new_dict

	def __iter__(self):
		return self.__dict__.items()

	def __repr__(self):
		return self.to_dictionary().__repr__()


def trycast(v, cast):
	try:
		return cast(v)
	except ValueError:
		return False


def normalize(x):
	return -1 if x < 0 else 1 if x > 0 else 0


def bound_str(s, l):
	return s if len(s) <= l else s[:l]


def bounded(val, limit):
	return val if val <= limit else limit


def error(b, e=AssertionError, message=""):
	if not b:
		raise e(message)


def float_range(*values):
	error(len(values) > 0, TypeError, message="float_range(): missing 1 required argument")

	if len(values) == 1:
		values = (0, values[0], 1)
	elif len(values) == 2:
		values = (values[0], values[1], 1)

	start, stop, step = values
	i = start
	while i < stop:
		yield i
		i += step
