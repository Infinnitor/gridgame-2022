def rect_collide(a, b, attr=True):
	rect1 = (a.x, a.y, a.w, a.h) if attr else a
	rect2 = (b.x, b.y, b.w, b.h) if attr else b

	if rect1[0] + rect1[2] > rect2[0] and rect1[0] < rect2[0] + rect2[2]:
		if rect1[1] + rect1[3] > rect2[1] and rect1[1] < rect2[1] + rect2[3]:
			return True
	return False


def circle_collide(a, b, attr=True):
	c1 = (a.x, a.y, a.r) if attr else a
	c2 = (b.x, b.y, b.r) if attr else b

	return math.dist(c1[:2], c2[:2]) < c1[2] + c2[2]
