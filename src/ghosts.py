from algorithms.a_star import AStar
from algorithms.genetic_algorithm import GeneticAlgorithm
from algorithms.run_away import Frightened

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
        ghost = Ghost(i, "ghost" + str(i), (270 + (i-1) * 20, 290), (i-1) * 3)

        # tell random ghost to start search from upper left corner
        if i == 3:
            ghost.path.append("n1_1")
        ghosts.append(ghost)

    return ghosts


def moveGhosts(ghosts):
    for ghost in ghosts:

        # ghosts start chasing player each after few seconds
        if time.time() - ghost.time >= ghost.seconds:
            # because all algorithms implement the same interface getNextStep can be called
            node = ghost.algorithm.getNextStep()
            if node is None:
                return

            index = node.find('_')

            animate(ghost, pos=(int(node[index + 1:]) * 20 + 10, int(node[1:index]) * 20 + 10),
                    duration=1 / 3, tween='linear')


def initGhostAlgorithm(ghosts, player, algorithm):
    for g in ghosts:

        if algorithm == 'A*':
            g.setAlgorithm(AStar(g, player))

        elif algorithm == 'GeneticAlgorithm':
            g.setAlgorithm(GeneticAlgorithm(g, player))

        elif algorithm == 'frightened':
            g.setAlgorithm(Frightened(g))

        elif algorithm == 'A*_bot':
            pass        # TODO
