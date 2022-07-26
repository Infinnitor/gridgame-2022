import pygame.image
import pygame.transform
from constants import TILE_SIZE

from util.base import Namespace

from visual_effects import mask_surface


def _killsmap():
	def _load(name):
		file = pygame.image.load(f"data/sprites/vfx/killsmap/{name}").convert()
		file.set_colorkey((0, 0, 0))
		file = pygame.transform.scale(file, (TILE_SIZE, TILE_SIZE))
		return mask_surface(file)

	files = Namespace(
		UP=_load("up.png"),
		DOWN=_load("down.png"),
		LEFT=_load("left.png"),
		RIGHT=_load("right.png"),
	)

	global vfx_killsmap; vfx_killsmap = files




def init_assets():
	_killsmap()
