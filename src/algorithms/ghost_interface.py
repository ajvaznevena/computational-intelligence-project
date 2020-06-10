import sys
from abc import ABC, abstractmethod
from algorithms.ghost_goals import *

from game_config import *


class AlgorithmInterface(ABC):

    def __init__(self):
        self.goalNameKey = ""

    @abstractmethod
    def run(self):
        pass

    def getNextStep(self):
        if self.ghost.path == [] or self.ghost.path[-1] != self.goalNameKey:
            path = self.run()

            if path is None:
                print("Error :(")
                sys.exit(1)

            self.ghost.path = path
            self.goalNameKey = self.ghost.path[-1]
        else:
            # if goal did not change, we dont'h have to recalculate path again
            self.ghost.path.pop(0)

        if len(self.ghost.path) == 0:
            return None
        else:
            return self.ghost.path[0]

    def get_goal(self, index):
        # Red ghost's goal is player (index = 1)
        if index == 1:
            return self.pixelToGrid((player.x, player.y))

        # Lightblue ghost's goal is 4 fields ahead of player's current position (index = 2)
        elif index == 2:
            return lightBlueGoal(self)

        # Orange ghost's goal is random node (index = 3)
        elif index == 3:
            return orangeGoal(self)

        # Pink ghost's goal is 8 fields behind player's current position (index = 4)
        elif index == 4:
            return pinkGoal(self)

    @staticmethod
    def pixelToGrid(node):
        # this is safe because player and ghosts only move on value 1 in grid
        return int(node[1] // 20), int(node[0] // 20)

    @staticmethod
    def getNodeName(node):
        return "n" + str(node[0]) + "_" + str(node[1])

    @staticmethod
    def getCoordsFromName(name):
        index = name.find('_')
        coordX = int(name[1:index])
        coordY = int(name[index + 1:])

        return coordX, coordY
