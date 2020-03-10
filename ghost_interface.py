from abc import ABC, abstractmethod
import sys

from game_config import *


class AlgorithmInterface(ABC):

    @abstractmethod
    def getNextStep(self):
        pass


class AStar(AlgorithmInterface):

    def __init__(self, ghost):
        self.ghost = ghost

    def run(self):

        start = AStar.pixelToGrid((self.ghost.x, self.ghost.y))
        startNameKey = "n" + str(start[0]) + "_" + str(start[1])

        goal = AStar.get_goal(self.ghost.index)
        goalNameKey = "n" + str(goal[0]) + "_" + str(goal[1])

        openset = set()
        openset.add(startNameKey)
        closedset = set()

        # distances
        g = {startNameKey: 0}
        parents = {startNameKey: startNameKey}

        while len(openset) > 0:
            n = None

            for v in openset:
                if n is None or g[v] + AStar.manhattan(v, goalNameKey) < g[n] + self.manhattan(n, goalNameKey):
                    n = v

            if n is None:
                print("Path doesn't exist")
                return None

            if n == goalNameKey:
                path = []
                while parents[n] != n:
                    path.append(n)
                    n = parents[n]

                path.reverse()
                return path

            for (m, weight) in graph.get_neighbors(n):
                if m not in openset and m not in closedset:
                    openset.add(m)
                    parents[m] = n
                    g[m] = g[n] + weight
                else:
                    if g[m] > g[n] + weight:
                        g[m] = g[n] + weight
                        parents[m] = n

                        if m in closedset:
                            closedset.remove(m)
                            openset.add(m)

            openset.remove(n)
            closedset.add(n)

        print("Path doesn't exist")
        return None

    # TODO: implement different goals
    @staticmethod
    def get_goal(index):
        # Blue ghost's goal is player (index = 1)
        if index == 1:
            return AStar.pixelToGrid((player.x, player.y))

        # Lightblue ghost's goal is player (index = 2)
        elif index == 2:
            return AStar.pixelToGrid((player.x, player.y))

        # Orange ghost's goal is player (index = 3)
        elif index == 3:
            return AStar.pixelToGrid((player.x, player.y))

        # Pink ghost's goal is player (index = 4)
        elif index == 4:
            return AStar.pixelToGrid((player.x, player.y))

    @staticmethod
    def pixelToGrid(node):
        # this is safe because player and ghosts only move on value 1 in grid
        return round(node[1] // 20), round(node[0] // 20)

    @staticmethod
    def manhattan(v_coords, goal):
        xx = v_coords.find('_')
        v_x = int(v_coords[1:xx])
        v_y = int(v_coords[xx + 1:])

        xx = goal.find('_')
        finish_x = int(goal[1:xx])
        finish_y = int(goal[xx + 1:])

        return abs(v_x - finish_x) + abs(v_y - finish_y)

    def getNextStep(self):
        goal = self.pixelToGrid((player.x, player.y))
        goalNameKey = "n" + str(goal[0]) + "_" + str(goal[1])

        # if player did not move we don't need to calculate path again
        # instead, we just give next node in calculated path

        if self.ghost.path == [] or self.ghost.path[-1] != goalNameKey:
            path = self.run()
            # print(path)

            if path is None:
                print("Error :(")
                sys.exit(1)

            self.ghost.path = path
        else:
            self.ghost.path.pop(0)

        return self.ghost.path[0]
