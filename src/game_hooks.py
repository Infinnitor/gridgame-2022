from visual_hooks import *


def reset_hook(callback):
	def inner(game):
		if game.input.check_key(pygame.K_r, buffer=True):
			callback(game)
			return

	inner.protected = True
	return inner


def fps_hook(game):
	game.debug.display_text(f"FPS: {round(game.state.framerate)}")



fps_hook.protected = True # TODO: Make hook.protected do something
