from sprite import *
import math
from random import randint

from pygame import Surface, SRCALPHA
import pygame.draw
import pygame.font

from util.decorators import kwargsdefaults


class Particle(CircleSprite):
	LAYER = "HIGHPARTICLE"

	def __init__(self, pos, radius, angle, speed, colour):
		super().__init__(pos, radius)
		self.angle = angle
		self.speed = speed

		self.xmove = math.cos(self.angle) * self.speed
		self.ymove = math.sin(self.angle) * self.speed

		self.c = colour

	def update_move(self, game):
		self.x += self.xmove
		self.y += self.ymove

		self.r -= 0.5
		if self.r < 1:
			self.kill()

	def update_draw(self, game):
		pygame.draw.circle(game.window, self.c, (self.x, self.y), self.r)


class TextParticle(RectSprite):
	LAYER = "HIGHPARTICLE"

	def __init__(self, pos, text, text_size, colour=(255, 255, 255), lifetime=45, font=None):
		self.x, self.y = pos
		self._text = text
		self._fontsize = text_size
		self.c = colour

		self._font = pygame.font.Font(None, self._fontsize) if font is None else font

		self._surface = self._font.render(self._text, True, self.c)
		self.w, self.h = self._surface.get_size()

		self._lifetime = lifetime
		self._decay_point = self._lifetime - self._lifetime//3
		self._decay_amt = (self._surface.get_height() // self._decay_point) + 1
		self._decay = 0

		print(self)

	def update_move(self, game):
		self._lifetime -= 1
		if self._lifetime < self._decay_point:
			self._decay += self._decay_amt
			pygame.draw.rect(self._surface, (255, 0, 255), (0, self.h-self._decay, self.w, self._decay))
			self._surface.set_colorkey((255, 0, 255))

		if self._lifetime < 1:
			self.kill()

		self.y -= 0.5

	def update_draw(self, game):
		game.window.blit(self._surface, [
			self.x - self.w/2,
			self.y - self.h/2
		])


@kwargsdefaults(radius=15, speed=5, colour=(10, 10, 10))
def explosion(num, pos, **kwargs):
	parts = []
	for n in range(num):
		kwargs["angle"] = randint(0, 360)
		parts.append(Particle(pos, **kwargs))

	return parts
