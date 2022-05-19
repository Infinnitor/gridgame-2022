from sprite import *
from pygame import Surface, SRCALPHA
import pygame.draw

import math
from random import randint


# Surface for storing gore pixels
class GoreSurface(RectSprite):
	LAYER = "GORE"

	def __init__(self, pos, size):
		super().__init__(pos, size)
		self.surface = Surface(size, SRCALPHA)
		# self.surface.fill((195, 35, 195))

	@staticmethod
	def from_grid(grid):
		return GoreSurface(grid.pos(), [grid.w*grid.TILE_SIZE, grid.h*grid.TILE_SIZE])

	def update_draw(self, game):
		game.window.blit(self.surface, self.pos())


# Gorebit that renders pixels to the GoreSurface
class Gore(RectSprite):
	LAYER = "GORE"

	# Takes similar arguments to a particle
	def __init__(self, pos, angle, speed, lifetime, parent):
		self.x, self.y = pos

		self.angle = angle
		self.speed = speed

		self.xmove = math.cos(self.angle)
		self.ymove = math.sin(self.angle)

		self._life = lifetime
		self._parent = parent

	# Staticmethod for creating a group of gorebits in an arc
	@staticmethod
	def goresplash(pos, a_range, parent):
		gores = []
		for n in range(randint(15, 25)):
			gores.append(Gore(pos, math.radians(randint(*a_range)), randint(5, 10), 20, parent))
		return gores

	def _get_colour(self):
		return (35, 35, 35 + (self.speed*10))

	def update_move(self, game, r=False):
		self.x += self.xmove * self.speed
		self.y += self.ymove * self.speed

		self.speed -= self.speed/self._life
		if self.speed < 1:
			self.kill()

		if not r:
			self.update_draw(game)
			self.update_move(game, r=True)

	def update_draw(self, game):
		sp = int(self.speed*2)

		# Rect size is based on speed
		br = (
			self.x + randint(sp*-2, sp*2), # Randomized position offset
			self.y + randint(sp*-2, sp*2),
			self.speed*4,
			self.speed*4,
		)

		pygame.draw.rect(self._parent.surface, self._get_colour(), br)
