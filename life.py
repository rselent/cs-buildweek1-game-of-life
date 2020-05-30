"""
An implementation of Conway's "Game of Life"
...
...
<more to come?>
...
...

"""
import numpy.random as rng
import numpy as np
import pygame
import os, sys
from pygame.locals import *


# since fonts are important to this game, we want to make sure
# the font subsystem is available:
if not pygame.font: print( "Warning, fonts disabled")
# and as an example, we can do this for other systems too, like sound:
if not pygame.mixer: print( "Warning, sound disabled")


RNG = np.random.default_rng()


WCELLS, HCELLS = 32, 32
#WIDTH, HEIGHT = 2*WCELLS*20, 2*HCELLS*20
WIDTH, HEIGHT = 1280, 720

FPS_TARGET = 32

COLOR_ALIVE = (0, 184, 255)			# Blue/Cyan
COLOR_DEAD = (0, 0, 0)				# Blaaaaaaaaaaack
BACKGROUND = (26, 108, 190)			# Gator Blue
TEST_BG = (252, 134, 45)			# Gator Orange


RULES = [["Overpopulation: if a living cell is surrounded by more", "than three other living cells, it dies."], 
		 ["Stasis: if a living cell is surrounded by two", "or three other living cells, it survives."],
		 ["Underpopulation: if a living cell is surrounded by fewer", "than two other living cells, it dies."],
		 ["Reproduction: if a dead cell is surrounded by three", "other living cells, it becomes a live cell."]
]



class EventHandler:
	paused = None

	def __init__( self):
		...


	def mouseOverGame( self, event):
		if event[0] > 0 and event[0] < WIDTH:
			if event[1] > 0 and event[1] < HEIGHT:
				return True
		return False
	

	def clickGrid( self, event):
		print( "CLICKITY CLACK!")
		# gridPos = [event[0]-(WIDTH), event[1]-(HEIGHT)]
		# gridPos[0] = int( gridPos[0]//16)
		# gridPos[1] = int( gridPos[1]//16)

		# alive = self.grids[ self.activeGrid][gridPos[0]][gridPos[1]]
		# if alive:
		# 	self.grids[ self.activeGrid][gridPos[0]][gridPos[1]] = 0
		# else:
		# 	self.grids[ self.activeGrid][gridPos[0]][gridPos[1]] = 1
	

	def pauseLife( self):
		if EventHandler.paused:
			print( "\tunpaused!")
			EventHandler.paused = False
		else:
			print( "\n\tpaused bitch!")
			EventHandler.paused = True
	

	def advanceFrame( self):
		if EventHandler.paused:
			print( "\tadvancing one frame!")
			self.update()
			self.render()
			Game._N += 1
			self.obj_Text( f"life cycle: {Game._N}")
			self.obj_Text( "FPS: {:.2f}".format( Game._fps.get_fps()), 
										center= (40, 710), 
										fontsize= 22,
			)
			pygame.display.flip()





	def randomize( self):
		if EventHandler.paused:
			...
		Game._N = 0
		self.activeGrid = 0
		self.setGrid( None, self.activeGrid)
		self.setGrid( 0, self.inactiveGrid())
		self.render()
		self.obj_Text( f"life cycle: {Game._N}")
		self.obj_Text( "FPS: {:.2f}".format( Game._fps.get_fps()), 
										center= (40, 710), 
										fontsize= 22,
		)
		pygame.display.flip()




