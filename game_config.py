from pgzero.builtins import Actor
from grid.get_grid import get_grid

import numpy as np


WIDTH = 600
HEIGHT = 580
SPEED = 3
CELLS_PER_INT = 30

player = Actor('pacman_eat')
dots = []       # list of all dots on screen
ghosts = []     # list of all four ghosts on screen
grid = np.array(get_grid())     # movement grid
