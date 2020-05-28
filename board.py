"""
Game of Life grid (structure, drawing, animating, etc)
"""


import matplotlib.pyplot as plt
import numpy.random as rng
import pygame
from engine import GameEngine


import time


# global vars
GAME_TITLE = "Tinder: The Game"
DESIRED_FRAMERATE = .0167		# in seconds -- frame time-> .0333 = 30fps, 
								#							 .0167 = 60fps
RANDOM_BIAS_ARRAY = [True, False]
RNG = rng.default_rng()

class DrawGrid:
	def __init__( self, size):
		"""
		Draw game's grid/universe

		Arguments:
			size {int tuple} -- size of grid to draw (x, y)
		"""
		# init self state as randomized binary value based on given tuple (size)
		self.state = RNG.integers( 2, size= size)
		# init self access to GameEngine class
		self.gameEngine = GameEngine( self)
	def animateGrid( self):
		"""
		"Animate" game's grid/universe using double-buffering.

		Yields:
			[self] -- enables while loop to re-up and draw new image data 
					  based on engine rules that were processed during 
					  previous pass, generating the illusion of animation
		"""
		start = 0
		n = 0
		plt.title( GAME_TITLE)
		while 1:
			if n == 0:
				# create image based on init state data
				image = plt.imshow( self.state)
			else:
				# update image based on yielded state from previous pass
				image.set_data( self.state)

			# increment n 
			n += 1
			self.gameEngine.rules()

			print( "life cycle: {}\t\t"\
				   "frame time: {:.3f}\t\t"\
				   "framerate: {:.2f}\t\t".format( 
											n, 
											(time.time() - start), 
											(1 / (time.time() - start)),
											), end= "\r",
			)
			start = 0
			start = time.time()
			plt.pause( DESIRED_FRAMERATE)
			yield self



class GameWindow:
	def __init__( self, screen, x, y):
		vector = pygame.math.Vector2
		self.screen = screen
		self.pos = vector( x, y)

#		self.rows = USER INPUT HERE
#		self.cols = USER INPUT HERE
#		self.width, self.height = self.rows*20, self.columns*20		# *20 = size of cell
		self.width, self.height = x*2+2, y*3+2
		self.image = pygame.Surface( (self.width, self.height))
		self.rect = self.image.get_rect()

		self.rows = int( self.height/20)
		self.columns = int( self.width/20)
		self.grid = [[DrawCells( self.image, x, y) for x in range( self.columns)] for y in range( self.rows)]



	def update( self):
		self.rect.topleft = self.pos
		for row in self.grid:
			for cell in row:
				cell.update()

	def draw( self):
		self.image.fill( (108, 26, 190))
		for row in self.grid:
			for cell in row:
				cell.draw()
		self.screen.blit( self.image, (self.pos.x, self.pos.y))


class DrawCells:
	def __init__( self, surface, gridX, gridY, randomSeed= True):
		if randomSeed:
			self.alive = RNG.choice( RANDOM_BIAS_ARRAY)
		else:
			self.alive = False
		self.surface = surface
		self.gridX = gridX
		self.gridY = gridY
		self.image = pygame.Surface( (20, 20))
		self.rect = self.image.get_rect()

	def update( self):
		self.rect.topleft = (self.gridX*20, self.gridY*20)

	def draw( self):
		if self.alive:
			self.image.fill( (0, 0, 0))
		else:
			self.image.fill( (0, 0, 0))
			pygame.draw.rect( self.image, (255, 255, 255), (2, 2, 18, 18))
		self.surface.blit( self.image, (self.gridX*20, self.gridY*20))

