import sys
import os


# TODO: type checking
class Arguments():
	def __init__(self, argv):
		self._argv = argv

		self.program = argv[0]
		self.args = []
		self.flags = []

		for a in argv[1:]:
			if a.startswith("-"):
				self.flags.append(a)
			else:
				self.args.append(a)

	@staticmethod
	def sys():
		return Arguments(sys.argv)

	@staticmethod
	def parse(func):
		def inner(argv):
			func(Arguments(argv))
		return inner

	@staticmethod
	def required_length(num):
		def outer(func):
			def inner(args):
				assert len(args) >= num
				func(args)
			return inner
		return outer


	def __len__(self):
		return len(self.args)

	def get(self, index):
		return None if len(self.args) >= index else self.args[index]

	def __call__(self, index):
		return self.get(index)

	def __getitem__(self, index):
		return self.args[index]

	def flagged(self, *names):
		for n in names:
			if n in self.flags:
				return True
		return False

	def flagstart(self, *names, val_sep=":", cast=None):
		for n in names:
			for f in self.flags:
				if f.startswith(n):
					s = f.split(val_sep)
					if len(s) == 2:
						return s[1] if cast is None else cast(s[1])

		return None

	def __repr__(self):
		return f"PROGRAM: {self.program}, ARGS: {self.args or 'NO ARGS'}, FLAGS: {self.flags or 'NO FLAGS'}"



def satinitised_input(message, cast):
	while True:
		u = input(message)
		try:
			return cast(u)
		except ValueError:
			print(f"Error! Input must be of type {cast.__repr__()}")


def workingdir_is_program(loc=sys.argv[0]):
	assert os.path.exists(loc), "Program path does not exist??"

	program_exec = loc.split(os.path.sep)[-1]
	fullpath = os.path.dirname(os.path.abspath(loc))

	os.chdir(fullpath)
	return fullpath
