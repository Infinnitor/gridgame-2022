import pygame
from sprite import *
from constants import Tiles, TILE_SIZE

from enemies import Enemy

import math

import particles
import gore

from player_keybinds import PlayerActions
from player_kill_tree import PlayerKillTree



class Player(Sprite):
	LAYER = "PLAYER"

	# Constructor
	def __init__(self, pos):
		self.x, self.y = pos

		# Boolean that permits enemy movement
		self.has_moved_this_frame = False
		self._enemy_spawn_counter = 0

	# update_move function
	def update_move(self, game):
		self.has_moved_this_frame = False

		# Reset to this position if player hits wall
		oldx, oldy = self.x, self.y

		# Get reference to grid
		grid = game.sprites.GRID
		grid.setsq(self.pos(), Tiles.Empty)

		if game.sprites.ENEMYAUTH.enemy_turn is False:
			vel = [0, 0]
			# Check movement on horizontal axis
			if game.input.check_key(*PlayerActions.LEFT, buffer=True):
				vel = [-1, 0]
				self.has_moved_this_frame = True
			elif game.input.check_key(*PlayerActions.RIGHT, buffer=True):
				vel = [1, 0]
				self.has_moved_this_frame = True


			self.x += vel[0]

			# Teleport player if they are off the grid
			self.x = 0 if self.x > grid.w-1 else self.x
			self.x = grid.w-1 if self.x < 0 else self.x

			if self.has_moved_this_frame is False:
				# Check movement on vertical axis
				if game.input.check_key(*PlayerActions.UP, buffer=True):
					vel = [0, -1]
					self.has_moved_this_frame = True

				elif game.input.check_key(*PlayerActions.DOWN, buffer=True):
					vel = [0, 1]
					self.has_moved_this_frame = True

			self.y += vel[1]

			# Teleport player if they are off the grid
			self.y = 0 if self.y > grid.h-1 else self.y
			self.y = grid.h-1 if self.y < 0 else self.y

		def collision_check(mut, kills=0):
			# Check for enemy collision
			sq = grid.getsq(self.pos())
			if sq == Tiles.Enemy:

				# Check for 3 enemies in a row
				for i in range(-1, 2):
					check_pos = (
						# If travelling up then the x stays the same, if travelling sideways the y stays the same
						self.x if abs(vel[0]) else self.x + i,
						self.y if abs(vel[1]) else self.y + i,
					)

					# Check position against all enemies
					if grid.getsq(check_pos) == Tiles.Enemy:
						for e in game.sprites.get("ENEMY"):
							if check_pos == e.pos():
								kills += 1
								killsmap.append(check_pos)

								e.kill()
								p = [check_pos[0]*TILE_SIZE + TILE_SIZE//2, check_pos[1]*TILE_SIZE + TILE_SIZE//2]
								a_range = math.degrees(math.atan2(vel[1], vel[0]))
								game.sprites.news(*gore.Gore.goresplash(p, [a_range-50, a_range+50], game.sprites.GORESURF))
								game.screenshake.init_box_shake(10, 4)
								game.audio.playsound("attack")

				# Keep moving the player forward if the next tile is an enemy
				check_again = [self.x + vel[0], self.y + vel[1]]
				if grid.getsq(check_again) == Tiles.Enemy:
					self.x += vel[0]
					self.y += vel[1]
					collision_check(mut, kills)

			# Reset position if touching wall
			elif sq == Tiles.Wall:
				self.x, self.y = oldx, oldy
				return kills

			return kills

		killsmap = []
		# Recursive function to kill enemies in a pattern
		killsno = collision_check(killsmap)
		game.sprites.SCORE.increase_score(killsno)

		if len(killsmap) > 1:
			game.sprites.new(PlayerKillTree(killsmap, game))

		grid.setsq(self.pos(), Tiles.Player)
		# self.has_moved_this_frame = game.input.check_key(pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN, buffer=True)

		if self.has_moved_this_frame:
			game.audio.playsound("walk")

		# collision_check()

	def death(self, game):
		self.kill()

		game.audio.playsound("attack")

		for i in range(3):
			gorebits = gore.Gore.goresplash(game.sprites.GRID.offset_pos(self.pos()), [0, 359], game.sprites.GORESURF)
			for g in gorebits:
				g._get_colour = lambda: (g.speed, g.speed, g.speed)

			game.sprites.news(*gorebits)
