from abc import ABC, abstractmethod
import sys
import random

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
        # Red ghost's goal is player (index = 1)
        if index == 1:
            return AStar.pixelToGrid((player.x, player.y))

        # Lightblue ghost's goal is 4 fiels ahead player's current postion (index = 2)
        elif index == 2:
            return AStar.lightBlueGoal()

        # Orange ghost's goal is random node (index = 3)
        elif index == 3:
            return AStar.orangeGoal()

        # Pink ghost's goal is player (index = 4)
        elif index == 4:
            # return AStar.pinkGoal()
            return AStar.pixelToGrid((player.x, player.y))

    @staticmethod
    def lightBlueGoal():
        targetx, targety = 0, 0

        if (player.angle // 90) % 2 == 0:
            targetx = -80 if player.movex < 0 else 80

        else:
            targety = -80 if player.movey < 0 else 80

        tarx, tary = AStar.pixelToGrid((player.x + targetx, player.y + targety))

        if 0 <= tarx < 29 and 0 <= tary < 30:
            if not grid[tarx, tary]:
                return AStar.pixelToGrid((player.x, player.y))
            else:
                return tarx, tary

        return AStar.pixelToGrid((player.x, player.y))

    @staticmethod
    def orangeGoal():
        nodesNo = len(graph.adjacency_list)
        r = random.randrange(nodesNo)
        goal = list(graph.adjacency_list.keys())[r]
        xx = goal.find('_')
        targetx = int(goal[1:xx])
        targety = int(goal[xx + 1:])
        return targetx, targety

    @staticmethod
    def pinkGoal():
        pass

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
        if self.ghost.index == 2:
            goal = AStar.lightBlueGoal()
        if self.ghost.index == 3:
            if self.ghost.path == []:
                goal = AStar.orangeGoal()
            else:
                goal = self.ghost.path[-1]

        else:
            goal = AStar.pixelToGrid((player.x, player.y))
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
