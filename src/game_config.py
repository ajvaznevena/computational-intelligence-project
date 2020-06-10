from grid.get_grid import get_grid
from graph import create_graph

import time
import pgzrun

from player import Player
from dots import initDots
from ghosts import initGhosts, moveGhosts

import numpy as np

WIDTH = 600
HEIGHT = 580

player = Player('pacman_eat')
dots = initDots()  # list of all dots on screen

ghosts = initGhosts()   # list of all four ghosts on screen

grid = np.array(get_grid())     # movement grid
graph = create_graph()  # movement graph

ghostMovement = 0
ITER = 25

isChasingMode = False   # when power dot is eaten
SECONDS = 5
timer = 0