class Game( EventHandler):
	_window = None
	_fps = None
	_N = 0

	def __init__( self):
		vector = pygame.math.Vector2
		
		self.pos = vector( WIDTH//4, HEIGHT//6)
		self.gridX = self.pos.x
		self.gridY = self.pos.y
		self.board = pygame.Surface( ((WIDTH//2), (HEIGHT//2)))
		self.rect = self.board.get_rect()
		
		
		self.size = WIDTH, HEIGHT
		
		
		self._window = None
		self._running = True
		

	def cleanup( self):
		pygame.quit()


	def on_init( self):
		"""
		On game initialization:
		init pygame library,
		init display window at desired resolution, (with possible hw accel & double buffering?)
		ensure 
		fill in window surface with global color,
		change app's title bar from default,
		init framerate counter,
		and set default game states:
			cols, rows,
			init dual (active/inactive) grids,
			and set active grid
		"""
		pygame.init()
		self._window = pygame.display.set_mode( (self.size))#, pygame.HWSURFACE & pygame.DOUBLEBUF)
		self.background = pygame.Surface( self._window.get_size())
		self.background = self.background.convert()
		self._window.fill( BACKGROUND)
		pygame.display.set_caption( "Life of Game of Life of Game of..."\
			"                                                           "\
			"                                                            "\
										" (hardcore alpha, yo)")
		pygame.display.flip()

		Game._fps = pygame.time.Clock()

		self.numCols = WCELLS
		self.numRows = HCELLS
		self.activeGrid = 0
		self.grids = []

#		self.on_initButtons()
		self.on_initGrids()
		self.setGrid()

		# if the above runs without error, set run state to True and bring up start screen
		self._running = True
		self.startScreen()

#		Game._window = GridWindow( self._windowBase, (WIDTH//4), (HEIGHT//6))



	def startScreen( self):
		self.intro = True

		self.obj_Text( "FPS: {:.2f}".format( Game._fps.get_fps()), 
										center= (40, 710), 
										fontsize= 22,
		)
		self.obj_Text( "HELLO THERE, I AM GAME!", 
#						color= (226, 108, 19), 
						color= TEST_BG,
						center= (640, 360),
						fontsize= 58
		)
		self.obj_Text( "PRESS SPACEBAR TO START", 
						color= (108, 226, 19), 
						center= (640, 480), 
						fontsize= 46
		)
		self.obj_Text( "HOW IT WORKS:", 
						color= TEST_BG, 
						center= (1018, 30), 
						fontsize= 42
		)
		self.obj_Text( RULES[0][0], 
						color= (108, 226, 19), 
						center= (1016, 60), 
						fontsize= 26
		)
		self.obj_Text( RULES[0][1], 
						color= (108, 226, 19), 
						center= (1082, 76), 
						fontsize= 26
		)
		self.obj_Text( RULES[1][0], 
						color= (108, 226, 19), 
						center= (1050, 100), 
						fontsize= 26
		)
		self.obj_Text( RULES[1][1], 
						color= (108, 226, 19), 
						center= (1089, 116), 
						fontsize= 26
		)
		self.obj_Text( RULES[2][0], 
						color= (108, 226, 19), 
						center= (1014, 146), 
						fontsize= 26
		)
		self.obj_Text( RULES[2][1], 
						color= (108, 226, 19), 
						center= (1078, 162), 
						fontsize= 26
		)
		self.obj_Text( RULES[3][0], 
						color= (108, 226, 19), 
						center= (1022, 188), 
						fontsize= 26
		)
		self.obj_Text( RULES[3][1], 
						color= (108, 226, 19), 
						center= (1098, 204), 
						fontsize= 26
		)



		while self.intro:
			for event in pygame.event.get():
				self.on_event( event)

			pygame.draw.rect( self._window, (64, 64, 227), (200, 450, 100, 50))
			pygame.draw.rect( self._window, (227, 64, 64), (1030, 450, 100, 50))
#			pygame.draw.rect( self._window, (64, 254, 64), (360, 360, 180, 180))




#			self._window.blit( hi, hi_rect)
#			self._window.blit( start, start_rect)



			pygame.display.flip()



	def on_initGrids( self):
		"""
		Build and stores the default active and inactive grid
		"""
		def buildGrid():
			"""
			generate empty 2d grid
			"""
			rows = []
			for row in range( self.numRows):
				cols = [0]*self.numCols
				rows.append( cols)
			return rows

		self.grids.append( buildGrid())
		self.grids.append( buildGrid())


	def setGrid( self, gridType= None, grid= 0):
		"""
		Set an entire grid at once. Set to a single value or random 0/1
		Usage:
			setGrid()		# random distribution (*stretch: based on weight*)
			setGrid( None)	# also random
			setGrid( 0)		# all cells dead
			setGrid( 1)		# all cells alive

		Passing a value for grid can do bad things...
		"""
		for row in range( self.numRows):				# iterate through 
			for col in range( self.numCols):			# rows and columns
				if gridType is None:					# if None:
					cellVal = RNG.choice( 2)			# randomize between 0,1
				else:									# otherwise:
					cellVal = gridType					# set to 1 or 0 manually
				self.grids[ grid][row][col] = cellVal	# and then apply cellVal


	def inactiveGrid( self):
		"""
		Helper function to get the index of the inactive grid
		If active grid is 1, will return 0 and vice versa
		"""
		return (self.activeGrid + 1) % 2

	def on_event( self, event):
		if event.type == QUIT:
			self._running = False
			self.cleanup()

		# MOUSE events
		elif event.type == MOUSEBUTTONDOWN:
			mousePos = pygame.mouse.get_pos()
			if self.mouseOverGame( mousePos):
				self.clickGrid( mousePos)

		# KEYPRESS events
		elif event.type == KEYDOWN:
			if event.key == K_SPACE:
				if self.intro == True:
					self.intro = False
				else:
					self.pauseLife()
			elif event.key == K_TAB or event.key == K_RETURN:
				self.advanceFrame()
			elif event.key == K_BACKSPACE:
				self.randomize()
			elif event.key == K_ESCAPE:
				if self.paused:
					self._running = False		# cleaner exit than directly 
												# calling self.cleanup()?



	def obj_Text( self, text_in= "DEFAULT TEXT", 
				  color= (255, 255, 255), 
				  center= ((WIDTH//2), (HEIGHT//2)), 
				  font= None, fontsize= 34, aa= 1):

		font = pygame.font.Font( font, fontsize)
		text = font.render( text_in, aa, color)
		textRect = text.get_rect( center= center)
		self._window.blit( text, textRect)


	def obj_Button( self):
		...
#		box = pygame.gfxdraw.box( stuff )
	def obj_BaseRects( self):
		...
#		testRec = pygame.draw.rect( self._window, (64, 254, 64), (360, 360, 360, 360))


	def update( self):
		"""
		Inspect current generation state, 
		check neighbours, 
		prepare next pass, 
		swap grids
		"""
#		Game._window.update()
		self.rect.topleft = self.pos

		self.setGrid(0, self.inactiveGrid())
		for row in range( self.numRows - 1):
			for col in range( self.numCols - 1):
				gameState_next = self.check_cellNeighbours(row, col)
				self.grids[ self.inactiveGrid()][row][col] = gameState_next

		self.activeGrid = self.inactiveGrid()


	def render( self):
		"""
		Given the grid and cell states, draw the cells on the screen
		"""
		self.board.fill( TEST_BG)
#		Game._window.draw()
		self._window.fill( BACKGROUND)

		image = pygame.Surface( (20, 20))
		rect = image.get_rect()

		for row in range( self.numRows):
			for col in range( self.numCols):
				if self.grids[ self.activeGrid][row][col] == 1:
					state = COLOR_ALIVE
					image.fill( (TEST_BG))
#					pygame.draw.circle( image, (COLOR_ALIVE), 
#									(int( col * 16),
#									int( row * 16)),
#									int( 15)
#					)
				else:
					state = COLOR_DEAD
					image.fill( (TEST_BG))
#				pygame.draw.circle( self.image, (COLOR_ALIVE), (10, 10), 11)
				pygame.draw.circle( self._window, state, 
									(int( col * 16),
									int( row * 16)),
									int( 15)
				)
#		self._window.blit( self.board, (self.pos.x, self.pos.y))
		self.board.blit( image, (self.gridX*20, self.gridY*20))
#		pygame.display.flip()
#		self._window.blit( self.board, (200, 200))



	def get_cellVal( self, numRow, numCol):
		"""
		Get the alive/dead (1/0) state of a specific cell in active grid
		"""
		try:
			cellVal = self.grids[ self.activeGrid][numRow][numCol]
		except:
			cellVal = 0

		return cellVal


	def check_cellNeighbours( self, indexRow, indexCol):
		"""
		Get the number of alive neighbor cells, and determine the state of the cell
		for the next generation. Determine whether it lives, dies, survives, or is born.
		"""

		alive = 0
		alive += self.get_cellVal( indexRow-1, indexCol-1)		# BL
		alive += self.get_cellVal( indexRow-1, indexCol)		# LL
		alive += self.get_cellVal( indexRow-1, indexCol+1)		# TL
		alive += self.get_cellVal( indexRow, indexCol-1)		# BB
		alive += self.get_cellVal( indexRow, indexCol+1)		# TT
		alive += self.get_cellVal( indexRow+1, indexCol-1)		# BR
		alive += self.get_cellVal( indexRow+1, indexCol)		# RR
		alive += self.get_cellVal( indexRow+1, indexCol+1)		# TR

		if self.grids[ self.activeGrid][indexRow][indexCol] == 1:
			if alive > 3:		# if > 3 adj cells are alive, active cell dies
				return 0
			if alive < 2:		# if < 2 adj cells are alive, active cell dies
				return 0
			if alive == 2 or alive == 3:	# if exactly 2 | 3 adj cells are alive,
				return 1					# active cell stays alive
		elif self.grids[ self.activeGrid][indexRow][indexCol] == 0:
			if alive == 3:		# if actice cell is dead, but exactly 3 adj cells
				return 1		# are alive, "bring me to life" - cell/evanescence

		return self.grids[ self.activeGrid][indexRow][indexCol]


	def on_execute( self):
		if self.on_init() == False:
			self._running = False

		while( self._running):
			for event in pygame.event.get():
				self.on_event( event)


			if EventHandler.paused:	
				continue	#---- NOTHING below this line runs while paused ----
			
			self.update()
			self.render()
			Game._N += 1
			self.obj_Text( f"life cycle: {Game._N}")		
			self.obj_Text( "FPS: {:.2f}".format( Game._fps.get_fps()), 
										center= (40, 710), 
										fontsize= 22,
			)
#			pygame.display.update()
			pygame.display.flip()
			Game._fps.tick( FPS_TARGET)


		self.cleanup()


def main():

	gameoflife = Game()

	gameoflife.on_execute()
	

if __name__ == "__main__":
	main()
	...
	
	
