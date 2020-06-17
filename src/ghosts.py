from algorithms.a_star import AStar
from algorithms.genetic_algorithm import GeneticAlgorithm
from algorithms.frightened_algorithm import Frightened
from game_constants import CELL_SIZE, HEIGHT
from algorithms.dfs import Dfs

from pgzero.builtins import Actor
from pgzero.animation import animate
import time



class Ghost(Actor):

    def __init__(self, index, img, pos, seconds):
        super().__init__(img, pos)
        self.index = index
        self.path = []
        self.algorithm = None
        self.time = time.time()
        self.seconds = seconds

    def setAlgorithm(self, algorithm):
        self.algorithm = algorithm

    def setImage(self, image):
        self.image = image


def initGhosts():
    ghosts = []

    for i in range(1, 5, 1):
        ghost = Ghost(i, "ghost" + str(i), (270 + (i-1) * 20, HEIGHT / 2), (i-1) * 3)

        # tell fourth ghost to start search from upper left corner
        if i == 3:
            ghost.path.append("n1_1")

        ghosts.append(ghost)

    return ghosts


def moveGhosts(ghosts):

    for ghost in ghosts:
        # ghosts start chasing player after few seconds
        if time.time() - ghost.time >= ghost.seconds:

            # because all algorithms implement the same interface getNextStep can be called
            node = ghost.algorithm.getNextStep()
            if node is None:
                return

            index = node.find('_')

            animate(ghost, pos=(int(node[index + 1:]) * CELL_SIZE + CELL_SIZE / 2,
                                int(node[1:index]) * CELL_SIZE + CELL_SIZE / 2),
                    duration=1 / 3, tween='linear')


def initGhostsAlgorithm(ghosts, player, algorithm):
    """ Inits algorithm, based on user input, which ghosts use to chase player"""

    for g in ghosts:
        initGhostAlgorithm(g, player, algorithm)


def initGhostAlgorithm(ghost, player, algorithm):
    if algorithm == 'A*':
        ghost.setAlgorithm(AStar(ghost, player))

    elif algorithm == 'DFS':
        ghost.setAlgorithm(Dfs(ghost, player))

    elif algorithm == 'GeneticAlgorithm':
        ghost.setAlgorithm(GeneticAlgorithm(ghost, player))

    elif algorithm == 'Frightened':
        ghost.setAlgorithm(Frightened(ghost))
