import pygame.draw
from constants import SCORE_TIMER, TILE_SIZE
from particles import TextParticle

from pygame import locals as keys


def UI_combo_ticker(game):
	if game.sprites.PLAYER.destroy:
		return

	obj = game.sprites.SCORE

	x, y = game.sprites.GRID.relative_pos(game.sprites.PLAYER.pos(), center=False)

	rat = 1 - (obj._combo_ticker / SCORE_TIMER)
	pygame.draw.rect(game.window, (195, 35, 35), [x, y+(TILE_SIZE-10), TILE_SIZE*rat, 10])


def spawn_text_particles(game):
	if game.input.check_key(keys.K_f, buffer=True):
		game.sprites.new(TextParticle([game.WIDTH//2, game.HEIGHT//2], "hello", 35, (255, 255, 255)))
