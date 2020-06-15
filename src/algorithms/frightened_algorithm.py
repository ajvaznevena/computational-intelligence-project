from algorithms.algorithm_interface import AlgorithmInterface, graph
from algorithms.help_functions import *

import random


class Frightened(AlgorithmInterface):

    def __init__(self, ghost):
        super().__init__()
        self.ghost = ghost

    def getNextStep(self):
        node = pixelToGrid((self.ghost.x, self.ghost.y))
        ghostNode = getNodeName(node)
        neighbours = list(map(lambda x: x[0], graph.get_neighbors(ghostNode)))

        return neighbours[random.randrange(0, len(neighbours))]
