from sprite import *
from constants import SCORE_TIMER, TILE_SIZE

import pygame.draw
from particles import TextParticle


class ScoreBoard(Sprite):
	LAYER = "UI"

	def __init__(self):
		self._score = 0
		self._combo = 0
		self._combo_ticker = 0

	def increase_score(self, killsmap, game):
		killsno = len(killsmap)

		if killsno < 1:
			return

		for pos in killsmap:
			x, y = game.sprites.GRID.relative_pos(pos, center=True)
			tp = TextParticle([x, y], str(self._combo + 1), 40, (255, 255, 255))
			tp.LAYER = "UI"

			game.sprites.new(tp)

		self._score += killsno * (self._combo + 1)
		self._combo += killsno
		self._combo_ticker = 0


	def update_move(self, game):
		game.debug.display_text(f"SCORE: {self._score}")
		game.debug.display_text(f"COMBO: {self._combo}")
		# game.debug.display_text(str(SCORE_TIMER - self._combo_ticker))

		if game.sprites.PLAYER.destroy is True:
			return

		self._combo_ticker += 1
		if self._combo_ticker > SCORE_TIMER:
			self._combo_ticker = 0
			self._combo = 0

	# def update_draw(self, game):
	# 	x, y = game.sprites.GRID.relative_pos(game.sprites.PLAYER.pos(), center=False)
	#
	# 	rat = 1 - (self._combo_ticker / SCORE_TIMER)
	# 	pygame.draw.rect(game.window, (195, 35, 35), [x, y+(TILE_SIZE-10), TILE_SIZE*rat, 10])

	def get_score(self):
		return self._score
