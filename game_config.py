from pgzero.builtins import Actor
from grid.get_grid import get_grid
from graph import create_graph

import numpy as np


WIDTH = 600
HEIGHT = 580
SPEED = 3

player = Actor('pacman_eat')
dots = []       # list of all dots on screen
ghosts = []     # list of all four ghosts on screen
grid = np.array(get_grid())     # movement grid
graph = create_graph()  # movement graph
ghost_move = 0
ITER = 25
isChasingMode = False   # when power dot is eaten
runGhosts = []  # list of all ghosts when players is chasing them
SECONDS = 5
isInitialized = False