"""
An implementation of Conway's "Game of Life"
...
...
<more to come?>
...
...

"""

from engine import GameEngine
from board import DrawGrid


HEIGHT = 192
WIDTH = HEIGHT


# main game loop?
def main():
	...
	grid = DrawGrid(( HEIGHT, WIDTH))
	for _ in grid.animateGrid():
		...


if __name__ == "__main__":
	main()
	...
	
	