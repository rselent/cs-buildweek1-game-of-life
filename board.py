"""
Game of Life grid (structure, drawing, animating, etc)
"""


import matplotlib.pyplot as plt
import numpy.random as random
from engine import GameEngine

import time


# global vars
GAME_TITLE = "Tinder: The Game"
DESIRED_FRAMERATE = .0167		# in seconds -- frame time-> .0333 = 30fps, 
								#							 .0167 = 60fps


class DrawGrid:
	def __init__( self, size):
		"""
		Draw game's grid/universe

		Arguments:
			size {int tuple} -- size of grid to draw (x, y)
		"""
		# init self state as randomized integer based on size tuple
		self.state = random.randint( 2, size= size)
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

