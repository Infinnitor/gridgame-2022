from util import decorators
from util.debug import Debug


@decorators.methodclass
class Sprite(Debug):
	destroy = False
	protected = False
	requires_gameref = False

	def pos(self):
		return self.x, self.y

	def update_move(self, game):
		pass

	def update_draw(self, game):
		pass

	def kill(self):
		self.destroy = True


class RectSprite(Sprite):
	def __init__(self, pos, size):
		self.x, self.y = pos
		self.w, self.h = size

	def get_rect(self):
		return (self.x, self.y, self.w, self.h)

	def get_rect_centered(self):
		return (self.x - self.w/2, self.y - self.h/2, self.w, self.h)


class CircleSprite(Sprite):
	def __init__(self, pos, size):
		self.x, self.y = pos
		self.r = size

	def get_circle(self):
		return ((self.x, self.y), self.r)
