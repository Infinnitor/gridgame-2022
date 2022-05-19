from sprite import *
from util import decorators


@decorators.methodclass
class FollowCollider:
	def update(self):
		self.x = self._parent.x + self._ox
		self.y = self._parent.y + self._oy


class RectCollider(RectSprite, FollowCollider):
	def __init__(self, parent, offset, size):
		self._parent = parent
		self._ox, self._oy = offset
		super().__init__(offset, size)
		self.update()


class CircleCollider(CircleSprite, FollowCollider):
	def __init__(self, parent, offset, size):
		self._parent = parent
		self._ox, self._oy = offset
		super().__init__(offset, size)
		self.update()
