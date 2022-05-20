#!/usr/bin/python3
import sys
import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"

from gameref import GameNamespace, gameloop
import pygame

from grid import Grid
from playerclass import Player
from enemies import Enemy, EnemySpawner, Sniper

import gore
from scoring import ScoreBoard

from textsprite import NoneFontSprite


@gameloop
def main(game):
	game.sprites.purge()

	game.sprites.GRID = Grid.new((10, 10), game)
	game.sprites.new(game.sprites.GRID)

	game.sprites.PLAYER = Player([1, 1])
	game.sprites.new(game.sprites.PLAYER)
	game.sprites.new(Enemy.new(game))

	game.sprites.GORESURF = gore.GoreSurface.from_grid(game.sprites.GRID)

	game.sprites.SPAWNER = EnemySpawner()
	game.sprites.new(game.sprites.SPAWNER)

	game.sprites.SCORETEXT = NoneFontSprite([125, 100], "0", True)
	game.sprites.COMBOTEXT = NoneFontSprite([125, 200], "0", True)
	game.sprites.COMBOTICK = NoneFontSprite([100, 300], "0", True)

	game.sprites.new(game.sprites.SCORETEXT)
	game.sprites.new(game.sprites.COMBOTEXT)
	game.sprites.new(game.sprites.COMBOTICK)

	game.sprites.SCORE = ScoreBoard()
	game.sprites.new(game.sprites.SCORE)


if __name__ == "__main__":

	g = GameNamespace([1280, 720])
	g.init_display([1280, 720])
	g.init_input()
	g.init_sprites("PLAYER", "MANAGER", "ENEMY", "GRID", "SNIPER", "GORE", "HIGHPARTICLE", "FOREGROUND", "UI")
	g.init_clock(60)
	# g.init_clock(60 if len(sys.argv) < 2 else int(sys.argv[1]))
	g.init_hooks(lambda game: main(game) if game.input.check_key(pygame.K_r, buffer=True) else None)
	g.init_audio(sfx={
		"walk" : "data/sfx/walk.wav",
		"attack" : "data/sfx/attack.wav",
		"hit" : "data/sfx/hit.wav",
		"snipe" : "data/sfx/snipe.wav",
		"err" : "data/sfx/err.wav",
	})

	main(g)
