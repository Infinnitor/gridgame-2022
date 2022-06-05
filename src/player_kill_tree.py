from pygame import Surface, SRCALPHA
import pygame.draw

from sprite import *
from constants import TILE_SIZE

import random
from visual_effects import decay_mut

import asset


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
					bpos = [
						x*TILE_SIZE,
						y*TILE_SIZE
					]

					if self._killsmap_check([x+1, y]):
						self._surface.blit(asset.vfx_killsmap.RIGHT, bpos)
					if self._killsmap_check([x-1, y]):
						self._surface.blit(asset.vfx_killsmap.LEFT, bpos)
					if self._killsmap_check([x, y+1]):
						self._surface.blit(asset.vfx_killsmap.DOWN, bpos)
					if self._killsmap_check([x, y-1]):
						self._surface.blit(asset.vfx_killsmap.UP, bpos)

					# clr = [35, 35, 35]
					# if self._killsmap_check([x+1, y]) or self._killsmap_check([x-1, y]):
					# 	clr[0] = 155
					# if self._killsmap_check([x, y+1]) or self._killsmap_check([x, y-1]):
					# 	clr[1] = 155
					#
					# # Green = above/below
					# # Red = left/right
					# # Yellow = left/right + above/below
					#
					# pygame.draw.rect(self._surface, clr, br)


		self._lifetime = 60
		self._decay_rate = self._lifetime*10

	def _killsmap_check(self, pos):
		try:
			return self._killsmap[pos[1]][pos[0]]
		except IndexError:
			return False

	def update_move(self, game):
		self._lifetime -= 1
		if self._lifetime < 1:
			self.kill()

		if self._lifetime < 40:
			if not decay_mut(self._surface, self._decay_rate):
				self.kill()


	def update_draw(self, game):
		game.window.blit(self._surface, self.pos())
