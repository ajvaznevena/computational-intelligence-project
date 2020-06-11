import sys
import random
import numpy as np

from abc import ABC, abstractmethod

from grid.get_grid import get_grid
from graph import create_graph

grid = np.array(get_grid(), copy=True)   # movement grid
graph = create_graph()  # movement graph


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
            self.goalNameKey = self.ghost.path[-1] if self.ghost.path != [] else ''
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
            return self.pixelToGrid((self.player.x, self.player.y))

        # Lightblue ghost's goal is 4 fields ahead of player's current position (index = 2)
        elif index == 2:
            return self.lightBlueGoal()

        # Orange ghost's goal is random node (index = 3)
        elif index == 3:
            return self.orangeGoal()

        # Pink ghost's goal is 8 fields behind player's current position (index = 4)
        elif index == 4:
            return self.pinkGoal()

    def lightBlueGoal(self):
        targetX, targetY = 0, 0

        # see where player is moving
        if (self.player.angle // 90) % 2 == 0:
            targetX = -80 if self.player.movex < 0 else 80  # 4 * 20
        else:
            targetY = -80 if self.player.movey < 0 else 80

        gridX, gridY = self.pixelToGrid((self.player.x + targetX, self.player.y + targetY))

        if 0 <= gridX < 29 and 0 <= gridY < 30:
            if grid[gridX, gridY]:
                return gridX, gridY

        return self.pixelToGrid((self.player.x, self.player.y))

    def orangeGoal(self):
        nodesNo = len(graph.adjacency_list)
        r = random.randrange(nodesNo)

        goal = list(graph.adjacency_list.keys())[r]
        return self.getCoordsFromName(goal)

    def pinkGoal(self):
        targetX, targetY = 0, 0

        # see where player is moving
        if (self.player.angle // 90) % 2 == 0:
            targetX = 160 if self.player.movex < 0 else -160  # 8 * 20
        else:
            targetY = 160 if self.player.movey < 0 else -160

        tarX, tarY = self.pixelToGrid((self.player.x + targetX, self.player.y + targetY))

        if 0 <= tarX < 29 and 0 <= tarY < 30:
            if grid[tarX, tarY]:
                return tarX, tarY

        return self.pixelToGrid((self.player.x, self.player.y))

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
