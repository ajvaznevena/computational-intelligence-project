from grid.get_grid import get_grid
from algorithms.rl.ghost import *

from pygame import image, Color
import numpy as np

from algorithms.rl.player import Player


class Environment:

    def __init__(self):
        self.grid = []
        self.player = None
        self.ghosts = []
        self.initialize()

    def initialize(self):
        self.grid = np.array(get_grid())
        self.mapDotsOnGrid()
        self.player = Player()
        self.ghosts = initGhosts()

    def mapDotsOnGrid(self):
        dotImage = image.load('images/dot_map.png')

        for i in range(30):
            for j in range(29):
                dotPos = (10 + i * 20, 10 + j * 20)

                if dotImage.get_at(dotPos) == Color('black'):
                    self.grid[j][i] = 10

                elif dotImage.get_at(dotPos) == Color('red'):
                    self.grid[j][i] = 20

    def sample(self):
        pass

    def step(self, action):
        if action == 'UP':
            self.player.moveUp()
        elif action == 'DOWN':
            self.player.moveDown()
        elif action == 'LEFT':
            self.player.moveLeft()
        elif action == 'RIGHT':
            self.player.moveRight()

        self.player.update()

        moveGhosts(self.ghosts)

        r = self.reward()

    def reward(self):
        return 0
