from sprite import *
import pygame.font
pygame.font.init()


class TextSprite(RectSprite):
	LAYER = "FOREGROUND"

	def __init__(self, pos, text, fontname, fontsize, colour, centered=False):
		self.x, self.y = pos

		self._text = text
		self._fontname = fontname
		self._fontsize = fontsize
		self.c = colour

		self._render()

		self._centered = centered

	def _render(self):
		self._font = pygame.font.Font(self._fontname, self._fontsize)
		self._font_surface = self._font.render(self._text, False, self.c)
		self.w, self.h = self._font_surface.get_size()

	def change_text(self, newtext, **kwargs):
		self.c = kwargs.get("colour", self.c)
		self._fontsize = kwargs.get("colour", self._fontsize)

		self._text = newtext
		self._render()

	def update_draw(self, game):
		p = self.pos() if not self._centered else self.get_rect_centered()[:2]
		game.window.blit(self._font_surface, p)


class NoneFontSprite(TextSprite):
	def __init__(self, pos, text, centered=False):
		super().__init__(pos, text, None, 66, (200, 200, 200), centered)
