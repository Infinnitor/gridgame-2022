from util.base import Namespace
import pygame.locals as keys


PlayerActions = Namespace(
	LEFT=[keys.K_LEFT, keys.K_a, keys.K_j],
	RIGHT=[keys.K_RIGHT, keys.K_d, keys.K_l],
	UP=[keys.K_UP, keys.K_w, keys.K_i],
	DOWN=[keys.K_DOWN, keys.K_s, keys.K_k],
)
