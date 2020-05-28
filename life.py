"""
An implementation of Conway's "Game of Life"
...
...
<more to come?>
...
...

"""


import pygame
from pygame.locals import *
from engine import GameEngine
from board import DrawGrid, GameWindow


WIDTH, HEIGHT = 1280, 720
BACKGROUND = (26, 108, 190)
FPS_TARGET = 60


class Events:
	def __init__( self):
		...
	def mouseOverGrid( self, event):
		if event[0] > WIDTH/4 and event[0] < WIDTH/4*3:
			if event[1] > HEIGHT/6 and event[1] < HEIGHT/6*4:
				return True
		return False
	
	def clickGrid( self, event):
		gridPos = [event[0]-(WIDTH/4), event[1]-(HEIGHT/6)]
		gridPos[0] = int( gridPos[0]//20)
		gridPos[1] = int( gridPos[1]//20)
		alive = Game._window.grid[gridPos[1]][gridPos[0]].alive

		if alive:
			Game._window.grid[gridPos[1]][gridPos[0]].alive = False
		else:
			Game._window.grid[gridPos[1]][gridPos[0]].alive = True




class Game( Events):
	_window = None
	_fps = None

	def __init__( self):
		self._running = True
		self._display_surf = None
		self.size = WIDTH, HEIGHT

	def cleanup( self):
		pygame.quit()

	def on_init( self):
		pygame.init()
		self._display_surf = pygame.display.set_mode( (self.size), 
									pygame.HWSURFACE | pygame.DOUBLEBUF)
		self._running = True

		Game._fps = pygame.time.Clock()
		Game._window = GameWindow( self._display_surf, (WIDTH/4), (HEIGHT/6))

	def on_event( self, event):
		if event.type == QUIT:
			self._running = False
		elif event.type == MOUSEMOTION:
			...
		elif event.type == MOUSEBUTTONDOWN:
			mousePos = pygame.mouse.get_pos()
			if self.mouseOverGrid( mousePos):
				self.clickGrid( mousePos)
		elif event.type == MOUSEBUTTONUP:
			...
		elif event.type >= USEREVENT:
			...
		elif event.type == ACTIVEEVENT:
			...

	def loop( self):
		Game._window.update()

	def render( self):
		self._display_surf.fill( BACKGROUND)
		Game._window.draw()
		pygame.display.flip()

	def on_execute( self):
		if self.on_init() == False:
			self._running = False

		while( self._running):
			for event in pygame.event.get():
				self.on_event( event)
				
			self.render()
#			self.loop()
			Game._fps.tick( FPS_TARGET)
			print( "framerate: {:.2f}\t\t".format( Game._fps.get_fps()), end= "\r")

		self.cleanup()



# main game loop?
def main():

	gameoflife = Game()

	gameoflife.on_init()
	gameoflife.on_execute()
	
	#grid = DrawGrid(( HEIGHT, WIDTH))
	#for _ in grid.animateGrid():
	#	...


if __name__ == "__main__":
	main()
	...
	
	