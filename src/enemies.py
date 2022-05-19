from sprite import Sprite
from grid import Tiles
from random import randint
from math import dist
import particles

from util.base import normalize
import gore

import pygame.draw
from pygame import Surface, SRCALPHA


class Enemy(Sprite):
	LAYER = "ENEMY"

	def __init__(self, pos):
		self.x, self.y = pos

	# Create new enemy at a random position
	@staticmethod
	def new(game):
		grid = game.sprites.GRID
		pos = [randint(0, grid.w-1), randint(0, grid.h-1)]

		# Must not be inside a wall or too close to the player
		if dist(pos, [game.sprites.PLAYER.x, game.sprites.PLAYER.y]) < 3 or grid.getsq(pos) != Tiles.Empty:
			return Enemy.new(game)

		return Enemy(pos)

	# Function to check if moving to a new position will compromise
	def _temp_movement(self, game, vel):
		sq = game.sprites.GRID.getsq([self.x + vel[0], self.y + vel[1]])

		# End game if moving to square where player is
		if sq == Tiles.Player:
			game.sprites.PLAYER.death(game)
			self.x += vel[0]
			self.y += vel[1]
			return True

		if sq != Tiles.Empty:
			return False

		self.x += vel[0]
		self.y += vel[1]
		return True

	def _movement(self, game):
		oldx, oldy = self.x, self.y

		# Get distance from player
		player = game.sprites.PLAYER
		xdiff, ydiff = (player.x - self.x, player.y - self.y)

		# Establish two velocities that represent valid movement for the enemy sprite
		# If the first veolicty points to an invalid position, try the second
		vels = [[], []]
		if abs(ydiff) > abs(xdiff):
			vels[0] = [0, normalize(ydiff)]
			vels[1] = [normalize(xdiff), 0]

		else:
			vels[0] = [normalize(xdiff), 0]
			vels[1] = [0, normalize(ydiff)]

		# If the first location is invalid, try move to the second location
		if not self._temp_movement(game, vels[0]):
			self._temp_movement(game, vels[1])

		# Double check
		if player.pos() == self.pos():
			game.sprites.PLAYER.death(game)

	def update_move(self, game):
		game.sprites.GRID.setsq([self.x, self.y], Tiles.Empty)
		if self.destroy:
			return

		if game.sprites.PLAYER.has_moved_this_frame is True:
			self._movement(game)

		game.sprites.GRID.setsq([self.x, self.y], Tiles.Enemy)


class Sniper(Sprite):
	COUNTDOWN_LEN = 2

	LAYER = "SNIPER"

	def __init__(self):
		self._target = None
		self._countdown = Sniper.COUNTDOWN_LEN

	def update_move(self, game):
		if not game.sprites.PLAYER.has_moved_this_frame:
			return

		if self._target is None:
			self._target = game.sprites.PLAYER.pos()
			self._countdown = Sniper.COUNTDOWN_LEN
		else:
			grid = game.sprites.GRID

			self._countdown -= 1
			if self._countdown >= 1:
				game.audio.playsound("err")

			if self._countdown < 1:
				game.audio.playsound("snipe")

				if self._target == game.sprites.PLAYER.pos():
					game.sprites.PLAYER.death(game)

				for enemy in game.sprites.get("ENEMY"):
					if enemy.pos() == self._target:
						enemy.kill()
						p = game.sprites.GRID.offset_pos(self._target)
						game.sprites.news(*gore.Gore.goresplash(p, [0, 359], game.sprites.GORESURF))

				game.sprites.news(*particles.explosion(10, grid.relative_pos(self._target), radius=10, speed=10))
				game.screenshake.init_box_shake(3, 2)
				self._target = None

	def update_draw(self, game):
		if self._target is not None:
			pos = list(game.sprites.GRID.relative_pos(self._target))
			pos[1] -= 10

			size = (game.sprites.GRID.TILE_SIZE)*(self._countdown/Sniper.COUNTDOWN_LEN)

			pygame.draw.rect(game.window, (35, 35, 135), [pos[0]-size, pos[1]-size, size*2, size*2], 5)

			size += 20
			pygame.draw.line(game.window, (35, 35, 135), (pos[0], pos[1] + size), (pos[0], pos[1] - size), 5)
			pygame.draw.line(game.window, (35, 35, 135), (pos[0] + size, pos[1]), (pos[0] - size, pos[1]), 5)


class EnemySpawner(Sprite):
	LAYER = "MANAGER"
	SPAWN_LIMIT_MIN = 0
	SPAWN_INCREASE_RATE = 2

	def __init__(self):
		self._spawn_counter = 0
		self._spawn_limit = 5
		self._spawn_limit_incr = 0

	def _spawn_enemy(self, game):
		game.sprites.new(Enemy.new(game))
		self._spawn_counter = 0

		self._spawn_limit_incr += 1
		if self._spawn_limit_incr >= EnemySpawner.SPAWN_INCREASE_RATE:
			self._spawn_limit -= 1 if self._spawn_limit > EnemySpawner.SPAWN_LIMIT_MIN else 0
			self._spawn_limit_incr = 0

	def update_move(self, game):
		player = game.sprites.PLAYER
		self._spawn_counter += int(player.has_moved_this_frame)

		# If counter is too tiny
		if self._spawn_counter > self._spawn_limit:
			self._spawn_enemy(game)

		# If there are no enemies on the board
		elif len(game.sprites.get("ENEMY")) < 1 and self._spawn_counter <= self._spawn_limit:
			self._spawn_enemy(game)

		if game.SCORE > 0 and not game.sprites.get("SNIPER"):
			game.sprites.new(Sniper())
