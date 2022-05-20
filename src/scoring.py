from sprite import *


class ScoreBoard(Sprite):
	COMBO_TICKER_LENGTH = 60
	LAYER = "MANAGER"

	def __init__(self):
		self._score = 0
		self._combo = 0
		self._combo_ticker = 0

	def increase_score(self, killsno):
		self._score += killsno * (self._combo + 1)
		self._combo += killsno
		self._combo_ticker = 0 if killsno else self._combo_ticker

	def update_move(self, game):
		self._combo_ticker += 1
		if self._combo_ticker > ScoreBoard.COMBO_TICKER_LENGTH:
			self._combo_ticker = 0
			self._combo -= 1 if self._combo > 0 else 0
		print(self._combo, end="\r")

	def get_score(self):
		return self._score
