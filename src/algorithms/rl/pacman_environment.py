from grid.get_grid import get_grid
from algorithms.rl.ghost import *
from algorithms.rl.dots import *
from algorithms.rl.player import Player
from algorithms.run_away import Frightened

import numpy as np
import random
import matplotlib.pyplot as plt

br = 0


class Environment:

    def __init__(self):
        self.grid = None
        self.player = None
        self.dots = []
        self.ghosts = []
        self.actions = {}
        self.chasing = False
        self.chasingLast = 0
        self.reset()

    def getStateShape(self):
        return self.grid.shape

    def getActionSize(self):
        return len(self.actions)

    def reset(self):
        self.grid = np.array(get_grid(), copy=True)
        self.dots = initDots()
        self.mapDotsOnGrid(self.dots, self.grid)
        self.player = Player()
        self.mapPlayerOnGrid(self.player, self.grid)
        self.ghosts = initGhosts(self.player)
        self.mapGhostsOnGrid(self.ghosts, self.grid, self.chasing)

        self.actions = {
            0: self.player.moveUp,
            1: self.player.moveDown,
            2: self.player.moveLeft,
            3: self.player.moveRight,
            # 4: self.player.move
        }

        return self.grid

    @staticmethod
    def mapDotsOnGrid(dots, grid):
        for dot in dots:
            grid[dot.i][dot.j] = REGULAR_PILL_CODE if dot.dotType == 1 else BIG_PILL_CODE

    @staticmethod
    def mapPlayerOnGrid(player, grid):
        grid[int(player.y // CELL_SIZE)][int(player.x // CELL_SIZE)] = PLAYER_CODE

    @staticmethod
    def mapGhostsOnGrid(ghosts, grid, chasing):
        for ghost in ghosts:
            i = int(ghost.y // CELL_SIZE)
            j = int(ghost.x // CELL_SIZE)
            grid[i][j] = ghost.index + GHOST_ADD
            grid[i][j] += GHOST_CODE_CHASE if chasing else 0

    def sample(self):
        return random.randrange(0, len(self.actions))

    def step(self, action):
        self.chasingLast += 1 if self.chasing else 0

        if self.chasingLast == FIVE_SECS:
            self.chasingLast = 0
            self.chasing = False
            for ghost in self.ghosts:
                ghost.path = []
                ghost.algorithm = AStar(ghost, self.player)

        self.grid = np.array(get_grid(), copy=True)

        reward = 0

        self.actions.get(action)()
        if self.player.notValid:
            reward += NOT_VALID_MOVE_REWARD
            self.player.notValid = False

        self.mapPlayerOnGrid(self.player, self.grid)

        eatPillReward = self.player.eatPill(self.dots)
        # if eatPillReward:
        #     self.chasing = True
        # else:
        #     reward += REGULAR_PILL_REWARD
        if eatPillReward == BIG_PILL_REWARD:
            self.chasing = True

        reward += eatPillReward

        done = False
        if len(self.dots) == 0:
            done = True

        self.mapDotsOnGrid(self.dots, self.grid)

        if self.chasing and self.chasingLast == 0:
            for ghost in self.ghosts:
                ghost.path = []
                ghost.algorithm = Frightened(ghost)

        reward += self.player.eatGhost(self.ghosts, self.chasing)

        moveGhosts(self.ghosts)
        self.mapGhostsOnGrid(self.ghosts, self.grid, self.chasing)

        for ghost in self.ghosts:
            if self.player.caught(ghost):
                reward += PLAYER_DEATH
                done = True
                break

        return self.grid, reward, done

    @staticmethod
    def renderState(state):
        global br

        img = plt.imshow(state)
        plt.colorbar(img, shrink=0.75)
        # plt.show()

        plt.savefig('start' + str(br) + '.png')
        plt.clf()
        br += 1
