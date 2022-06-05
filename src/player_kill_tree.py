from pygame import Surface, SRCALPHA
import pygame.draw
import math

from sprite import *
from constants import TILE_SIZE

import random
from visual_effects import decay_mut

import asset


class PlayerKillMarker(RectSprite):
	LAYER = "GORE"

	def __init__(self, pos, size):
		super().__init__(pos, size)
		self.c = (10, 10, 10)
		self.speed = 1

	def update_move(self, game):
		px, py = game.sprites.GRID.relative_pos(game.sprites.PLAYER.pos())
		if math.dist([px, py], self.pos()) < self.w:
			self.kill()

		a = math.atan2(py-self.y, px-self.x)

		self.x += math.cos(a) * self.speed
		self.y += math.sin(a) * self.speed

		self.speed *= 1.05

	def update_draw(self, game):
		pygame.draw.rect(game.window, self.c, self.get_rect())



def player_kill_tree_collection(killsmap, game):
	objs = []
	for kill in killsmap:
		objs.append(PlayerKillMarker(game.sprites.GRID.relative_pos(kill), [TILE_SIZE//2, TILE_SIZE//2]))

	return objs
