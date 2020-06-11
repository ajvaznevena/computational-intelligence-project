from grid.get_grid import get_grid
from algorithms.rl.ghost import *
from algorithms.rl.dots import *
from algorithms.rl.player import Player

import numpy as np
import random
import matplotlib.pyplot as plt

br = 0


class Environment:

    def __init__(self):
        self.player = Player()
        self.dots = []
        self.ghosts = []
        self.chasingLast = 0
        self.actions = {}

    def reset(self):
        grid = np.array(get_grid(), copy=True)
        self.dots = initDots()
        self.mapDotsOnGrid(grid)
        self.player = Player()
        self.mapPlayerOnGrid(grid)
        self.ghosts = initGhosts(self.player)
        self.mapGhostsOnGrid(grid)

        self.actions = {
            'UP': self.player.moveUp,
            'DOWN': self.player.moveDown,
            'LEFT': self.player.moveLeft,
            'RIGHT': self.player.moveRight,
            'STAY': self.player.move
        }

        return grid

    def mapDotsOnGrid(self, grid):
        for dot in self.dots:
            if not dot.eaten:
                grid[dot.i][dot.j] = REGULAR_PILL_CODE if dot.dotType == 1 else BIG_PILL_CODE

    def mapPlayerOnGrid(self, grid):
        grid[int(self.player.y // CELL_SIZE)][int(self.player.x // CELL_SIZE)] = PLAYER_CODE

    def mapGhostsOnGrid(self,  grid, chasing=False):
        for ghost in self.ghosts:
            i = int(ghost.y // CELL_SIZE)
            j = int(ghost.x // CELL_SIZE)
            grid[i][j] = ghost.index + GHOST_ADD
            grid[i][j] += GHOST_CODE_CHASE if chasing else 0

    @staticmethod
    def sample():
        actions = ['UP', 'DOWN', 'LEFT', 'RIGHT', 'STAY']

        return actions[random.randrange(0, 5)]

    def step(self, action):
        grid = np.array(get_grid(), copy=True)

        self.actions.get(action)()
        self.mapPlayerOnGrid(grid)

        self.player.eatPill(self.dots)
        self.mapDotsOnGrid(grid)

        moveGhosts(self.ghosts)
        self.mapGhostsOnGrid(grid, self.player.getChasing())

        r = self.reward()

        done = False
        for ghost in self.ghosts:
            if self.player.caught(ghost):
                done = True
                break

        return grid, r, done

    def reward(self):
        return self.player.getScore()

    @staticmethod
    def renderState(state):
        global br

        img = plt.imshow(state)
        plt.colorbar(img, shrink=0.75)
        # plt.show()

        plt.savefig('start' + str(br) + '.png')
        plt.clf()
        br += 1


env = Environment()
g = env.reset()
Environment.renderState(g)
while True:
    act = env.sample()

    n, rew, done1 = env.step(act)
    Environment.renderState(n)

    if done1:
        break
