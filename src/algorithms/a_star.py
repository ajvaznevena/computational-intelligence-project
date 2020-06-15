from algorithms.algorithm_interface import AlgorithmInterface, graph
from algorithms.help_functions import *

import sys


class AStar(AlgorithmInterface):

    def __init__(self, ghost, player):
        super().__init__()
        self.ghost = ghost
        self.player = player

    def run(self):
        start = pixelToGrid((self.ghost.x, self.ghost.y))
        startNameKey = getNodeName(start)

        goal = self.getGoal(self.ghost.index)
        goalNameKey = getNodeName(goal)

        openset = set()
        openset.add(startNameKey)
        closedset = set()

        distances = {startNameKey: 0}
        parents = {startNameKey: startNameKey}

        while len(openset) > 0:
            n = None

            for v in openset:
                if n is None or distances[v] + AStar.manhattan(v, goalNameKey) < \
                                distances[n] + AStar.manhattan(n, goalNameKey):
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
                    distances[m] = distances[n] + weight
                else:
                    if distances[m] > distances[n] + weight:
                        distances[m] = distances[n] + weight
                        parents[m] = n

                        if m in closedset:
                            closedset.remove(m)
                            openset.add(m)

            openset.remove(n)
            closedset.add(n)

        print("Path doesn't exist")
        return None

    def getNextStep(self):
        goal = self.getGoal(self.ghost.index)
        self.goalNameKey = getNodeName(goal)

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

    @staticmethod
    def manhattan(v_coords, goal):
        vX, vY = getCoordsFromName(v_coords)
        finishX, finishY = getCoordsFromName(goal)

        return abs(vX - finishX) + abs(vY - finishY)
