import pygame
import time
from util.debug import Debug
from util.base import Namespace

import os.path
from random import randint


class GameClass(Debug):
	def __init__(self, game):
		self.game = game

	@staticmethod
	def constructor(func):
		def inner(obj, game, *args, **kwargs):
			obj.game = game
			return func(obj, *args, **kwargs)

		return inner


class InputManager(GameClass):

	@GameClass.constructor
	def __init__(self):
		self._last_keys = []
		self._keys = []

		self._last_mouse = []
		self._mouse = []

	def update(self):
		self._last_keys = self._keys
		self._last_mouse = self._mouse

		self._keys = pygame.key.get_pressed()
		self._mouse = pygame.mouse.get_pressed()

	def check_mouse(self, index, buffer=False):
		assert index < 3, "Index must be less than 3"
		return self._mouse[index] and ((not self._last_mouse[index]) if buffer else True)

	def check_key(self, *keys, buffer=False):
		if not (self._keys and self._last_keys):
			return False

		if buffer and any([self._last_keys[k] for k in keys]):
			return False

		for k in keys:
			if self._keys[k]:
				return True

		return False


class SpriteManager(GameClass):

	@GameClass.constructor
	def __init__(self, *strarr):
		self.sprites = {}
		self.add_layers(*strarr)

	def add_layers(self, *new_layers):
		assert all([n not in self.sprites.keys() for n in new_layers])
		assert all([type(n) == str for n in new_layers]), "All layernames must be strings"

		for n in new_layers:
			self.sprites[n] = []

	def new(self, s):
		assert s.LAYER in self.sprites.keys()
		self.sprites[s.LAYER].append(s)

	def news(self, *new_sprites):
		assert [s.LAYER in self.sprites.keys() for s in new_sprites]
		for s in new_sprites:
			self.sprites[s.LAYER].append(s)

	def get(self, layer_name):
		return self.sprites[layer_name]

	def gets(self, *layer_names):
		ext = []
		for ln in layer_names:
			ext.extend(self.get(ln))
		return ext

	def purge(self, *layer_names):
		if not len(layer_names):
			for ln in self.sprites:
				self.sprites[ln] = [s for s in self.sprites[ln] if s.protected]

		for ln in layer_names:
			self.sprites[ln] = [s for s in self.sprites[ln] if s.protected]

	def update(self):
		for k in self.sprites.keys():
			v = self.sprites[k]
			for i in range(len(v)-1, -1, -1):
				v[i].update_move(self.game)
				if v[i].destroy:
					self.sprites[k].pop(i)

		for k in self.sprites.keys():
			v = self.sprites[k]
			for sprite in v:
				sprite.update_draw(self.game)


class StateManager(GameClass):

	@GameClass.constructor
	def __init__(self, framecap=None):
		self.framecap = framecap
		self.FRAMES = 0
		self.clock = pygame.time.Clock()

		self.INIT_TIME = time.time()
		self._elapsed_time = time.time() - self.INIT_TIME
		self._last_frame_time = time.time()

		self.framerate = 0

	def update(self):
		self._delta_time = time.time() - self._last_frame_time

		self._elapsed_time = time.time() - self.INIT_TIME
		self._last_frame_time = time.time()

		self.framerate = 1 / self._delta_time

		if self.framecap is not None:
			self.clock.tick(self.framecap)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.game.running = False

		self.FRAMES += 1


class HooksManager(GameClass):
	@GameClass.constructor
	def __init__(self):
		self._pre_hooks = []
		self._post_hooks = []

	def new(self, hook, pre=True):
		assert hasattr(hook, "__call__"), f"Hook: \"{hook.__name__}\" is not a callable"
		ap = self._pre_hooks if pre else self._post_hooks
		ap.append(hook)

	def update(self, pre=True):
		ap = self._pre_hooks if pre else self._post_hooks
		for h in ap:
			h(self.game)

	def clear(self):
		self._pre_hooks = []
		self._post_hooks = []



class AudioManager(GameClass):
	@GameClass.constructor
	def __init__(self):
		self.sounds = {}
		self.music = {}

		pygame.mixer.init()

	def new_sound(self, sname, spath):
		assert os.path.exists(spath)
		assert sname not in self.sounds.keys()

		self.sounds[sname] = [pygame.mixer.Sound(spath), len(self.sounds)]
		pygame.mixer.set_num_channels(len(self.sounds.keys()))

	def new_sounds(self, *args):
		for a in args:
			assert type(a) == list and len(a) == 2
			self.new_sound(*a)

	def new_sounds_batch(self, **kwargs):
		for k, v in kwargs.items():
			self.new_sound(k, v)

	def playsound(self, sname):
		s = self.sounds[sname]
		pygame.mixer.Channel(s[1]).play(s[0])


class ScreenshakeManager(GameClass):

	@GameClass.constructor
	def __init__(self):
		self.x, self.y = 0, 0

		self._shake_positions = []
		self._is_shaking = False

	def init_box_shake(self, strength, length):
		if self._shake_positions and sum(self._shake_positions[0]) > strength:
			return

		self._shake_positions = []
		for i in range(length):
			while True:
				offset = [strength*randint(-1, 1), strength*randint(-1, 1)]
				if self._shake_positions:
					if offset != self._shake_positions[-1]:
						self._shake_positions.append(offset)
						break
				else:
					self._shake_positions.append(offset)

		self._is_shaking = True

	def update(self):
		if self.game.state.FRAMES % 2 == 0 and self._is_shaking:
			if self._shake_positions:
				self.x, self.y = self._shake_positions.pop(-1)
			else:
				self._is_shaking = False
				self.x, self.y = 0, 0


class DebugTools(GameClass):
	@GameClass.constructor
	def __init__(self, font=None, fontsize=30):
		pygame.font.init()

		if font is None:
			print("Initilialising optional Gameref module DebugTools with font of None. This will cause the program to break when built with pyinstaller")

		self._fontname = font
		self._fontsize = fontsize
		self._font = pygame.font.Font(self._fontname, self._fontsize)

		self._text = []

	def display_text(self, text):
		assert type(text) == str
		for line in text.split('\n'):
			self._text.append(line)

	def update(self):
		for y in range(len(self._text)-1, -1, -1):
			txt = self._text.pop(y)

			f = self._font.render(txt, False, (255, 255, 255))
			self.game.window.blit(f, (10, (self._fontsize+(self._fontsize//6)) * y + 10))
