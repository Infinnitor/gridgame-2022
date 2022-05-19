# Functions for dealing with RGB colours represented as tuples with length of 3/4

# Ensure that no colour value exceeds 255 or goes below 0
def safe_col(colour):
	return tuple([0 if c<0 else 0xFF if c>0xFF else c for c in colour])


# Randomize colour variance based on step
def randcol(colour, step):
	return safe_col([c + randint(-step, step) for c in colour])


def shiftcol(colour, shift):
	return safe_col([c + shift for c in colour])


def rgb(r, g, b):
	return safe_col([r, g, b])


def rgba(r, g, b, a):
	return safe_col([r, g, b, a])
