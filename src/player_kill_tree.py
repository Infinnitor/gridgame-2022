from pygame import Surface, SRCALPHA
import pygame.draw

import math
from random import randint

from sprite import *
from constants import TILE_SIZE


class PlayerKillTree(RectSprite):
	LAYER = "UI"

	def __init__(self, killsmap, game):
		self._kills = killsmap
		kr = [*self._kills[0], *self._kills[0]]

		for k in self._kills:
			x, y = k
			kr[0] = x if x < kr[0] else kr[0]
			kr[1] = y if y < kr[1] else kr[1]
			kr[2] = x if x > kr[2] else kr[2]
			kr[3] = y if y > kr[3] else kr[3]

		# TODO: Organise self._kills into a 2d array of True and False to allow for sprite complexity
		self._killsmap = [[False for x in range(kr[2])] for y in range(kr[3])]

		for k in self._kills:
			x, y = k[0]-kr[0], k[1]-kr[1]
			self._killsmap[y][x] = True

		self.x, self.y = game.sprites.GRID.relative_pos(kr[:2], center=False)
		self.w = (kr[2]-kr[0]+1)*TILE_SIZE
		self.h = (kr[3]-kr[1]+1)*TILE_SIZE

		self._surface = Surface((self.w, self.h), SRCALPHA)
		for y in range(len(self._killsmap)):
			for x in range(len(self._killsmap[y])):
				if self._killsmap[y][x]:
					br = [
						x*TILE_SIZE + 10,
						y*TILE_SIZE + 10,
						TILE_SIZE - 20,
						TILE_SIZE - 20
					]

					clr = [35, 35, 35]
					if self._killsmap_check([x+1, y]) or self._killsmap_check([x-1, y]):
						clr[0] = 155
					if self._killsmap_check([x, y+1]) or self._killsmap_check([x, y-1]):
						clr[1] = 155

					pygame.draw.rect(self._surface, clr, br)


		self._lifetime = 60

	def _killsmap_check(self, pos):
		try:
			return self._killsmap[pos[1]][pos[0]]
		except IndexError:
			return False

	def update_move(self, game):
		self._lifetime -= 1
		if self._lifetime < 1:
			self.kill()

	def update_draw(self, game):
		game.window.blit(self._surface, self.pos())



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

def player_kills_locs(killsmap, game):
	tendrils = []

	if len(killsmap) < 2:
		return tendrils

	for k in killsmap:
		tendrils.append(PlayerKillTendril(game.sprites.GRID.relative_pos(k), game.sprites.PLAYER))

	return tendrils
