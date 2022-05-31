from util.base import Namespace
import pygame.locals as keys


PlayerActions = Namespace(
	LEFT=[keys.K_LEFT, keys.K_a],
	RIGHT=[keys.K_RIGHT, keys.K_d],
	UP=[keys.K_UP, keys.K_w],
	DOWN=[keys.K_DOWN, keys.K_s],
)
