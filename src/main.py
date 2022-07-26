#!/usr/bin/python3
import sys
import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"

from gameref import GameNamespace, gameloop
import pygame
import asset

from using_sprites import *
from game_hooks import *
from visual_effects import *


@gameloop
def main(game):
	game.sprites.purge()
	game.hooks.clear()

	game.sprites.GRID = Grid.new((10, 10), game)
	game.sprites.new(game.sprites.GRID)

	game.sprites.PLAYER = Player([1, 1])
	game.sprites.new(game.sprites.PLAYER)
	for x in range(game.sprites.PLAYER.x+1, game.sprites.PLAYER.x+5):
		game.sprites.new(Enemy([x, game.sprites.PLAYER.y]))
	for x in range(game.sprites.PLAYER.x+1, game.sprites.PLAYER.x+4):
		game.sprites.new(Enemy([x, game.sprites.PLAYER.y+1]))


	# game.sprites.new(Enemy.new(game))

	game.sprites.GORESURF = GoreSurface.from_grid(game.sprites.GRID)

	game.sprites.SPAWNER = EnemySpawner()
	game.sprites.new(game.sprites.SPAWNER)

	game.sprites.SCORE = ScoreBoard()
	game.sprites.new(game.sprites.SCORE)

	game.sprites.ENEMYAUTH = EnemyMoveAuth()
	game.sprites.new(game.sprites.ENEMYAUTH)

	game.hooks.new(UI_combo_ticker, pre=False)

	game.hooks.new(reset_hook(main))
	game.hooks.new(fps_hook)

if __name__ == "__main__":

	g = GameNamespace([1280, 720])
	g.init_display([1280, 720], name="H I T")
	g.init_input()
	g.init_sprites("ENEMYVISUALS", "PLAYER", "MANAGER", "ENEMY", "GRID", "SNIPER", "GORE", "HIGHPARTICLE", "FOREGROUND", "UI")
	g.init_clock(60)
	# g.init_clock(60 if len(sys.argv) < 2 else int(sys.argv[1]))
	g.init_hooks()
	g.init_audio(sfx={
		"walk" : "data/sfx/walk.wav",
		"attack" : "data/sfx/attack.wav",
		"hit" : "data/sfx/hit.wav",
		"snipe" : "data/sfx/snipe.wav",
		"err" : "data/sfx/err.wav",
	})
	g.init_debug(fontsize=60)

	asset.init_assets()
	main(g)
