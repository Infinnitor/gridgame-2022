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



def mask_surface(surf):
	b = Surface(surf.get_size(), SRCALPHA)
	b.blit(surf, (0, 0))


	size = b.get_size()

	b.lock()
	for y in range(size[1]):
		for x in range(size[0]):
			rgba = b.get_at([x, y])
			clr = [10, 10, 10]
			clr.append(rgba[3] if len(rgba) == 4 else 255)
			b.set_at([x, y], clr)

	b.unlock()

	return b


def decay_mut(surf, rate):
	size = surf.get_size()

	surf.lock()

	valid_pos = []
	for y in range(size[1]):
		for x in range(size[0]):
			pos = (x, y)

			g = surf.get_at(pos)
			if len(g) < 4 or g[3] != 0:
				valid_pos.append(pos)

	for i in range(rate):
		if valid_pos:
			pos = random.choice(valid_pos)
			surf.set_at(pos, (0, 0, 0, 0))
		else:
			return False

		surf.set_at(pos, (0, 0, 0, 0))
	surf.unlock()
	return True


def decay(surf, rate):
	newsurf = Surface(surf.get_size(), SRCALPHA)
	decay_mut(newsurf)
	return newsurf
