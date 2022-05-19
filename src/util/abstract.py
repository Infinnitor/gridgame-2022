class ExposeDict():
	def __getitem__(self, key):
		return self.__dict__[key]
