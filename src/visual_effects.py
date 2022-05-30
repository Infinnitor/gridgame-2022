from pygame import Surface, SRCALPHA
import random


def tv_static_surface(surf):
	tv = Surface(surf.get_size(), SRCALPHA)
	tv.blit(surf, (0, 0))


	size = tv.get_size()

	tv.lock()
	for y in range(size[1]):
		for x in range(size[0]):
			rgba = tv.get_at([x, y])

			c = random.randint(0, 195)
			clr = [c, c, c]
			clr.append(rgba[3] if len(rgba) == 4 else 255)

			tv.set_at([x, y], clr)
	tv.unlock()

	return tv
