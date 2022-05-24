from sprite import *
import pygame.draw
from pygame import Surface

from random import randint
from util.base import Namespace
from util.colour import shiftcol

from constants import Tiles, TILE_SIZE


_tile_colours = {
	0 : (95, 95, 95),
	1 : (65, 65, 65),
	2 : (10, 10, 10),
	3 : (35, 35, 195)
}


class Grid(RectSprite):
	LAYER = "GRID"
	TILE_SIZE = TILE_SIZE

	def __init__(self, pos, size, squares):
		super().__init__(pos, size)
		self._squares = squares

	# Create a new grid at the correct position given the grid size
	@staticmethod
	def new(size, game):
		pos = (
			game.WIDTH/2 - (size[0]*TILE_SIZE)/2,
			game.HEIGHT/2 - (size[1]*TILE_SIZE)/2,
		)
		g = Grid(pos, size, [Tiles.Empty for s in range(size[0]*size[1])])
		for x in range(g.w):
			g.setsq([x, 0], Tiles.Wall)
			g.setsq([x, g.h-1], Tiles.Wall)

		for y in range(g.w):
			g.setsq([0, y], Tiles.Wall)
			g.setsq([g.w-1, y], Tiles.Wall)

		g.setsq([g.w//2, g.h//2], Tiles.Wall)
		g.setsq([g.w//2 - 1, g.h//2], Tiles.Wall)
		g.setsq([g.w//2, g.h//2 - 1], Tiles.Wall)
		g.setsq([g.w//2 - 1, g.h//2 - 1], Tiles.Wall)

		return g

	def _loc(self, x, y):
		return y*self.w + x

	def offset_pos(self, pos, center=True):
		if center:
			return pos[0]*TILE_SIZE + TILE_SIZE//2, pos[1]*TILE_SIZE + TILE_SIZE//2
		return pos[0]*TILE_SIZE, pos[1]*TILE_SIZE

	def relative_pos(self, pos, center=True):
		p = self.offset_pos(pos, center)
		z = (p[0] + self.x, p[1] + self.y)
		return z

	def getsq(self, pos):
		return self._squares[self._loc(*pos)]

	def setsq(self, pos, tile):
		assert Tiles.exists(tile)
		self._squares[self._loc(*pos)] = tile

	def update_move(self, game):
		pass

	def update_draw(self, game):
		RIM = 10

		for y in range(self.h):
			for x in range(self.w):
				sq = self.getsq([x, y])
				if sq != Tiles.Empty:
					continue

				pygame.draw.rect(
					game.window,
					shiftcol(_tile_colours[sq], -15),
					[self.x + x*TILE_SIZE, self.y + y*TILE_SIZE, TILE_SIZE, TILE_SIZE]
				)

				pygame.draw.rect(
					game.window,
					_tile_colours[sq],
					[self.x + x*TILE_SIZE, self.y + y*TILE_SIZE - RIM, TILE_SIZE, TILE_SIZE]
				)

		game.sprites.GORESURF.update_draw(game)

		for y in range(self.h):
			for x in range(self.w):
				sq = self.getsq([x, y])
				if sq == Tiles.Empty:
					continue

				if sq == Tiles.Player and game.sprites.PLAYER.destroy:
					continue

				r1 = [self.x + x*TILE_SIZE, self.y + y*TILE_SIZE, TILE_SIZE, TILE_SIZE]
				r2 = [self.x + x*TILE_SIZE, self.y + y*TILE_SIZE - RIM, TILE_SIZE, TILE_SIZE]

				pygame.draw.rect(
					game.window,
					shiftcol(_tile_colours[sq], -15),
					r1
				)

				pygame.draw.rect(
					game.window,
					_tile_colours[sq],
					r2
				)
