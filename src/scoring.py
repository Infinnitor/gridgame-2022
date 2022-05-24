from sprite import *
from constants import SCORE_TIMER


class ScoreBoard(Sprite):
	LAYER = "MANAGER"

	def __init__(self):
		self._score = 0
		self._combo = 0
		self._combo_ticker = 0

	def increase_score(self, killsno):
		if killsno < 1:
			return

		self._score += killsno * (self._combo + 1)
		self._combo += killsno
		self._combo_ticker = 0

	def update_move(self, game):
		game.debug.display_text(f"SCORE: {self._score}")
		game.debug.display_text(f"COMBO: {self._combo}")
		game.debug.display_text(str(SCORE_TIMER - self._combo_ticker))

		if game.sprites.PLAYER.destroy is True:
			return

		self._combo_ticker += 1
		if self._combo_ticker > SCORE_TIMER:
			self._combo_ticker = 0
			self._combo = 0

	def get_score(self):
		return self._score
