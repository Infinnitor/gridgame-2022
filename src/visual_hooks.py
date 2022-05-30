import pygame.draw
from constants import SCORE_TIMER, TILE_SIZE


def UI_combo_ticker(game):
	if game.sprites.PLAYER.destroy:
		return

	obj = game.sprites.SCORE

	x, y = game.sprites.GRID.relative_pos(game.sprites.PLAYER.pos(), center=False)

	rat = 1 - (obj._combo_ticker / SCORE_TIMER)
	pygame.draw.rect(game.window, (195, 35, 35), [x, y+(TILE_SIZE-10), TILE_SIZE*rat, 10])
