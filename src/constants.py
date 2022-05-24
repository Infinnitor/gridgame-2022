from util.base import Namespace


Tiles = Namespace(
	Empty=0,
	Wall=1,
	Player=2,
	Enemy=3,
)

Tiles.exists = lambda c: c in Tiles.__dict__.values()
TILE_SIZE = 60


SCORE_TIMER = 120
