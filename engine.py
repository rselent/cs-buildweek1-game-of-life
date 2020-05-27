"""
Game of Life engine (rules, etc)
"""


class GameEngine( object):
	def __init__( self, grid):
		"""
		Core game logic

		Arguments:
			grid {ndarray} -- inits input array as self state
		"""
		self.state = grid.state
	def neighbourCount( self):
		"""
		Counts all 8 neighbouring cells

		Returns:
			n {int} -- sum of surrounding cell states / values
					   if a cell is filled, state is 1
		"""
		state = self.state
		# State order:	right-top		right-mid		right-bottom
		#						mid-top			mid-bottom
		#				left-top		left-mid		left-bottom
		n = (state[ 0:-2, 0:-2] + state[ 0:-2, 1:-1] + state[ 0:-2, 2:] +
			 state[ 1:-1, 0:-2] + state[ 1:-1, 2:] +
			 state[ 2:, 0:-2] + state[ 2:, 1:-1] + state[ 2:, 2:]
		)
		return n
	def rules( self):
		...
		state = self.state
		n = self.neighbourCount()
		# define 'new' cell: 3 neighbours and current cell == 0
		new = (n == 3) & (state[ 1:-1, 1:-1] == 0)
		# define 'stillAlive' cell: 2 or 3 neighbours and current cell == 1
		stillAlive = ((n == 2) | (n == 3)) & (state[ 1:-1, 1:-1] == 1)
		# zero out state ndarray
		state[...] = 0
		# set current cell state to 1 if 'new' or 'stillAlive' is True
		state[1:-1, 1:-1][new | stillAlive] = 1

		self.totalNew = sum( new)
		self.totalStillAlive = sum( stillAlive)
		
		return state



"""

_	_	_
X	X	X
_	_	_
X	O	X
_	_	_
X	X	X

"""