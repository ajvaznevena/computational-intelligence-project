import time
import pgzrun
import numpy as np

from player import Player
from dots import initDots
from ghosts import *
from game_constants import WIDTH, HEIGHT, CELL_SIZE

TITLE = "Pac-Man game"

player = Player('pacman_eat', 'tree')  # Choose agent :). It can be: human, rl, greedy, tree
dots = initDots()       # list of all dots on screen
ghosts = initGhosts()   # list of all four ghosts on screen

ghostMovement = 0
ghostsInitialized = False
ITER = 30   # ghosts move 30fps

isChasingMode = False   # when power dot is eaten
