from pygame import Surface, SRCALPHA
import pygame.draw

import math
from random import randint

from sprite import *
from constants import TILE_SIZE

import random
from visual_effects import decay_mut

import asset


class PlayerKillTendril(RectSprite):
	LAYER = "HIGHPARTICLE"
	c = (10, 10, 10)

	def __init__(self, pos, player):
		super().__init__(pos, (TILE_SIZE//3, TILE_SIZE//3))
		self._player = player


		self._start_pos = self._player.pos()

		self._speed = 0.5
		self._firstframe = False
		self._rects = []

	def update_move(self, game):
		if not self._firstframe:
			px, py = game.sprites.GRID.relative_pos(self._player.pos())
			a = math.atan2(self.y-py, self.x-px)

			rd = (
				math.cos(a + (math.pi/2)),
				math.sin(a + (math.pi/2))
			)

			while math.dist(self.pos(), (px, py)) > self.w:
				offset = randint(-1, 1)*(self.w//3)

				p = [
					self.x + rd[0]*offset,
					self.y + rd[1]*offset
				]

				self._rects.append(p)

				self.x += math.cos(a)*-self._speed
				self.y += math.sin(a)*-self._speed

				self._speed *= 1.1

		self._firstframe = True
		if self._player.pos() != self._start_pos:
			self._firstframe = False

	def update_draw(self, game):
		for r in self._rects:
			pygame.draw.rect(game.window, PlayerKillTendril.c, [r[0]-(self.w/2), r[1]-(self.h/2), self.w, self.h])

		if not self._rects:
			self.kill()
			return

		self._rects.pop(0)

def player_kills_tendrils(killsmap, game):
	tendrils = []

	if len(killsmap) < 2:
		return tendrils

	for k in killsmap:
		tendrils.append(PlayerKillTendril(game.sprites.GRID.relative_pos(k), game.sprites.PLAYER))

	return tendrils
