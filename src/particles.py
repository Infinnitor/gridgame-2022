from sprite import *
import math
from random import randint

import pygame.draw

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


@kwargsdefaults(radius=15, speed=5, colour=(10, 10, 10))
def explosion(num, pos, **kwargs):
	parts = []
	for n in range(num):
		kwargs["angle"] = randint(0, 360)
		parts.append(Particle(pos, **kwargs))

	return parts
