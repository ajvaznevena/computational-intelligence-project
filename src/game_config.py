import pgzrun

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

ghostMovement = 0
ITER = 30

isChasingMode = False   # when power dot is eaten
