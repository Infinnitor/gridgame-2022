from util.system import workingdir_is_program
workingdir_is_program()

from gameref_classes import *
import pygame
pygame.init()
pygame.mixer.init()


# This allows for different initialisers to be used for the same modules
REQUIRED_MODULES = {
	"init_display" : False,
	"init_input" : False,
	"init_sprites" : False,
	"init_clock" : False,
	"init_hooks" : False,
	"init_audio" : False,
}


class GameNamespace:
	def __init__(self, size):
		self.WIDTH, self.HEIGHT = size
		self.window = pygame.Surface(size)
		self.running = True

	def init_display(self, size, window_type=pygame.SHOWN):
		self.UWIDTH, self.UHEIGHT = size
		self.uwindow = pygame.display.set_mode(size, window_type)

		self.screenshake = ScreenshakeManager(self)

		REQUIRED_MODULES["init_display"] = True
		return self

	def init_input(self):
		self.input = InputManager(self)

		REQUIRED_MODULES["init_input"] = True
		return self

	def init_sprites(self, *layers):
		self.sprites = SpriteManager(self, *layers)

		REQUIRED_MODULES["init_sprites"] = True
		return self

	def init_clock(self, framerate):
		self.state = StateManager(self, framerate)

		REQUIRED_MODULES["init_clock"] = True
		return self

	def init_hooks(self, *start_hooks):
		self.hooks = HooksManager(self)
		for h in start_hooks:
			self.hooks.new(h)

		REQUIRED_MODULES["init_hooks"] = True
		return self

	def init_audio(self, sfx={}, music={}):
		self.audio = AudioManager(self)
		self.audio.new_sounds_batch(**sfx)
		self.audio.new_sounds_batch(**music)

		REQUIRED_MODULES["init_audio"] = True
		return self

	def validate(self):
		if not all(REQUIRED_MODULES.values()):
			msg = f"Not all required modules have been initialised. Missing: {[k for k, v in REQUIRED_MODULES.items() if not v]}"
			raise AssertionError(msg)

	def stop_running(self):
		self.running = False

	def on_exit(self):
		print(self.SCORE)


def gameloop(func):
	def inner(game):
		game.validate()
		func(game)
		while game.running:
			game.input.update()
			game.hooks.update(pre=True)
			game.sprites.update()
			game.screenshake.update()
			game.hooks.update(pre=False)

			t = pygame.transform.scale(game.window, [game.UWIDTH, game.UHEIGHT])
			game.uwindow.blit(t, (game.screenshake.x, game.screenshake.y))
			pygame.display.flip()
			game.window.fill((0, 0, 0))

			game.state.update()

		game.on_exit()
		pygame.quit()
		exit(0)

	return inner
